#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Lähettää palvelimelle viestin ja vastaanottaa
# palvelimelta viestin
import socket

HOST = '127.0.0.1'
PORT = 24000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST,PORT))
s.send('moikka')

data = s.recv(size)
s.close()

print data[0:data.find(';')] + "\n" + data[data.find(';')+1:]