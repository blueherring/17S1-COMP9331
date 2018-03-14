#!/usr/bin/env python3.4.3
      
import socket
import time
import sys
import random
import re
import time
from copy import deepcopy

host = '127.0.0.1'
# NODE_ID=sys.argv[1]
# NODE_PORT=int(sys.argv[2])
NODE_ID = input('node id')
NODE_PORT = int(input('node port'))

UPDATE_INTERVAL=1
ROUTE_UPDATE_INTERVAL=30
NODE_NUM=ord(NODE_ID)-65

count=0
timeout=1
address=(host,NODE_PORT)
file_txt=''
# CONFIG_TXT=sys.argv[3]
CONFIG_TXT = input('which file you want?')
MAX=9999
alive_record=set()
fail_times=dict()



s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.settimeout(timeout)


def gettable(table,file,source):
 
    for i in file:
        index=ord(i[0])-65
        table[source][index]=int(i[1])
        table[index][source]=int(i[1])
    return table

def getlinkstate(info):#info [('AB', 2), ('AC', 5), ('AD', 1), ('ED', 3)]
    node_set=set()
 
    node_num=[]
    count=0

    for i in info:
        node_set.add(i[0][0])
        node_set.add(i[0][1])
    N=len(node_set)
    graph=[[9999 for _ in range(N)] for _ in range(N)]
    for n in info:
        if n[0][0] in node_num:
      
            i=node_num.index(n[0][0])
        else:
       
            node_num.append(n[0][0])
            i=count
            count+=1
            
        if n[0][1] in node_num:
      
            j=node_num.index(n[0][1])
        else:
        
            node_num.append(n[0][1])
            j=count
            count+=1
        graph[i][j]=n[1]
        graph[j][i]=n[1]
    return graph,node_num


def updatemessage(old,new):
    if new==old:
        return old
    else:
        for i in new:
            if i not in old:
                
                old.append(i)
    return old            

def updatetable(table,newtable):
  global N
  for l in range(N):
    for r in range(N):
      if newtable[l][r] != 9999:
        
        table[l][r]=int(newtable[l][r])
  return table

def getmessage(file,source):
    message=[]
    for i in file:
        message.append(((source+i[0]),int(i[1])))
    return message
    pass


def failnode(fail_node_set,fail_times,node_record):
    fail=[]
    for node in fail_node_set:
        fail_times[node]+=1
    for i in node_record:
        if node_record[i]==3:
           fail.append(i)
           fail_node_set.remove(i)
    return fail

def getnode(port,nodefile):
  for i in nodefile:
    if i[2] is ip:
      return i[0]
  return ""

def updatefailedtable(failed_node,table):
    node=ord(failed_node)-65
    for i in range(len(table)):
        table[i][node]=9999
        table[node][i]=9999
    return table
    
def readfile(CONFIG_TXT):
  f=open(CONFIG_TXT)
  line=f.readline()
  adjnode=[]
  while line:
      #print(line)
      
      line=f.readline()
      if line is not "":
          adjnode.append(line.split())
  return adjnode

def get_node_set(file):
    node_set=set()
    for i in file:
        node_set.add(i[0])
    return node_set
    
def update(l1,l2):
    for i in l2:
        if i not in l1:
            l1.append(i)
    return l1
  
def send(s,message,host,port):
    try:
        s.sendto(bytes(str(message),encoding="utf8"),(host,port))
    except :
        print("not sent")
        s.close()
def recv(s):
  try:
    data,addr=s.recvfrom(1024)
    return data,addr
  except socket.timeout:
    #print("timeout")
    return "",""
#table[des][start]


def dijkstra(graph,n,start,node_num):  
    dis=[0]*n  
    flag=[False]*n
    k=node_num.index(start)
    flag[k]=True  
    
    L=[start for i in range(n)]
    for i in range(n-1):  
        dis[i]=graph[k][i]  
  
    for j in range(n-1):  
        mini=9999 
        for i in range(n):  
            if dis[i]<mini and not flag[i]:  
                mini=dis[i]  
                k=i  
        if k==9999:  
            return dis,L 
        flag[k]=True
 
        for i in range(0,n):  
            if dis[i]>dis[k]+graph[k][i]:  
                dis[i]=dis[k]+graph[k][i]
                
                L[i]=L[k]+node_num[k]
                

    return dis,L   
            

file=readfile(CONFIG_TXT)
#print(file)
message=getmessage(file,NODE_ID)

graph,node_num=getlinkstate(message)

dis,pre=dijkstra(graph,len(graph),NODE_ID,node_num)


TOTAL_NODE=len(file)

node_set=get_node_set(file)
#print(node_set)
for node in node_set:
    fail_times[node]=0

#node_num=['P','Q','R','S','T','U']
#test=[[9999, 2, 5, 1.3, 9999, 9999], [2, 9999, 3, 2, 9999, 9999], [5, 3, 9999, 3, 1, 5], [1, 2, 3, 9999, 1, 9999], [9999,9999, 1, 1, 9999, 2], [9999, 9999, 5, 9999, 2, 9999]]

#test2=[[9999,1,2,5,9999,9999],[1,9999,5,9999,10,4],[2,5,9999,1,9999,9999],[5,9999,1,9999,4,9999],[9999,10,9999,4,9999,1],[9999,4,9999,9999,1,9999]]

#dis,pre=dijkstra(test2,len(test2),'P',node_num)
#print(dis,pre)



count=0
while count<10:
    count+=1
    time.sleep(UPDATE_INTERVAL)
    for i in file:
        port=int(i[2])
        send(s,message,host,port)
        send(s,NODE_NUM,host,port)
    s.close()
    
    
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.settimeout(timeout)
    s.bind(address)

    for _ in range(TOTAL_NODE*2):
        data,addr= recv(s)
        
        if data is not "" and isinstance(eval(data),list):
            message=updatemessage(message,eval(data))
     
    #print(message)
#print(message) 


table,node_num=getlinkstate(message)
NODE_NUM=node_num.index(NODE_ID)
dis,pre=dijkstra(table,len(table),NODE_ID,node_num)
#print(dis,pre)

for i in range(len(table)):
   if i !=NODE_NUM and dis[i]!=9999:
      print("least_cost path to node {:} :{:} and the cost is {:}".format(node_num[i],pre[i]+node_num[i],dis[i]))