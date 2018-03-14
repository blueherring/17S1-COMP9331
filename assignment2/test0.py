# -*- coding: utf-8 -*-
"""
Created on Mon May 29 22:07:31 2017

@author: Dennis
"""

import socket  
  
address = ('127.0.0.1', 31500)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
  
while True:  
    msg = input()  
    if not msg:  
        break  
    s.sendto(str.encode(msg), address)  
  
s.close()  