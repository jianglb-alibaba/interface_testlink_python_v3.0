#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'shouke'

import  configparser
from globalpkg.log import logger


class RunModeConfig:
    def __init__(self, run_mode_conf):
        config = configparser.ConfigParser()

        # 从配置文件中读取运行模式
        config.read(run_mode_conf, encoding='utf-8-sig')
        try:
            self.run_mode = config['RUNMODE']['runmode']
            self.project_mode = int(config['PROJECTS']['project_mode'])
            self.projects = config['PROJECTS']['projects']
            self.testplans = config['PLANS']['plans']
            self.project_of_plans = config['PLANS']['project']
            self.testsuites = config['TESTSUITES']['testsuites']
            self.case_id_list = eval(config['TESTCASES']['case_id_list'])
            self.global_case_id_list = eval(config['GLOBALCASES']['global_case_id_list'])
        except Exception as e:
            logger.error('读取运行模式配置失败：%s' % e)
            exit()

    def get_run_mode(self):
        return  self.run_mode

    def get_project_mode(self):
        return self.project_mode

    def get_projects(self):
        return self.projects

    def get_testplans(self):
        return self.testplans

    def get_project_of_testplans(self):
        return  self.project_of_plans

    def get_testsuits(self):
        return self.testsuites

    def get_testcase_id_list(self):
        return self.case_id_list

    def get_global_case_id_list(self):
        return self.global_case_id_list




