#!/usr/bin/env python3

from argparse import ArgumentParser
from socket import AF_INET, socket, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET

parser = ArgumentParser(description='TCP client')
parser.add_argument('-t', '--timeout', default='5', type=int, help='socket timeout')
parser.add_argument('-a', '--adress', default='127.0.0.1', help='Address to connect')
parser.add_argument('-p', '--port', default=7000, type=int, help='Port to connect')
parser.add_argument('-m', '--message', default=None, type=str, help='Message send to server')
args = parser.parse_args()


class TcpClient:
    def __init__(self, addr, port, msg, timeout):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.timeout = timeout
        self.addr = addr
        self.port = port
        self.msg = str(msg)

    def run(self):
        try:
            self.sock.settimeout(self.timeout)
            self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.sock.connect((self.addr, self.port))
            self.sock.send(bytes(self.msg, 'utf-8'))
            print('send data to ', self.addr, '=>\n', self.msg)
            data = self.sock.recv(1024)
            data_str = data.decode('utf-8')
            print('data received from ', self.addr, '<=\n', data_str)
            self.sock.close()
        except Exception as er:
            print(er)


def connect():
    if (args.message == None):
        print('you must specify message [-m]')
        return
    cli = TcpClient(args.adress, args.port, args.message, args.timeout)
    cli.run()


if __name__ == "__main__":
    connect()
