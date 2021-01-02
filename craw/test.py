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
import chardet

# 正则操作库
import re
from Spider.until import websites, untils
import random



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
# print(url1 in bloom)
# print(url2 in bloom)
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
        #print(url_time) 
        #print(DEFAULT_END_TIME.strftime('%Y-%m-%d'))   
        if url_time > DEFAULT_START_TIME:
            return url_time.strftime('%Y-%m-%d')
        else:
            return None   




#获取当前页面内容并换页
def get_baidu_info(urls, count, url_cnt=10, max_cnt= 10, start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):
    try:
        response = urlopen(urls)
        if response == None:
            return "网页未获取"
        data = response.read().decode()
        html = etree.HTML(data)
        for i in range(url_cnt):
            count[0] += 1
            print(count)
            #print('\n')

            time = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/div/span[2])')
            if len(time) == 0:
                    time = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/div/span[2])')
            time = time_check(time)
            if time:

                title = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/h3/a)')
                print(title)

                url = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/h3/a/@href)')
                #print(url)
                if url in bloom:
                    print("结束")
                    #file.close()
                    return count[0]
                else: 
                    bloom.add(url)

                text = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/span)')
                #无配图的另一种情况
                if len(text) == 0:
                    text = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/span)')
                
                #print(text)
            else:
                print("结束")
                #file.close()
                return count[0]
            
            if count[0] % (url_cnt) == 0:
                if count[0] >= max_cnt:
                    print("结束")
                    #file.close()
                    return count[0]
                sleep(random.random()*8)
                next_url = html.xpath('string(//*[@id="page"]/div/a[contains(text(),"下一页")]/@href)')
                next_url = "http://www.baidu.com"+next_url
                get_baidu_info(next_url, count, url_cnt, max_cnt, start_time, end_time)    
    except error.URLError as e:
        pass            


# 爬取百度驱动函数
def baidu_crawl(keys, website='', url_cnt=10, max_cnt= 10,start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):

    url_key = quote(keys, encoding='utf8')
    #url_key = keys
    count = [0]
    i = 0
    filename = keys + DEFAULT_END_TIME.__str__() + ".csv"
    #f = open(filename, "a+")
    search_result_url = r"http://www.baidu.com/s?rtt=4&bsst=1&cl=2&tn=news&ie=utf-8&word=" + url_key + website
    #print (search_result_url)
    sleep(random.random()*8)
    get_baidu_info(search_result_url, count, url_cnt, max_cnt, start_time, end_time)
    


def info():
    url = 'http://cache.baiducontent.com/c?m=JeeOAJumUDZaBPOF2BoAC5bfCrx6ayLli2ArQesItWvKFA8cl2KIN7tp1701O7S9k7MKJhOqP-heV2YYC3FU1JZ72of8_-j91U9xRisuOgTa35g-aVLTwrcA0yI1sa7nWJNbNnJ7fTULQ6ZhSeXaHSE-ReKE4kBcvjMXHner9aO&p=8b2a975f86cc4ab50e818a3744&newp=c93ece1786cc4af346be9b7c4253d8265f15ed6239c3864e1290c408d23f061d4866e0bf2d241703d0c1777347c2080ba8ff612e615f3e&s=c81e728d9d4c2f63&user=baidu&fm=sc&query=%D4%AA%B5%A9+site%3Abaidu%2Ecom&qid=9d6917870004b9a0&p1=1'
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read()
    html = etree.HTML(data)
    text = html.xpath('string(//*[@id="article"]/div)')
    text = tool.clean(text)
    print(text)
    return text  
    '''    
    else:  
        response = urlopen(url)
        if response == None:
            return "网页未获取"
        data = response.read().decode('gbk')
        html = etree.HTML(data)  
        print("____________________________\n")
        text = html.xpath('string(/html/body/div[3]/div[1]/div[1]/div[2])')
        print(text)
    '''
def baijiahao_info(url):
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read()
    html = etree.HTML(data)
    text = html.xpath('string(//*[@id="article"]/div)')
    text = tool.clean(text)
    print(text)
    if len(text) == 0:
        return "ERROR_NONTEXT"
    return text  

