#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Peliasiakas
# Ottaa yhteyden UDP:llä pelipalvelimeen
# Pelin tarkoituksena on arvata oikea numero
# moninpelissä, missä palvelin arpoo numeron
# ja ilmoittaa voittajan



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
        s.sendto('ACK;500'.rstrip(), server)
        gameover = True
        sys.exit(1)

    elif status == 'ACK':
        if code == '202':
            data(server)

        elif code == '203' or code == '300':
            return

    elif status == 'DATA':
        if datagiven:
            ack('300'.rstrip(), server)

            if not gameover:
                data(server)

        else:
            ack('300'.rstrip(), server)
            data(server)
        return

    else:
        if code[0:1] == '4':
            print 'Error: ' + code + status
            checkerrors(code, server)
            return

def checkerrors(code, server):
    if code == '400':
        print 'Määrittelemätön virhe, ohjelma suljetaan.'
        sys.exit('400')
    elif code == '401':
        print 'Peliin liittyminen ei onnistu, yritä myöhemmin uudelleen'
        sys.exit('401')
    elif code == '402':
        print 'Vastustajan vuoro, odota hetki'
        return
    elif code == '403':
        print 'Virheellinen ACK viesti, aja ohjelma uusiksi mikäli tämä toistuu'
        return
    elif code == '404':
        print 'Väärä kehysrakenne'
        return
    elif code == '407':
        print 'Arvaus ei ollut numero, yritä uudelleen'
        data(server)
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

    except socket.timeout:
        pass


