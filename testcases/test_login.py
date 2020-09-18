"""
============================
Author:柠檬班-木森
Time:2019/8/31
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

"""
测试用例模块

"""
import os
import random
import unittest
from pack_lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.http_requests import HTTPRequest
from common.mylogger import log
from common.constant import DATA_DIR
from common.do_mysql import ReadSQL
from common.conifg import myconf
from common.text_replace import data_replace

# 拼接数据文件路径
data_file_path = os.path.join(DATA_DIR, "cases.xlsx")


@ddt
class LoginTestCase(unittest.TestCase):
    """登录接口"""
    excel = ReadExcel(data_file_path, 'login')
    cases = excel.read_data_obj()
    http = HTTPRequest()
    db = ReadSQL()

    @data(*cases)
    def test_case_login(self, case):

        # 登录接口用例执行的逻辑
        # 第一步：准备测试用例数据
        url = myconf.get('url','url')+case.url
        method = case.method
        excepted = eval(case.excepted)
        row = case.case_id + 1
        # 替换用例参数
        # 替换配置文件夹中固定的参数
        data = data_replace(case.data)
        print(data)
        # 随机生成手机号码
        phone = self.random_phone()
        # 替换动态化的参数
        case.data = case.data.replace("*phone*", phone)

        # 第二步：发送请求到接口，获取结果
        log.info('正在请求地址{}'.format(url))
        response = self.http.request(method=method, url=url, data=eval(data))
        # 获取返回的内容
        res = response.json()
        # 第三步：比对预期结果和实际结果，断言用例是否通过
        try:
            self.assertEqual(excepted, res)
        except AssertionError as e:
            # 测试用例未通过
            # 获取当前用例所在行
            self.excel.write_data(row=row, column=8, value='未通过')
            log.debug('{}，该条用例执行未通过'.format(case.title))
            raise e
        else:
            # 测试用例执行通过
            self.excel.write_data(row=row, column=8, value='通过')
            log.debug('{}，该条用例执行通过'.format(case.title))

    def random_phone(self):
        """随机生成手机号"""
        while True:
            phone = "13"
            for i in range(9):
                num = random.randint(1, 9)
                phone += str(num)

            # 数据库中查找该手机号是否存在
            sql = "SELECT * FROM member WHERE MobilePhone='{}';".format(phone)
            if not self.db.find_count(sql):
                return phone


@ddt
class RegisterTestCase(unittest.TestCase):
    """注册接口"""
    excel = ReadExcel(data_file_path, 'register')
    cases = excel.read_data_obj()
    http = HTTPRequest()
    db = ReadSQL()

    @data(*cases)
    def test_register(self, case):
        # 第一步：准备用例数据
        # 拼接完整的接口地址
        url = myconf.get('url','url')+case.url

        case.data = data_replace(case.data)

        # 随机生成手机号码
        phone = self.random_phone()
        # 替换动态化的参数
        case.data = case.data.replace("*phone*",phone)

        # 第二步：发送请求,获取到实际结果
        response = self.http.request(method=case.method, url=url, data=eval(case.data))
        res = response.json()

        # 第三步：比对预期和实际结果
        try:
            self.assertEqual(eval(case.excepted), res)
            # 判断是否需要sql校验
            # 判断是否需要进行sql校验
            if case.check_sql:
                case.check_sql = case.check_sql.replace('*phone*',phone)
                db_res = self.db.find_count(case.check_sql)
                self.assertEqual(1, db_res)

        except AssertionError as e:
            # 用例执行为通过，写入结果
            self.excel.write_data(row=case.case_id + 1, column=8, value='未通过')
            log.info('用例执行未通过')
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=case.case_id + 1, column=8, value='通过')
            log.info('用例执行通过')

    def random_phone(self):
        """随机生成手机号"""
        while True:
            phone = "13"
            for i in range(9):
                num = random.randint(1, 9)
                phone += str(num)

            # 数据库中查找该手机号是否存在
            sql = "SELECT * FROM member WHERE MobilePhone='{}';".format(phone)
            if not self.db.find_count(sql):
                return phone
