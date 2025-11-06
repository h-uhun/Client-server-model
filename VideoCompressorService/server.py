import socket
import os
import json
from pathlib import Path
import random

class CreateServer:
    def __init__(self):
        self.config = json.load(open('config.json'))
        self.SOCKET_PATH = self.config['socket_path']
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.dpath = 'temp'
    
    def start(self):
        
        if not os.path.exists(self.dpath):
            os.makedirs(self.dpath)
        
        if os.path.exists(self.SOCKET_PATH):
            os.remove(self.SOCKET_PATH)

        self.sock.bind(self.SOCKET_PATH)
        self.sock.listen(1)

        while True:
            connection, client_address = self.sock.accept()
            try:
                header = connection.recv(32)
                data_length = int.from_bytes(header, "big")
                stream_rate = 1400

                if data_length == 0:
                    raise Exception('No data to read from client.')
                
                with open(os.path.join(self.dpath, str(random.randint(1000, 9999))) + '.mp4','wb+') as f:
                    while data_length > 0:
                        data = connection.recv(stream_rate)
                        f.write(data)
                        data_length -= len(data)
                print('Finished downloading the file from client.')

            except KeyboardInterrupt:
                print('Shutting down the server')
                break
        self.sock.close()

def main():
    server = CreateServer()
    server.start()

if __name__ == "__main__":
    main()