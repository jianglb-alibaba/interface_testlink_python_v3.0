#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

from globalpkg.log import logger
from globalpkg.global_var import mytestlink
from globalpkg.global_var import other_tools
from testplan import TestPlan

class TestProject:
    def __init__(self, active_status, name, notes, id):
        self.active_status = active_status
        self.name = name
        self.notes = notes
        self.project_id = id

    # 获取项目的配置信息(ip,端口，协议)
    def get_testproject_conf(self):
        return self.notes

    def run_testproject(self, http):
        logger.info('正在获取测试项目[id：%s, name：%s]对应对应的测试计划名称列表' % (self.project_id, self.name))
        testplans_name_list = []
        testplans = mytestlink.getProjectTestPlans(self.project_id)
        for testplan in testplans:
            testplans_name_list.append(testplan['name'])
        logger.info('成功获取项目测试计划名称列表[list=%s]' % testplans_name_list)

        for testplan in testplans_name_list:
            testplan_info = mytestlink.getTestPlanByName(self.name, testplan)
            testplan_name = testplan_info[0]['name']
            testplan_id = int(testplan_info[0]['id'])
            active_status = int(testplan_info[0]['active'])
            notes = other_tools.conver_date_from_testlink(testplan_info[0]['notes'])
            testplan_obj = TestPlan(testplan_name, testplan_id, active_status, notes, self.name)

            logger.info('正在执行项目测试计划[project：%s，testplan：%s]' % (self.name, testplan))
            testplan_obj.run_testplan(http)