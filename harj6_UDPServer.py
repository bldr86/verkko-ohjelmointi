#!/usr/bin/python
# -*- coding: UTF-8 -*-

# UDP chat-palvelin
# Ottaa vastaan asiakkaiden chat-viestejä
# ja välittä ne muille asiakkaille

import socket


HOST = '127.0.0.1'
PORT = 24001
size = 1024
connections = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))


while True:
    print "UDP Server listening"
    recv_data, addr = s.recvfrom(size)
    if addr not in connections:
        connections.append((addr[0],addr[1]))
    print recv_data
    data = recv_data
    recv_data = None
    if data != None:
        for connection in connections:
            try:
                s.sendto(data, connection)
                print 'sending to: ' + connection
            except TypeError:
                print 'No data to send'
        data = None


s.close()