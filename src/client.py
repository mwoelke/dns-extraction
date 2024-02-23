import socket
import sys

assert len(sys.argv) == 2
assert len(sys.argv[1]) <= 64, "You can only send 64 bytes at once"

HOST = "127.0.0.1"

######
### Build DNS Header
######

# 2 Bytes: Transaction ID. Just set to 1, we don't care
transaction_id = b"\x00\x01"

# 2 Bytes: Flags. Just use standard headers.
flags = b"\x01\x20"

# 2 Bytes: Amount of questions we have. We only need one.
no_questions = b"\x00\x01"

# 2 Bytes: Amount of Answers. We are making a request, so no answers.
no_answers = b"\x00\x00"

# 2 Bytes: Number of authority. 0
no_authority = b"\x00\x00"

# 2 Bytes: Number of additional information. 0
no_additional = b"\x00\x00"

header = transaction_id + flags + no_questions + no_answers + no_authority + no_additional

######
### Build actual DNS query
######

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

body = header + query_length + query_name + query_type + query_class

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST,53))
    #s.sendall(bytes.fromhex("b529012000010000000000010474657374026465000001000100002904d000000000000c000a0008157fdfee532dc6b2"))
    s.sendall(body)
    print('SUCCESS')
    exit()
print('FAILED')