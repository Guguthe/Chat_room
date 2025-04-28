from response_protocol import *
from db import *


class SocketWrapper(object):
    def __init__(self,sock):
        self.sock = sock


    def recv_data(self):
        data =  self.sock.recv(512).decode("utf-8")

        return data

    def send_data(self,message):
        return self.sock.send(message.encode("utf-8"))
    def close(self):

        self.sock.close()





