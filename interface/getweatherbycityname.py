#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import xml.etree.ElementTree as ET
import urllib.parse

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase

class GetWeatherByCityName(MyUnittestTestCase):
   def setUp(self):
       pass

   # 测试天气查询接口
   def test_get_weather_by_city_name(self):
       """演示接口返回数据为xml（webservice）格式的数据处理"""

       self.params = urllib.parse.urlencode(self.params)

       logger.info('正在发起GET请求...')
       response = self.http.get(self.url, self.params)
       response = response[0]
       response = response.decode('utf-8')

       print(response)
       logger.info('正在解析返回结果')
       root = ET.fromstring(response)

       # 断言
       self.assertEqual(root[2].text,  self.expected_result['city'], msg='直辖市不等于上海')
       self.assertEqual(root[2].text,  self.expected_result['citycode'], msg='城市代码不等于58367')


