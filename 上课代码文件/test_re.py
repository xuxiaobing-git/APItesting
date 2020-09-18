"""
============================
Author:柠檬班-木森
Time:2019/9/5
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
"""
正则表达式

"""
import re

# search: 查找


# sub:  替换
phone = "13488889999"
pwd = "123qwe"


data = '{"mobilephone":"#phone#","pwd":"#pwd#,"regname":"#name#"}'



def replace(data):
    while re.search(r'#(.+?)#',data):
        res = re.search(r'#(.+?)#',data)
        rdata = res.group()
        key = res.group(1)
        # 通过key去获取配置文件中动态参数的值
        value = key

        data = data.replace(rdata,value)

    return data


# print(rdata)
# print(key)







# res2 = re.search(r'#(\d.+?)h(.+?)#','dddddddddd#1234hsdasda#888888888889')
# print(res2.group())
# print(res2.group(1))
# print(res2.group(2))
