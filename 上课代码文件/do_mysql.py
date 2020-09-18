"""
============================
Author:柠檬班-木森
Time:2019/9/3
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

"""
为什么要封装？
方便使用，


封装的需求是什么？
逻辑代码封装成方法，关键数据做参数化处理


"""
import pymysql


class ReadSQL(object):

    def __init__(self):
        # 建立连接
        self.coon = pymysql.connect(
            host="test.lemonban.com",  # 数据库地址
            port=3306,  # 端口
            user="test",  # 账号
            password="test",  # 密码
            database="future"  # 数据库名
        )
        # 创建一个游标
        self.cur = self.coon.cursor()

    def close(self):
        # 关闭游标，
        self.cur.close()

        # 断开连接
        self.coon.close()

    def find_one(self,sql):
        """查询一条数据"""
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_all(self,sql):
        """返回sql语句查询到的所有结果"""
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_count(self,sql):
        # 查询数据的条数
        count = self.cur.execute(sql)
        return count

if __name__ == '__main__':
    sql = "SELECT * FROM member WHERE MobilePhone='18999990252';"
    sql2 = "SELECT * FROM member LIMIT 0, 5;"

    db = ReadSQL()
    res = db.find_count(sql2)
    print(res)