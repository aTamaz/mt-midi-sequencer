import socket
import Queue
import threading

class MidiServer(threading.Thread):
	def __init__(self, **kwargs):
		kwargs.setdefault('logging', True)
		self.__logging = kwargs.get('logging')
		self.__log('initializing MidiServer')

		# mandatory for threading
		threading.Thread.__init__(self)
		
		# thread safe queue for music data
		self.playDataQueue=Queue.Queue(maxsize=32) #32

		# network connection setup
		self.__TCP_IP = '127.0.0.1'
		self.__TCP_PORT = 5005
		self.__BUFFER_SIZE = 1024

		# socket
		self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		
		self.__DELIMITER = '<*>'
		
		
	''' mainloop '''
	def run(self):
		self.__sock.bind((self.__TCP_IP, self.__TCP_PORT))
		self.__sock.listen(1)
		
		while 1:
			self.__log('wait for connection accept')
			conn, addr = self.__sock.accept()
			self.__log('Connection accepted, address:'+str(addr))
		
			# work that request!
			self.__work(conn,addr)
	
	def __work(self,conn,addr):
		while 1:
			self.__log('wait for data')
			data = conn.recv(self.__BUFFER_SIZE)

			if not data: break
			
			self.__log('==== new data ====')
			list = str(data).split(self.__DELIMITER)
			list = self.removeBlanksInList(list)			
			self.__log(str(list))
		

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
	