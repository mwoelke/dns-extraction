#!/bin/python3

import socket
import sys

HOST = "127.0.0.1"
PORT = 53

def SortMessages(messages):
    pass


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST,PORT))
    while True:
        print("Server is up and running")
        data = s.recvfrom(1024)
        data = data[0]
        # greps the length field
        rec_length = data[12:13]
        # greps the message
        rec_incoming_messages = data[13:-5]
        print(data)
        print(type(data))
        print("length: ",rec_length)
        print("message: ", rec_incoming_messages)
        if len(rec_incoming_messages) > 63:
            message1 = rec_incoming_messages[:63]
            message2 = rec_incoming_messages[64:]
            concat_message = message1+message2
            print("concat message: ", concat_message)



