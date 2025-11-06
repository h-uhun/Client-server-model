import socket
import time
from datetime import datetime, timedelta


class CreateServer:
    def __init__(self):
        self.UDP_IP = ''
        self.UDP_PORT = 9001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.relay = {}
    
    def check_relay_time(self, relay):
        now = datetime.now()
        limit = now - timedelta(minutes=30)
        print(limit)
        delete = []
        for key, data in relay.items():
            if data["timestamp"] < limit:
                delete.append(key)
        for key in delete:
            del relay[key]
    
    def start(self):
        self.sock.bind((self.UDP_IP, self.UDP_PORT))
        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
                usernamelen = data[0]
                username = data[1:1 + usernamelen]
                message = data[1 + usernamelen:]

                self.relay[username] = {
                    "address": addr,
                    "timestamp": datetime.now()
                    }
                self.check_relay_time(self.relay)
                print(self.relay)

                usernamelen = usernamelen.to_bytes(1, 'big')
                sendMessage = usernamelen + username + message

                for value in self.relay.values():
                    self.sock.sendto(sendMessage, value["address"])

            except KeyboardInterrupt:
                print('Shutting down the server')
                break
        self.sock.close()

def main():
    server = CreateServer()
    server.start()

if __name__ == "__main__":
    main()