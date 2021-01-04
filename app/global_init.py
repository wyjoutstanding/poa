# from config import *
import config as cfg

import sys
import os

def update_keyword_list(filename, list_data):
    # list_data = ['1', '我们', '大家']
    file=open(filename,'a+')
    for data in list_data:
        file.write(str(data) + '\n')
    file.close()

def get_keyword_list(filename):
    file = open(filename, 'r')
    l = file.readlines()
    file.close()
    for i in range(len(l)):
        l[i] = l[i][0:-1]
    # if '大家' not in l:
    #     print('1 not in l')
    # else:
    #     print('1 in l')
    # print(type(l), l)
    return l

def global_data_init():
    CWDIR = os.getcwd()

    CSV_FILENAME_BAIDU_DIR = CWDIR + '/topic/'
    CSV_FILENAME_HOTSPOT_DIR = CWDIR + '/topic/'
    CSV_FILENAME_WEIBO_DIR = CWDIR + '/topic/'

    cfg.set_value("CSV_FILENAME_BAIDU_DIR", CSV_FILENAME_BAIDU_DIR)
    cfg.set_value("CSV_FILENAME_HOTSPOT_DIR", CSV_FILENAME_HOTSPOT_DIR)
    cfg.set_value("CSV_FILENAME_WEIBO_DIR", CSV_FILENAME_WEIBO_DIR)
    print(CSV_FILENAME_BAIDU_DIR, CSV_FILENAME_HOTSPOT_DIR, CSV_FILENAME_WEIBO_DIR)
    
    # 默认值设置
    cfg.set_value('DEFAULT_NAME', '科比')
    DEFAULT_NAME = cfg.get_value('DEFAULT_NAME')
    #======= 默认数据 ==========
    # KEYWORDS = '元旦'
    # 百度默认数据
    # CSV_FILENAME_BAIDU = CSV_FILENAME_BAIDU_DIR + "元旦.csv"
    cfg.set_value("CSV_FILENAME_BAIDU" , CSV_FILENAME_BAIDU_DIR + ".csv")
    # 焦点排序的数据
    # CSV_FILENAME_HOTSPOT = CSV_FILENAME_HOTSPOT_DIR + "元旦_TOP10.csv"
    cfg.set_value("CSV_FILENAME_HOTSPOT", CSV_FILENAME_HOTSPOT_DIR + DEFAULT_NAME + "_TOP10.csv")
    # 微博数据
    # CSV_FILENAME_WEIBO = CSV_FILENAME_WEIBO_DIR + "元旦.csv"
    cfg.set_value("CSV_FILENAME_WEIBO", CSV_FILENAME_WEIBO_DIR + DEFAULT_NAME + "_WEIBO.csv")

    KEYWORD_LIST = get_keyword_list('data.txt')
    print(KEYWORD_LIST)

if __name__ == "__main__":
    get_keyword_list('data.txt')
