"""
============================
Author:柠檬班-木森
Time:2019/8/27
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""
import os
from configparser import ConfigParser
from common.constant import CONF_DIR

switch_file_path = os.path.join(CONF_DIR, 'env.ini')


class MyConfig(ConfigParser):
    """读取配置文件的类"""

    def __init__(self):
        super().__init__()

        c = ConfigParser()
        c.read(switch_file_path, encoding='utf8')
        env = c.getint('env', 'switch')
        # 根据开关的值，分别去读取不同环境的配置文件
        if env == 1:
            self.read(os.path.join(CONF_DIR, 'conf.ini'), encoding='utf8')
        elif env == 2:
            self.read(os.path.join(CONF_DIR, 'conf1.ini'), encoding='utf8')
        else:
            self.read(os.path.join(CONF_DIR, 'conf.ini'), encoding='utf8')


myconf = MyConfig()
