#!/bin/python3

import socket
import sys

HOST = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST,53))
    while True:
        data = s.recvfrom(1024)
        print(data[0])

print("socket closed")
