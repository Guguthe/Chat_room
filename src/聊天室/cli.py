import socket

class send_msg():
    def __init__(self):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 8080))
        print("连接成功")

    def send(self,msg):

        self.client_socket.send(msg.encode('utf-8'))
        data = self.client_socket.recv(512)
        recv = data.decode('utf-8')
        print(recv)
        return recv,self.client_socket



if __name__ == '__main__':
    msg = '0001|gugu|333'
    send = send_msg()
    while True:
        if msg == 'exit' or msg == '':
            break
        else:
            send.send(msg)
            break