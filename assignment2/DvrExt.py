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
	l1[0]=sendID+l1[0]
	l1[-1] = str(int(l1[-1])+int(cost))
	message = ''
	for i in l1:
		message = message+i+' '
	return message

def costUpdate(cost,Message):
	global portAliveTime
	if Message[0][-1] not in cost:
		cost[Message[0][-1]] = Message
		portAliveTime[Message[0][-1]] = time.time()
	else:
		if int(cost[Message[0][-1]][-1]) == int(Message[-1]):
			portAliveTime[Message[0][-1]] = time.time()
		if int(cost[Message[0][-1]][-1]) > int(Message[-1]):
			cost[Message[0][-1]] = Message
			portAliveTime[Message[0][-1]] = time.time()
		elif cost[Message[0][-1]][0] == Message[0] and cost[Message[0][-1]][-1] != Message[-1]:
			cost[Message[0][-1]][-1] = Message[-1]
			portAliveTime[Message[0][-1]] = time.time()

def printShortestPath(cost):
	for i in cost:
		if i == NODE_ID:
			continue
		print('shortest path to node ',i,': the next hop is ',cost[i][0][1],' and the cost is ',cost[i][-1])

def checkAlive():
	global targetPort
	global portAliveTime
	global cost
	t = time.time()
	try:
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
				if i in cost[j][0]:
					remove.append(j)
		for i in remove:
			if i in cost:
				del cost[i]
	except RuntimeError as e:
		pass


def sendMessageFuction():
	global cost
	global targetPort
	global originalCost
	global s
	global portAliveTime
	while 1:
		checkAlive()
		sendMessage =[]
		try:
			for i in cost:
				sendMessage.append(cost[i])
		
			for i in targetPort:
				sMessage = ''
				for j in sendMessage:
					if i not in j[0]:
						sMessage = sMessage + toString(j,i,originalCost[i])+'|'
				#print('send:',sMessage)
				s.sendto(str.encode(sMessage),(IP,targetPort[i]))
				time.sleep(1)
		except RuntimeError as e:
			pass

		
def receive():
	global cost
	global s
	global portAliveTime
	global copytime
	global costCopy
	global starFlag
	global argv
	count = 0
	stableState = 0
	while 1:
		try:
			data,addr = s.recvfrom(1024)
			message = bytes.decode(data)
			message = message.strip('|').split('|')
			#print('receive:',message)
			for i in message:
				i = i.strip().split(' ')
				costUpdate(cost,i)
				portAliveTime[i[1]] = time.time()
			if costCopy != cost:
				# print(cost)
				# print(costCopy)
				costCopy = copy.deepcopy(cost)
				copytime = time.time()
			if time.time() - copytime > 10:
				printShortestPath(cost)
				print('-----------------------------------------------')
				if len(argv) == 4 and count >= 10 and starFlag == 1:
					stableState += 1
					if stableState == 3:
						poisonStart()
						print('Poisoned Reverse Start')
						starFlag = 0
				if len(argv) == 5 and count >= 10 and starFlag == 1:
					stableState += 1
					if stableState == 3:
						infinityStart()
						print('Count to Infinity Start')
						starFlag = 0
		except socket.timeout:
			if time.time() - copytime > 10:
				printShortestPath(cost)
				print('-----------------------------------------------')
		except ConnectionResetError:
			if time.time() - copytime > 10:
				printShortestPath(cost)
				print('-----------------------------------------------')
		count += 1

def poisonStart():
	global cost
	global poisonedCost
	global originalCost
	remove = []
	for i in poisonedCost:
		if poisonedCost[i] != originalCost[i]:
			remove.append(i)
	for i in remove:
		if i in cost:
			del cost[i]
	originalCost = poisonedCost

def infinityStart():
	global cost
	global infinityCost
	global originalCost
	global targetPort
	remove = []
	removeTargetPort = []
	for i in infinityCost:
		if infinityCost[i] != originalCost[i]:
			remove.append(i)
		if infinityCost[i] == '-':
			removeTargetPort.append(i)
	for i in remove:
		if i in cost:
			del cost[i]
	for i in removeTargetPort:
		if i in targetPort:
			del targetPort[i]
	originalCost = infinityCost

argv = sys.argv[1:]
fileName = argv[2]
NODE_ID = argv[0]
NODE_PORT = int(argv[1])
if len(argv) == 4:
	if argv[3] == '-p':
		poisonedCost = {}
	else:
		print('Wrong commomd')
		sys.exit()
if len(argv) == 5:
	if argv[4] == '-e':
		infinityCost == {}
	else:
		print('Wrong commomd')
		sys.exit()

# NODE_ID = input('node id')
# NODE_PORT = int(input('node port'))
# fileName = input('which file you want?')

# argv = input('~~')
# argv = argv.strip().split(' ')
# NODE_ID = argv[0]
# NODE_PORT = int(argv[1])
# fileName = argv[2]
if len(argv) == 4:
	if argv[3] == '-p':
		poisonedCost = {}
	else:
		print('Wrong commomd')
		sys.exit()
if len(argv) == 5:
	if argv[4] == '-e':
		infinityCost = {}
	else:
		print('Wrong commomd')
		sys.exit()

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
starFlag = 1


for i in info:
	originalCost[i[0]] = i[1]
	cost[i[0]]=[NODE_ID+i[0],i[1]]
	targetPort[i[0]] = int(i[-1])
	if len(argv) == 4:
		poisonedCost[i[0]] = i[2]
	if len(argv) == 5:
		infinityCost[i[0]] = i[2]


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



 		

		

	