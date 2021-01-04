import  threading
from Spider.baidu import baidu_crawl
from Spider.topTen import topTen
from Spider.until import websites, csvTool
from time import sleep
import csv
import os


import sys
sys.path.append("..")
import config as cfg
# from app.config import *

class MyThread(threading.Thread):

    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


def craw_baidu(key):
    t = []
    fname = []
    MAX_CNT = 20 # 最大数目
    t.append( MyThread(baidu_crawl, args=(key, websites.bajiahao, 10, MAX_CNT)) )
    fname.append(key+websites.bajiahao+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.qq, 10, MAX_CNT)) )
    fname.append(key+websites.qq+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.people, 10, MAX_CNT)) )
    fname.append(key+websites.people+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.fenghuang, 10, MAX_CNT)) )
    fname.append(key+websites.fenghuang+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.xinhua, 10, MAX_CNT)) )
    fname.append(key+websites.xinhua+".tmp")  
    t.append( MyThread(baidu_crawl, args=(key, websites.huanqiu, 10, MAX_CNT)) )
    fname.append(key+websites.huanqiu+".tmp")


    for ti in t:
        ti.start()
        sleep(5)

    for ti in t:
        ti.join()
        print( ti.get_result())
        print("_______________________________________")

    file = open('topic/' + key + ".csv","w+", encoding='utf-8')
    writer = csv.writer(file)
    csvTool.write_csv(writer)

    for i in fname:
        f = open (i, "r", encoding='UTF-8')
        if f:
            for l in f:
                file.write(l)
            f.close()
            os.remove(i)
            
    file.close()


def craw_topTen(key):
    DIR = cfg.get_value('CSV_FILENAME_HOTSPOT_DIR')
    cfg.set_value('CSV_FILENAME_HOTSPOT', DIR + key + '_TOP10.csv')
    print('craw_topTen weibo:', cfg._global_dict)
    topTen(key)

import WeiBo
def craw_start(key):
    DIR = cfg.get_value('CSV_FILENAME_WEIBO_DIR')
    cfg.set_value('CSV_FILENAME_WEIBO', DIR + key + '_WEIBO.csv')
    print('craw_start: ', cfg._global_dict)
    WeiBo.sina_crawl(key, url_cnt=4)

    DIR = cfg.get_value('CSV_FILENAME_BAIDU_DIR')
    cfg.set_value('CSV_FILENAME_BAIDU', DIR + key + '.csv')
    print('craw_topTen baidu:', cfg._global_dict)
    craw_baidu(key)



if __name__ == "__main__":
    key = input("关键词: ")

    out = []

    topTen(key)

    #for i in topTen(key):
    #    print(i)
    #    print('\n')

    
    t = []
    fname = []
    t.append( MyThread(baidu_crawl, args=(key, websites.bajiahao, 10, 40)) )
    fname.append(key+websites.bajiahao+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.qq, 10, 40)) )
    fname.append(key+websites.qq+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.people, 10, 40)) )
    fname.append(key+websites.people+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.fenghuang, 10, 40)) )
    fname.append(key+websites.fenghuang+".tmp")
    t.append( MyThread(baidu_crawl, args=(key, websites.xinhua, 10, 40)) )
    fname.append(key+websites.xinhua+".tmp")  
    t.append( MyThread(baidu_crawl, args=(key, websites.huanqiu, 10, 40)) )
    fname.append(key+websites.huanqiu+".tmp")


    for ti in t:
        ti.start()
        sleep(5)

    for ti in t:
        ti.join()
        print( ti.get_result())
        print("_______________________________________")

    file = open(key + "_WEIBO.csv","w+", encoding='utf-8')
    writer = csv.writer(file)
    csvTool.write_csv(writer)

    for i in fname:
        f = open (i, "r", encoding='UTF-8')
        if f:
            for l in f:
                file.write(l)
            f.close()
            os.remove(i)
            

    file.close()    
    
      

    
