#!/usr/bin/python
# -*- coding: UTF-8 -*-

# UDP Pelipalvelin
# Palvelee kahta asiakasta numeronarvauspelissä

# TODO: WAIT ja END tilat
# TODO: WAIT_ACK ja GAME tilat
# TODO: Looginen toiminta, virheviestit ja vuoron ylläpito



import socket

# testi
HOST = '127.0.0.1'
PORT = 24001
size = 1024
connections = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))
#connections = [(,)]
playerstate = []
players = 0
names = []
STATE = "WAIT"
quitack = 0
numero = -1
on = True

def getjoin(addr, connections, data):
    global players
    global names
    if players < 2:
        connections.append((addr[0],addr[1]))
        players+=1
        names.append(data[data.find(';') + 1:])
        if len(connections) < 2:
            send('ACK;201', addr, connections)
    else:
        send('405;Liikaa pelaajia', addr)
    return

def send(data, connection, connections):
    if connection in connections:
        try:
            s.sendto(data, connection)
            print 'Sending ' + data + ' to ' + connection
        except TypeError:
            print 'No data to send'
        data = None
    else:
        print 'Connection not in connections'
    return data





while on:
    print "UDP Server listening"
    recv_data, addr = s.recvfrom(size)

    print recv_data
    data = recv_data
    recv_data = None

    if STATE == 'WAIT':
        print 'STATE: ' + STATE
        if players < 2:
            if addr not in connections:
                getjoin(addr, connections, data)
    elif STATE == 'GAME':
        print 'STATE: ' + STATE
        break
    elif STATE == 'WAIT_ACK':
        print 'STATE: ' + STATE
        break
    elif STATE == 'END':
        print 'STATE: ' + STATE
        break
    else:
        pass
   # s.sendto(recv_data, addr)

s.close()