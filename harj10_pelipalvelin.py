#!/usr/bin/python
# -*- coding: UTF-8 -*-

# UDP Pelipalvelin
# Palvelee kahta asiakasta numeronarvauspelissä


import socket
import random


HOST = '127.0.0.1'
PORT = 24001
size = 1024
connections = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST,PORT))

playerturn = 0
players = 0
names = []
STATE = "WAIT"
quitack = 0
numero = -1
on = True
guess = -1

def getjoin(addr, connections, data):
    if addr != '':
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
    else:
        return

def send(data, connection, connections):
    if connection in connections:
        try:
            s.sendto(data, connection)
            print 'Sending ' + data + ' to ' + connection
        except TypeError:
            #print 'No data to send'
            pass
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
    if addr != '':
        global playerturn
        global numero
        global guess
        guess = data[data.find(';') + 1:]
        if connections[playerturn] == (addr[0],addr[1]):
            if RepresentsInt(guess):
                if int(guess) > 0 and int(guess) < 11:
                    send('ACK300;DATA OK', connections[playerturn], connections)

                    if int(guess) == numero:
                        send('QUIT;501 Voitit pelin!', connections[playerturn], connections)
                        send('QUIT;502 Vastustajasi voitti pelin.', connections[flip(playerturn)], connections)
                        state = 'END'
                        return state
                    else:
                        send('DATA;' + guess, connections[flip(playerturn)], connections)
                        state = 'WAIT_ACK'
                        return state
            else:
                send('ACK;407 Vastaus ei ollut numero', connections[playerturn], connections)
                return state
        else:
            send('ACK;402 Vaara vuoro', connections[flip(playerturn)], connections)
            return state
    else:
        return state



def wait_ack(connections, state):
    global playerturn
    if data[:data.find(';')] == 'ACK':
        if data[data.find(';') + 1:] == '300':
            playerturn = flip(playerturn)
            state = 'GAME'
            return state
        else:
            send('ACK;403 Virheellinen ACK', connections[playerturn], connections)
            state = 'WAIT_ACK'
            return state
    elif data[:data.find(';')] == 'ACK':
        send('ACK;404 Väärä kehysrakenne', connections[playerturn], connections)
        state = 'WAIT_ACK'
        return state
    else:
        state = 'WAIT_ACK'
        return state


def endgame(connections, state):
    global quitack
    global on
    if data[:data.find(';')] == 'ACK':
        if data[data.find(';') + 1:] == '500':
            quitack += 1
            if quitack == 2:
                on = False
                return state
        else:
            send('ACK;403 Virheellinen ACK', connections[playerturn], connections)
            STATE = 'WAIT_ACK'
            return state
    elif data[:data.find(';')] == 'ACK':
        send('ACK;404 Väärä kehysrakenne', connections[playerturn], connections)
        state = 'WAIT_ACK'
        return state
    else:
        return state

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def flip(i):
    return 1 - i


while on:
    recv_data = ''
    addr = ''
    data = ''
    address = ''
    try:
        s.settimeout(2)
        recv_data, addr = s.recvfrom(size)
        print recv_data
        if recv_data != '':
            data = recv_data
            recv_data = None
            address = addr

    except socket.timeout:
        recv_data = ''
        addr = ''


    if STATE == 'WAIT':
        print 'STATE: ' + STATE
        if players < 2:
            if address not in connections and address != '':
                getjoin(addr, connections, data)
        if players == 2:
            STATE = 'GAME'
            connections = startgame(connections)
    elif STATE == 'GAME':
        print 'STATE: ' + STATE
        STATE = game(address, connections, data, STATE)

    elif STATE == 'WAIT_ACK':
        print 'STATE: ' + STATE
        STATE = wait_ack(connections, STATE)

    elif STATE == 'END':
        print 'STATE: ' + STATE
        state = endgame(connections, STATE)
    else:
        pass



s.close()