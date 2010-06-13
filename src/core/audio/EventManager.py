import EventWorkerimport OutputAdapterimport timeimport threadingimport Queueimport core.Constants'''- Class: EventManager- Description:This class is the worker's manager. Here we can register new objectswith callback functions while the worker is busy working'''class EventManager(threading.Thread):	def __init__(self, **kwargs):		kwargs.setdefault('logging', True)		self.__logging = kwargs.get('logging')		self.__log('initializing EventManager')		# thread safe queue for music data		self.playDataQueue=Queue.Queue(maxsize=core.Constants.EventManager_playDataQueue_maxsize) #32		# mandatory for threading		threading.Thread.__init__(self)		# setup worker		self.worker=EventWorker.EventWorker(manager=self, logging=self.__logging)		self.worker.setDaemon(True)		# setup output		self.output=OutputAdapter.OutputAdapter(manager=self, logging=self.__logging)		self.output.setDaemon(True)		self.__callbacks={} # dictionary for callback methods <obj>:<callback>		__singleton = self	''' register an object '''	def register(self, object, method):		self.__log('registering callback method for ' + str(object.id))		self.__callbacks[object]=method		# tell worker to get new registered method:		self.worker.refreshConfig.set()	''' unregister an object '''	def unregister(self, object):		self.__log('unregistering callback method for ' + str(object.id))		del self.__callbacks[object]		# tell worker to get new registered method:		self.worker.refreshConfig.set()			''' for EventWorker to fetch it '''	def getCallbacks(self):		return self.__callbacks	''' set speed in bpm = beats per minute '''	def setBPM(self,bpm):		self.output.setBPM(bpm)	''' tunnel for log messages '''	def __log(self, msg):		if(self.__logging):			print 'EventManager:\t' + msg	''' mainloop '''	def run(self):		# start EventWorker-Thread		self.__log('starting EventWorker-Thread')		self.worker.start()		# start OutputAdapter-Thread		self.__log('starting OutputAdapter-Thread')		self.output.start()''' singleton pattern a little bit dirty because python does not know what a static variable is '''__singleton = Nonedef getInstance(): return __singleton