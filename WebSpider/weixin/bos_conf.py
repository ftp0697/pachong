# -*- coding: utf-8 -*-
__author__ = 'Administrator'


# 导入Python标准日志模块
import logging

# 从Python SDK导入BOS配置管理模块以及安全认证模块
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

# 设置访问BOS服务的代理
# PROXY_HOST = 'localhost:8080'

# 设置BosClient的Host，Access Key ID和Secret Access Key
bos_host = "http://bj.bcebos.com"
access_key_id = "4804d257a8f64468ab0da12d3ce2c825"
secret_access_key = "fec02876c71341c7920977a367f5d4fe"

# 设置日志文件的句柄和日志级别
logger = logging.getLogger('baidubce.services.bos.bosclient')
fh = logging.FileHandler("baidubce.log")
fh.setLevel(logging.DEBUG)

# 设置日志文件输出的顺序、结构和内容
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

# 创建BceClientConfiguration
config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=bos_host)