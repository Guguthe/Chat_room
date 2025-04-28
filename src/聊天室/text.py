import threading
from Server_socket import ServerSocket
from socket_wrapper import *
import asyncio
class Server(ServerSocket):
    def __init__(self):
        self.server_socket  = ServerSocket()
        self.request_handle_function = dict()
        self.request_handle_function[REQUEST_LOGIN] = self.request_login_handle
        self.request_handle_function[REQUEST_CHAT] = self.request_chat_handle
        self.client = {}
        self.db = DB()

    async def request_handle(self,client_soc):
        while True:
            msg = client_soc.recv_data()

            if not msg or msg == 'exit':
                client_soc.close()
                self.delete_client(client_soc)
                break
            else:
                recv_msg = self.parse_data(msg, client_soc)
                msg = [msg for msg in recv_msg.split('|')]
                client_soc.send_data("服务器收到" + msg[2])



    def parse_data(self,data,client_soc):
        parse = self.parse_request_test(data)
        print("解析" + str(parse))
        # 解析数据

        handle_function = self.request_handle_function.get(parse['request_id'])
        if not handle_function is None:
            rec_msg = handle_function(client_soc,parse)
            return rec_msg
        else:
            print(f"非法请求{parse}")
            return 'hava something wrong'

    def parse_request_test(self,text):
        """
        登陆信息:0001|username|password
        聊天信息:0002|username|message
        :return:

        """

        request_list = text.split("|")
        request_data = {}
        #把list转为字典
        request_data['request_id'] = request_list[0]
        if request_data['request_id'] == REQUEST_LOGIN:
            request_data['username'] = request_list[1]
            request_data['password'] = request_list[2]

        elif request_data['request_id'] == REQUEST_CHAT:
            request_data['username'] = request_list[1]
            request_data['message'] = request_list[2]
        return request_data
    def request_login_handle(self,client_soc,parse):
        """
        确定用户登陆，创建用户信息
        :return:
        """
        print('收到登陆请求')
        user = parse['username']
        passwd = parse['password']
        ret, nickname, username = self.check_user_login(user, passwd)
        response_text = ResponseProtocol.response_login(ret, username, nickname)
        if ret == '1':
            self.client[user] = {'nickname': nickname, 'sock': client_soc}
        print(response_text)
        return response_text




    def check_user_login(self,user,passwd):
        """
        进行登陆数据处理
        :param user:
        :param passwd:
        :return:
        """
        sql = "select * from users where user_name='%s'" % user
        result = self.db.select_db(sql)
        if  result is None:
            ret = '0'
            print('登录失败')
            return ret,'null',user
        elif result['user_password'] == passwd:
            ret = '1'
            print('登陆成功')
            return ret, result['user_nickname'], user
        else:
            ret = '0'
            print('登录失败')
            return '0','null',user


    def request_chat_handle(self,client_soc,parse_data):
        """

        :param client_soc: 套接字
        :param parse_data: 收到的消息
        :return:
        """
        print('收到聊天请求')
        message = parse_data['message']
        username = parse_data['username']
        nickname = self.client[username]['nickname']
        msg = ResponseProtocol.response_chat(nickname,message)
        #转发给目标用户
        for u_name,info in self.client.items():
            if username == u_name:
                #info["sock"].send_data(msg)
                print(u_name)
            continue
        return msg



    def startup(self):
        """
        开启服务器
        :return:
        """
        while True:
            print("正在接收客户端连接")
            soc,addr = self.server_socket.accept()
            client_soc = SocketWrapper(soc)
            print("获取客户端信息")

            #套接字接收数据
            t = threading.Thread(target=self.request_handle,args=(client_soc,))
            t.start()


    def delete_client(self,client_soc):
        for username,info in self.client.items():
            if info['sock'] == client_soc:
                print(self.client)
                del self.client[username]
                print(self.client)
                break
        print("客户端断开连接")




if __name__ == '__main__':
    Server().startup()