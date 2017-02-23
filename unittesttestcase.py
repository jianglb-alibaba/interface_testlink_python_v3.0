#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import  unittest

class MyUnittestTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest', http=None, casestep=None):
        super(MyUnittestTestCase, self).__init__(methodName)
        self.http = http
        self.class_name =casestep.get_action()['class']
        self.function =casestep.get_action()['function']
        self.method =casestep.get_action()['method']
        self.url = casestep.get_action()['url']
        self.params = casestep.get_action()['params']
        self.testcase_id = casestep.get_tasecase_id()
        self.step_id = casestep.get_step_id()
        self.expected_result = casestep.get_expected_result()
        self.casestep = casestep

    def tearDown(self):
        # 设置action
        self.casestep.set_class_of_action(self.class_name)
        self.casestep.set_function_of_action(self.function)
        self.casestep.set_method_of_action(self.method)
        self.casestep.set_url_of_action(self.url)
        self.casestep.set_params_of_action(self.params)

        # 设置预期结果
        self.casestep.set_expected_result(self.expected_result)
