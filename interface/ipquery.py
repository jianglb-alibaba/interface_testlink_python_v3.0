#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

from globalpkg.log import logger
from globalpkg.global_var import testdb
from globalpkg.global_var import case_step_report_tb
from globalpkg.global_var import executed_history_id
from httpprotocol import MyHttp
from unittesttestcase import MyUnittestTestCase

class IPQuery(MyUnittestTestCase):
   def setUp(self):
       pass

   city_name = None
  # 测试获取省市名称
   def test_get_address_info(self):
       '''演示接口使用host，port，协议和统一配置不一致的时的处理
       (注：推荐做法：把由该方法组成的用例单独放到某个的独立项目的套件中，对项目及套件等做配置，
       然后把该用例做为其它某个用例的步骤，当然如果该方法仅为某个项目所有，且仅为其它某个用例所需，则可以这么做)'''

       myhttp = MyHttp('http', 'ip.ws.126.net', '80')

       logger.info('正在发起GET请求...')
       response = myhttp.get(self.url)

       sql_update = 'UPDATE '+ case_step_report_tb +' SET protocol=\"%s\",host=\"%s\", port=\"%s\"' \
                             ' WHERE executed_history_id = %s and testcase_id = %s and step_id = %s' % \
                             ('http', 'ditu.amap.com', '80', executed_history_id, self.testcase_id, self.step_id)
       logger.info('正在更新步骤端口，主机，协议等配置信息: %s' % sql_update)
       testdb.execute_update(sql_update)

       logger.info('正在解析返回结果')
       response_body = response[0]
       response_body = response_body.decode('gbk')  # decode函数对获取的字节数据进行解码
       logger.info(response_body)

       city_name = response_body.split('localAddress=')[1]
       city_name = city_name.split(',')[0]
       city_name = city_name.split(':')[1]
       city_name = city_name.replace('\"', '')
       logger.info(city_name)
       IPQuery.city_name = city_name  # 保存返回结果供其它接口使用

       self.assertEqual(city_name,  self.expected_result['city_name'], msg='city不为深圳市')


