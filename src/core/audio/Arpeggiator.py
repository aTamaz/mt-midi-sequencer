import time
import random

class Arpeggiator():
	def __init__(self, instrument, channel, velocity):
		self.channel = channel
		self.velocity = velocity
	def setInstr(self, instr):
		self.instrument = instr
	"""
	Generates a whole-number of loops in an array.
	a, b, c e[60, 71] eZ
	a < b < c

	One loop is a half of a bar -> two beats (2/4)
	"""
	def __generateLoop(self, a, b, c, loopTimes, currentLoop=None, getRandom=True):
		# constants for MIDI Status
		ON = 1		# note on
		OFF = 0		# note off

		if a > b or b > c or a < 60 or a > 72 or b < 60 or b > 72 or c < 60 or c > 72 or loopTimes < 1:
			#print "Arpeggio generation failed."
			return None

		if(getRandom):
			# random instrument and channel
			ins = random.randint(0, 127)
			cha=random.randint(0, 15)
			# debug for all notes off
			cha=1
		else:
			ins=self.instrument
			cha=self.channel

		loop = [
			[[ins,cha, a - 24, self.velocity, ON]],
			[[ins,cha, a - 24, self.velocity, OFF], [ins,cha, c - 24, self.velocity, ON]],
			[[ins,cha, c - 24, self.velocity, OFF], [ins,cha, a - 12, self.velocity, ON]],
			[[ins,cha, a - 12, self.velocity, OFF], [ins,cha, b - 12, self.velocity, ON]],
			[[ins,cha, b - 12, self.velocity, OFF], [ins,cha, c - 12, self.velocity, ON]],
			[[ins,cha, c - 12, self.velocity, OFF], [ins,cha, a, self.velocity, ON]],
			[[ins,cha, a, self.velocity, OFF], [ins,cha, b, self.velocity, ON]],
			[[ins,cha, b, self.velocity, OFF], [ins,cha, c, self.velocity, ON]]
		]

		if (currentLoop != None):
			notesToClose = list()
			for lastNote in currentLoop[len(currentLoop) - 1]:
				# if a note was played
				if lastNote[4] == 1:
					noteToClose = [lastNote[0],lastNote[1],lastNote[2], lastNote[3], 0]
					notesToClose.append(noteToClose)
			loop[0] = notesToClose + loop[0]

			loop = currentLoop + loop

		if loopTimes > 1:
			return self.__generateLoop(a, b, c, loopTimes - 1, loop, getRandom)
		else:
			return loop

	def getLoop(self, a, b, c):
		myLoop = self.__generateLoop(a, b, c, 4, None, True)
		myLoop = self.__generateLoop(a, b, c, 2, myLoop, getRandom=True)
		myLoop = self.__generateLoop(a, b, c, 2, myLoop, getRandom=True)
		return myLoop

	def getUgh(self):
		myLoop = self.__generateLoop(62, 65, 69, 4, getRandom=False)
		myLoop = self.__generateLoop(62, 67, 70, 2, myLoop, getRandom=False)
		myLoop = self.__generateLoop(62, 65, 70, 2, myLoop, getRandom=False)
		return myLoop

	def getRandomLoop(self):
		loop=None
		i=1
		while(loop==None):
			#print 'RAANANDOM Attempt ' + str(i)
			i=i+1
			a = random.randint(61, 70)
			b = random.randint(61, 70)
			c = random.randint(61, 70)
			#print a,b,c
			loop = self.getLoop(a,b,c)

		return loop
	
	def arpeggiate(self, playdata):
		notes = []
		currentTimeStep = playdata[0]
		for note in currentTimeStep:
			notes.append(note[2])
		
		if len(notes) < 3:
			return playdata
		
		notes = self.__sortArray(notes)
		playdata = self.getLoop(notes[0], notes[1], notes[2])
		return playdata
	
	
	def __sortArray(self, notes):
		for j in notes:
			for i in range(len(notes) - 1):
				if notes[i] > notes[i + 1]:
					self.__exchangeNotes(notes[i], notes[i + 1])
		return notes;
	
	def __exchangeNotes(self, note1, note2):
		tmp = note2
		note2 = note1
		note1 = tmp