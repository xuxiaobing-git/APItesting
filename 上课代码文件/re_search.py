"""
============================
Author:柠檬班-木森
Time:2019/9/7
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

import re

"""
match:  从字符串头部开始匹配，如果匹配到了，返回一个匹配的对象
search:  在整个字符串中进行匹配，如果匹配到了，返回一个匹配的对象（只会匹配到符合规则的第一个）
findall：把所有符合规则的都匹配出来，返回的是一个列表
参数：
var1 匹配的规则，
var2 要匹配的目标字符串

sub：替换

"""

# s = "123python456java789python111python"

# 字符串的查找方法
# res1 = s.find('python')
# print(res1)

# 正则

# macth：从字符串开头处进行匹配
# res2 = re.match('23',s)
# print(res2)

# search:
# res3 = re.search('python9',s)
# print(res3)

# findall:
# res4 = re.findall("python",s)
# print(res4)


# 替换的方法
# res5 = re.sub('python1','LMB',s,count=2)
# print(res5)

# ================正则的基本语法====================
phone = "13298766789"
pwd = '123qwe'
n123 = "789"

s = "python121111_python 4566java789!python th999th"
s2 = '{"mobilephone":"#phone#","pwd":"#pwd123#","regname":"#n123#"}'
#
# res6 = re.findall(r'#(.+?)#', s2)
# print(res6, len(res6))

res7 = re.search(r'#(.+?)#', s2)

r_data = res7.group()
s2 = re.sub(r_data,phone,s2)
print(s2)
res2 = re.search(r'#(.+?)#', s2)

print(res7.group(1))


