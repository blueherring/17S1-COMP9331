import socket
import sys
import time
import copy

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
		del cost[i]

# fileName = sys.argv[3]
# NODE_ID = sys.argv[1]
# NODE_PORT = int(sys.argv[2])

# NODE_ID = input('node id')
# NODE_PORT = int(input('node port'))
# fileName = input('which file you want?')
inputInfo = input('~~')
inputInfo = inputInfo.strip().split(' ')
NODE_ID = inputInfo[0]
NODE_PORT = int(inputInfo[1])
fileName = inputInfo[2]

IP = '127.0.0.1'

info = readfile(fileName)
nodeNB = len(info)
cost = {NODE_ID:[NODE_ID,0]}
targetPort = {}
originalCost = {}
blackNote = []
portAliveTime = {}

for i in info:
	originalCost[i[0]] = i[1]
	cost[i[0]]=[NODE_ID,i[0],i[1]]
	targetPort[i[0]] = int(i[2])
	


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.settimeout(1)

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
		print('send:',sMessage)
		s.sendto(str.encode(sMessage),(IP,targetPort[i]))
	
	
	for _ in range(nodeNB):
		s.close()

		time.sleep(1)

		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.settimeout(6-nodeNB)
		s.bind((IP,NODE_PORT))
		try:
			data,addr = s.recvfrom(1024)
			message = bytes.decode(data)
			message = message.strip('|').split('|')
			print('receive:',message)
			for i in message:
				i = i.strip().split(' ')
				costUpdate(cost,i)
			printShortestPath(cost)
			print('-----------------------------------------------')
		except Exception as e:
			printShortestPath(cost)
			print('-----------------------------------------------')

	