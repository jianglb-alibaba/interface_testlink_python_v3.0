#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'laifuyu'

import os


class OtherTools:
    def __init__(self):
        pass

    def conver_date_from_testlink(self, data):
        '''加工处理从testlink获取的数据'''

        data = data.replace('<p>', '')
        data = data.replace('</p>', '')
        data =  data.replace('\t', '')
        data =  data.replace('\n', '')
        data =  data.replace('<br />', '')    # 替换空行
        data =  data.replace('&nbsp;', ' ')    # 替换空格
        data =  data.replace('&rsquo;', '"')  # 转换中文单引号 ’为英文的 "
        data =  data.replace('&lsquo;', '"')  # 转换中文单引号‘ 为英文的 "
        data =  data.replace('：', ",")        # 转换中文的冒号 ：为英文的冒号 :
        data =  data.replace('，', ',')        # 转换中文的逗号 ，为英文的逗号 ,
        data =  data.replace('&quot;', '\"')  # 转换 &quot; 为双引号
        data =  data.replace('&#39;', '\'')   # 转换 &#39;  为单引号
        data =  data.replace('｛', '{')        # 转换中文｛ 为英文的 {
        data =  data.replace('｝', '}')        # 转换中文 ｝ 为英文的 }
        data =  data.replace('&lt;', '<')      # 转换 &lt; 为 <
        data =  data.replace('&gt;', '>')      # 转换 &gt为 >
        data =  data.replace('<p align="left">', '')
        data =  data.replace('<p align="right">', '')
        data =  data.replace('<p align="center">', '')
        data = data.replace('&amp;','&')
        return  data

    # 批量创建目录
    def mkdirs_once_many(self, path):
        path = os.path.normpath(path)  # 去掉路径最右侧的 \\ 、/
        path = path.replace('\\', '/') # 将所有的\\转为/，避免出现转义字符串

        head, tail = os.path.split(path)
        new_dir_path = ''  # 反转后的目录路径
        root = ''  #根目录

        if not os.path.isdir(path) and os.path.isfile(path):  # 如果path指向的是文件，则继续分解文件所在目录
            head, tail = os.path.split(head)

        if tail == '':
            return

        while tail:
            new_dir_path = new_dir_path + tail + '/'
            head, tail = os.path.split(head)
            root = head
        else:
            new_dir_path = root + new_dir_path
            # print(new_dir_path)

            # 批量创建目录
            new_dir_path = os.path.normpath(new_dir_path)
            head, tail = os.path.split(new_dir_path)
            temp = ''
            while tail:
                temp = temp + '/' + tail
                dir_path = root + temp
                if not os.path.isdir(dir_path):
                    os.mkdir(dir_path)
                head, tail = os.path.split(head)



