"""Multi-Chat server application"""
import socket
import sys
import select
import threading


class ChatServer(threading.Thread):
    """Server Class contains socketbind()--for starting the server, 
    receivedata()--to receive data senddata()-- sends data to client
    userdetails() -- splits user information and the message
    startserver() -- calls two function socketbind() and senddata()
    endserver() -- closes the server and make a system exit"""

    def __init__(self, ):
        threading.Thread.__init__(self)
        self.host = ''
        self.port = 10000
        self.hostname = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.recvdict = dict()
        self.clientlist = list()
        self.message = ''

    def socketbind(self):
        """Binds host and port to form socket"""

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            sys.exit()
        self.server.listen(100)
        self.clientlist.append(self.server)

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
        """filter the recevied data to send to particular node
        readsock: list ready to be read will be readsock
        """

        while True:
            try:
                readsock, writesock, errorsock = select.select(
                    self.clientlist, [], [])
            except socket.error:
                continue
            for sock in readsock:
                if sock == self.server:
                    try:  # accepts new connection here
                        conn, addr = self.server.accept()
                        self.clientlist.append(conn)
                    except socket.error:
                        break
                    else:
                        self.clientlist.append(conn)
                else:
                    try:
                        # data has 'receivername>>sendername:message'
                        data = self.receivedata(sock)
                        # recvname has 'sendername:message'
                        recvname = self.userdetails(data, addr[0])
                        print(recvname, '\n')
                        #self.broadcast(sock, self.message, recvname)

                    except socket.error:
                        continue
        self.endserver()

    def userdetails(self, data, addr):
        """ Splits the sender name receiver name and data
        detail[1] has 'sendername:message'
        detail[0] has 'receviername'
        senderdetail[0] has 'sendername'
        self.recvdict stores {addr:'sendername'}
        """

        detail = str(data).split('<<')
        self.message = detail[1]
        recvname = detail[0]

        senderdetail = self.message.split(':')

        #print(self.recvdict, )
        #print(addr[1], )
        #print(senderdetail[0], )

        self.recvdict[addr] = senderdetail[0]
        print(self.recvdict, )

        return recvname
