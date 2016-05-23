#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Peliasiakas
# Ottaa yhteyden UDP:llä pelipalvelimeen
# Pelin tarkoituksena on arvata oikea numero
# moninpelissä, missä palvelin arpoo numeron
# ja ilmoittaa voittajan


# TODO: Virheenkäsittely

import socket
import sys


HOST = '127.0.0.1'
PORT = 24001
size = 1024
name = ''
message = []
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
datagiven = False
gameover = False



def checkmessage(message, server):
    print message[0]
    status = message[0]
    code = message[1][0:message[1].find(' ')]
    print code
    global datagiven
    global gameover
    if status == 'QUIT':
    # ack('500', server)
        s.sendto('ACK;500'.rstrip(), server)
        gameover = True
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
            if not gameover:
                data(server)
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
    while not gameover:

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
