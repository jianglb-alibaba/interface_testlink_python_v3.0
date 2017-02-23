#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json
import urllib.parse

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase
from interface.ipquery import IPQuery

class GeoCoding(MyUnittestTestCase):
   def setUp(self):
       pass

   def test_get_ip_info(self):
       '''演示步骤之间存在依赖(前一步骤的输出为后一步骤的是输入)的情况'''

       logger.info('正在发起GET请求...')

       self.params['a'] = IPQuery.city_name

       self.params = urllib.parse.urlencode(self.params)
       response = self.http.get(self.url, self.params)
       response_body = response[0]

       logger.info('正在解析返回结果')
       self.expected_result['var_value'] = 'var_value'

       json_response = json.loads(response_body.decode('utf-8'))  #如果有必要，用decode函数对获取的字节数据进行解码

       self.assertEqual(json_response['lat'],  self.expected_result['lat'], msg='lat值错误')
       self.assertEqual(json_response['lon'],  self.expected_result['lon'], msg='lon值错误')

   # def tearDown(self):
   #     pass
   #     logger.info('tesss')