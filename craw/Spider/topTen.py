# -*- coding: utf-8 -*-
# python爬取百度资讯, 字符为GBK

'''
 out字段:
    public_no	bigint	20				编号
    topic	varchar	50				话题
    sensitive_word	varchar	50				敏感词
    source	varchar	10				来源
    type	varchar	10				类型
    theme	varchar	50				主题
    content	text	0				详细内容
    public_time	datetime	6				发布时间
    is_publish	tinyint	1				是否公布
    election_score	varchar	10				选报分
    adopt_points	varchar	10				采纳分
    publisher	varchar	10				发布人
    status	tinyint	2				状态

'''

# 日期时间
from datetime import datetime, timedelta
from time import mktime, sleep
# 网页去重工具--布隆过滤器 安装命令: pip install pybloom_live
from pybloom_live import ScalableBloomFilter, BloomFilter
# 中文符号转URL编码操作库---res = quote(....,encodeing='GBK')
from urllib.parse import quote, unquote
from urllib.request import urlopen, Request
from urllib import error
from lxml import etree
import ssl

# 正则操作库
import re
from Spider.until import websites, untils, csvTool
#from until import websites, untils, csvTool
import random
import csv



# 可自动扩容的布隆过滤器
bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)
#####################################
## 博隆过滤器使用方法 ##
# url1 = 'http://www.baidu.com'
# url2 = 'http://qq.com'
#
# bloom.add(url1) # 添加 url
#
# url in bloom 即可判断 url 是否重复
# #print(url1 in bloom)
# #print(url2 in bloom)
#####################################

DEFAULT_START_TIME = datetime.now() - timedelta(days=30)
DEFAULT_END_TIME = datetime.now()

# 防止403 请求头
my_headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
              "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
              "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"

              ]

issuseCount = 0
num = 0

ssl._create_default_https_context = ssl._create_unverified_context

# 定义全局工具类tool
tool = untils.Tool()

def time_check( url_time):
    if "分钟前" in url_time or "小时前" in url_time:
        return DEFAULT_END_TIME.strftime('%Y-%m-%d')
    else:
        url_time = url_time.replace("年","-",1)
        url_time = url_time.replace("月","-",1)
        url_time = url_time.replace("日","",1)
        url_time = datetime.strptime(url_time, "%Y-%m-%d %H:%M")
        ##print(url_time) 
        ##print(DEFAULT_END_TIME.strftime('%Y-%m-%d'))   
        if url_time > DEFAULT_START_TIME:
            return url_time.strftime('%Y-%m-%d')
        else:
            return None   




#获取当前页面内容并换页
def get_ten(urls, count, url_cnt=10, max_cnt= 10, start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):
    try:

        item = []

        response = urlopen(urls)
        if response == None:
            return "网页未获取"
        data = response.read().decode()
        html = etree.HTML(data,etree.HTMLParser(encoding='utf8'))
        for i in range(url_cnt):
            count[0] += 1
            #print(count)
            ##print('\n')
            ##print('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/div/span[2])')
            time = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/div/span[2])')
            #print(time)
            if len(time) == 0:
                    time = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/div/span[2])')
                    #print(time)
            if time:
                time = time_check(time)
            else:
                time = DEFAULT_END_TIME.strftime('%Y-%m-%d')     
            
            title = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/h3/a)')
            #print(title)
            url = html.xpath('string(/html/body/div/div[3]/div[1]/div[4]/div[2]/div['+ str(count[0]) +']/div/h3/a/@href)')
            #print(url)
            
            text = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/span)')
            #无配图的另一种情况
            if len(text) == 0:
                text = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/span)')
            
            item.append([title,time,url,text])
            
            if count[0] % (url_cnt) == 0:
                if count[0] >= max_cnt:
                    #print("结束")
                    #file.close()
                    return item
                sleep(random.random()*8)
                next_url = html.xpath('string(//*[@id="page"]/div/a[contains(text(),"下一页")]/@href)')
                next_url = "http://www.baidu.com"+next_url
                get_ten(next_url, count, url_cnt, max_cnt, start_time, end_time)    
        return item        
    except error.URLError as e:
        pass            


# 爬取百度驱动函数
def topTen(keys, url_cnt=10, max_cnt= 10,start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):

    url_key = quote(keys, encoding='utf8')
    #url_key = keys
    count = [0]
    i = 0
    search_result_url = r"http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word=" + url_key
    #print (search_result_url)
    return get_ten(search_result_url, count, url_cnt, max_cnt, start_time, end_time)
    

    

if __name__ == "__main__":
    baidu_crawl("元旦", websites.huanqiu)
    #time_check("2020年12月29日 17:28")
    # get_baidu_info_keys("https://baidu.baidu.com/p/6862614326")
