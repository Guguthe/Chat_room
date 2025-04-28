import socket

def test(msg):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    print("连接成功")
    while True:
        #msg = input("请输入:\n")
        if msg == 'exit' or msg == '':
            break
        else:
            client_socket.send(msg.encode('utf-8'))
            data = client_socket.recv(512)
            recv = data.decode('utf-8')
            print(recv)
            recv_l = recv.split('|')
            msg_l = msg.split('|')
            if msg_l[0] == '0001' :
                if recv_l[2] == '':
                    print('登录失败')
                else :
                    print('成功')
                break
            elif msg_l[0] == '0002':
                continue
            else:
                print(msg_l[0])
                break


if __name__ == '__main__':
    msg = '0001|gugu|333'
    test(msg)