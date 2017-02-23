#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import os

from pyh import *
from globalpkg.log import logger
from globalpkg.global_var import testdb
from globalpkg.global_var import case_step_report_tb
from globalpkg.global_var import testcase_report_tb
from globalpkg.global_var import executed_history_id
from globalpkg.global_var import other_tools

class HtmlReport:
    def __init__(self, title, head):
        self.title = title                                       # 网页标签名称
        self.head = head                                         # 标题
        self.filename = 'testrepot.html'   # 结果文件名
        self.dir = './testreport/'         # 结果文件目录
        self.time_took = '00:00:00'         # 测试耗时
        self.success_num = 0                  # 测试通过的用例数
        self.fail_num = 0                     # 测试失败的用例数
        self.error_num = 0                    # 运行出错的用例数
        self.block_num = 0                    # 未运行的测试用例总数
        self.case_total = 0                   # 运行测试用例总数


    # 生成HTML报告
    def generate_html(self, file):
        page = PyH(self.title)
        page << h1(self.head, align='center') # 标题居中

        page << p('测试总耗时：' + self.time_took)

        logger.info('正在查询测试用例总数')
        query = 'SELECT count(testcase_id) FROM ' + testcase_report_tb + ' WHERE executed_history_id = %s'
        data = (executed_history_id,)
        result = testdb.select_one_record(query, data)
        self.case_total = result[0]

        logger.info('正在查询执行通过的用例数')
        query = 'SELECT count(testcase_id) FROM ' + testcase_report_tb + ' WHERE runresult = %s AND executed_history_id = %s'
        data = ('Pass', executed_history_id)
        result = testdb.select_one_record(query, data)
        self.success_num = result[0]

        logger.info('正在查询执行失败的用例数')
        query = 'SELECT count(testcase_id) FROM ' + testcase_report_tb + ' WHERE runresult = %s AND executed_history_id = %s'
        data = ('Fail', executed_history_id)
        result = testdb.select_one_record(query, data)
        self.fail_num = result[0]

        logger.info('正在查询执行出错的用例数')
        query = 'SELECT count(testcase_id) FROM ' + testcase_report_tb + ' WHERE runresult = %s AND executed_history_id = %s'
        data = ('Error', executed_history_id)
        result = testdb.select_one_record(query, data)
        self.error_num = result[0]

        logger.info('正在查询未执行的用例数')
        query = 'SELECT count(testcase_id) FROM ' + testcase_report_tb + ' WHERE runresult = %s AND executed_history_id = %s'
        data = ('Block', executed_history_id)
        result = testdb.select_one_record(query, data)
        self.block_num = result[0]

        page << p('用例总数：' + str(self.case_total) + '&nbsp'*10 + '成功用例数(Pass)：' + str(self.success_num) +\
                      '&nbsp'*10 + '失败用例数(Fail)：' + str(self.fail_num) + '&nbsp'*10 +  '出错用例数(Error)：' + str(self.error_num) +\
                      '&nbsp'*10 +  '未执行用例数(Block)：' + str(self.block_num))

        page << p('<br/>####################################################用例执行摘要####################################################<br/>')
        logger.info('正在查询已运的测试计划')
        query = ('SELECT project, testplan FROM ' + testcase_report_tb +\
                             ' WHERE executed_history_id = %s GROUP BY project, testplan ORDER BY id ASC')
        data = (executed_history_id,)
        result = testdb.select_many_record(query, data)

        for row in result:
            project = row[0]
            testplan = row[1]
            page << p('###测试计划【项目名称：' + project + ', 计划名称：<a name=\"first'+ testplan + '\"' + 'href=\"#second' + testplan + '\">'
                     + testplan + '</a>】')

            #  表格标题caption 表格边框border 单元格边缘与其内容之间的空白cellpadding 单元格之间间隔为cellspacing
            tab = table( border='1', cellpadding='1', cellspacing='0', cl='table')
            tab1 = page << tab

            tab1 << tr(td('ID', bgcolor='#ABABAB', align='center')
                           + td('执行编号', bgcolor='#ABABAB', align='center')
                           + td('用例ID', bgcolor='#ABABAB', align='center')
                           + td('用例名称', bgcolor='#ABABAB', align='center')
                           + td('测试套件', bgcolor='#ABABAB', align='center')
                           + td('测试计划', bgcolor='#ABABAB', align='center')
                           + td('测试项目', bgcolor='#ABABAB', align='center')
                           + td('执行结果', bgcolor='#ABABAB', align='center')
                           + td('运行时间', bgcolor='#ABABAB', align='center'))

            logger.info('正在查询测试计划[project：%s, testplan：%s]的测试用例执行结果' % (row[0],row[1]))
            query = ('SELECT id, executed_history_id, testcase_id, testcase_name,'
                                 'testsuit, testplan, project, runresult, runtime FROM ' + testcase_report_tb +\
                                 ' WHERE project=%s AND testplan=%s AND executed_history_id = %s GROUP BY testcase_id ORDER BY id ASC')
            data = (project,testplan, executed_history_id)
            result = testdb.select_many_record(query, data)

            logger.info('正在记录测试测试计划[project：%s, testplan：%s]的测试用例运行结果到测试报告' % (row[0],row[1]))
            for row in result:
                tab1 << tr(td(str(row[0]), align='center') + td(row[1], align='center') + td(row[2], align='center') +
                                td('<a name=\"first'+str(row[2]) + project + testplan + '\"' + 'href=\"#second' + str(row[2]) + project + testplan + '\">' + row[3] + '</a>')
                                + td(row[4]) + td(row[5], align='center') + td(row[6], align='center') + td(row[7], align='center')
                                + td(row[8], align='center'))

            page << p('<br/>')

        page << p('<br/>####################################################用例执行明细####################################################<br/>')
        logger.info('正在查询已运的测试计划')
        query = ('SELECT project, testplan FROM ' + testcase_report_tb +\
                             ' WHERE executed_history_id = %s GROUP BY project, testplan ORDER BY id ASC')
        data = (executed_history_id,)
        result = testdb.select_many_record(query, data)
        for row in result:
            project = row[0]
            testplan = row[1]

            page << p('###测试计划【项目名称：' + project + ', 计划名称：<a name=\"second'+ testplan + '\"' + 'href=\"#first' + testplan + '\">'
                     + testplan + '</a>】')

            logger.info('正在查询测试计划[project：%s, testplan：%s]已运行的测试用例' % (project, testplan))
            query = ('SELECT testcase_id, testcase_name, project, testplan FROM ' + testcase_report_tb + \
                     ' WHERE project=%s AND testplan=%s AND executed_history_id = %s '\
                     ' GROUP BY testcase_id ORDER BY id ASC')
            data = (project, testplan, executed_history_id)
            result = testdb.select_many_record(query, data)

            # 遍历测试用例的测试步骤执行结果
            for row in result:
                case_id = row[0]
                case_name = row[1]
                project = row[2]
                testplan = row[3]

                page << p('>>>测试用例【caseID：' + str(case_id) + '，名称：<a name=\"second'+ str(case_id) + project + testplan +'\"' + \
                          'href=\"#first' + str(case_id) + project + testplan + '\">' + case_name + '</a>】')

                tab = table( border='1', cellpadding='1', cellspacing='0', cl='table')
                tab2 = page << tab
                tab2 << tr(td('步骤ID', bgcolor='#ABABAB', align='center')
                       + td('步序', bgcolor='#ABABAB', align='center')
                       + td('协议方法', bgcolor='#ABABAB', align='center')
                       + td('协议', bgcolor='#ABABAB', align='center')
                       + td('主机', bgcolor='#ABABAB', align='center')
                       + td('端口', bgcolor='#ABABAB', align='center')
                       + td('ACTION', bgcolor='#ABABAB', align='center')
                       + td('预期结果', bgcolor='#ABABAB', align='center')
                       + td('运行结果', bgcolor='#ABABAB', align='center')
                       + td('原因分析', bgcolor='#ABABAB', align='center')
                       + td('运行时间', bgcolor='#ABABAB', align='center'))

                logger.info('正在查询测试用例[id=%s]步骤运行结果' % case_id)
                # query = ('SELECT step_id, step_num, protocol_method, protocol, host, port, '
                #      'step_action, expected_results, cstb.runresult, reason, cstb.runtime'\
                #      ' FROM ' + case_step_report_tb + ' AS cstb'\
                #      ' JOIN ' + testcase_report_tb + ' AS tstb ON cstb.testcase_id =  tstb.testcase_id'\
                #      ' AND cstb.project=tstb.project AND cstb.testplan=tstb.testplan AND cstb.executed_history_id = tstb.executed_history_id'
                #      ' WHERE tstb.project= %s AND tstb.testplan=%s'\
                #      ' AND cstb.testcase_id=%s AND cstb.executed_history_id = %s ORDER BY step_num asc')
                query= 'SELECT step_id, step_num, protocol_method, protocol, HOST, PORT, step_action, expected_results, runresult, reason, runtime ' \
                      'FROM case_step_report_tb ' \
                      'WHERE project= %s AND testplan= %s AND testcase_id = %s ' \
                      'AND executed_history_id = %s ' \
                      'GROUP BY step_num ' \
                      'ORDER BY step_num ASC'
                data = (project, testplan, case_id, executed_history_id)
                result = testdb.select_many_record(query, data)
                for row in result:
                    tab2 << tr(td(str(row[0]), align='center') + td(row[1], align='center') + td(row[2], align='center') +
                            td(row[3], align='center') +  td(row[4], align='center') + td(str(row[5]), align='center') +
                            td(str(row[6]), align='left') + td(row[7], align='left') + td(row[8], align='center')
                            + td(row[9], align='left') + td(row[10], align='center'))
                page << p('<br/>')

        page << p('<br/>')

        logger.info('正在设置测试报告结果文件名')
        self.__set_result_filename(file)

        logger.info('正在生成测试报告')
        page.printOut(self.filename)

    # 设置结果文件名
    def __set_result_filename(self, filename):
        parent_path, ext = os.path.splitext(filename)
        self.filename = self.dir + parent_path  + str(executed_history_id) + ext
        logger.info('测试报告文件名所在路径为：%s' % self.filename)

    # 创建报告保存目录
    def mkdir_of_report(self, path):
        other_tools.mkdirs_once_many(path)
        self.dir = path

    def get_filename(self):
        return self.filename

    # 统计运行耗时
    def set_time_took(self, time):
        self.time_took = time
        return self.time_took
