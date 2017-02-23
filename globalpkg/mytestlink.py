#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

from testlink import TestLinkHelper, TestlinkAPIClient
#from testlink.testlinkerrors import TLResponseError
from globalpkg.log import logger

class TestLink():
    def __init__(self):
        tlk_helper = TestLinkHelper()
        try:
            self.testlink = tlk_helper.connect(TestlinkAPIClient)  # 连接TestLink
        except Exception as e:
            logger.error('连接testlink失败：%s' % e)
            exit()

    def get_testlink(self):
        return self.testlink


