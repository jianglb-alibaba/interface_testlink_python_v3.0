#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

from html.parser import HTMLParser
from html.entities import name2codepoint

from globalpkg.log import logger

class MyHTMLParser(HTMLParser):
    def __init__(self, strict):
        super().__init__(strict)
        self.start_tag = ''
        self.starttag_arrts = []
        self.starttag_data = []

    def handle_starttag(self, tag, attrs):
        logger.debug('Start tag: %s' % tag)
        tmp_list = [tag, attrs]
        self.start_tag = tag
        self.starttag_arrts.append(tmp_list)

    def handle_endtag(self, tag):
        pass
        logger.debug('End tag: %s' % tag)

    def handle_data(self, data):
        logger.debug('Data %s' % data)
        tmp_list = [self.start_tag, data]
        self.starttag_data.append(tmp_list)

    def handle_comment(self, data):
        pass
        logger.debug('Comment：%s' % data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        logger.debug('Named ent：%s' % c)

    def handle_charref(self, name):
        if name.startswitch('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        logger.debug('Num ent：%s' % c)

    def handle_decl(self, data):
        pass
        #logger.info('Decl：' % data)

    def get_starttag_attrs(self):
        return self.starttag_arrts

    def get_starttag_data(self):
        return self.starttag_data





