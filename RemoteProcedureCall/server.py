import socket
import os
import json
import math
import threading
    
def floor(params):
    return math.floor(float(params[0]))

def nroot(params):
    return pow(int(params[1]), (1/int(params[0])))

def reverse(params):
    return str(params[0])[::-1]

def validAnagram(params):
    s1 = str(params[0]).replace(" ", "").lower()
    s2 = str(params[1]).replace(" ", "").lower()
    if len(s1) != len(s2): return False
    return sorted(s1) == sorted(s2)

def sort(params):
    return sorted(params)
    
functions = {
    "floor" : floor,
    "nroot" : nroot,
    "reverse" : reverse,
    "validAnagram" : validAnagram,
    "sort" : sort
}
    
def dispatch(request_str):
    try:
        request = json.loads(request_str)
        method = request["method"]
        params = request["params"]
        request_id = request["id"]
        if method in functions:
            results = functions[method](params)
            response = {
                "results" : results,
                "result_type" : str(type(results)),
                "id" : request_id
            }
        else :
            response = {
                "results" : "No method found.",
                "result_type" : "Error",
                "id" : request_id
            }
        return json.dumps(response)
    except Exception as e:
        response = {
            "results" : str(e),
            "result_type" : str(type(e)),
            "id" : request_id
        }
        return json.dumps(response)

    
def handle_client(connection, client_address):
    client_address = client_address
    client_file = connection.makefile('rw', encoding='utf-8')
    for line in client_file:
        request_str = line.strip()
        request_str = dispatch(request_str)
        client_file.write(request_str + '\n')
        client_file.flush()
    connection.close()

class RPC_Server:
    def __init__(self):
        config = json.load(open('config.json'))
        self.address = config['filepath']
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def start(self):
        try:
            os.unlink(self.address)
        except FileNotFoundError:
            pass
        self.server_socket.bind(self.address)
        self.server_socket.listen()
        while True:
            connection, client_address = self.server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(connection, client_address))
            thread.start()

def main():
    server = RPC_Server()
    server.start()

if __name__ == "__main__":
    main()