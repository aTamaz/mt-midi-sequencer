import sys
import os
import time
import threading
import random
import socket

import pygame
import pygame.midi
from pygame.locals import *

import core.Constants as Constants

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
		kwargs.setdefault('bpm', Constants.DEFAULT_bpm)
		self.setBPM(kwargs.get('bpm'))

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
		self.__ticktime=16000/int(float(bpm))	# 1/16 rhytm, 64 notes = 1 sequence length

	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'Output:\t\t' + msg

	def run(self):
		while 1:
			queue=self.manager.playDataQueue

			playdata = queue.get()
			self.__log('got music data to play')
			if(playdata!=None):

				self.play(playdata)

			queue.task_done()


	def play(self, playdata):
		if(playdata==[]):
			return

		if(self.__timestamp==0):
			# first start
			self.__timestamp=pygame.midi.time()
		else:
			self.__timestamp=self.__timestamp+self.__ticktime

		# constants for MIDI Status
		ON = 1		# note on
		OFF = 0		# note off




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
				self.midi_out.write([[[status_change,instrument],self.__timestamp]])
				self.__lastInstrument=instrument

			if status == ON:
				status_on = 144+channel
				self.midi_out.write([[[status_on,note,velocity],self.__timestamp]])
				self.__log('\tnote on>\t' + str(note)) #LOG
			elif status == OFF:
				status_off = 128+channel
				self.midi_out.write([[[status_off,note,velocity],self.__timestamp]])
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