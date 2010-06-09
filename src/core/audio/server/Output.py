import socket


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
        print "received data:", data
        #conn.send(data)  # echo
    conn.close()
    print 'connection terminated'