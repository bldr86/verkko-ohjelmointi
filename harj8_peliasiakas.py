#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Peliasiakas
# Ottaa yhteyden UDP:llä pelipalvelimeen
# Pelin tarkoituksena on arvata oikea numero
# moninpelissä, missä palvelin arpoo numeron
# ja ilmoittaa voittajan


# TODO: Peli jää jumiin jos kumpikaan ei arvaa ensimmäisellä kierroksella oikein

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
datagiven = False

# Read a line. Using select for non blocking reading of sys.stdin
def getline():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline()
            return input
    return False

def checkmessage(message, server):
    print message[0]
    status = message[0]
    code = message[1][0:message[1].find(' ')]
    print code
    global datagiven
    if status == 'QUIT':
    # ack('500', server)
        s.sendto('ACK;500'.rstrip(), server)
        sys.exit(1)
    elif status == 'ACK':
        if code == '300':
            ack(code, server)
        elif status == 'ACK' and code == '202':
            data(server)
        elif status == '203':
            return
    elif status == 'DATA':
        if datagiven:
            ack('300', server)
        else:
            data(server)
        return
    else:
        if code[0:1] == '4':
            print 'Error: ' + code + status
            return



def ack(code, server):
    s.sendto('ACK;' + code, server)
    return

def data(server):
    input = raw_input('Anna numero> ')
    global datagiven
    datagiven = True
    s.sendto('DATA;' + input.rstrip(), server)
    return

def join(server):
    input = raw_input('Anna nimesi> ')
    s.sendto('JOIN;' + input.rstrip(), server)
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

                print message
                checkmessage(message, (HOST, PORT))
                message = []
                #game((HOST, PORT))

        except socket.timeout:
            pass


        # TODO: Tän käsittely aliohjelmiin, ei toimi muuten
        '''input = getline()
        if input != False:

                s.sendto(input.rstrip(), (HOST, PORT))
'''

