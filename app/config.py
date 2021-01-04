#!/usr/bin/env python
# encoding: utf-8

import os
# -*- coding: utf-8 -*-
def _init():#初始化
    global _global_dict
    _global_dict = {}

def set_value(key,value):
    """ 定义一个全局变量 """
    _global_dict[key] = value

def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    # print(type(_global_dict))
    # global _global_dict
    # if not '_global_dict' in dir():
    #     return defValue
    try:
        return _global_dict[key]
    except KeyError:
        return defValue


# Session key: https://www.jianshu.com/p/278d4f59839d
SECRET_KEY = os.urandom(24)

KEYWORDS = ''
KEYWORD_LIST = ''
# 当前工作目录
CWDIR = ''

# CSV_FILENAME_BAIDU_DIR = ''
# CSV_FILENAME_HOTSPOT_DIR = ''
# CSV_FILENAME_WEIBO_DIR = ''
# 百度爬取的所有网站的数据
# CSV_FILE_BAIDU_DIR = 
# 爬取标记
CSV_FILE_BAIDU_NAME = False

# CSV_FILENAME_BAIDU = get_value("CSV_FILENAME_BAIDU", 'DEFUALT')

# 焦点排序的数据
# CSV_FILENAME_HOTSPOT = get_value('CSV_FILENAME_HOTSPOT', 'DEFUALT')

# 微博数据
# CSV_FILENAME_WEIBO = get_value("CSV_FILENAME_WEIBO", 'DEFUALT')

CSV_FILENAME_HOTSPOT_FLAG = False
CSV_FILENAME_WEIBO_FLAG  = False

TOKEN_BAIDU = '24.d1b6bbb9cfd8cdc8f670e5a5e36eeba4.2592000.1612230823.282335-18713558'