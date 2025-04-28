from pack import socket
from config import *



class ServerSocket(socket.socket):
    def __init__(self):
        super(ServerSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((ip,port))
        self.listen(5)