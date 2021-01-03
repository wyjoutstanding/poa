# coding=utf-8

import sys
import json
import base64
import time


# make it work in both python2 both python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# skip https auth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'HDkaKNcmq2rkV3GE3VxeNWyA'

SECRET_KEY = 'YFfyLOpf9Sc1XkGpROFZTSLft1rHGvxP'


COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag"

# 关键词提取
KEYWORD_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    get token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
        print('result_str', result_str)
    except URLError as err:
        print('error===========')
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        print("toens:", result['access_token'])
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    call remote http server
"""
def make_request(url, comment):
    print("---------------------------------------------------")
    print("评论文本：")
    print("    " + comment)
    print("\n评论观点：")

    response = request(url, json.dumps(
    {
        "text": comment,
        # 13为3C手机类型评论，其他类别评论请参考 https://ai.baidu.com/docs#/NLP-Apply-API/09fc895f
        "type": 13
    }))

    data = json.loads(response)

    if "error_code" not in data or data["error_code"] == 0:
        for item in data["items"]:
            # 积极的评论观点
            if item["sentiment"] == 2:
                print(u"    积极的评论观点: " + item["prop"] + item["adj"])
            # 中性的评论观点
            if item["sentiment"] == 1:
                print(u"    中性的评论观点: " + item["prop"] + item["adj"])
            # 消极的评论观点
            if item["sentiment"] == 0:
                print(u"    消极的评论观点: " + item["prop"] + item["adj"])
    else:
        # print error response
        print(response)

    # 防止qps超限
    time.sleep(0.5)

"""
    call remote http server
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

def test_comment_tag():

    comment1 = "手机已经收到，非常完美超出自己的想象，外观惊艳 黑色高端加外形时尚融为一体比较喜欢的类型。系统流畅优化的很好，操作界面简洁大方好上手。电池用量很满意，快充很不错。相机拍人拍物都美。总而言之一句话很喜欢的宝贝。"
    comment2 = "外观精美大小正合适，做工精细，线条流畅，拍照完美，吃鸡最高画质无压力。连续玩了三个小时掉电百分之二十，电池强劲持久，无明显发热，操作流畅，准备再买一台给老婆生日礼物！"
    comment3 = "大家千万不要在上当了，耗电特别快，手机激活后不支持7天无理由退货，请大家小心购买"

    # get access token
    token = fetch_token()

    # concat url
    url = COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token

    make_request(url, comment1)
    make_request(url, comment2)
    make_request(url, comment3)


def get_keywords(url, title, content):

    response = request(url, json.dumps(
    {
        "title": title,
        "content": content 
    }))
    data = json.loads(response)
    if "error_code" not in data or data["error_code"] == 0:
        # print("get_keyword ok")
        pass
        # for item in data["items"]:
        #     print('tag: {}, score: {}'.format(item['tag'], item['score']))
    else:
        # print error response
        print(response)
    
    return data['items']


import pandas as pd
import sys
sys.path.append("..")
from config import *
def stat_keyword():
    # title = "iphone手机出现“白苹果”原因及解决办法，用苹果手机的可以看下"
    # content = "如果下面的方法还是没有解决你的问题建议来我们门店看下成都市锦江区红星路三段99号银石广场24层01室。在通电的情况下掉进清水，这种情况一不需要拆机处理。尽快断电。用力甩干，但别把机器甩掉，主意要把屏幕内的水甩出来。如果屏幕残留有水滴，干后会有痕迹。^H3 放在台灯，射灯等轻微热源下让水分慢慢散去。"

    # token = fetch_token()
    # 30天后重新获取
    token = TOKEN_BAIDU

    url = KEYWORD_URL + "?charset=UTF-8&access_token=" + token

    df = pd.DataFrame(pd.read_csv(CSV_FILENAME_BAIDU))
    titles = df['topic'].tolist()
    contents = df['content'].tolist()

    cnts = {}
    val_cnt = 0
    MAX_CNT = 20
    for i in range(len(titles)):
        if titles[i] == "" or titles[i] == None or contents[i] == "" or contents[i] == None:
            continue
        items = get_keywords(url, titles[i], contents[i])
        val_cnt = val_cnt + 1
        if val_cnt == MAX_CNT:
            break

        for it in items:
            cnts[it['tag']] = cnts.get(it['tag'], 0) + it['score']
        time.sleep(0.4)
        # get_keywords(url, title, content)
    
    # print(cnts.keys(), cnts.values())
    return list(cnts.keys()), list(cnts.values())
    # return cnts
if __name__ == '__main__':
    # cnt = {'A':12, 'B':12}
    # print(list(cnt.keys()))
    stat_keyword()