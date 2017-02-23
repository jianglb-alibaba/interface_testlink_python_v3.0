#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import urllib.parse

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase

class BaiFuBaoCallback(MyUnittestTestCase):
   def setUp(self):
       pass

  # 测试获取省市名称
   def test_baifubao_callback(self):
       # 演示协议类型为https接口时的处理

       logger.info('正在发起GET请求...')
       self.params = urllib.parse.urlencode(self.params)  # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
       response = self.http.get(self.url, self.params)

       logger.info('正在解析返回结果')
       response = response[0]
       response = response.decode('unicode_escape')  # decode函数对获取的字节数据进行解码
       response = response.split('phone(')
       response = response[1].rstrip(')')
       response = json.loads(response)
       response = response['data']['area_operator']

       self.assertEqual(response,  self.expected_result['area_operator'], msg='area_operator不为江苏移动')

