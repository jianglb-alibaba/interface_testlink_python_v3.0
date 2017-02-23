#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import time
import sys

from globalpkg.log import logger
from globalpkg.mydb import MyDB
from globalpkg.mytestlink import TestLink
from globalpkg.othertools import OtherTools

# 根据自己的实际需要进行合理的调整
if sys.argv[1] == '1':
    logger.info('当前运行环境：测试环境')
    logger.info('正在初始化数据库[名称：SAOFUDB1]对象')
    saofudb = MyDB('./config/dbconfig.conf', 'SAOFUDB1')
elif sys.argv[1] == '2':
    logger.info('已选择运行环境：预发布环境')
    logger.info('正在初始化数据库[名称：SAOFUDB2]对象')
    saofudb = MyDB('./config/dbconfig.conf', 'SAOFUDB2')

logger.info('正在初始化数据库[名称：TESTDB]对象')
testdb = MyDB('./config/dbconfig.conf', 'TESTDB')

logger.info('正在获取testlink')
mytestlink = TestLink().get_testlink()

other_tools = OtherTools()

executed_history_id = time.strftime('%Y%m%d%H%M%S', time.localtime())  # 流水记录编号
# testcase_report_tb = 'testcase_report_tb' + str(executed_history_id)
# case_step_report_tb = 'case_step_report_tb' + str(executed_history_id)
testcase_report_tb = 'testcase_report_tb'
case_step_report_tb = 'case_step_report_tb'

# 请求都携带的公用请求头、请求参数
if sys.argv[1] == '1': # 测试环境的全局变量
    cookie = {'Cookie':'10549840601068216320=ous64uFCCLMyXYDJ-MkNilyCI5CY'}
    global_serial = '10549840601068216320'
    global_openId = 'ous64uFCCLMyXYDJ-MkNilyCI5CY'
    product_version = '3.2.12C'
    protocol_version = '4.0'
elif sys.argv[1] == '2': # 预发布环境的全局变量
    cookie = {'Cookie':'10549840601068216320=ous64uFCCLMyXYDJ-MkNilyCI5CY'}
    global_serial = '10549840601068216320'
    global_openId = 'ous64uFCCLMyXYDJ-MkNilyCI5CY'
    product_version = '3.2.12C'
    protocol_version = '4.0'

# 自己自由扩展和更改
