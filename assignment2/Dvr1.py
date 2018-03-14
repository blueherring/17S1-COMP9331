import socket
import sys
import time
import copy
import threading

def readfile(file):
  f=open(file)
  line=f.readline()
  adjnode=[]
  while line:
      #print(line)
      
      line=f.readline()
      if line is not "":
          adjnode.append(line.split())
  return adjnode

def toString(List,sendID,cost):
	l1 = copy.deepcopy(List)
	l1.insert(0, sendID)
	l1[-1] = str(int(l1[-1])+int(cost))
	message = ''
	for i in l1:
		message = message+i+' '
	return message

def costUpdate(cost,Message):
	global portAliveTime
	if Message[-2] not in cost:
		cost[Message[-2]] = Message
		portAliveTime[Message[-2]] = time.time()
	else:
		if int(cost[Message[-2]][-1]) >= int(Message[-1]):
			cost[Message[-2]] = Message
			portAliveTime[Message[-2]] = time.time()

def printShortestPath(cost):
	for i in cost:
		if i == NODE_ID:
			continue
		print('shortest path to node ',i,': the next hop is ',cost[i][1],' and the cost is ',cost[i][-1])

def checkAlive():
	global targetPort
	global portAliveTime
	global cost
	t = time.time()
	for i in portAliveTime:
		if t-portAliveTime[i] > 5:
			if i not in blackNote:
				blackNote.append(i)
		else:
			if i in blackNote:
				blackNote.remove(i)

	remove = []		
	for i in blackNote:
		for j in cost:
			if i in cost[j]:
				remove.append(j)
	for i in remove:
		if i in cost:
			del cost[i]


def sendMessageFuction():
	global cost
	global targetPort
	global originalCost
	global s
	global portAliveTime
	while 1:
		checkAlive()
		sendMessage =[]
		for i in cost:
			sendMessage.append(cost[i])

		for i in targetPort:
			sMessage = ''
			for j in sendMessage:
				if i not in j:
					sMessage = sMessage + toString(j,i,originalCost[i])+'|'
			#print('send:',sMessage)
			s.sendto(str.encode(sMessage),(IP,targetPort[i]))
			time.sleep(1)
		
def receive():
	global cost
	global s
	global portAliveTime
	global copytime
	global costCopy
	while 1:
		try:
			data,addr = s.recvfrom(1024)
			message = bytes.decode(data)
			message = message.strip('|').split('|')
			print('receive:',message)
			for i in message:
				i = i.strip().split(' ')
				costUpdate(cost,i)
				portAliveTime[i[1]] = time.time()
			if costCopy != cost:
				costCopy = copy.deepcopy(cost)
				copytime = time.time()
			if time.time() - copytime > 5:
				printShortestPath(cost)
				print('-----------------------------------------------')
		except socket.timeout:
			if time.time() - copytime > 5:
				printShortestPath(cost)
				print('-----------------------------------------------')
		except ConnectionResetError:
			if time.time() - copytime > 5:
				printShortestPath(cost)
				print('-----------------------------------------------')

# def poisonStar():
# 	global cost
# 	global poisonedCost
# 	global originalCost
# 	for i in poisonedCost:
# 		if poisonedCost[i] != originalCost[i]:

# 	pass

# argv = sys.argv[1:]
# if len(argv) == 3:
# 	fileName = argv[2]
# 	NODE_ID = argv[0]
# 	NODE_PORT = int(argv[1])
# elif len(argv) == 4:
# 	fileName = argv[2]
# 	NODE_ID = argv[0]
# 	NODE_PORT = int(argv[1])
#	poisonedCost = {NODE_ID:[NODE_ID,0]}

# NODE_ID = input('node id')
# NODE_PORT = int(input('node port'))
# fileName = input('which file you want?')
argv = input('~~')
argv = argv.strip().split(' ')
NODE_ID = argv[0]
NODE_PORT = int(argv[1])
fileName = argv[2]
if len(argv) == 4 and argv[3] ==  '-p':
	poisonedCost = {NODE_ID:[NODE_ID,0]}

IP = '127.0.0.1'

info = readfile(fileName)
nodeNB = len(info)
cost = {NODE_ID:[NODE_ID,0]}
targetPort = {}
originalCost = {}
portAliveTime={}
blackNote = []
costCopy = {}
copytime = time.time()


for i in info:
	originalCost[i[0]] = i[1]
	cost[i[0]]=[NODE_ID,i[0],i[1]]
	targetPort[i[0]] = int(i[-1])
	if len(argv) == 4:
		poisonedCost[i[0]]=[NODE_ID,i[0],i[2]]



s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((IP,NODE_PORT))
s.settimeout(5)

threads = []

t1=threading.Thread(target=sendMessageFuction)
t2=threading.Thread(target=receive)
threads.append(t2)
threads.append(t1)
for t in threads:
	t.setDaemon(True)
	t.start()
t.join()


# while 1:
	
	
# 	for _ in range(nodeNB):
# 		s.close()

# 		time.sleep(1)

# 		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 		

		

	