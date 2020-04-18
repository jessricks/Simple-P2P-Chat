# Jessica Ricksgers
# CIS 457
# Project 2
# P2P Chat With Emojis

import socket
import sys
#import emoji
# emojis not importing properly
import threading
import tkinter as tk

# FUNCTIONS #

def listenForConnection(portd, si):
    si = socket.socket()
    si.bind(('', portd))
    print("socket binded to " + str(portd))
    si.listen(5)
    print("listening")
    c, addr = si.accept()
    print("Got a connection from ", addr)
    return c

def connectToListener(port, s, host):
    s.connect((host, port))
    return s

def sendData(s, toSend):
    sendString = toSend.get()
    sent = "ME: " + sendString
    List.insert(tk.END, sent)
    s.sendall(sendString.encode())

def receiveData(s):
    while True:
        data = (s.recv(4096)).decode()
        data = "FRIEND: " + data
        if not data: sys.exit(0)
        List.insert(tk.END, data)

def closeConnection(s):
    s.close()
    exit(0)

# MAIN #

sock = socket.socket()
port = int(input("Enter port no: "))
host = input("Enter host (127.0.0.1) : ")

try:
    connectToListener(port, sock, host)
    c = sock
except:
    print("... ")
    c = listenForConnection(port, sock)

# GUI #

mainGUI = tk.Tk()
mainGUI.title('P2P Chat')
Frame = tk.Frame(mainGUI)
mainGUI['background']= '#856ff8'
scroll = tk.Scrollbar(Frame)
List = tk.Listbox(Frame, height=20, width=50, yscrollcommand=scroll.set, font=30)
List['background']= '#856ff8'
scroll.pack(side=tk.RIGHT, fill=tk.Y)
List.pack(side=tk.LEFT, fill=tk.BOTH)
List.pack()
Frame.pack()
toSend = tk.StringVar()
message = tk.Entry(mainGUI, textvariable=toSend)
message.pack(side=tk.LEFT)
send = tk.Button(mainGUI, text="Send", command=lambda: sendData(c, toSend))
send.pack(side=tk.LEFT)
close = tk.Button(mainGUI, text="Quit", command=lambda: closeConnection(c))
close.pack(side=tk.RIGHT)
message.pack()
send.pack()
close.pack()
threading.Thread(target=receiveData, args=(c,)).start()
mainGUI.mainloop()
