# coding: utf-8
# python爬取贴吧, 字符为GBK

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
# 正则操作库
import re

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


# 处理页面标签类


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
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()


# 定义全局工具类tool
tool = Tool()


# 得到帖子标题
def get_tieba_title(html):
    # 提取每条结果的标题
    pattern_title = re.compile(
        '<h3 class="core_title_txt pull-left text-overflow(.*?)</h3>', re.S)
    item_title = re.search(pattern_title, html)
    if item_title:
        # print (tool.replace(item_title.group(0)))
        return tool.replace(item_title.group(0))

    else:
        return

# 获取帖子路径


def get_tieba_herf(html):
    # 提取每条结果的url
    pattern_herf = re.compile('href="(.*?)"', re.S)
    item_herf = re.search(pattern_herf, html)
    if item_herf:
        item_herf = tool.replace(item_herf.group(0))
        item_herf = re.sub(r"href=", "", item_herf)
        item_herf = re.sub(r'"', "", item_herf)
        item_herf = r"https://tieba.baidu.com"+item_herf
        if item_herf in bloom:
            return
        bloom.add(item_herf)
        # print (item_herf)

        return item_herf
    else:
        return

# 获取帖子楼主


def get_tieba_author(html):
    pattern_author_div = re.compile(
        '<div class="louzhubiaoshi_wrap">(.*?)</ul>', re.S)
    pattern_author = re.compile('<li class="d_name"(.*?)</li>', re.S)
    #
    item_author = re.search(pattern_author_div, html)
    if item_author:
        item_author = re.search(pattern_author, item_author.group())
    if item_author:
        # print("楼主:")
        # print(tool.replace(item_author.group()))

        return tool.replace(item_author.group())
    else:
        return

# 获取回复数


def get_tieba_replay_num(html):
    pattern_reply_num = re.compile(
        '<li class="l_reply_num" (.*?)</span>页</li>')
    item_replay_num = re.search(pattern_reply_num, html)
    if item_replay_num:
        # print("回复数:")
        item_replay_num = tool.replace(item_replay_num.group(0))
        item_replay_num = re.sub('回.*$', "", item_replay_num)
        # print(item_replay_num)

        return item_replay_num
    else:
        return
# 获取主楼内容


def get_tieba_firstfloor(html):
    pattern_firstfloor = re.compile(
        '<div class="d_post_content_main(.*?)d_post_content_firstfloor">(.*?)</cc>', re.S)
    pattern_firstfloor_true = re.compile('<div id="post_content_(.*?)</div>')

    # 获取主楼内容
    item_firstfloor = re.search(pattern_firstfloor, html)
    if item_firstfloor:
        # print("内容:")
        item_firstfloor = re.search(
            pattern_firstfloor_true, item_firstfloor.group())
        if item_firstfloor:
            item_firstfloor = tool.replace(item_firstfloor.group())
            # print(item_firstfloor)
            return item_firstfloor

# 获取时间戳


def get_tieba_date(html, start_time, end_time):
    pattern_date = re.compile('<font class="p_green p_date.*$', re.S)
    item_date = re.search(pattern_date, html)
    # print (item_date)
    if item_date:
        return date_judge(tool.replace(item_date.group()), start_time, end_time)


def date_judge(date, start_time, end_time):
    date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    if date >= start_time and date <= end_time:
        # print(date)
        return date
    else:
        return

# 提取搜索结果页中子链接
def get_tieba_sraech_result_url(keys, count, search_result_url, out, start_time, end_time):
    # 打开链接
    global issuseCount
    try:
        response = urlopen(search_result_url)
        if response == None:
            issuseCount = issuseCount + 1
            return

        # 匹配每条结果
        pattern_div = re.compile(
            '<div class="s_post">(.*?)</font>        </div>', re.S)

        result = re.findall(pattern_div, response.read().decode('gbk'))
        if result:
            for item in result:
                #sleep(3)
                if count[0] == 0:
                    print("贴吧线程阻塞")
                    sleep(3)
                    return
                outkeys = {}
                outkeys['topic'] = keys
                item_date = get_tieba_date(item, start_time, end_time)

                if item_date:
                    outkeys['public_time'] = item_date
                    item_herf = get_tieba_herf(item)
                    if item_herf:
                        outkeys['source'] = item_herf
                        
                        #print ( item_herf)

                        randdom_header = random.choice(my_headers)
                        req=Request(item_herf) 
                        req.add_header("User-Agent",randdom_header) 
                        req.add_header("GET",item_herf) 

                        get_tieba_info_keys(req, outkeys)
                        # print(str(i)+"###########\n")
                        out.append(outkeys)
                        count[0] = count[0] - 1
                        global num
                        num += 1
                        #print(count[0])
                        #print(outkeys['publisher'])  
                    else:
                        issuseCount = issuseCount + 1
            # return result.group(1).strip()
        else:
            return None
    except error.URLError as e:
        print(e.reason)
        #count[0] == 0
        #sleep(60)

        issuseCount = 10
        return


def get_tieba_info_keys(herf, outkeys):
    response = urlopen(herf)
    html = response.read().decode('utf-8')
    item_title = get_tieba_title(html)
    if item_title:
        outkeys['theme'] = item_title
        print(item_title)
    item_author = get_tieba_author(html)
    if item_author:
        outkeys['publisher'] = item_author
    item_replay_num = get_tieba_replay_num(html)

    item_firstfloor = get_tieba_firstfloor(html)
    if item_firstfloor:
        outkeys['content'] = item_firstfloor


# 爬取贴吧调用函数
def tieba_crawl(keys, url_cnt=10, start_time=DEFAULT_START_TIME,
                end_time=DEFAULT_END_TIME):

    url_key = quote(keys, encoding='gbk')
    count = [url_cnt]
    i = 0
    j = 0
    out = []

    search_result_url = r"https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=" + \
        url_key + r"&un=&rn=20&pn=" + str(i) + r"&sd=&ed=&sm=1&only_thread=1"
    while True:
        if get_tieba_sraech_result_url(keys, count, search_result_url, out, start_time, end_time) == None:
            global issuseCount
            #print("异常事件"+str(issuseCount))
            if issuseCount == 10:
                issuseCount = 0
                break
            elif count[0] == 0:
                    issuseCount = 0
                    count[0] = url_cnt
                    print("贴吧爬取 第{}轮结束".format(str(j)))
                    j = j + 1
            else:
                i = i + 1

        search_result_url = r"https://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=" + \
            url_key + r"&rn=20&un=&only_thread=1&sm=1&sd=&ed=&pn=" + str(i)

    print("爬取结束,共爬取" + str(num))
    # processing
    return out


if __name__ == "__main__":
    tieba_crawl("美国大选")
    # get_tieba_info_keys("https://tieba.baidu.com/p/6862614326")
