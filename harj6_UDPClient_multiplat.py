#!/usr/bin/python
# -*- coding: UTF-8 -*-

# UDP asiakas
# Lähettää palvelimelle chat-viestejä sekä
# vastaanottaa muiden käyttäjien viestejä
# palvelimen kautta.
# *nix toteutus lukee suoraan käyttäjän syötettä
# win32 tarvitsee enter-painalluksen ennen viestiä

import socket
import sys, select
if sys.platform == 'win32':
    import msvcrt

# Read a line. Using select for non blocking reading of sys.stdin
def getLine():
    i,o,e = select.select([sys.stdin],[],[],0.0001)

    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False

HOST = '127.0.0.1'
PORT = 24001
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

name = raw_input('Name:')

if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
    while input != 'QUIT':

        try:
            s.settimeout(2)
            recv_data, addr = s.recvfrom(size)
            if recv_data:
                sys.stdout.write(recv_data[0:recv_data.find(';')] + ': ' +
                                 recv_data[recv_data.find(';') + 1:])

        except socket.timeout:
            pass

        input = getLine()
        if input != False:
                s.sendto(name + ';' + input, (HOST, PORT))

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