def qq_info(url):
    if "cache.baiducontent.com" in url:
        response = urlopen(url)
        if response == None:
            return "网页未获取"
        data = response.read()
        html = etree.HTML(data)
        text = html.xpath('string(/html/body/div[4]/div/div/div[3]/div/div[2]/div[2]/div[1])')
        text = tool.clean(text)
        print(text)
        if len(text) == 0:
        return "ERROR_NONTEXT"
        return text  
    else:  
        response = urlopen(url)
        if response == None:
            return "网页未获取"
        data = response.read().decode('gbk')
        html = etree.HTML(data)  
        text = html.xpath('string(/html/body/div[3]/div[1]/div[1]/div[2])')
        text = tool.clean(text)
        print(text)
        if len(text) == 0:
        return "ERROR_NONTEXT"
        return text  


def people_info(url):
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read()
    html = etree.HTML(data)
    text = html.xpath('string(//div[@class="box_con"])')
    
    text = tool.clean(text)
    print(text)
    if len(text) == 0:
        return "ERROR_NONTEXT"
    return text

def huanqiu_info(url):
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    #转换编码,网页编码不统一,无法编译的直接忽略    
    data = response.read().decode("gb2312","ignore")
    #print(data)
    #print (chardet.detect(data)['encoding'])
    html = etree.HTML(data)#,etree.HTMLParser(encoding='gbk'))
    text = html.xpath('string(/html/body/div[4]/div[2]/div/div[4]/div[1]/div[1]/article/section)')

    if len(text) == 0:
        text = html.xpath('string(/html/body/div[2]/div/div[4]/div[1]/div[1]/div[1]/div)')
    text = tool.clean(text)
    print(text)
    if len(text) == 0:
        return "ERROR_NONTEXT"
    return text

def fenghuang_info(url):

    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read()
    html = etree.HTML(data)
    if html.xpath('//*[@id="js_playVideo"]'):
        return "ERROR_NONTEXT"
    text = html.xpath('string(//div[@class="text-3w2e3DBc"])')
    
    text = tool.clean(text)
    print(text)
    if len(text) == 0:
        return "ERROR_NONTEXT"
    return text

def xinhua_info(url):
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read().decode('gb2312','ignore')
    html = etree.HTML(data)
    text = ''
    for i in html.xpath('//div[@id="detail"]/p/text()') :
        text = text + i
    if len(text) == 0:
        text = html.xpath('string(//*[@id="detail"])')   
    if len(text) == 0:
        text = html.xpath('string(//div[@class="content"])')
    
    text = tool.clean(text)
    print(text)
    if len(text) == 0:
        return "ERROR_NONTEXT"
    return text



if __name__ == "__main__":
    #info()
    #baijiahao_info('http://cache.baidu.com/c?m=2F7sTj5CuNkgQZooEFYyHZ8t9ny8jJINyC6Hb8-3atlkC2OGgm5e296IwWH-lQbAhhOMbweRPVwbHt0Gk6IBCMGLepepD4bbiglne_Kp1HawNA7kqe5X_vu2-b1qGkxhpai4ck8K4yYupwiT4A9jUKF6hzDNIk5bsoUv82rjXh7&p=c3769a478cd511a05cf3db364c&newp=9a769a47c08911a05ca2d03a4553d8265f15ed6728818b783b83d309c839074e4765e7b121251707d7ce68216cee1e1ee5a76a242149&s=cfcd208495d565ef&user=baidu&fm=sc&query=%D4%AA%B5%A9+site%3Abaidu%2Ecom&qid=c667528b0004acfe&p1=1')
    fenghuang_info('http://cache.baiducontent.com/c?m=k-W75B5Zafb4qdTdrfv0DzfddjtN1DX0F0Q_P9-ydzSAbcZ4YRrTLiHGoePs6keYG7DEJlJTLGpjc7M10rffRONRJYH7qrlVnMwt62-htKS&p=8b2a9753ce9b0bef08e2943e4c&newp=c377c54ad68912a05ab9f8664f53d8265f15ed623ec3864e1290c408d23f061d4866e0bf2d241703d0c1777347c2080ba8ff612e6149&s=8eb92db0d591d7ea&user=baidu&fm=sc&query=%D4%AA%B5%A9+site%3Aifeng%2Ecom&qid=afa9904a002cd54f&p1=41')
    #time_check("2020年12月29日 17:28")
    # get_baidu_info_keys("https://baidu.baidu.com/p/6862614326")
