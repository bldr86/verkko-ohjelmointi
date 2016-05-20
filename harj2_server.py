#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Luo yksinkertaisen TCP-palvelimen joka kaiuttaa
# asiakkaan viestin ja lisää perään oman viestinsä
import socket, sys

HOST = '127.0.0.1'
PORT = 24000
backlog = 5
BUF_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(backlog)
while True:
    client, address = s.accept()
    data = client.recv(BUF_SIZE)
    if data:
        client.send("Antin palvelin;" + data)
    client.close()