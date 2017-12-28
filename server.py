"""Multi-Chat server application"""
import socket
import sys
import select
import threading


class ChatServer(threading.Thread):
    """Server Class"""

    def __init__(self, ):
        threading.Thread.__init__(self)
        self.host = ''
        self.port = 10000
        self.clientlist = []
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recvdict = {}
        self.message = ''

    def socketbind(self):
        """Binds host and port to form socket"""

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            sys.exit()
        self.server.listen(100)
        self.clientlist.append(self.server)
        self.recvdict[self.server] = 'Server'

    @classmethod
    def receivedata(cls, sock):
        """Receiving data"""
        data = ''
        data = sock.recv(2048)
        return data

    def endserver(self):
        """Closing Server"""
        self.server.close()
        sys.exit()

    def startserver(self):
        """Start the two functions socketbind and validate"""
        self.socketbind()
        self.senddata()

    def senddata(self):
        """filter the recevied data to send to particular node"""

        while True:
            try:
                readsock, writesock, errorsock = select.select(
                    self.clientlist, [], [])
            except socket.error:
                continue
            for sock in readsock:
                if sock == self.server:
                    try:
                        conn, addr = self.server.accept()
                    except socket.error:
                        break
                    else:
                        self.clientlist.append(conn)
                else:
                    try:
                        data = self.receivedata(sock)
                        data = str(data)
                        detail = data.split('<<')
                        recvname = detail[0]
                        self.message = detail[1]

                        senderdetail = self.message.split(':')
                        sendername = senderdetail[0]
                        self.recvdict[sock] = sendername

                        self.broadcast(sock, self.message, recvname)

                    except socket.error:
                        continue
        self.endserver()

    def broadcast(self, sock, msg, recvname):
        """Send messages to all active clients"""
        msg.encode()
        print(msg, )
        for clients in self.clientlist:
            print(1, )
            if clients != self.server and clients != sock and msg:
                print(2, )
                for receivername in self.recvdict[sock]:
                    print(3, )
                    if receivername == recvname:
                        try:
                            print(receivername, )
                            clients.send(msg)
                        except socket.error:
                            clients.close()
                            self.clientlist.remove(clients)
                    else:
                        continue
            else:
                if clients in self.clientlist:
                    self.clientlist.remove(clients)
