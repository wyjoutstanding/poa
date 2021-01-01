# -*- coding: utf-8 -*-
"""
获取摘要的相关实现模块
"""
from pyhanlp import *

def get_summary(text, num):
    """
    获取指定句子个数的文本摘要
    Args
        @text 文本
        @num  句子个数
    Return 
        文本摘要
    """
    # 加载模型
    TextRankSentence = JClass("com.hankcs.hanlp.summary.TextRankSentence")
    # 抽取摘要
    sentence_list = HanLP.extractSummary(text, num)
    # 返回摘要
    return str(sentence_list)[1:-1]

def read_text(filename, num):
    """
    从指定文件读取num条数据: (url,text)
    若文件总数目小于num，则返回整个文件
    """
    url_list  = []
    text_list = []
    with open(filename, 'r') as f:
        for i in range(num):
            url = f.readline()
            text = f.readline()
            print(url)
            if url == "" or text == "":
                break
            print(text, len(text))
            if (len(text) < 10):
                continue
            url_list.append(url.strip())
            text_list.append(text.strip())

    return url_list, text_list

def get_summary_lists(filename, num):
    """
    获取(url,summary)列表的接口
    """
    # 从文件读取数据
    url_list, text_list = read_text(filename, num)

    summary_list = []
    
    # 抽取摘要
    for text in text_list:
        summary_list.append(get_summary(text, 3))
    
    return url_list, summary_list


if __name__ == "__main__":
    document = '''水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，
     根据刚刚完成了水资源管理制度的考核，Test有部分省接近了红线的指标，
     有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，
     严格地进行水资源论证和取水许可的批准。
    '''
    # demo_summary(document)
    # print(get_summary(document, 3))
    # print(read_text("baidu.txt",8))
    print(get_summary_lists("baidu.txt", 8))
    
