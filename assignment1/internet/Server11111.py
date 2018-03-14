#This code is made under Python 3.5
from socket import *
from select import select
import time
import sys
def getUsernamePassword():
    with open('credentials.txt') as file:
        data =[]
        temp =[]
        for i in file.read().strip().split('\n'):
            temp.append(i)
        for i in temp:
            j=i.split()
            data.append(j)
    return data


def judgeCommand(recv_data,obj):
    clientCommand = bytes.decode(recv_data)
    print(clientCommand)
    clientCommand = clientCommand.split(' ')
    print(clientCommand)
    #log in---------------------------------
    if clientCommand[0] == 'UPinfo':
        if clientCommand[1] in userAndPassword:
            for i in onLineClients:
                if onLineClients[i] == clientCommand[1]:
                    return 'User has been log in',obj
            if clientCommand[1] not in blockList or (clientCommand[1] in blackList and (time.time()-blockList[clientCommand[1]]) > blockDuration):
                if clientCommand[1] in blockList:
                    del blackList[clientCommand[1]]
                if clientCommand[2] == userAndPassword[clientCommand[1]]:
                    print('Right Username and password')
                    onLineClients[obj] = clientCommand[1]
                    lastActiveTime[obj] = time.time()
                    #print('1------------------')
                    presenceBroadcasts(obj,1)
                    #print('2------------------------------')
                    onLineHistory[clientCommand[1]] = time.time()
                    loginTime[clientCommand[1]] = time.time()
                    return 'Welcome!!',obj
                else:
                    if wrongPasswordList[clientCommand[1]] < 2:
                        wrongPasswordList[clientCommand[1]] += 1
                        return 'Invalid Password. Please try again.',obj
                    else:
                        blockList[clientCommand[1]] = time.time()
                        wrongPasswordList[clientCommand[1]] = 0
                        return 'Invalid Password. Your account has been blocked. Please try again later.',obj
            elif (time.time()-blockList[clientCommand[1]]) <= blockDuration:
                return'Your account is blocked due to multiple login failures. Please try again later.',obj
        else:
            return 'Invalid username.',obj
    #send message---------------------------
    elif clientCommand[0] == 'message':
        if clientCommand[1] in userAndPassword and clientCommand[1] != onLineClients[obj]:
            print('right object')
            if checkBlackList(obj,clientCommand[1]):
                print('been block')
                return 'You message could not be delivered as the recipient has blocked you',obj
            else:
                for i in onLineClients:
                    if onLineClients[i] == clientCommand[1]:
                        print('find object user socket')
                        return onLineClients[obj]+':'+clientCommand[2],i
                #the user is no on the line
                print('objcet not online')
                offlineMessaging[clientCommand[1]] = onLineClients[obj]+':'+clientCommand[2]
                return None,None
        else:
            return 'Error. Invalid user',obj
    #broadcast-------------------------------
    elif clientCommand[0] == 'broadcast':
        beBlockOrNot = 0
        for i in onLineClients:
            if checkBlackList(obj,onLineClients[i]):
                beBlockOrNot = 1
                continue            
            else:
                if i != obj:
                    i.send(str.encode(onLineClients[obj]+':'+clientCommand[1]))
                else:
                    continue
        if beBlockOrNot == 1:
            return 'Your message could not be delivered to some recipients',obj
        return None,None
    #block & unblock---------------------------
    elif clientCommand[0] == 'block':
        if clientCommand[1] in userAndPassword:
            if clientCommand[1] != onLineClients[obj]:
                blackList[onLineClients[obj]].append(clientCommand[1])
                return clientCommand[1]+' is blocked',obj
            else:
                return 'Error. Cannot block self',obj
        else:
            return 'Error. Invalid user',obj
    elif clientCommand[0] == 'unblock':
        if clientCommand[1] in blackList[onLineClients[obj]]:
            blackList[onLineClients[obj]].remove(clientCommand[1])
            return clientCommand[1]+' is unblocked',obj
        else:
            return 'Error. '+clientCommand[1]+'was not blocked',obj
    #whoelse---------------------------------
    elif clientCommand[0] == 'whoelse':
        outOnlineList =[]
        outMessage = '*'
        for i in onLineClients:
            if i != obj:
                outOnlineList.append(onLineClients[i])
            else:
                continue
        for i in outOnlineList:
            outMessage = outMessage+'|&'+i
        #print(outMessage)
        return outMessage,obj
    #whoelseSince-------------------------------
    elif clientCommand[0] == 'whoelsesince':
        outOnlineSince = '*'
        for i in loginTime:
            if i != onLineClients[obj]:
                if (time.time()-loginTime[i]) < clientCommand[1]:
                    outOnlineSince = outOnlineSince+'|&'+i
        return outOnlineSince,obj
    #logout--------------------------------------
    elif clientCommand[0] == 'logout':
        logOut(obj)
        return None,None
    #startPrivate---------------------------------------
    elif clientCommand[0] == 'startprivate':
        if checkBlackList(obj,clientCommand[1]):
            return 'You could not be delivered private messaging as the recipient has blocked you',obj
        else:
            if clientCommand[1] == onLineClients[obj]:
                return 'Error. Cannot private with self',obj
            else:
                userAddress = 'UserAddress'
                for i in onLineClients:
                    if onLineClients[i] == clientCommand[1]:
                        userAddress = userAddress+'|&'+clientMap[i][0]+'|&'+str(clientMap[i][1])
                        objAddress = 'ObjAddress'+'|&'+clientMap[obj][0]+'|&'+str(clientMap[obj][1])
                        i.send(objAddress)
                        return userAddress,obj
                    else:
                        return clientCommand[1]+' is not online',obj
    #-------------------------------------------------------------------------
    else:
        return 'Wrong command',obj

        




