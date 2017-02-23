#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase


class SubmitWebsite(MyUnittestTestCase):
   def setUp(self):
       pass

   #测试提交网站
   def test_submit_website(self):
       '''演示POST请求，请求头内容类型为：Content-Type: application/x-www-form-urlencoded'''
       header = {'Content-Type':'application/x-www-form-urlencoded','charset':'utf-8'}
       self.http.set_header(header)

       self.params = str(self.params)
       self.params = self.params.replace('|', ':')
       self.params = self.params.encode('utf-8')
       logger.info('正在发起POST请求...')

       response = self.http.post(self.url,  self.params)
       response = response[0].decode('utf-8')

       logger.info('正在解析返回结果:%s' % response)

       logger.debug(response)
      # 断言
      # 略


