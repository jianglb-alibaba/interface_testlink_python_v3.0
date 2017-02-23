#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import urllib.parse

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase

class Sug(MyUnittestTestCase):
   def setUp(self):
       pass

    # 测试淘宝商品搜索建议接口
   def test_taobao_sug(self):
       """演示接口返回数据为json格式时的数据处理"""

       self.params = urllib.parse.urlencode(self.params)

       logger.info('正在发起GET请求...')
       response = self.http.get(self.url, self.params)
       logger.info(response[0])

       logger.info('正在分析返回结果')
       response = response[0]
       response = response.decode('utf-8')
       response = response.replace('cb(', '')
       response = response.replace(')', '')
       json_response = json.loads(response)  # 将返回数据转为json格式的数据

       # 断言
       self.assertEqual(json_response['result'][0][1],self.expected_result['手机支架'] ,msg='手机支架数不相等')
       self.assertEqual(json_response['result'][0][2],self.expected_result['手机壳'], msg='手机壳数不相等')

