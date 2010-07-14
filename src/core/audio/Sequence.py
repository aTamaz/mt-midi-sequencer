
import Arpeggiator
import pygame
import time
import random
import core.Constants as Constants

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
		kwargs.setdefault('arpeggiated', False)
		self.arpeggiated = kwargs.get('arpeggiated')
		self.id = int(kwargs.get('id'))
		self.__logging = kwargs.get('logging')
		self.__Arpeggiator = Arpeggiator.Arpeggiator()
		
		# get reference to manager. if no -> exception
		self.manager=kwargs.get('manager')
		if self.manager==None:
			raise Exception('Sequence must be instantiated with an associated EventManager!')

		# for internal clock
		self.__internalTick=0
		
		self.instrument = 0
		self.channel = 0
	
		# this is used to send off events for all switched on notes and then die
		self.__die_next_tick=False
		self.__die_now=False
		self.__die_notes=[]
			
		self.note1 = 0
		self.note2 = 0
		self.note3 = 0
		
		# create an empty playdata:
		self.__on_notes = []
		for i in range(0,127):
			self.__on_notes.append(False)

		# specification for __playdata structure: http://wiki.github.com/timlandgraf/multitouch/234-midi-events-datenhaltung

		if(self.id==0):
			# first static for reference
			self.__playdata = self.__Arpeggiator.getUgh()
		else:
			# all others are random arpgeggiator
			self.__playdata = self.__Arpeggiator.getRandomLoop()
	
	def getPlaydata(self):
		return self.__playdata

	''' callback method for exposing music information '''
	def getMidiData(self,tick):
		# if Sequence has to die, play off notes for all switched on notes and
		# unregister and die
		if (self.__die_now):
			self.manager.unregister(self)
			del self
			return None
		if (self.__die_next_tick):
			self.__die_now=True
			return self.__die_notes
		
		# if sequence is shorter than the general sequence length do nothing
		if(tick>=len(self.__playdata)):
			print 'ausgelassen'
			return None

		# internal tick deprecated: bad synch properties!
		#self.__internalTick=(self.__internalTick+1)%len(self.__playdata)
		#index=self.__internalTick
		index=tick

		self.__log('getting data for tick ' + str(tick) + ' at position ' + str(index))
		
		output = []
		for item in self.__playdata[index]:
			# instrument overwrite
			item[0] = int(self.instrument)
			
			# channel overwrite
			item[1] = int(self.channel)
			
			note = item[2]
			# refresh on notes so we know which do switch off when swtching this sequence off
			if (self.__on_notes[note]):
				self.__on_notes[note]=False
			else:
				self.__on_notes[note]=True
				
			output.append(item)
			
		return output

	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'Sequence <'+str(self.id)+'>:\t' + msg
			
	def setInstrument(self, instr):
		if (int(instr) < 0 or int(instr) > 127):
			return
		
		self.instrument = instr
		
		''' TODO add effect to playdata storage '''
		self.__log('Sequence was set to instrument ' + str(instr))
		
			
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
	
	''' TODO check if this still needed and delete if not '''
	def exchange(self, note1, note2):
		tmp = note2
		note2 = note1
		note1 = tmp
		
	''' deletes this sequence in the right way '''
	def delete(self):
		self.__log('deleting sequence')
		
		for i in range(0,127):
			if (self.__on_notes[i]):
				self.__die_notes.append([self.instrument,self.channel,i,0,0])
				
		self.__die_next_tick=True
