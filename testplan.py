#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import time

from globalpkg.log import logger
from globalpkg.global_var import mytestlink
from globalpkg.global_var import testcase_report_tb
from globalpkg.global_var import executed_history_id
from globalpkg.global_var import testdb
from testcase import TestCase

class TestPlan:
    def __init__(self, name, id, active_status, notes, testproject):
        self.testplan_name = name
        self.testplan_id = id
        self.active_status = active_status
        self.notes =notes
        self.testproject = testproject
        #self.testproject_id = ''

    # 获取测试计划的配置信息(ip,端口，协议)
    def get_testplan_conf(self):
        return self.notes

    def run_testplan(self, http):
        logger.info('正在获取测试计划[project=%s，name=%s]的测试用例' % (self.testproject, self.testplan_name))
        testcases_for_testplan = mytestlink.getTestCasesForTestPlan(self.testplan_id)
        if [] == testcases_for_testplan:
            logger.warning('未获取到测试用例')
            return
        testcases_id_for_testplan = testcases_for_testplan.keys()
        logger.info('成功获取测试计划[project=%s，name=%s]的测试用例id：%s' % (self.testproject, self.testplan_name, testcases_id_for_testplan))

        if 0 == self.active_status:
            logger.warning('测试计划[project=%s，name=%s]处于不活动状态[active=0]，不执行' % (self.testproject, self.testplan_name))
            return

        for testcase_id_str in testcases_id_for_testplan:
            testcase_id = int(testcase_id_str)
            testcase_info = mytestlink.getTestCase(testcase_id)  # 获取测试用例基本信息

            logger.info('获取测试用例信息 %s' % testcase_info)

            # 构造测试用例对象
            testcase_steps = testcase_info[0]['steps']
            testcase_name = testcase_info[0]['name']
            preconditions = testcase_info[0]['preconditions']
            if preconditions.find('isglobal') != -1:
                logger.info('用例[id=%s, name=%s]为全局初始化用例，已跳过执行' % (testcase_id, testcase_name))
                continue
            testcase_isactive = int(testcase_info[0]['active'])

            # 获取测试套件名称
            full_path = mytestlink.getFullPath([testcase_id])
            full_path = full_path[str(testcase_id)]
            testsuite_name = ''
            for suit in full_path[1:]:
                testsuite_name = testsuite_name + '-' + suit
            testsuite_name = testsuite_name.lstrip('-')

            testcase_obj = TestCase(testcase_id, testcase_name, testcase_steps, testcase_isactive, self.testproject)

            sql_insert = 'INSERT INTO '+testcase_report_tb +'(executed_history_id, testcase_id, testcase_name, testsuit, testplan, project, runresult, runtime)' \
                         ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
            data = (executed_history_id, testcase_id, str(testcase_name), testsuite_name, self.testplan_name, self.testproject, 'Block', '')
            logger.info('记录测试用例到测试用例报表')
            testdb.execute_insert(sql_insert, data)

            logger.info('开始执行测试用例[id=%s，name=%s]' % (testcase_id, testcase_name))
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
            testcase_run_result = testcase_obj.run_testcase(http, self.testplan_name)

            logger.info('正在更新用例执行结果')
            sql_update = 'UPDATE '+testcase_report_tb +' SET runresult=\"%s\", runtime=\"%s\"' \
                        ' WHERE executed_history_id = %s AND testcase_id = %s' \
                        ' AND project=\'%s\' AND testplan=\'%s\'' % \
                        (testcase_run_result, run_time, executed_history_id, testcase_id, self.testproject, self.testplan_name)
            testdb.execute_update(sql_update)

            bulid_info = mytestlink.getLatestBuildForTestPlan(self.testplan_id) # 固定取最新的版本
            bulid_version = bulid_info['name']

            logger.info('正在更新testlink上测试计划[testplan_id=%s, bulid_version=%s],对应用例[testcase_id=%s]的执行结果'
                        % (self.testplan_id, bulid_version, testcase_id))
            notes = '用例[id：%s]在测试计划[testplan_id：%s，testplan_name：%s,bulidversion：%s]中的执行结果' \
                    % (testcase_id, self.testplan_id,self.testplan_name, bulid_version)
            if 'Fail' == testcase_run_result or 'Error' == testcase_run_result:
                self.__execute_case_in_testlink(testcase_id, bulid_version, 'f', notes) # f - 失败
            elif 'Pass' == testcase_run_result:
                self.__execute_case_in_testlink(testcase_id, bulid_version, 'p', notes) # f - 成功
            else:
                pass # 如果未执行，啥都不做

        logger.info('测试计划[project=%s ,testplan=%s]已执行完' % (self.testproject, self.testplan_name))

    def __execute_case_in_testlink(self, case_id, bulid_for_plan, runresult, notes=''):
        '''更新Testlink上的用例执行结果'''

        mytestlink.reportTCResult(case_id, self.testplan_id, bulid_for_plan, runresult, notes)

