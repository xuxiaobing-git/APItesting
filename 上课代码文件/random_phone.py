"""
============================
Author:柠檬班-木森
Time:2019/9/5
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

import random




# 随机生成一个手机号码？


def random_phone():
    """随机生成手机号"""
    phone = "13"
    for i in range(9):
        num = random.randint(1,9)
        phone+=str(num)
    return phone
