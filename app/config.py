#!/usr/bin/env python
# encoding: utf-8

import os
# Session key: https://www.jianshu.com/p/278d4f59839d
SECRET_KEY = os.urandom(24)

# 百度爬取的所有网站的数据
CSV_FILENAME_BAIDU = "/home/wyj/poa/craw/元旦.csv"
# 爬取标记
CSV_FILENAME_BAIDU_FLAG = False

# 焦点排序的数据
CSV_FILENAME_HOTSPOT = "/home/wyj/poa/craw/元旦_TOP10.csv"
CSV_FILENAME_HOTSPOT_FLAG = False

# 微博数据
CSV_FILENAME_WEIBO = ""
CSV_FILENAME_WEIBO_FLAG  = False

TOKEN_BAIDU = '24.d1b6bbb9cfd8cdc8f670e5a5e36eeba4.2592000.1612230823.282335-18713558'