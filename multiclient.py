#!/usr/bin/python3
"""Client Program - Minimum 2 clients needed"""
import socket
import sys
import select
import threading


class ChatClient(threading.Thread):
    """Client chat class"""

    def __init__(self, usrname, recvrname):
        threading.Thread.__init__(self)
        self.host = ''
        self.port = 10000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientlist = []
        self.name = usrname
        self.frndname = recvrname

    def startconnection(self):
        """Connecting to server"""
        self.server.settimeout(2)
        try:
            self.server.connect((self.host, self.port))
        except socket.error as msg:
            print("Can't connect ", msg)
            sys.exit()
        print("Connected to server", )
        sys.stdout.flush()
        self.waitfordata()

    @classmethod
    def waitfordata(cls):
        """Getting user data and flushing the buffer"""
        sys.stdout.write('>')
        sys.stdout.flush()

    def startchat(self):
        """Start to receive and send data simultaneously"""

        while True:
            self.clientlist = [sys.stdin, self.server]
            readsock, writesock, errorsock = select.select(
                self.clientlist, [], [])
            for clients in readsock:
                if clients == self.server:
                    data = clients.recv(2048)
                    if not data:
                        print('\n Disconnected', )
                        self.server.close()
                        sys.exit()
                    else:
                        sys.stdout.write(data.decode('utf-8'))
                        self.waitfordata()

                else:
                    message = sys.stdin.readline()
                    if message == '\n':
                        continue
                    message = self.frndname + '<<' + self.name + ':' + message
                    self.server.send(message.encode('utf-8'))
                    self.waitfordata()
                    continue
        self.endchat()

    def endchat(self):
        """Program To end chat"""
        exitmessage = self.frndname + '<<' + self.name + ' Disconnected\n'
        self.server.send(exitmessage.encode('utf-8'))
        self.server.close()
        sys.exit()

    def startclient(self):
        """Starts the client program by calling startconnection and
        startchat program """
        self.startconnection()
        self.startchat()
