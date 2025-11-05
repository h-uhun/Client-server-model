import socket
import os
import json
import faker

config = json.load(open('config.json'))
server_address = config['filepath']

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

fake = faker.Factory.create()

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

print('Starting up on {}'.format(server_address))

sock.bind(server_address)

sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        print(f"connection from : {client_address}")

        while True:
            data = connection.recv(16).decode()
            print('Received ' + data)
            if data:
                response = 'Processing ' + fake.name()
                connection.sendall(response.encode())
            else:
                print('no data from', client_address)
                break
    finally:
        print("Closing current connection")
        connection.close()