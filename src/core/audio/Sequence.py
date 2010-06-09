import EventManager
import Arpeggiator

import time
import random

'''
- Class: Sequence
- Description:
This class is a sequence displayed as an object on the GUI.
'''


class Sequence():

	def __init__(self, **kwargs):
		kwargs.setdefault('id', '')
		kwargs.setdefault('logging', True)
		self.id = kwargs.get('id')
		self.__logging = kwargs.get('logging')
		self.__Arpeggiator = Arpeggiator.Arpeggiator()

		# for internal clock
		self.__internalTick=0

		# constants for MIDI Status
		ON = 1		# note on
		OFF = 0		# note off

		# specification for __playdata structure: http://wiki.github.com/timlandgraf/multitouch/234-midi-events-datenhaltung

		if(self.id=='seq1'):
			# first static for reference
			self.__playdata = self.__Arpeggiator.getUgh()
		else:
			# all others are random arpgeggiator
			self.__playdata = self.__Arpeggiator.getRandomLoop()

	''' callback method for exposing music information '''
	def getMidiData(self,tick):
		# if sequence is shorter than the general sequence length do nothing
		if(tick>=len(self.__playdata)):
			print 'ausgelassen'
			return None

		# internal tick deprecated: bad synch properties!
		#self.__internalTick=(self.__internalTick+1)%len(self.__playdata)
		#index=self.__internalTick
		index=tick

		self.__log('getting data for tick ' + str(tick) + ' at position ' + str(index))
		return self.__playdata[index]

	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'Sequence <'+self.id+'>:\t' + msg