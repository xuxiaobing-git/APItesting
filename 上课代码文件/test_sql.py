"""
============================
Author:柠檬班-木森
Time:2019/9/3
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
"""
第一件：  下载班级群里的数据字典文件

第二件：  安装pymysql模块： pip install pymysql

数据库地址：test.lemonban.com
端口：3306
账号：test
密码：test

"""

import pymysql

# 第一步：连接到数据库,创建游标
conn = pymysql.connect(host="test.lemonban.com",  # 数据库地址
                port=3306,  # 端口
                user="test" , # 账号
                password = "test",  # 密码
                database = "future"  # 数据库名
                )
# 创建一个游标
cur = conn.cursor()

# 第二步：执行sql语句
sql = "SELECT * FROM member WHERE MobilePhone='18999990252';"
sql2 = "SELECT * FROM member LIMIT 0, 5;"

# 执行sql语句
res = cur.execute(sql2)
print(res)

# 第三步：获取结果


# fetchone:获取查询集中的第一条数据
# data1 = cur.fetchone()
# print(data1)

# fetchall，获取查询到的所有数据
datas = cur.fetchall()
for i in datas:
    print(i)

# 执行  增加 删除 修改的sql语句时，执行完了要提交事务才会生效
conn.commit()