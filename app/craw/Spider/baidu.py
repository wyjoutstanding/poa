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
def get_baidu_info(urls, count, website, writer, url_cnt=10, max_cnt= 10, start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):
    try:
        response = urlopen(urls)
        if response == None:
            return "网页未获取"
        data = response.read().decode()
        html = etree.HTML(data,etree.HTMLParser(encoding='utf8'))
        for i in range(url_cnt):
            count[0] += 1
            print(count)
            #print('\n')
            #print('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/div/span[2])')
            time = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/div/span[2])')
            print(time)
            if len(time) == 0:
                    time = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/div/span[2])')
                    print(time)
            if time:
                time = time_check(time)
            else:
                time = DEFAULT_END_TIME.strftime('%Y-%m-%d')     
            if time:
                title = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/h3/a)')
                print(title)
            
                url = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/h3/a/@href)')
                
                print(url)
                # text为摘要
                text = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/span)')
                #无配图的另一种情况
                if len(text) == 0:
                    text = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/span)')

                # info为正文
                info_url = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div[2]/a/@href)')
                if len(info_url) == 0:
                    info_url = html.xpath('string(//*[@id="'+ str(count[0]) +'"]/div/div/div/a/@href)')
                info = ''
                print("URL: "+info_url)
                sleep(3)
                if (website == websites.bajiahao):
                    if info_url:
                        info = baijiahao_info(info_url)
                    #file.write('百家号\n')
                    else: 
                        info = text
                    if info:
                        write_csv(writer, ['百家号', time, info, title, url])
                    else:
                        write_csv(writer, ['百家号', time, text, title, url])

                elif(website == websites.qq):
                    if info_url:
                        info = qq_info(info_url)
                    else: 
                        info = text
                    #file.write('腾讯新闻\n')
                    if info:
                        write_csv(writer, ['腾讯新闻', time, info, title, url])
                    else:
                        write_csv(writer, ['腾讯新闻', time, text, title, url])

                elif(website == websites.people):
                    if info_url:
                        info = people_info(info_url)
                    else: 
                        info = text
                    #file.write('人民网\n')
                    if info:
                        write_csv(writer, ['人民网', time, info, title, url])
                    else:
                        write_csv(writer, ['人民网', time, text, title, url])

                elif(website == websites.fenghuang):
                    if info_url:
                        info = fenghuang_info(info_url)
                    else: 
                        info = text
                    #file.write('凤凰网\n')
                    if info:
                        write_csv(writer, ['凤凰网', time, info, title, url])
                    else:
                        write_csv(writer, ['凤凰网', time, text, title, url])

                elif(website == websites.huanqiu):
                    if info_url:
                        info = huanqiu_info(info_url)
                    else: 
                        info = text
                    #file.write('环球网\n')
                    if info:
                        write_csv(writer, ['环球网', time, info, title, url])
                    else:
                        write_csv(writer, ['环球网', time, text, title, url])
                
                elif(website == websites.xinhua):
                    if info_url:
                        info = xinhua_info(url) 
                    else: 
                        info = text    
                    #file.write('新华社\n')
                    if info:
                        write_csv(writer, ['新华社', time, info, title, url])       
                    else:
                        write_csv(writer, ['新华社', time, text, title, url])     

                #file.write(time+'\n')
                #file.write(title+'\n')
                #file.write(text+'\n')
                #file.write(info+'\n')

                
                #print(text)
            else:
                print("时间结束")
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
                get_baidu_info(next_url, count, website, writer, url_cnt, max_cnt, start_time, end_time)    
    except error.URLError as e:
        pass            


# 爬取百度驱动函数
def baidu_crawl(keys, website='', url_cnt=10, max_cnt= 10,start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):

    url_key = quote(keys, encoding='utf8')
    #url_key = keys
    count = [0]
    i = 0

    filename = keys + website + ".tmp"
    f = open(filename, "w+", encoding='utf-8')
    writer = csv.writer(f)
    #write_csv(writer)

    search_result_url = r"http://www.baidu.com/s?rtt=4&bsst=1&cl=2&tn=news&ie=utf-8&word=" + url_key + website
    print (search_result_url)
    sleep(random.random()*8)
    get_baidu_info(search_result_url, count, website, writer, url_cnt, max_cnt, start_time, end_time)
    
    f.close()



'''正文获取'''
def baijiahao_info(url):
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read()
    html = etree.HTML(data)
    text = html.xpath('string(//*[@id="article"]/div)')
    text = tool.clean(text)
    print(text)
    return text  

def qq_info(url):
    if "cache.baiducontent.com" in url:
        response = urlopen(url)
        if response == None:
            return "网页未获取"
        data = response.read()
        html = etree.HTML(data)
        text = html.xpath('string(/html/body/div[4]/div/div/div[3]/div/div[2]/div[2]/div[1])')
        if len(text) == 0:
            text = html.xpath('string(//*[@id="article_body"])')
        text = tool.clean(text)
        print(text)

        return text  
    else:  
        response = urlopen(url)
        if response == None:
            return "网页未获取"
        data = response.read().decode('gbk', 'ignore')
        html = etree.HTML(data)  
        text = html.xpath('string(/html/body/div[3]/div[1]/div[1]/div[2])')
        text = tool.clean(text)
        print(text)

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

    return text

def fenghuang_info(url):

    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read()
    html = etree.HTML(data)
    if html.xpath('//*[@id="js_playVideo"]') or html.xpath('//div[@class="vPlayer_zone"]'):
        return "ERROR_NONTEXT"
    text = html.xpath('string(//div[@class="text-3w2e3DBc"])')
    
    text = tool.clean(text)
    print(text)

    return text

def xinhua_info(url):
    response = urlopen(url)
    if response == None:
        return "网页未获取"
    data = response.read().decode('utf','ignore')
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

    return text



def write_csv(file, info = None):
    """将爬取的信息写入csv文件"""
    try:
        result_headers = [
            'source',           #来源
            'public_time',      #发布时间
            'content',          #正文
            'topic',            #标题
            'url',              #网页链接
        ]
        if info == None:
            file.writerows([result_headers])
        else:
            file.writerows([info])   
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()
    

if __name__ == "__main__":
    baidu_crawl("元旦", websites.huanqiu)
    #time_check("2020年12月29日 17:28")
    # get_baidu_info_keys("https://baidu.baidu.com/p/6862614326")
