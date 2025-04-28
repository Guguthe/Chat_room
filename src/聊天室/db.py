from pack import connect
from  config import *


class DB(object):
    def __init__(self):
        self.conn = connect(host=db_host,
                port=db_port,
                database=db_name,
                user =mysql_user,password=passwd,
                charset='utf8')

#获取游标
        self.cursor = self.conn.cursor()


    def close(self):
        """
        释放数据库
        :return:
        """
        self.cursor.close()
        self.conn.close()

    def select_db(self,sql):
        self.cursor.execute(sql)
        query_result = self.cursor.fetchone()
        if not query_result:
            return None
        return_data = {}
        fileds = [fileds[0] for fileds in self.cursor.description]
        for filed, value in zip(fileds, query_result):
            return_data[filed] = value


        return return_data

if __name__ == '__main__':

    db = DB()
    data = db.select_db('select * from users')
    print(data)
    db.close()