#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Peliasiakas
# Ottaa yhteyden UDP:llä pelipalvelimeen
# Pelin tarkoituksena on arvata oikea numero
# moninpelissä, missä palvelin arpoo numeron
# ja ilmoittaa voittajan


# TODO: Peruskommunikaatio
# TODO: JOIN -tila
# TODO: GAME -tila
# TODO: ACK -käsittely
# TODO: viestin kuuntelu ja käsittely ennen reagointia

import socket
import sys, select
if sys.platform == 'win32':
    import msvcrt

HOST = '127.0.0.1'
PORT = 24001
size = 1024
name = ''
message = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Read a line. Using select for non blocking reading of sys.stdin
def getLine():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False

def join(server):
    name = raw_input('Name:')
    s.sendto('JOIN;' + name, server)
    return

def game(server):
    number = raw_input('Valitse numero:')
    s.sendto('DATA;' + number, server)
    return



join((HOST, PORT))


# Jos käyttöjärjestelmänä Linux tai OSX
if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
    while True:

        try:
            s.settimeout(2)
            recv_data, addr = s.recvfrom(size)
            if recv_data:
                message.append(recv_data[0:recv_data.find(';')])
                message.append(recv_data[recv_data.find(';') + 1:])
                #sys.stdout.write(recv_data[0:recv_data.find(';')] + ': ' +
                                 #recv_data[recv_data.find(';') + 1:])
                print message
                game((HOST, PORT))

        except socket.timeout:
            pass

        input = getLine()
        if input != False:
                s.sendto(name + ';' + input, (HOST, PORT))

# Jos käyttöjärjestelmänä windows
else:
    while True:
        ready = select.select([s], [], [], 0.001)
        if ready[0]:
            recv_data = s.recv(size)
            sys.stdout.write(recv_data[0:recv_data.find(';')] + ': ' +
                             recv_data[recv_data.find(';') + 1:] + '\n')
        else:
            if msvcrt.kbhit():
                char = msvcrt.getch()
                if char == "\r":
                    s.sendto(name + ';' + raw_input(">"), (HOST, PORT))
