import socket
import Queue
import threading
import Output
import core.Constants

class MidiServer(threading.Thread):
	def __init__(self, **kwargs):
		kwargs.setdefault('logging', True)
		self.__logging = kwargs.get('logging')
		self.__log('initializing MidiServer')

		# mandatory for threading
		threading.Thread.__init__(self)
		
		# thread safe queue for music data
		self.playDataQueue=Queue.Queue(maxsize=core.Constants.MidiServer_playDataQueue_maxsize) #32

		# network connection setup
		self.__TCP_IP = core.Constants.TCP_ip
		self.__TCP_PORT = core.Constants.TCP_port
		self.__BUFFER_SIZE = core.Constants.TCP_buffer_size		

		# socket
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# setup output
		self.output=Output.Output(manager=self, logging=self.__logging)
		#self.output.setDaemon(True)
		
		
	''' mainloop '''
	def run(self):
		self.output.start()
		self.__sock.bind((self.__TCP_IP, self.__TCP_PORT))
		self.__sock.listen(1)
		
		while 1:
			self.__log('wait for connection accept')
			conn, addr = self.__sock.accept()
			self.__log('Connection accepted, address:'+str(addr))
		
			# work that request!
			self.__work(conn,addr)
	
	def __work(self,conn,addr):
		'''
		message format:
		<tick-start><DELIMITER><event-start><DELIMITER><instrument><DELIMITER><channel><DELIMITER><note><DELIMITER><velocity><DELIMITER><status><DELIMITER><event-end><DELIMITER><event-start>...<event-end>...<DELIMITER><tick-end><DELIMITER>
		'''
		TCP_tick_start 	= core.Constants.TCP_tick_start
		TCP_tick_end 	= core.Constants.TCP_tick_end
		TCP_event_start	= core.Constants.TCP_event_start
		TCP_event_end	= core.Constants.TCP_event_end
		TCP_delimiter 	= core.Constants.TCP_delimiter
		

		
		
		while 1:
			'''
			cycle begins here:
			
			0)  request data for a new tick from OutputAdapter
			1)  wait for a <tick-start>
			2)  wait for a <event-start>
			3)  evaluate data
			4)  wait for a <event-end>
			5)  receive data
				- if <event-start> occurs go to 3)
				- if <tick-end> occurs goto 0)
				- else goto 5)
			
			'''
			playdata = []
			
			''' step 0) request data '''
			list = []			
			while(len(list)==0):
				self.__log('requesting data')
				conn.send('ugh')
				list = self.__receiveData(conn)
					
			''' step 1) wait for <tick-start> '''
			#list = self.__receiveData(conn)
			while 1:	
				if(len(list)==0):
					list = self.__receiveData(conn)
					
				value = list[0]				
				if(value==TCP_tick_start):
					list.remove(value)
					self.__log('found <tick-start>')
					break
				else:
					self.__filterOthers(conn,list)
			
			''' step 2) wait for <event-start> '''
			while 1:	
				if(len(list)==0):
					list = self.__receiveData(conn)
					
				value = list[0]
				if(value==TCP_event_start):
					list.remove(value)
					self.__log('found <event-start>')
					break
				else:
					self.__filterOthers(conn,list)
	
			''' step 3) evaluate data '''
			stepDone = False
			while not stepDone:	
				if(len(list)==0):
					list = self.__receiveData(conn)

				self.__log('evaluate event data')
				eventData=[]
				for i in range(0, 5):					
					value = list[0]
					list.remove(value)
					eventData.append(int(value))
					if(len(list)==0):
						list = self.__receiveData(conn)
				
				self.__log('extend playdata with:\t'+str(eventData))		
				playdata.extend([eventData])
				

				''' nested step 4) wait for a <event-end> '''
				while 1:	
					if(len(list)==0):
						list = self.__receiveData(conn)
						
					value = list[0]					
					if(value==TCP_event_end):
						list.remove(value)
						self.__log('found <event-end>')
						break	
					else:
						self.__filterOthers(conn,list)			
				
				''' nested step 5)  receive data
					- if <event-start> occurs go to 3)
					- if <tick-end> occurs goto 0)
					- else goto 5)
				'''
				while 1:	
					if(len(list)==0):
						list = self.__receiveData(conn)
						
					value = list[0]					
					if(value==TCP_tick_end):
						list.remove(value)
						stepDone=True
						self.__log('found <tick-end>, request a new tick')
						break
					elif(value==TCP_event_start):
						list.remove(value)
						self.__log('another <event-start> occured')
						break			
					else:
						self.__filterOthers(conn,list)
			
			# finally:
			self.playDataQueue.put(playdata)
			print playdata
		
	'''
	This method filters other TCP Messages than handled in __work()
	'''		
	def __filterOthers(self,conn,list):
		TCP_setBPM		= core.Constants.TCP_setBPM
		
		''' filter <setBPM> event '''
		value = list[0]
		if(value==TCP_setBPM):
			list.remove(value)
			bpm=list[0]
			list.remove(bpm)
			print '>>>>>>'+str(bpm)
			self.output.setBPM(bpm)
			
						
		
		
						
	def __receiveData(self,conn):	
		self.__log('wait for data')
		data = conn.recv(self.__BUFFER_SIZE)

		if not data: return None
		
		self.__log('==== new data ====')
		list = str(data).split(core.Constants.TCP_delimiter)
		list = self.removeBlanksInList(list)			
		self.__log('received:\t'+str(list))
		
		
		outfile=open("log.txt","a")
		outfile.write(str(list))
		outfile.close()
		
		
		return list
			
			
	''' tunnel for log messages '''
	def __log(self, msg):
		if(self.__logging):
			print 'MidiServer:\t' + msg		
			
	'''
	Created on 10.06.2010
	
	@author: Bao
	
	removes blanks from a list
	'''
	def removeBlanksInList(self,list):
	    err=None
	    while(err==None):
	        try:
	            list.remove('')
	        except:
	            err=True
	    return list 			

		
if __name__ == '__main__':
	server = MidiServer()
	server.start()
	