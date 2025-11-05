import socket
import sys
import json

config = json.load(open('config.json'))
server_address = config['filepath']

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

print('connecting to {}'.format(server_address))

try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)

while True:
    input = sys.stdin.buffer.readline()
    if(input.decode('utf-8').strip() == 'exit'):
        break
    sock.sendall(input)
    data = sock.recv(32).decode()
    if data:
        print('Server response: ' + data)

print('closing socket')
sock.close()