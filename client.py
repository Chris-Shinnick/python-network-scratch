#!/usr/bin/env python3
"""Script for TkinterGUI chat client."""

from socket import AF_INET, socket ,SOCK_STREAM
from _thread import *
import tkinter
from network import Network

def receive(n,conn):
        """Handles receiving of messages."""
        while True:
            try:
                msg = n.receive(conn)
                msg_list.insert(tkinter.END,msg)
            except OSError: #OSError. Possibly client has left the chat.
                break
        
def send(event=None): #event is passed by binders.
    msg = my_msg.get()
    my_msg.set("") # Clears input field.
    N.send(conn,msg)
    if msg == "{quit}":
        conn.close()
        top.quit()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()



top = tkinter.Tk()
top.title("Chatter")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

N = Network()
conn = N.connect()

def main():
    start_new_thread(receive,(N,conn))
    tkinter.mainloop()

main()    