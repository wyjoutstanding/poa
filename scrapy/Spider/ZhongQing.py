# -*- coding: utf-8 -*-
# 日期时间
from datetime import datetime, timedelta
# 网页去重工具--布隆过滤器 安装命令: pip install pybloom_live
#from pybloom_live import ScalableBloomFilter, BloomFilter

import urllib.request
import re
import numpy as np
from urllib.parse import quote, unquote

class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self. removeImg, "", x)
        x = re.sub(self. removeAddr, "", x)
        x = re.sub(self. replaceLine, "", x)
        x = re.sub(self. replaceTD, "\t", x)
        x = re.sub(self. replacePara, "", x)
        x = re.sub(self. replaceBR, "", x)
        x = re.sub(self. removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

tool = Tool()

# 可自动扩容的布隆过滤器
# bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)
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

def get_page(key):
    # 中青网搜索链接，爬取10个页面，暂取五页的搜索结果
    url1 = 'http://search.youth.cn/cse/search?q=' + key + '&p=0&s=15107678543080134641&sti=43200&entry=1'
    url2 = 'http://search.youth.cn/cse/search?q=' + key + '&p=1&s=15107678543080134641&sti=43200&entry=1'
    url3 = 'http://search.youth.cn/cse/search?q=' + key + '&p=2&s=15107678543080134641&sti=43200&entry=1'
    url4 = 'http://search.youth.cn/cse/search?q=' + key + '&p=3&s=15107678543080134641&sti=43200&entry=1'
    url5 = 'http://search.youth.cn/cse/search?q=' + key + '&p=4&s=15107678543080134641&sti=43200&entry=1'
    # 结果链接正则表达式
    pattern1 = '.*?(http://news.youth.cn/gj.*?.htm).*?'
    # 模拟成浏览器爬取网页 谷歌浏览器
    headers = {'User-Agent',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]

    # 获取结果链接去重
    data = opener.open(url1).read().decode('utf8')
    content_href = re.findall(pattern1, data, re.I)
    urls1 = list(set(content_href))

    data = opener.open(url2).read().decode('utf8')
    content_href = re.findall(pattern1, data, re.I)
    urls2 = list(set(content_href))

    data = opener.open(url3).read().decode('utf8')
    content_href = re.findall(pattern1, data, re.I)
    urls3 = list(set(content_href))

    data = opener.open(url4).read().decode('utf8')
    content_href = re.findall(pattern1, data, re.I)
    urls4 = list(set(content_href))

    data = opener.open(url5).read().decode('utf8')
    content_href = re.findall(pattern1, data, re.I)
    urls5 = list(set(content_href))

    links = urls1 + urls2
    links += urls3
    links += urls4
    links += urls5
    # print(links)
    return links

# 中青网爬取接口：张峥
def youth_crawl(keys, url_cnt=10, start_time=DEFAULT_START_TIME,
end_time=DEFAULT_END_TIME):

    keys = quote(keys, encoding='utf8')

    links = get_page(keys)
    out = []
    i = 0

    # 依次爬取结果链接
    for link in links:
        url = str(link)

        # 定义爬取内容的正则表达式，除正文内容外
        pattern1 = '.*?<title>(.*?)_.*?</title>.*?'
        pattern2 = '.*?发稿时间：(.*[0-9]).*?</span>.*?'
        pattern3 = '.*?<meta name="source" content="(.*?)".*?'
        pattern4 = '.*?<meta name="keywords" content=\'(.*?)\'.*?'
        pattern5 = '.*?<meta name="author" content="(.*?)".*?'

        headers = {'User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        html = opener.open(url).read().decode('gbk')
        # print(html)

        # 依次获取信息：主题、发布时间、来源、话题、作者
        theme = re.findall(pattern1, html, re.I)
        print(theme)

        public_time = re.findall(pattern2, html, re.I)
        # print(public_time)

        source = re.findall(pattern3, html, re.I)
        # print(source)

        topic = re.findall(pattern4, html, re.I)
        # print(topic)

        publisher = re.findall(pattern5, html, re.I)
        # print(publisher)

        # 先缩小范围，再裁取正文内容
        pattern6 = re.compile('发稿时间：.*?<p>(.*?)</div>', re.S)
        pattern7 = re.compile('<p>(.*?)</div>', re.S)
        rang1 = re.search(pattern6, html)
        rang2 = re.search(pattern7, rang1.group())
        content = tool.replace(rang2.group())
        # print(content)

        # 构建关键字列表，并把爬取的数据放在值列表
        keylist = ['source', 'public_time', 'content', 'topic', 'sensitive_word', 'theme', 'publisher']
        valuelist = source
        valuelist += public_time
        valuelist.append(content)
        valuelist += topic
        valuelist.append(keys)
        valuelist += theme
        valuelist += publisher
        # print(valuelist)

        # 将两个列表合并为字典，并将字典加入输出列表
        outdict = dict(zip(keylist, valuelist))
        out.append(outdict)
        i = i + 1
        if i >= url_cnt:
            break

    print(out)
    # processing
    return out

if __name__ == '__main__':
    keyword = input("key:")
    youth_crawl(keyword, url_cnt=10, start_time=DEFAULT_START_TIME,
                 end_time=DEFAULT_END_TIME)
    # people_crawl("abc")
