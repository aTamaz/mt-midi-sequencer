import sys
import os
import time
import threading
import random
import socket




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

		self.__timestamp=0
		self.__lastInstrument=-1


	def __del__(self):
		del self.midi_out


	''' sets ticktime (in miliseconds) -> speed '''
	def setTickTime(self, time):
		self.__ticktime=time

	''' set speed in BPM = bits per minute '''
	def setBPM(self,bpm):
		self.__ticktime=16000/bpm	# 1/16 rhytm, 64 notes = 1 sequence length

	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'OutputAdapter:\t\t' + msg

	def run(self):
		
		# constants
		DELIMITER = '<*>'

		# network connection setup
		TCP_IP = '127.0.0.1'
		TCP_PORT = 5005
		BUFFER_SIZE = 5024

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((TCP_IP, TCP_PORT))



		while 1:
			queue=self.manager.playDataQueue

			playdata = queue.get()
			self.__log('got music data to play')
			if(playdata!=None):
				# wait for next request
				self.s.recv(BUFFER_SIZE)
				
				self.play(playdata)
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
		TCP_tick_start 	= '<tick-start>'
		TCP_tick_end 	= '<tick-end'
		TCP_event_start	= '<event-start>'
		TCP_event_end	= '<event-end>'
		TCP_delimiter 	= '<*>'

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
			
			


	