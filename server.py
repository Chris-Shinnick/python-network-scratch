import socket
from _thread import *
import sys
from network import Network


clients = {}
addresses = {}

N = Network()
SERVER = N.bind_server()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        conn_msg = "Greetings from the cave! Now type your name and press enter!"
        N.send(client,conn_msg)
        addresses[client] = client_address
        start_new_thread(handle_client,(client,))

def handle_client(client): # Takes client socket as argument.
    """Handles a single client connection."""
    name = N.receive(client)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    N.send(client,welcome)
    clients[client] = name
    while True:
        msg = N.receive(client)
        if msg != "{quit}":
            broadcast(msg, name+": ")
        else:
            N.send(client,"{quit}")
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % name)
            break

def broadcast(msg, prefix=""): # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        N.send(sock,prefix+msg)



SERVER.listen(5)
print("Waiting for connection...")
accept_incoming_connections()
