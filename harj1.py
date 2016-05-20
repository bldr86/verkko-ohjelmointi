#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Skripti joka luo soketilla yhteyden web-palvelimeen,
# noutaa sieltä sivun ja tulostaa noudetun tavaran
# ruudulle ilman HTTP-headeria.
import socket

HOSTNAME = "127.0.0.1"
PORT = 25000
READBUF = 1024
s = None
command = "GET / HTTP/1.1\r\nHost: "+ HOSTNAME + "\r\nConnection: Close\r\n\r\n"
printdata = ""

for res in socket.getaddrinfo(HOSTNAME, PORT, socket.AF_INET, 
        socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
          s = socket.socket(af, socktype, proto)
        except socket.error:
          s = None
          continue
        try:
          s.connect(sa)
        except socket.error, msg:
          s.close()
          s = None
          continue
        
        if s:
          s.send(command)
          finished = False
          count = 0
          while not finished:
            data = s.recv(READBUF)
            count = count + 1
            if len(data) != 0:
              printdata = printdata + data
            else:
              finished = True
        s.shutdown(socket.SHUT_WR)
        s.close()
        break
          
print printdata[printdata.find("<html>"):]
