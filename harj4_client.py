#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Yksinkertainen SMTP-asiakas
# Osaa käyttää HELO ja QUIT komentoja
import socket

HOST = '127.0.0.1'
PORT = 25000
size = 1024
commands = ['HELO ' + HOST + '\r\n', 'QUIT\r\n', 'MAIL FROM:', 'RCPT TO:', 'DATA' ]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ajo = True
data = ''
s.connect((HOST,PORT))
def getcode(data):
     code = data[:3]
     return code

def sendmail():
    userinput = raw_input("Enter your mail address: ")
    s.send('MAIL FROM: ' + userinput + '\r\n')
    data = s.recv(size)
    print data
    if getcode(data) == '250':
        userinput = raw_input('Recipient: ')
        s.send('RCPT TO: ' + userinput + '\r\n')
        line = getdata()
        print line
        if getcode(data) == '250':
            #line = getdata()
            #print line
            userinput = raw_input("Subject: ")
            message = userinput + '\r\n\r\n'
            userinput = raw_input("Message: ")
            message = message + userinput + '\r\n'
            s.send('DATA\r\n)')
            line = getdata()
            s.send('Subject: ' + message + '.\r\n')

            line = getdata()
            print line
            if getcode(line) == '250':
                userinput = raw_input("Send another? 1) Yes 2)No")
                newmail(userinput)
            else:
                print 'Error: Send another'
        else:
            print 'Error: Mail body'
    else:
        print 'Error: Mail from'
    return

def getdata():
    data = s.recv(size)
    line = data[0:data.find('\r\n')]
    data = data.replace(line, '')
    return line
     
def start():
    line = getdata()
    code = getcode(line)
    if code == '220':
        s.send(commands[0])
        data = s.recv(size)
        code = getcode(data)
        if code == '250':
            userinput = raw_input("1) Send 2)Quit")
            newmail(userinput)

def newmail(choice):
    if choice == '1':
        sendmail()
    elif choice == '2':
        s.send('QUIT\r\n')
    else:
        print 'Invalid choice'
        newmail()
    return

start()

s.close()

#print data[0:data.find(';')] + "\n" + data[data.find(';')+1:]