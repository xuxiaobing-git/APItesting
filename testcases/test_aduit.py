"""
============================
Author:柠檬班-木森
Time:2019/9/10
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os
import unittest
import decimal
from pack_lib.ddt import ddt, data
from common.read_excel import ReadExcel
from common.constant import DATA_DIR
from common.http_requests import HTTPSession
from common.mylogger import log
from common.do_mysql import ReadSQL
from common.text_replace import data_replace
from common.conifg import myconf
from common.text_replace import ConText


data_file_path = os.path.join(DATA_DIR, 'cases.xlsx')


@ddt
class AuditTestCase(unittest.TestCase):
    """加标接口"""
    excel = ReadExcel(data_file_path, 'audit')
    cases = excel.read_data_obj()
    http = HTTPSession()
    db = ReadSQL()

    @data(*cases)
    def test_audit(self, case):
        # 第一步：准备用例数据
        # 拼接接口路径
        case.url = myconf.get('url', 'url') + case.url
        # 替换用例参数
        case.data = data_replace(case.data)

        # 判断是否有*load_id* 的参数要替换
        if "*loan_id*" in case.data:
            max_id = self.db.find_one("SELECT max(id) FROM loan")[0]
            loan_id = max_id + 1
            case.data = case.data.replace("*loan_id*", str(loan_id))

        # 第二步 发送请求，获取结果
        response = self.http.request(method=case.method, url=case.url, data=eval(case.data))
        res = response.json()
        res_code = res['code']

        # 判断是否是执行的加标用例，
        if case.interface == "加标":
            loan_id = self.db.find_one(
                "SELECT Id FROM loan WHERE MemberId='{}' ORDER BY id DESC".format(myconf.get('data', 'memberId')))
            # 将添加的标id，保存为临时变量
            setattr(ConText,'loan_id',loan_id[0])

        # 第三步 比对预期和实际结果
        try:
            self.assertEqual(str(case.excepted_code), res_code)
            # 判断是否需要sql校验
            if case.check_sql:
                case.check_sql = data_replace(case.check_sql)
                # 获取当前用户加标前的标数量
                print(case.check_sql)
                status = self.db.find_one(case.check_sql)[0]
                self.assertEqual(eval(case.data)["status"], status)

        except AssertionError as e:
            # 用例执行未通过
            self.excel.write_data(row=case.case_id + 1, column=8, value='未通过')
            log.info('{}:用例执行未通过'.format(case.title))
            log.exception(e)
            raise e
        else:
            # 用例执行通过
            self.excel.write_data(row=case.case_id + 1, column=8, value='通过')
            log.info('{}:用例执行通过'.format(case.title))
