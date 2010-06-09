import sys
import os
import time
import threading
import random
import socket

import pygame
import pygame.midi
from pygame.locals import *


################################################################################

class Output(threading.Thread): # Output runs in its own Thread

	def __init__(self, **kwargs):
		# logging on/off
		kwargs.setdefault('logging', True)
		self.__logging = kwargs.get('logging')

		self.__log('initializing Output')

		# mandatory for threading
		threading.Thread.__init__(self)

		# speed in bpm = beats per minute
		kwargs.setdefault('bpm', 128)
		self.__ticktime = self.setBPM(kwargs.get('bpm'))

		# get reference to manager. if no -> exception
		self.manager=kwargs.get('manager')
		if self.manager==None:
			raise Exception('Output must be instantiated with an associated EventManager!')

		self.__timestamp=0
		self.__lastInstrument=-1

		#######################################
		device_id = None

		pygame.init()
		pygame.midi.init()

		self._print_device_info()

		if device_id is None:
			port = pygame.midi.get_default_output_id()
		else:
			port = device_id

		print ("using output_id :%s:" % port)

		# no latency no scheduling of midi events with timestamp
		self.midi_out = pygame.midi.Output(port, latency = 1)



	def __del__(self):
		del self.midi_out
		pygame.midi.quit()

	''' sets ticktime (in miliseconds) -> speed '''
	def setTickTime(self, time):
		self.__ticktime=time

	''' set speed in BPM = bits per minute '''
	def setBPM(self,bpm):
		self.__ticktime=16000/bpm	# 1/16 rhytm, 64 notes = 1 sequence length

	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'Output:\t\t' + msg

	def run(self):
		
		# constants
		DELIMITER = '<*>'

		# network connection setup
		TCP_IP = '127.0.0.1'
		TCP_PORT = 5005
		BUFFER_SIZE = 5024

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((TCP_IP, TCP_PORT))

		# sleep and wait for tcp connection successfull
		# if i omitted this, the synch signal doesn't get to the server 
		time.sleep(0.5)
			
		# send synch
		self.s.send(DELIMITER+'<synch>'+DELIMITER+str(pygame.midi.time()))
		print pygame.midi.time()


		while 1:
			queue=self.manager.playDataQueue

			playdata = queue.get()
			self.__log('got music data to play')
			if(playdata!=None):
				self.play(playdata)
			queue.task_done()

			# kein warten mehr noetig weil synch ueber timestamp geht
			# time.sleep(self.__ticktime)

			#print 'next one  ' + str(pygame.midi.time())


		# close network connection
		self.s.close()

	def play(self, playdata):
		if(playdata==[]):
			return

		if(self.__timestamp==0):
			# first start
			self.__timestamp=pygame.midi.time()
		else:
			self.__timestamp=self.__timestamp+self.__ticktime

		'''DEBUG'''
		self.__timestamp=self.__ticktime
		
		
		# constants for MIDI Status
		ON = 1		# note on
		OFF = 0		# note off

		print 'timestamp: '+str(self.__timestamp)


		# send midi data
		for mididata in playdata:
			instrument = mididata[0]
			channel = mididata[1]
			note = mididata[2]
			velocity = mididata[3]
			status = mididata[4]

			# change instrument if necessary
			if(self.__lastInstrument!=instrument):
				status_change = 192+channel
				#self.midi_out.write([[[status_change,instrument],self.__timestamp]])
				self.__lastInstrument=instrument

			
			# constants
			DELIMITER = '<*>'		


			if status == ON:
				status_on = 144+channel
				#self.midi_out.write([[[status_on,note,velocity],self.__timestamp]])
				self.s.send(DELIMITER+str(status_on)+DELIMITER+str(note)+DELIMITER+str(velocity)+DELIMITER+str(self.__timestamp)+DELIMITER)
				print DELIMITER+str(status_on)+DELIMITER+str(note)+DELIMITER+str(velocity)+DELIMITER+str(self.__timestamp)+DELIMITER
				self.__log('\tnote on>\t' + str(note)) #LOG
			elif status == OFF:
				status_off = 128+channel
				#self.midi_out.write([[[status_off,note,velocity],self.__timestamp]])
				self.s.send(DELIMITER+str(status_off)+DELIMITER+str(note)+DELIMITER+str(velocity)+DELIMITER+str(self.__timestamp)+DELIMITER)
				print DELIMITER+str(status_off)+DELIMITER+str(note)+DELIMITER+str(velocity)+DELIMITER+str(self.__timestamp)+DELIMITER
				self.__log('\t< note off\t' + str(note)) # LOG

			#self.__log('played notes: ' + str(self.__on_notes)) # LOG


	def print_device_info(self):
		pygame.midi.init()
		self._print_device_info()
		pygame.midi.quit()

	def _print_device_info(self):
		for i in range( pygame.midi.get_count() ):
			r = pygame.midi.get_device_info(i)
			(interf, name, input, output, opened) = r

			in_out = ""
			if input:
				in_out = "(input)"
			if output:
				in_out = "(output)"

			print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
				(i, interf, name, opened, in_out))