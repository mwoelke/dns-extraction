#!/bin/python3

import socket
from base64 import b64decode
import datetime
import sys

HOST = "127.0.0.1"
PORT = 53

def extract_messages(rec_incoming_messages) -> bytes:
    """
    Extract message parts from incoming messages
    """

    # Initialize an empty bytes object to hold the concatenated message
    concat_message = b""

    # Iterate over the bytes object in steps of 64 bytes (63 bytes of message + 1 byte dividing character)
    for i in range(0, len(rec_incoming_messages), 64):
        # Append the first 63 bytes of each chunk to the concat_message
        concat_message += rec_incoming_messages[i:i + 63]
    
    # Return message
    return concat_message

def write_msg_to_file(msg: bytes) -> None:
    """
    Write received bytestring to a file
    """

    msg = b64decode(msg).decode("utf-8")

    # build file name and open file
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file = f"received_message_{date}.txt"
    with open(file, "w") as f:
        # write to file
        f.write(msg)

    print(f'RECEIVED NEW MESSAGE: {file}')
    print(msg)

msg = b""
if len(sys.argv) >= 2:
    HOST = sys.argv[1]

    if len(sys.argv) == 3:
        PORT = int(sys.argv[2],10)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST,PORT))
    print(f"Server is up and running on {HOST}:{PORT}")
    while True:
        data = s.recv(1024)

        # grep the length field
        # brauchen wir eigentlich nicht?
        #rec_length = data[12:13]

        # grep the message
        rec_incoming_messages = data[13:-5]

        if len(rec_incoming_messages) > 63:
            #ends the connection & adds the message to the concat message
            if rec_incoming_messages[-2:] == b"\xff\xff":
                msg += extract_messages(rec_incoming_messages[:-2])

                # Write message to disk and print to screen
                write_msg_to_file(msg)
                
                # reset incoming message
                msg = b""

            #adds the message to the concat message
            else:
                msg += extract_messages(rec_incoming_messages)
        else:
            msg = extract_messages(rec_incoming_messages[:-2])
