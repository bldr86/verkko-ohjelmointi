#!/usr/bin/python
# -*- coding: UTF-8 -*-

# UDP Pelipalvelin
# Palvelee kahta asiakasta numeronarvauspelissä

# TODO: WAIT ja END tilat
# TODO: WAIT_ACK ja GAME tilat
# TODO: Looginen toiminta, virheviestit ja vuoron ylläpito



import socket
import random

# testi
HOST = '127.0.0.1'
PORT = 24001
size = 1024
connections = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))
#connections = [(,)]
playerturn = 0
players = 0
names = []
STATE = "WAIT"
quitack = 0
numero = -1
on = True

def getjoin(addr, connections, data):
    global players
    global names
    if players < 3:
        connections.append((addr[0],addr[1]))
        players+=1
        names.append(data[data.find(';') + 1:])
        if len(connections) == 1:
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

def startgame(connections):
    global numero
    global names
    randomnumber = random.randint(0,1)
    player1 = [names[0],connections[0]]
    player2 = [names[1], connections[1]]

    names[randomnumber] = player1[0]
    connections[randomnumber] = player1[1]

    names[flip(randomnumber)] = player2[0]
    connections[flip(randomnumber)] = player2[1]

    send('ACK;202 ' + names[1], connections[0], connections)
    send('ACK;203 ' + names[0], connections[1], connections)

    numero = random.randint(1,10)
    return connections

def game(addr, connections, data, state):
    global playerturn
    global numero
    guess = data[data.find(';') + 1:]
    if connections[playerturn] == (addr[0],addr[1]):
        if RepresentsInt(guess):
            if guess > 0 and guess < 11:
                send('ACK300;DATA OK', connections[playerturn], connections)

                if guess == numero:
                    send('QUIT;501', connections[playerturn], connections)
                    send('QUIT;502', connections[flip(playerturn)], connections)
                    state = 'QUIT'

    else:
        send('ACK;402 Väärä vuoro', connections[flip(playerturn)], connections)
    return state

def wait_ack(guess, connections):
    global playerturn
    send('DATA;' + guess, connections[flip(playerturn)], connections)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def flip(i):
    return 1 - i





while on:
    print "UDP Server listening"
    try:
        s.settimeout(2)
        recv_data, addr = s.recvfrom(size)
        print recv_data
        if recv_data != '':
            data = recv_data
            recv_data = None

        if STATE == 'WAIT':
            print 'STATE: ' + STATE
            if players < 2:
                if addr not in connections:
                    getjoin(addr, connections, data)
            if players == 2:
                STATE == 'GAME'
                connections = startgame(connections)
        elif STATE == 'GAME':
            print 'STATE: ' + STATE
            STATE = game(addr, connections, data, STATE)
            break
        elif STATE == 'WAIT_ACK':
            print 'STATE: ' + STATE
            break
        elif STATE == 'END':
            print 'STATE: ' + STATE
            break
        else:
            break
    except socket.timeout:
        print





   # s.sendto(recv_data, addr)

s.close()