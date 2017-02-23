#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import xml.etree.ElementTree as ET

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase

class WeatherWebService(MyUnittestTestCase):
   def setUp(self):
       pass

   #测试获取支持的省市
   def test_get_support_province(self):
       '''演示Body为XML格式数据的POST请求"""'''
       header = {'Content-Type':'text/xml','charset':'utf-8'}
       self.http.set_header(header)

       # 参数处理
       self.params = self.params.replace('|', ':')
       self.params = self.params.replace('(', '"')
       self.params = self.params.replace(')', '"')

       logger.info('正在发起POST请求...')

       self.params = self.params.encode(encoding='utf-8')

       response = self.http.post(self.url,  self.params)
       response = response[0]
       response = response.decode('utf-8')

       logger.info('正在解析返回结果:%s' % response)
       root = ET.fromstring(response)

       city_heilongjiang = root[0][0][0][2]
       # 断言
       self.assertEqual(city_heilongjiang.text,  self.expected_result['city'], msg='支持天气服务的城市少了"黑龙江"')





