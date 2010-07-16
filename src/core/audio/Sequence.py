
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
		
		self.__on_notes = []
		for i in xrange(128):
			self.__on_notes.append(False)

		'''
		playdata contains information for midi events, which will be played
		rawNoteData contains information for midi events before a effect is 
		applied to it. rawNoteData's information will be displayed in the
		ButtonMatrix
		'''
		# specification for __playdata structure: http://wiki.github.com/timlandgraf/multitouch/234-midi-events-datenhaltung

		''' playdata '''
		'''
		if(self.id==0):
			# first static for reference
			self.__playdata = self.__Arpeggiator.getUgh()
		else:
			# all others are random arpgeggiator
			self.__playdata = self.__Arpeggiator.getRandomLoop()
		'''
		self.__playdata = []

		''' rawNoteData '''	
		self.__rawNoteData = []
		for i in xrange(32):
			self.__rawNoteData.append([])
			for j in xrange(12):
				self.__rawNoteData[i].append(None)
	
	def getPlaydata(self):
		return self.__playdata
	
	def getRawNoteData(self):
		return self.__rawNoteData
	
	def setRawNoteData(self,data):
		self.__rawNoteData = data
		self.transformRawDataToPlayData()

	def transformRawDataToPlayData(self):
		offset = Constants.NOTE_BEGIN
		
		self.__playdata = []
		for i in xrange(64):
			self.__playdata.append([])
		
		for tick in xrange(32):
			for pitch in xrange(12):
				if (self.__rawNoteData[tick][pitch] != None):
					# on event
					midi = [1,1,offset+pitch,127,1]
					self.__playdata[tick*2].append(midi)
					
					# off event
					midi = [1,1,offset+pitch,127,0]
					self.__playdata[(tick*2 +1)%64].append(midi)
					
		if (self.arpeggiated):
			# do your arppeggiator
			print 'do your arppeggiator'

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
			self.__log("skipped this tick because this tick ("+str(tick)+") is too big for this sequence with maximum ticks: "+str(len(self.__playdata)))
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
		
		for i in xrange(128):
			if (self.__on_notes[i]):
				self.__die_notes.append([self.instrument,self.channel,i,0,0])
				
		self.__die_next_tick=True
