#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import urllib.parse
import json

from globalpkg.log import logger
from htmlparser import  MyHTMLParser
from unittesttestcase import MyUnittestTestCase

step_output = None

class WebTours(MyUnittestTestCase):
   def setUp(self):
       pass

   # 测试访问WebTours首页
   def test_visit_webtours(self):
       # 根据被测接口的实际情况，合理的添加HTTP头
       # header = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       #    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'
       #    }
       logger.info('正在发起GET请求...')
       response = self.http.get(self.url,  (self.params))
       response_body = response[0]
       response_body = response_body.decode('utf-8')

       logger.info('正在解析返回结果')

       # 解析HTML文档
       parser = MyHTMLParser(strict = False)
       parser.feed(response_body)

       # 比较结果
       starttag_data = parser.get_starttag_data()
       i = 0
       for data_list in starttag_data:
           if data_list[0] == 'title' and data_list[1] == 'Web Tours':
               i = i + 1

       self.assertNotEqual(str(i), self.expected_result['result'], msg='访问WebTours失败')

       # 如果有需要，连接数据库，读取数据库相关值，用于和接口请求返回结果做比较

   # 测试接口2
   def test_xxxxxx(self):
       '''提交body数据为json格式的POST请求'''

       header = {'Content-Type':'application/json','charset':'utf-8'}
       self.http.set_header(header)

       self.params = json.dumps(eval(self.params))
       self.params = self.params.encode('utf-8')

       response = self.http.post(self.url, self.params)
       response_body = response[0]
       self.assertEqual(response_body['code'], 0, msg='返回code不等于0')
