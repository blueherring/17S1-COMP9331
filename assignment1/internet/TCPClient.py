import sys
total = len(sys.argv)
cmdargs = str(sys.argv)

from socket import *
serverName = str('127.0.0.1');
serverPort = 12002 #change this port number if required
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(str.encode(sentence))
modifiedSentence = clientSocket.recv(1024)
print ('From Server:', bytes.decode(modifiedSentence))
clientSocket.close()
