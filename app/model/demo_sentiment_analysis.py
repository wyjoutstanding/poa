# -*- coding:utf-8 -*-
# Author: hankcs
# Date: 2019-01-07 13:53

from pyhanlp import *
from test_utility import ensure_data
print("helloworld")
IClassifier = JClass('com.hankcs.hanlp.classification.classifiers.IClassifier')
NaiveBayesClassifier = JClass('com.hankcs.hanlp.classification.classifiers.NaiveBayesClassifier')
# 中文情感挖掘语料-ChnSentiCorp 谭松波
chn_senti_corp = ensure_data("ChnSentiCorp情感分析酒店评论", "http://file.hankcs.com/corpus/ChnSentiCorp.zip")
#  http://file.hankcs.com/corpus/ChnSentiCorp.zip 到 /home/wyj/pyhanlp/pyhanlp/static/data/test/ChnSentiCorp情感分析酒店评论.zip

def predict(classifier, text):
    print("《%s》 情感极性是 【%s】" % (text, classifier.classify(text)))

def get_predict_sentiment(classifier, text):
    return classifier.classify(text)


if __name__ == '__main__':
    classifier = NaiveBayesClassifier()
    #  创建分类器，更高级的功能请参考IClassifier的接口定义
    classifier.train(chn_senti_corp)
    #  训练后的模型支持持久化，下次就不必训练了
    predict(classifier, "前台客房服务态度非常好！早餐很丰富，房价很干净。再接再厉！")
    predict(classifier, "结果大失所望，灯光昏暗，空间极其狭小，床垫质量恶劣，房间还伴着一股霉味。")
    predict(classifier, "可利用文本分类实现情感分析，效果不是不行")
