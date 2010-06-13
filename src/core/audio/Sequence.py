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
	__playdata = []

	def __init__(self, **kwargs):
		kwargs.setdefault('id', -1)
		kwargs.setdefault('logging', True)
		self.id = int(kwargs.get('id'))
		self.__logging = kwargs.get('logging')
		self.__Arpeggiator = Arpeggiator.Arpeggiator()

		# for internal clock
		self.__internalTick=0
		
		self.note1 = 0
		self.note2 = 0
		self.note3 = 0
		
		'''
		# create an empty playdata:
		self.__playdata = []
		for i in range(64):
			self.__playdata.append([])
		'''
		# specification for __playdata structure: http://wiki.github.com/timlandgraf/multitouch/234-midi-events-datenhaltung

		if(self.id==1):
			# first static for reference
			self.__playdata = self.__Arpeggiator.getUgh()
	#	else:
	#		# all others are random arpgeggiator
	#		self.__playdata = self.__Arpeggiator.getRandomLoop()
	

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
			print 'Sequence <'+str(self.id)+'>:\t' + msg
			
			
	def setNote(self, note):
		if self.note1 == 0:
			self.note1 = note
			print "first set"
		elif self.note2 == 0:
			self.note2 = note
			print "second set"
		elif self.note3 == 0:
			self.note3 = note
			print "third set"
		
		if (self.note3 != 0):
			if self.note1 > self.note2:
				self.exchange(self.note1, self.note2)
			if self.note2 > self.note3:
				self.exchange(self.note2, self.note3)
			if self.note1 > self.note2:
				self.exchange(self.note1, self.note2)
			self.__playdata = self.__Arpeggiator.getLoop(self.note1, self.note2, self.note3)
			print "playdata set!"
			print self.note1
			print self.note2
			print self.note3
			print self.__playdata
	
	def exchange(self, note1, note2):
		tmp = note2
		note2 = note1
		note1 = tmp