#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Skripti joka luo soketilla yhteyden web-palvelimeen,
# noutaa sieltä sivun ja tulostaa noudetun tavaran
# ruudulle ilman HTTP-headeria.
import socket

HOST = '127.0.0.1'
PORT = 24000
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST,PORT))
s.send('moikka')

data = s.recv(size)
s.close()

print data