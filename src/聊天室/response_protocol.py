from config import *
class ResponseProtocol(object):
    def __init__(self):
        pass
    @staticmethod
    def response_login(result,username, nickname):
        """

        :param result: 表示是否登录失败
        :param username: 用户名
        :param nickname: 昵称
        :return: 返回结果
        """


        return DELIMTER.join([REQUEST_LOGIN_RESULT,username,nickname])
    @staticmethod
    def response_chat(nickname,messages):
        """

        :param nickname:
        :param messages: 发送的信息
        :return: 返回拼接字符串
        """

        return DELIMTER.join([REQUEST_CHAT_RESULT,nickname,messages])