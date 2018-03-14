#This code is made under Python 3.5
import sys
from socket import *
import threading
import time
if len(sys.argv) != 3:
	print('Only require Server IP and port.')
	sys.exit()
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2])

# serverName = str('127.0.0.1')
# serverPort = 12008

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
addressAndUsername = {}
usernameAndAddress = {}
socketAndAddress = {}
privateState = 0

def judgeRecvData(recvData):
    global logOutState
    recvData = recvData.split('|&') 
    if recvData[0] == '*':
        if len(recvData) > 1:
            for i in range(1,len(recvData)):
                print('>{}'.format(recvData[i]))
        else:
            return
    elif recvData[0] == 'User logout successfully':
    	#print('has been logout')
    	logOutState = 1
    	clientSocket.close()
    	sys.exit()
    elif recvData[0] == 'ObjAddress':
    	#get private require prepare to be server
    	addressAndUsername[(recvData[1],int(recvData[2]))] = recvData[3]
    	usernameAndAddress[recvData[3]] = (recvData[1],int(recvData[2]))
    	t4 = threading.Thread(target=privateServer,args = (recvData[1],int(recvData[2]),int(recvData[4])))
    	pass
    elif recvData[0] == 'UserAddress':
    	#have get the private IP and port ready to send message
    	addressAndUsername[(recvData[1],int(recvData[2]))] = recvData[3]
    	usernameAndAddress[recvData[3]] = (recvData[1],int(recvData[2]))
    	
    	pass
    else:
    	print('>{}'.format(recvData[0]))

def privateServer(IP,port,localport):
	privateServerSocket = socket(AF_INET, SOCK_STREAM)
	privateServerSocket.bind(('',localport))
	privateServerSocket.listen(5)
	while True:
		connectPrivateSocket, add = privateServerSocket.accept()
		socketAndAddress[connectPrivateSocket] = add
		privateMessage = connectPrivateSocket.recv(1024)
		privateMessage = bytes.decode(recv_data)
		privateMessage = privateMessage.split(' ')
		printMessage = ''
		for i in range(2,len(privateMessage)):
			printMessage = printMessage + privateMessage[i] + ' '
		print('>'+addressAndUsername[socketAndAddress[connectPrivateSocket]]+printMessage)

def privateMessage(msg):
	if msg[1] in privateUser:
		privateSocket = socket(AF_INET, SOCK_STREAM)
		privateSocket.connect(usernameAndAddress[msg[1]])
		privateMsg = ''
		for i in range(2,len(msg)):
			privateMsg = privateMsg + msg[i] + ' ' 
		privateSocket.send(str.encode(privateMsg))
		backmsg = bytes.decode(privateSocket.recv(1024))
		print('>{}(private): '.format(msg[1])+backmsg)

def getInput():
	global logOutState
	while True:
		if logOutState == 1:
			break
		msg = input('>')
		if len(msg) == 0:
			continue
		elif msg == 'exit':
			break
		msg = msg.split(' ')
		if msg[0] == 'private':
			t3 = threading.Thread(target=privateMessage,args=msg)
			threads.append(t3)
		else:
			outmsg = ''
			for i in msg:
				outmsg = outmsg + i + ' '
		outmsg = str.encode(outmsg)		
		clientSocket.send(outmsg)
		time.sleep(0.3)

def recvDataFuction():
	while True:
		recvData = bytes.decode(clientSocket.recv(1024))
		if not recvData:
			continue
		elif len(recvData) != 0:
			judgeRecvData(recvData)

while True:
	Username = input('Username:')
	Password = input('Password:')
	UPinfo = str.encode('UPinfo '+Username+' '+Password)
	clientSocket.send(UPinfo)
	recvData = bytes.decode(clientSocket.recv(1024))
	print ('From Server:', recvData)
	if recvData == 'Invalid this user.':
		continue
	elif recvData == 'Invalid Password. Please try again.':
		while recvData == 'Invalid Password. Please try again.':
			Password = input('Password:')
			UPinfo = str.encode('UPinfo '+Username+' '+Password)
			clientSocket.send(UPinfo)
			recvData = bytes.decode(clientSocket.recv(1024))
			print ('From Server:', recvData)
			if recvData == 'Welcome!!':
				break
	if recvData == 'Welcome!!':
		break
threads = []

logOutState = 0
t1=threading.Thread(target=getInput)
t2=threading.Thread(target=recvDataFuction)
threads.append(t2)
threads.append(t1)
for t in threads:
	t.setDaemon(True)
	t.start()
t.join()



clientSocket.close()
