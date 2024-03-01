#!/bin/python3

import socket
import sys

assert len(sys.argv) == 2
#assert len(sys.argv[1]) <= 250, "You can only send 64 bytes at once"

HOST = "127.0.0.1"


def get_dns_header(transaction_id: int) -> bytes:
    """
    Build standard DNS header with given transaction ID
    """
    # 2 Bytes: Transaction ID. Just set to 1, we don't care
    transaction_id = transaction_id.to_bytes(2, byteorder='big')

    # 2 Bytes: Flags. Just use standard headers.
    flags = b"\x01\x20"

    # 2 Bytes: Amount of questions we have. We only need one.
    no_questions = b"\x00\x01"

    # 2 Bytes: Amount of Answers. We are making a request, so no answers.
    no_answers = b"\x00\x00"

    # 2 Bytes: Number of authority. 0
    no_authority = b"\x00\x00"

    # 2 Bytes: Amount of additional information. 0
    no_additional = b"\x00\x00"

    return (transaction_id + flags + no_questions + no_answers + no_authority + no_additional)

def send_payloads(payloads: list) -> None:

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((HOST,53))

        header_count = 1

        for payload in payloads:
            body = get_dns_header(header_count)
            body += payload
            print(body)

            s.sendall(body)

            header_count += 1
        print('SUCCESS')
        return
    print('FAILED')

# split payload into several queries, each query having upto 250 bytes
query_raw = sys.argv[1].encode('ascii')
query_raw += b"\xff\xff"
all_payloads = []

count_queries = len(query_raw) // 250
if len(query_raw) % 250 != 0:
    count_queries += 1

queries = []
for i in range(count_queries):
    queries.append(query_raw[(i*250):((i+1)*250)])

# split content of each query into up to 4 parts (a.b.c.d)
for query in queries:
    count_query_parts = len(query) // 63
    if len(query) % 63 != 0:
        count_query_parts += 1

    query_parts = b""
    for i in range(count_query_parts):
        encoded = query[(i*63):((i+1)*63)]
        # append len(query) + query + 0 byte to payload
        query_parts += ((len(encoded)).to_bytes(1, byteorder='big') + encoded)
    # append 0 byte to end string
    query_parts += b"\x00\x00\x01\x00\x01"

    # append request payload to all_payloads
    all_payloads.append(query_parts)


send_payloads(all_payloads)
exit()



# TODO: loop over every 64 characters

# Variable length: Our actual payload >:D
# must be terminated with a 0 byte
# Note: The length of the field must be prepended
query_name = bytes(sys.argv[1], 'ascii') + b"\x00"
#query_name = b"\x00"
query_length = (len(query_name) - 1).to_bytes(byteorder='big')
print(f"Query is of length {len(query_name) - 1}")

# 2 Byte: Type, 1
query_type = b"\x00\x01"

# 2 Bytes: Class, 1
query_class = b"\x00\x01"

#body = header + query_length + query_name + query_type + query_class

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST,53))
    #s.sendall(bytes.fromhex("b529012000010000000000010474657374026465000001000100002904d000000000000c000a0008157fdfee532dc6b2"))
    s.sendall(bytes.fromhex("b529012000010000000000010474657374000001000100002904d000000000000c000a0008157fdfee532dc6b2"))
    #s.sendall(body)
    print('SUCCESS')
    exit()
print('FAILED')