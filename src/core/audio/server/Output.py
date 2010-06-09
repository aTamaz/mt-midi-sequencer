import socket
import pygame
import pygame.midi
from pygame.locals import *



'''
Created on 10.06.2010

@author: Bao

removes blanks from a list
'''
def removeBlanksInList(list):
    err=None
    while(err==None):
        try:
            list.remove('')
        except:
            err=True
    return list    







""" constants """
DELIMITER = '<*>'

""" init stuff """
pygame.init()
pygame.midi.init()

""" time stuff """
timestamp_first = pygame.midi.time()
timestamp_offset = 0

""" audio stuff """
# no latency no scheduling of midi events with timestamp
port=0
midi_out = pygame.midi.Output(port, latency = 1)

channel = 0
instrument = 0
status_change = 192+channel
midi_out.write([[[status_change,instrument],pygame.midi.time()]])

""" network stuff """
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 5024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


print 'starting'
while 1:
    print 'wait for connection accept'
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        print 'wait for data'
        data = conn.recv(BUFFER_SIZE)
        
        if not data: break
        
        print '==== new data ===='
        list = str(data).split(DELIMITER)
        list = removeBlanksInList(list)
        
        if(str(list[0])=='<synch>'):
            timestamp_offset = int(list[1]) - int(timestamp_first)
            print 'my first timestamp: '+str(timestamp_first)
            print 'your timestamp: '+str(list[1])
            print 'offset: ' +str(timestamp_offset)
            #exit()
            continue
        
        print str(list[0]) # status (beinhaltet channel)
        print str(list[1]) # note
        print str(list[2]) # velo
        print str(list[3]) # time
        
        status = int(list[0])
        note = int(list[1])
        velocity = int(list[2])
        timestamp = long(pygame.midi.time()) + int(list[3])
        
        print 'aktuelle zeit: '+str(pygame.midi.time())
        print 'offset: '+str(timestamp_offset)
        print 'spielzeit: '+str(timestamp)
        
        """
        status = 144
        note = 38
        velocity = 100
        timestamp = pygame.midi.time()
        """
        
        try:
            midi_out.write([[[status,note,velocity],timestamp]])
        except:
            pass
        
        #print "received data:", data
        #conn.send(data)  # echo
    conn.close()
    print 'connection terminated'
    
    
    
