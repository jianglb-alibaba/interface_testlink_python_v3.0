#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import urllib.parse

from globalpkg.log import logger
from globalpkg.global_var import testdb
from globalpkg.global_var import case_step_report_tb
from globalpkg.global_var import executed_history_id
from httpprotocol import MyHttp
from unittesttestcase import MyUnittestTestCase

class Pl(MyUnittestTestCase):
   def setUp(self):
       pass

   # 测试获取用户经纬度
   def test_get_lng_and_lat(self):
       '''演示当某个测试步骤使用的接口所在host，port，和协议和当前套件、项目等统一配置信息不一致时的处理操作'''

       self.params = urllib.parse.urlencode(self.params)

       myhttp = MyHttp('http', 'ditu.amap.com', '80')

       logger.info('正在发起GET请求...')
       response = myhttp.get(self.url, self.params)
       response_body = response[0]

       sql_update = 'UPDATE '+ case_step_report_tb +' SET protocol=\"%s\",host=\"%s\", port=\"%s\"' \
                             ' WHERE executed_history_id = %s and testcase_id = %s and step_id = %s' % \
                             ('http', 'ditu.amap.com', '80', executed_history_id, self.testcase_id, self.step_id)
       logger.info('正在更新步骤端口，主机，协议等配置信息: %s' % sql_update)
       testdb.execute_update(sql_update)

       logger.info('正在解析返回结果')
       json_response = json.loads(response_body.decode('utf-8'))
       self.assertEqual(json_response['code'],  self.expected_result['code'], msg='code != 1, 获取用户经纬度失败')

