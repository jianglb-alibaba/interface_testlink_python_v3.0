#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import unittest

from globalpkg.log import logger
from interface.wechatno_wemall import *
from interface.wecharno_card_coupon import *
from interface.pos_public import *
from interface.pos_scan import *
from interface.geocoding import GeoCoding
from interface.webtours import WebTours
from interface.getweatherbycityname import GetWeatherByCityName
from interface.ipquery import IPQuery
from interface.pl import Pl
from interface.sug import Sug
from interface.baifubaocallback import BaiFuBaoCallback
from interface.regeocoding import Regeocoding
from interface.weatherwebservice import WeatherWebService
from interface.submitwebsite import SubmitWebsite

class CaseStep:
    def __init__(self, step_id, step_number, expected_result, action, testcase_id):
        self.step_id = step_id
        self.expected_result= expected_result
        self.action = action
        self.step_number = step_number
        self.testcase_id = testcase_id

    def get_step_id(self):
        return self.step_id

    def get_expected_result(self):
        return self.expected_result

    def set_expected_result(self, expected_result):
        self.expected_result = expected_result

    def get_action(self):
        return  self.action

    def set_action(self, action):
        self.action = action

    def set_class_of_action(self, class_name):
        self.action['class'] = class_name


    def get_class_of_action(self):
        return self.action['class']

    def set_function_of_action(self,function):
        self.action['function'] = function

    def get_function_of_action(self):
        return self.action['function']

    def set_method_of_action(self, method):
        self.action['method'] = method

    def get_method_of_action(self):
        return  self.action['method']

    def set_params_of_action(self, params):
        self.action['params'] = params

    def get_params_of_action(self):
        return self.action['params']

    def get_url_of_action(self):
        return self.action['url']

    def set_url_of_action(self, url):
        self.action['url'] = url

    def get_step_number(self):
        return  self.step_number

    def get_preconditions(self):
        return  self.get_preconditions

    def get_summary(self):
        return self.summary

    def get_tasecase_id(self):
        return  self.testcase_id


    def run_step(self, http):
        try:
            class_name = self.action['class']
            function = self.action['function']
            logger.info('调用的方法为：%s.%s' % (class_name, function))
        except Exception as e:
            logger.error('步骤[%s]信息填写不正确: %e，执行失败' % (self.step_number,e))
            return ('Error',('%s' % e))

        runner = unittest.TextTestRunner()
        test_step_action = unittest.TestSuite()
        test_step_action.addTest((globals()[class_name])(function, http, self))
        step_run_result = runner.run(test_step_action)

        logger.debug('step_run_result：%s, errors：%s，failures：%s' % (step_run_result, step_run_result.errors, step_run_result.failures))
        if 0 != len(step_run_result.errors):
            return ('Error', step_run_result.errors)
        elif 0 != len(step_run_result.failures):
            return ('Fail', step_run_result.failures)
        else:
            return ('Pass', '')