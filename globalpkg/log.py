#!/usr/bin/env python
# -*- coding:utf-8 -*-


__author__ = 'laifuyu'
import logging
from logging.handlers import RotatingFileHandler
import threading
import configparser


class LogSignleton(object):
    def __init__(self, log_config):
        pass

    def __new__(cls, log_config):
        mutex=threading.Lock()
        mutex.acquire() # 上锁，防止多线程下出问题
        if not hasattr(cls, 'instance'):
            cls.instance = super(LogSignleton, cls).__new__(cls)
            config = configparser.ConfigParser()
            config.read(log_config, encoding='utf-8')
            cls.instance.log_filename = config.get('LOGGING', 'log_file')
            cls.instance.max_bytes_each = int(config.get('LOGGING', 'max_bytes_each'))
            cls.instance.backup_count = int(config.get('LOGGING', 'backup_count'))
            cls.instance.fmt = config.get('LOGGING', 'fmt')
            cls.instance.log_level_in_console = int(config.get('LOGGING', 'log_level_in_console'))
            cls.instance.log_level_in_logfile = int(config.get('LOGGING', 'log_level_in_logfile'))
            cls.instance.logger_name = config.get('LOGGING', 'logger_name')
            cls.instance.console_log_on = int(config.get('LOGGING', 'console_log_on'))
            cls.instance.logfile_log_on = int(config.get('LOGGING', 'logfile_log_on'))
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
        mutex.release()
        return cls.instance

    def get_logger(self):
        return  self.logger

    def __config_logger(self):
        # 设置日志格式
        fmt = self.fmt.replace('|','%')
        formatter = logging.Formatter(fmt)

        if self.console_log_on == 1: # 如果开启控制台日志
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)
            self.logger.setLevel(self.log_level_in_console)

        if self.logfile_log_on == 1: # 如果开启文件日志
            rt_file_handler = RotatingFileHandler(self.log_filename, maxBytes=self.max_bytes_each, backupCount=self.backup_count)
            rt_file_handler.setFormatter(formatter)
            self.logger.addHandler(rt_file_handler)
            self.logger.setLevel(self.log_level_in_logfile)

logsignleton = LogSignleton('./config/logconfig.conf')
logger = logsignleton.get_logger()


