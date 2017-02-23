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

class Regeocoding(MyUnittestTestCase):
   def setUp(self):
       pass

    # 测试根据经纬度获取地区名
   def test_regeocoding(self):
       self.params = urllib.parse.urlencode(self.params)

       logger.info('正在发起GET请求...')
       response = self.http.get(self.url, self.params)

       logger.info('正在解析返回结果')
       response = response[0]
       response = response.decode('utf-8')
       response = json.loads(response)
       response = response['addrList'][0]

       # 断言
       self.assertEqual(response['name'],  self.expected_result['name'], msg='name <> 地安门外大街')



