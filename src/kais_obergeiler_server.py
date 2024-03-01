#!/bin/python3

import socket
import sys

HOST = "127.0.0.1"
PORT = 53


def concatenate_messages(rec_incoming_messages):
    # Initialize an empty bytes object to hold the concatenated message
    # print(rec_incoming_messages)

    concat_message = b""

    # Iterate over the bytes object in steps of 64 bytes (63 bytes of message + 1 byte dividing character)
    for i in range(0, len(rec_incoming_messages), 64):
        # Append the first 63 bytes of each chunk to the concat_message
        concat_message += rec_incoming_messages[i:i + 63]

    if concat_message != b'':
        print("concat message: ", concat_message)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST,PORT))
    print("Server is up and running")
    while True:
        data = s.recv(1024)
        # greps the length field
        rec_length = data[12:13]
        # greps the message
        rec_incoming_messages = data[13:-5]
        #print(data)
        #print(type(data))
        #print("length: ",rec_length)
        #print("message: ", rec_incoming_messages)
        if len(rec_incoming_messages) > 63:
            #ends the connection & adds the message to the concat message
            if rec_incoming_messages[-2:] == b"\xff\xff":
                concatenate_messages(rec_incoming_messages[:-2])
                print('ENDE')
            #adds the message to the concat message
            else:
                concatenate_messages(rec_incoming_messages)
        else:
            concatenate_messages(rec_incoming_messages[:-2])