def timeOutCheck(outTime):
    if outTime == 0:
        return
    else:
        if lastActiveTime:
            for i in lastActiveTime:
                if (time.time() - lastActiveTime[i]) > outTime:
                    logOut(i)
                    return
    return

def getOnlineHistory():
    if onLineHistory:
        for i in onLineHistory:
            if (time.time() - onLineHistory[i]) > 900:
                onLineHistory.pop(i)
        outOnLineHistory = []
        for i in onLineHistory:
            outOnLineHistory.append([i,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(onLineHistory[i]))])
    return outOnLineHistory


def logOut(i):
    i.send(str.encode('User logout successfully'))
    print('send log out message')
    input_list.remove(i)
    lastActiveTime.pop(i)
    clientMap.pop(i)
    presenceBroadcasts(onLineClients.pop(i),0)
    i.close()
    return

def presenceBroadcasts(userSocket,logstate):
    if onLineClients:
        #print('1----------------')
        for i in onLineClients:
            if userSocket != i:
                #print('2------------------------')
                if onLineClients[userSocket] not in blackList[onLineClients[i]]:
                    
                    if logstate == 0:
                        i.send(str.encode(onLineClients[userSocket] + 'log out.'))
                    if logstate == 1:
                        i.send(str.encode(onLineClients[userSocket] + 'log in.' ))
                    #print('3-------------------------------')
                    continue
            else:
                continue
        return
    else:
        return

def sendOfflineMessags():
    for i in onLineClients:
        if onLineClients[i] in offlineMessaging:
            i.send(offlineMessaging.pop(onLineClients[i]))
    return

def creatBlackList(blackList):
    for i in userAndPassword:
        blackList[i] = []

def checkBlackList(fromUserSocket,toUser):
    if onLineClients[fromUserSocket] in blackList[toUser]:
        return 1
    else:
        return None
    

data = getUsernamePassword()
userAndPassword = {}
blockList = {}
wrongPasswordList ={}
for i in data:
    userAndPassword[i[0]] = i[1]
    wrongPasswordList[i[0]] = 0
##print(userAndPassword)
##serverPort = int(sys.argv[1])
##blockDuration = int(sys.argv[2])
##outTime = int(sys.argv[3])
serverPort = 12008
outTime = 0
blockDuration = 10

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
serverSocket.setblocking(False)
print ("The server is ready to receive")

input_list = [serverSocket]
output_list = []


onLineClients = {} #socket:user
outPut = {} #socket:message
lastActiveTime = {} #socket:time
onLineHistory = {} #user:time
loginTime = {} #user:time
offlineMessaging = {} #user:message
blackList = {} #user:user
clientMap = {} #socket:address
creatBlackList(blackList)
serverRunningTime = time.time()

while 1:
    timeOutCheck(outTime)
    serinput, seroutput, sererror = select(input_list, output_list, input_list)

    for obj in serinput:
        if obj == serverSocket:
            connectionSocket, addr = serverSocket.accept()
            input_list.append(connectionSocket)
            clientMap[connectionSocket] = addr
            print('new soecket')
        else:
            try:
                recv_data = obj.recv(1024)
                if recv_data:
                    lastActiveTime[obj] = time.time()
                    returnInfo, returnObj = judgeCommand(recv_data,obj)
                    print('return result')
                    print(returnInfo,returnObj)
                    if returnInfo and returnObj:
                        outPut[returnObj] = returnInfo
                        print('socket and message')
                        print(outPut)
                        print(output_list)
                        if returnObj not in output_list:
                            output_list.append(obj)
                print('receive data')
            except Exception :
                input_list.remove(obj)
        print('in serinput---------------------------')
                
    print(output_list)
    for returnObj in output_list:
        print('go seroutput ')
        print(returnObj,outPut[returnObj])
        try:
            if outPut[returnObj]:
                send_data = outPut[returnObj]
                outPut[returnObj] = None
                returnObj.send(str.encode(send_data))
                #output_list.pop(returnObj)
                print('send data-------------------------')
                print()

            else:
                output_list.remove(returnObj)

        except Exception :
            output_list.remove(returnObj)
    sendOfflineMessags()       
    
##    capitalizedSentence = sentence.upper()
##    connectionSocket.send(capitalizedSentence)
##    connectionSocket.close()

