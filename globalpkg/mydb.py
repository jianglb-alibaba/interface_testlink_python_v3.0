#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import configparser
import sys
import mysql.connector

from globalpkg.global_var import logger

class MyDB:
    """动作类，获取数据库连接，配置数据库IP，端口等信息，获取数据库连接"""

    def __init__(self, config_file, db):
        config = configparser.ConfigParser()

        # 从配置文件中读取数据库服务器IP、域名，端口
        config.read(config_file, encoding='utf-8')
        host = config[db]['host']
        port = config[db]['port']
        user = config[db]['user']
        passwd = config[db]['passwd']
        db_name = config[db]['db']
        charset = config[db]['charset']

        try:
            self.dbconn = mysql.connector.connect(host=host, port=port, user=user, password=passwd, database=db_name, charset=charset)
        except Exception as e:
            logger.error('初始化数据连接失败：%s' % e)
            sys.exit()

    def get_conn(self):
        return self.dbconn

    def execute_create(self,query):
        logger.info('query：%s' % query)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            return True
        except Exception as e:
            logger.error('创建数据库表操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit()

    def execute_insert(self, query, data):
        logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query, data)
            db_cursor.execute('commit')
            return True
        except Exception as e:
            logger.error('执行数据库插入操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit()

    def execute_update(self, query):
        logger.info('query：%s' % query)
        try:
            db_cursor = self.dbconn.cursor()
            db_cursor.execute(query)
            db_cursor.execute('commit')
            return True
        except Exception as e:
            logger.error('执行数据库更新操作失败：%s' % e)
            db_cursor.execute('rollback')
            db_cursor.close()
            exit()

    def select_one_record(self, query, data=""):
        '''返回结果只包含一条记录'''
        logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            query_result = db_cursor.fetchone()
            return query_result
        except Exception as e:
            logger.error('执行数据库查询操作失败：%s' % e)
            db_cursor.close()
            exit()

    def select_many_record(self, query, data=""):
        '''返回结果只包含多条记录'''
        logger.info('query：%s  data：%s' % (query, data))
        try:
            db_cursor = self.dbconn.cursor()
            if data:
                db_cursor.execute(query, data)
            else:
                db_cursor.execute(query)
            query_result = db_cursor.fetchall()
            return query_result
        except Exception as e:
            logger.error('执行数据库查询操作失败：%s' % e)
            db_cursor.close()
            exit()

    def close(self):
        self.dbconn.close
