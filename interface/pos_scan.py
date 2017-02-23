#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

#import urllib.request
import json

from globalpkg.log import logger
#from globalpkg.global_var import saofudb
from globalpkg.global_var import product_version
from globalpkg.global_var import protocol_version
from unittesttestcase import MyUnittestTestCase
from interface.pos_public import LoginPos

__all__ = ['CustomerBonusUpdateV3']

class CustomerBonusUpdateV3(MyUnittestTestCase):
    def test_update_customer_bonus(self):
        # 查询设备DeviceId，SerialNo

        self.expected_result['bonus'] = self.params['bonus']

        # 添加请求头
        headers = {'DeviceId':LoginPos.device_id, 'SerialNo':LoginPos.serial_no, 'Content-Type':'application/json;charset=utf-8','ProductVersion': product_version, 'ProtocolVersion':protocol_version,
                   'OperatorId':LoginPos.operator_id, 'Token':LoginPos.token}
        self.http.set_header(headers)

        logger.info('正在发起POST请求...')
        self.params = json.dumps(self.params)
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response_body = response[0].decode('utf-8')
        response_body = json.loads(response_body)

        logger.info('正在解析返回结果:%s' % response)

        # 断言
        self.assertEqual(response_body['code'], self.expected_result['code'], msg='code不为4001')
        self.assertEqual(response_body['bonus'], self.expected_result['bonus'], msg='bonus积分错误')
        self.assertEqual(response_body['success'], bool(self.expected_result['success']), msg='success不等于True')