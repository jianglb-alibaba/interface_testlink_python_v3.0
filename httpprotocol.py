#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import urllib.request
import http.cookiejar
import urllib.parse
import ssl

from globalpkg.log import logger

class MyHttp:
    '''配置要测试接口服务器的ip、端口、域名等信息，封装http请求方法，http头设置'''

    def __init__(self, protocol, host, port, header = {}):
        # 从配置文件中读取接口服务器IP、域名，端口
        self.protocol = protocol
        self.host = host
        self.port = port
        self.headers = header  # http 头

        #install cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

        # 添加以支持ssl # 注意，发起的请求要为443端口
        https_sslv3_handler = urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv2))
        opener = urllib.request.build_opener(https_sslv3_handler)
        urllib.request.install_opener(opener)

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def get_protocol(self):
        return self.protocol

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return  self.port

    # 设置http头
    def set_header(self, headers):
        self.headers = headers

    # 封装HTTP GET请求方法
    def get(self, url, params=''):
        url = self.protocol + '://' + self.host + ':' + str(self.port)  + url + params

        logger.info('发起的请求为：%s' % url)
        logger.info('请求头为：%s' % self.headers)
        request = urllib.request.Request(url, headers=self.headers)
        try:
            response = urllib.request.urlopen(request)
            response_body = response.read()
            response_header = response.getheaders()
            response_status_code = response.status
            response = [response_body, response_header, response_status_code]
            return response
        except Exception as e:
            logger.error('发送请求失败，原因：%s' % e)
            return None

    # 封装HTTP POST请求方法
    def post(self, url, data=''):
        url = self.protocol + '://' + self.host + ':' + str(self.port)  + url

        logger.info('发起的请求为：%s' % url)
        logger.info('参数为：%s' % data)
        logger.info('请求头为：%s' % self.headers)
        request = urllib.request.Request(url, headers=self.headers)
        try:
            response = urllib.request.urlopen(request, data)
            response_body = response.read()
            response_header = response.getheaders()
            response_status_code = response.status
            response = [response_body, response_header, response_status_code]
            return response
        except Exception as e:
            logger.error('发送请求失败，原因：%s' % e)
            return None

    # 封装HTTP xxx请求方法
    # 自由扩展