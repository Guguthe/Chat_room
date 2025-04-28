from 聊天室.cli import send_msg
from 聊天室.config import *
from PySide6.QtWidgets import QApplication,QWidget,QDialog
from login import Ui_Dialog
import sys
from chat import Ui_Form
name = ''
class Chatwindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind()
        self.plainTextEdit.setReadOnly(True)

    def send(self,name,msg):

        send_message = DELIMTER.join([REQUEST_CHAT,name[0],msg])
        #cli = send_msg()
        cli_socket.send(send_message.encode('utf-8'))
        self.plainTextEdit.appendPlainText(name[1] + ':  ' + msg)

    def send_chat_ontext(self):
        message = self.lineEdit_chat.text()
        self.send(name,message)
        self.lineEdit_chat.clear()

    def bind(self):
        self.pushButtonsend.clicked.connect(self.send_chat_ontext)



class Loginwindow(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.login)
        #账号


    def login(self):
        #账号
        account = self.lineEdit.text()
        #密码
        password = self.lineEdit_2.text()
        msg = DELIMTER.join([REQUEST_LOGIN,account,password])
        global cli_socket
        send = send_msg()
        global name
        recv_name,cli_socket = send.send(msg)
        name = [name for name in recv_name.split('|')]
        print(name)
        if name[1] == 'null':
            print('登录失败')
        else :
            print('成功')
            self.finished.emit(0)


def switch():
    app_login.close()
    app_chat.show()



app = QApplication(sys.argv)
app_login = Loginwindow()
app_chat = Chatwindow()
app_login.show()

app_login.finished.connect(switch)
app.exec()

