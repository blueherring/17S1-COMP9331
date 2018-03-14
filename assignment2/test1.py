# -*- coding: utf-8 -*-
"""
Created on Mon May 29 22:07:37 2017

@author: Dennis
"""

import socket  
  
address = ('127.0.0.1', 31500)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  
  
while True:  
    data, addr = s.recvfrom(2048)  
    if not data:  
        print("client has exist")
        break  
    print ("received:", data, "from", addr  )
  
s.close()  