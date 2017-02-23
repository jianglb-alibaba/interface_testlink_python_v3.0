#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import time
from globalpkg.log import logger
from globalpkg.global_var import testcase_report_tb
from globalpkg.global_var import executed_history_id
from globalpkg.global_var import testdb
from globalpkg.global_var import mytestlink
from testcase import TestCase


class TestSuite:
    def __init__(self, testsuite_id, testsuite_name, details, project_name):
        self.testsuite_id = testsuite_id
        self.testsuite_name = testsuite_name
        self.details = details
        self.project_name = project_name
        self.sub_testsuits = {}
        self.testcase_id_list = []

    # 获取测试套件包含的所有用例的id
    def get_testcases_id_for_testsuite(self):
        #testcases_id = mytestlink.getTestCasesForTestSuite(self.testsuite_id, False, 'only_id')

        logger.info('正在获取子套件……')
        sub_testsuits = self.get_sub_testsuits_for_testsuit(self.testsuite_id)
        logger.info('成功获取子套件id列表：%s' % sub_testsuits)

        testsuits_id_list = []
        for key in sub_testsuits.keys():
            testsuits_id_list.append(int(key))

        testsuits_id_list.insert(0, self.testsuite_id)

        for testsuit_id in testsuits_id_list:
            self.testcase_id_list.extend(mytestlink.getTestCasesForTestSuite(testsuit_id, False, 'only_id'))

        return self.testcase_id_list

    # 递归获取测试套件包含的子套件
    def get_sub_testsuits_for_testsuit(self,testsuite_id):
        response = mytestlink.getTestSuitesForTestSuite(testsuite_id)
        if response == []:
            return {}
        else:
            for sub_testsuit_id, value in (response.copy()).items():
                if not sub_testsuit_id.isdigit():
                    return {response['id']:response}
                sub_testsuit_id = int(sub_testsuit_id)
                response.update(self.get_sub_testsuits_for_testsuit(sub_testsuit_id))
                self.sub_testsuits = response
            return self.sub_testsuits

    # 获取测试套件包含的所有用例的完整信息
    def get_testcases_info_for_testsuite(self):
        testcase_info = mytestlink.getTestCasesForTestSuite(self.testsuite_id, True, 'full')
        return testcase_info

    # 获取测试套件的配置信息(ip,端口，协议)
    def get_testsuite_conf(self):
        return self.details

    # 获取测试套件所属项目
    def get_project_name(self):
        return self.project_name

    # 运行测试套件
    def run_testsuite(self, http):
        logger.info('正在获取套件[id=%s，name=%s]的测试用例...' % (self.testsuite_id, self.testsuite_name))
        testcases_id_list_for_testsuit = self.get_testcases_id_for_testsuite()

        logger.info('获取到用例id列表：%s', testcases_id_list_for_testsuit)

        for testcase_id in testcases_id_list_for_testsuit[:]:
            testcase_info = mytestlink.getTestCase(testcase_id)  # 获取测试用例基本信息
            logger.info('获取测试用例信息 %s' % testcase_info)

            # 构造测试用例对象
            testcase_name = testcase_info[0]['name']
            preconditions = testcase_info[0]['preconditions']
            if preconditions.find('isglobal') != -1:
                logger.info('用例[id=%s, name=%s]为全局初始化用例，已跳过执行' % (testcase_id, testcase_name))
                continue

            testcase_steps = testcase_info[0]['steps']
            testcase_isactive = int(testcase_info[0]['active'])
            testcase_obj = TestCase(testcase_id, testcase_name, testcase_steps, testcase_isactive, self.project_name)

            # 获取测试套件名称
            logger.info(testcase_id)
            full_path = mytestlink.getFullPath(int(testcase_id))
            full_path = full_path[testcase_id]
            testsuite_name = ''
            for suit in full_path[1:]:
                testsuite_name = testsuite_name + '-' + suit
            testsuite_name = testsuite_name.lstrip('-')

            sql_insert = 'INSERT INTO '+testcase_report_tb +'(executed_history_id, testcase_id, testcase_name, testsuit, testplan, project, runresult, runtime)' \
                         ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
            testplan = '无计划'
            data = (executed_history_id, testcase_id, testcase_name, testsuite_name, testplan, self.project_name, 'Block','')
            logger.info('记录测试用例到测试用例报表')
            testdb.execute_insert(sql_insert, data)

            logger.info('开始执行测试用例[id=%s，name=%s]' % (testcase_id, testcase_name))
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
            testcase_run_result = testcase_obj.run_testcase(http, testplan)

            logger.info('正在更新用例执行结果')
            sql_update = 'UPDATE '+testcase_report_tb +' SET runresult=\"%s\", runtime=\"%s\"' \
                         ' WHERE executed_history_id = %s and testcase_id = %s' \
                         ' AND project=\'%s\' AND testplan=\'%s\'' % \
                           (testcase_run_result, run_time, executed_history_id, testcase_id, self.project_name, testplan)
            testdb.execute_update(sql_update)

        logger.info('测试套件[id=%s ,name=%s]已执行完' % (self.testsuite_id, self.testsuite_name))

