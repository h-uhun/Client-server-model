import socket
import sys
import json
import os
import filetype

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
config = json.load(open('config.json'))
SOCKET_PATH = config['socket_path']

try:
    sock.connect(SOCKET_PATH)
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    while True:
        filepath = input('Type in a mp4 file to upload:')
        kind = filetype.guess(filepath)
        if kind is None:
            print('Supported file types : mp4')
        elif kind.extension != 'mp4':
            print('Supported file types : mp4')
        else :
            break

    with open(filepath, 'rb') as f:
        f.seek(0, os.SEEK_END)
        filesize = f.tell()
        f.seek(0,0)

        if filesize > pow(2,32):
            raise Exception('File must be below 2GB.')
        header = filesize.to_bytes(8, 'big')
        sock.send(header)

        data = f.read(1400)
        while data:
            sock.send(data)
            data = f.read(1400)
finally:
    print('closing socket')
    sock.close()