import sys
import os
import time
import threading
import random
import socket
import core.Constants



################################################################################

class OutputAdapter(threading.Thread): # OutputAdapter runs in its own Thread

	def __init__(self, **kwargs):
		# logging on/off
		kwargs.setdefault('logging', True)
		self.__logging = kwargs.get('logging')

		self.__log('initializing OutputAdapter')

		# mandatory for threading
		threading.Thread.__init__(self)

		# speed in bpm = beats per minute
		kwargs.setdefault('bpm', 128)
		self.__ticktime = self.setBPM(kwargs.get('bpm'))

		# get reference to manager. if no -> exception
		self.manager=kwargs.get('manager')
		if self.manager==None:
			raise Exception('OutputAdapter must be instantiated with an associated EventManager!')

		


	def __del__(self):
		del self.midi_out




	''' set speed in BPM = bits per minute '''
	def setBPM(self,bpm):
		#self.__ticktime=16000/bpm	# 1/16 rhytm, 64 notes = 1 sequence length
		try:
			self.s
		except:
			return
		
		self.__log('send setBPM Message')
		delim = core.Constants.TCP_delimiter
		setMsg = core.Constants.TCP_setBPM
		self.s.send(delim+setMsg+delim+str(bpm)+delim)
		

	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'OutputAdapter:\t\t' + msg

	def run(self):

		# network connection setup
		TCP_IP = core.Constants.TCP_ip
		TCP_PORT = core.Constants.TCP_port
		BUFFER_SIZE = core.Constants.TCP_buffer_size

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((TCP_IP, TCP_PORT))

		firstRun=True

		while 1:
			queue=self.manager.playDataQueue

			playdata = queue.get()
			self.__log('got music data to play')
			if(playdata!=None):
				if(not firstRun):
					# wait for next request
					self.s.recv(BUFFER_SIZE)
				
				self.play(playdata)
				
				if(firstRun): firstRun=False
			queue.task_done()



		# close network connection
		self.s.close()

	def play(self, playdata):
		if(playdata==[]):
			return		
		
		# constants for MIDI Status
		ON = 1		# note on
		OFF = 0		# note off



		'''
		message format:
		<tick-start><DELIMITER><event-start><DELIMITER><instrument><DELIMITER><channel><DELIMITER><note><DELIMITER><velocity><DELIMITER><status><DELIMITER><event-end><DELIMITER><event-start>...<event-end>...<DELIMITER><tick-end><DELIMITER>
		'''		
		TCP_tick_start 	= core.Constants.TCP_tick_start
		TCP_tick_end 	= core.Constants.TCP_tick_end
		TCP_event_start	= core.Constants.TCP_event_start
		TCP_event_end	= core.Constants.TCP_event_end
		TCP_delimiter 	= core.Constants.TCP_delimiter		

		# send begin of tick
		self.s.send(TCP_tick_start+TCP_delimiter)
				
		# send midi data
		for mididata in playdata:
			instrument = mididata[0]
			channel = mididata[1]
			note = mididata[2]
			velocity = mididata[3]
			status = mididata[4]

			# send begin of midi event
			self.s.send(TCP_event_start+TCP_delimiter)	
			
			# send event data
			msg=str(instrument)+TCP_delimiter+str(channel)+TCP_delimiter+str(note)+TCP_delimiter+str(velocity)+TCP_delimiter+str(status)+TCP_delimiter
			self.s.send(msg)
			
			# send end of midi event
			self.s.send(TCP_event_end+TCP_delimiter)
			
		# send end of tick
		self.s.send(TCP_tick_end+TCP_delimiter)			
			
			


	