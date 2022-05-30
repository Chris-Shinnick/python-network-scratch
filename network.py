import socket
import pickle
import os
import configparser



class Network:
    BUFSIZE = 2048
    print(os.getcwd())
    config = configparser.ConfigParser()
    candidates = ['settings.txt']
    found = config.read(candidates)

    for key in config['settings']:
        print(key)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = self.config['settings']['host']
        self.port = int(self.config['settings']['port'])
        self.server_addr = (self.server, self.port)
        
    def bind_server(self):
        try:
            self.sock.bind(self.server_addr)
            return self.sock
        except socket.error as e:    
            print("error binding port")
            print(e)

    def connect(self):
        try:
            self.sock.connect(self.server_addr)
            return self.sock
        except socket.error as e:
            print("connection error")
            print(e)
    def send(self,conn,data):
        try:
            conn.send(pickle.dumps(data))
           
        except socket.error as e:
            print("error sending data:")
            print(e)

    def receive(self,conn):
        try:
            return pickle.loads(conn.recv(self.BUFSIZE))
        except socket.error as e:
            print("error receiving data:")
            print(e)