#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laiyu'

import json

from globalpkg.log import logger
from globalpkg.global_var import saofudb
from globalpkg.global_var import product_version
from globalpkg.global_var import protocol_version
from unittesttestcase import MyUnittestTestCase

__all__ = ['LoginPos']

class LoginPos(MyUnittestTestCase):
    token = ''
    device_id = ''
    serial_no = ''
    operator_id = ''

    def test_login_pos(self):
        # 查询设备DeviceId，SerialNo
        LoginPos.operator_id = int(self.params['id'])
        query = 'SELECT branch_id, name, number FROM account_operator WHERE id = %s'
        data = (self.params['id'],)
        result = saofudb.select_one_record(query, data)
        branch_id = result[0]
        self.expected_result['operator']['name'] = result[1]
        self.expected_result['operator']['number'] = result[2]

        query = 'SELECT device_no, serial_no FROM device WHERE shop_branch_id = %s'
        data = (branch_id,)
        result = saofudb.select_one_record(query, data)
        LoginPos.device_id = result[0]
        LoginPos.serial_no = result[1]


        self.expected_result['operator']['id'] = int(self.params['id'])

        # 添加请求头
        headers = {'DeviceId':LoginPos.device_id, 'SerialNo':LoginPos.serial_no, 'Content-Type':'application/json;charset=utf-8','ProductVersion': product_version, 'ProtocolVersion':protocol_version}
        self.http.set_header(headers)

        logger.info('正在发起POST请求...')
        self.params = json.dumps(self.params)
        self.params = self.params.encode('utf-8')
        response = self.http.post(self.url, self.params)
        response_body = response[0].decode('utf-8')
        response_body = json.loads(response_body)
        logger.info('正在解析返回结果:%s' % response)

        LoginPos.token = response_body['token']

        # 断言
        self.assertEqual(response_body['code'], self.expected_result['code'], msg='code不为4001')
        self.assertEqual(response_body['message'], self.expected_result['message'], msg='message 不等于“成功”')
        self.assertEqual(response_body['operator']['id'], self.expected_result['operator']['id'], msg='operator_id 错误')
        self.assertEqual(response_body['operator']['name'], self.expected_result['operator']['name'], msg='operator_name错误')
        self.assertEqual(response_body['operator']['number'], self.expected_result['operator']['number'], msg='operator_number错误')
        self.assertEqual(response_body['reason'], self.expected_result['reason'], msg='登录不成功 reason不等于“成功”')
        self.assertEqual(response_body['success'], bool(self.expected_result['success']), msg='success不等于True')