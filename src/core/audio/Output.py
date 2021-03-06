import threading

import pygame

import core.Constants as Constants

import time

################################################################################

class Output(threading.Thread): # Output runs in its own Thread

	def __init__(self, **kwargs):
		# logging on/off
		kwargs.setdefault('logging', Constants.LOGGING_output)
		self.__logging = kwargs.get('logging')

		self.__log('initializing Output')

		# midi output
		self.midi_out = kwargs.get('midi_out')
		if self.midi_out==None:
			raise Exception('Output must be instantiated with an associated pygame midi Output!')

		# get reference to manager. if no -> exception
		self.manager=kwargs.get('manager')
		if self.manager==None:
			raise Exception('Output must be instantiated with an associated EventManager!')
		
		# mandatory for threading
		threading.Thread.__init__(self)

		# speed in bpm = beats per minute
		kwargs.setdefault('bpm', Constants.DEFAULT_bpm)
		self.setBPM(kwargs.get('bpm'))

		self.__timestamp=0
		self.__lastInstrument=-1
		self.__volume=Constants.GLOBAL_START_VOLUME

		#######################################
		
	''' sets volume. volume must be between 0 and 100. float allowed '''
	def setVolume(self, volume):
		if (volume<0 or volume>100):
			return
		self.__volume=volume

	def getVolume(self):
		return self.__volume

	def __del__(self):
		del self.midi_out
		#pygame.midi.quit()

	''' sets ticktime (in miliseconds) -> speed '''
	def setTickTime(self, time):
		self.__ticktime=time

	''' set speed in BPM = bits per minute '''
	def setBPM(self,bpm):
		self.__ticktime=16000/int(float(bpm))	# 1/16 rhytm, 64 notes = 1 sequence length
		
	def getBPM(self):
		if (int(self.__ticktime) == 0):
			return 0
		return int(16000.0/float(self.__ticktime))

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
			
			''' sleep 3/4 of the real time you should wait. rest of waiting
				does the OS
			'''
			sleepTime = float(self.__ticktime)/1000.0*(29.0/30.0) # wait 3/4 of time unit
			#sleepTime = float(self.__ticktime)/1000.0*(99.0/100.0)
			#sleepTime = float(self.__ticktime)/1000.0*(1.0/2.0)
			time.sleep(sleepTime)


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
			velocity = int(float(mididata[3])*float(self.__volume)/float(100))
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
				if note == -1:
					self.midi_out.write([[[176 + channel, 123, 0], self.__timestamp]])
				else:  
					self.midi_out.write([[[status_off,note,velocity],self.__timestamp]])
				self.__log('\t< note off\t' + str(note)) # LOG

			self.__log("\t velocity \t"+str(velocity))
			#self.__log('played notes: ' + str(self.__on_notes)) # LOG


	