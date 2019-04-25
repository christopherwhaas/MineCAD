from socket import socket, gethostbyname, AF_INET, SOCK_STREAM, gethostname, SOCK_DGRAM
import pickle
import sys


#THIS FILE SHOULD BE RUN WHEN MULTIPLAYER IS DESIRED. ONLY ONE PLAYER NEEDS TO RUN THIS FILE TO HOST MULTIPLAYER
#Written based off of Documentation of Sockets Example 18.1.15 https://docs.python.org/3/library/socket.html#timeouts-and-the-accept-method

clients = {'player1':None,'player2':None}
PORT_NUMBER = 5009
SIZE = 4096

hostName = gethostbyname( gethostname() )
socket = socket( AF_INET, SOCK_DGRAM )
socket.bind( (hostName, PORT_NUMBER) )


print ("Test server listening on port %s\n at %s\n\n" % (str(PORT_NUMBER), str(gethostbyname( gethostname() ))) )

while True:
    incoming = socket.recvfrom(SIZE)
    (data,addr) = incoming
    if pickle.loads(data) == '':
        if clients.get('player2', None) == None:
            if clients.get('player1',None) != None:
                clients['player2'] = addr
                print('Player 2 Connected')
            else:
                clients['player1'] = addr
                print('Player 1 Connected')
    
    if incoming[1] == clients['player1']:
        if clients['player2']!=None:
            socket.sendto(data,clients['player2'])
    if incoming[1] == clients['player2']:
        if clients['player1']!=None:
            socket.sendto(data,clients['player1'])
    
  
    
sys.exit()