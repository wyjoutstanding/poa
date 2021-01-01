# # -*- coding:utf-8 -*-
from pyhanlp import *

def get_keyword(content):
    """ 关键词提取

    >>> content = (
    ...    "程序员(英文Programmer)是从事程序开发、维护的专业人员。"
    ...    "一般将程序员分为程序设计人员和程序编码人员，"
    ...    "但两者的界限并不非常清楚，特别是在中国。"
    ...    "软件从业人员分为初级程序员、高级程序员、系统"
    ...    "分析员和项目经理四大类。")
    >>> demo_keyword(content)
    [程序员, 程序, 分为, 人员, 软件]
    """
    # 加载模型
    TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
    # 抽取关键词
    keyword_list = HanLP.extractKeyword(content, 10)
    # print(keyword_list)
    return list(keyword_list)

def get_cnt_keywords(words, cnts):
    for word in words:
        cnts[word] = cnts.get(word, 0) + 1
    
    return cnts

def get_sorted_keyword_frequency_list(words_list, num:int):
    cnts = {}
    for words in words_list:
        cnts = get_cnt_keywords(words, cnts)
    
    items = list(cnts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    print(items)
    return items[0:num]

    
    
if __name__ == "__main__":
    # import doctest
    # doctest.testmod(verbose=True)
    content = """
        程序员(英文Programmer)是从事程序开发、维护的专业人员。
        一般将程序员分为程序设计人员和程序编码人员，
        但两者的界限并不非常清楚，特别是在中国。
        软件从业人员分为初级程序员、高级程序员、系统
        分析员和项目经理四大类。
        """
    data2 = '''程序员分为程序设计人员和程序编码'''
    # print(get_keyword(content))
    cnts = {}
    # print(get_cnt_keywords(get_keyword(content), cnts))
    l1 = get_keyword(content)
    l2 = get_keyword(data2)
    print(get_sorted_keyword_frequency_list([l1,l2],5))