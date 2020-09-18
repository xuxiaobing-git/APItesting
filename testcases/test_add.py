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

data_file_path = os.path.join(DATA_DIR, 'cases.xlsx')


@ddt
class AddTestCase(unittest.TestCase):
    """加标接口"""
    excel = ReadExcel(data_file_path, 'add')
    cases = excel.read_data_obj()
    http = HTTPSession()
    db = ReadSQL()

    @data(*cases)
    def test_add(self, case):
        # 第一步：准备用例数据
        # 拼接接口路径
        case.url = myconf.get('url','url')+case.url
        # 替换用例参数
        case.data = data_replace(case.data)

        if "*memberId*" in case.data:
            max_id = self.db.find_one("SELECT max(id) FROM member")[0]
            memberid = max_id+1
            case.data = case.data.replace("*memberId*",str(memberid))

        # 判断是否需要sql校验
        if case.check_sql:
            case.check_sql = data_replace(case.check_sql)
            # 获取当前用户加标前的标数量
            start_count = self.db.find_count(case.check_sql)

        # 第二步 发送请求，获取结果
        response = self.http.request(method=case.method, url=case.url, data=eval(case.data))
        res = response.json()
        res_code = res['code']
        # 第三步 比对预期和实际结果
        try:
            self.assertEqual(str(case.excepted_code), res_code)
            if case.check_sql:
                # 获取当前用户加标之后的标数量
                end_count = self.db.find_count(case.check_sql)
                self.assertEqual(1,end_count-start_count)
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
