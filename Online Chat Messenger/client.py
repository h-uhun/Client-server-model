import socket
import sys
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ''
server_port = 9001
username = ''
usernamelen = 0

print('Connecting to the chat room.')

while True:  
    username = input('Please enter your name : ')
    if(username.strip() == 'exit'):
        print('See you later!')
        break
    usernamelen = len(username.encode('utf-8'))

    if usernamelen >= 255:
        print('Make your name shorter!!')
    else:
        print('Your username has been registerd.\n')
        break

print('connecting to {}'.format(server_address, server_port))
try:
    sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)


def get_message():
    while True:
        data, addr = sock.recvfrom(4096)
        usernamelen = data[0]
        username = data[1:1 + usernamelen].decode('utf-8')
        message = data[1 + usernamelen:].decode('utf-8')
        print(f'{username} : {message}')
get_message_thread = threading.Thread(target=get_message, daemon=True)
get_message_thread.start()

while True:
    sendMessage = input()
    if(sendMessage.strip() == 'exit'):
        print('See you later!')
        break
    usernamelen_bytes = usernamelen.to_bytes(1, 'big')
    sendMessage = usernamelen_bytes + (username + sendMessage).encode('utf-8')
    sock.sendall(sendMessage)

print('closing socket')
sock.close()