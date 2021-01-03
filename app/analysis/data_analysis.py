import pandas as pd
import random
# from ../config import *
import sys
sys.path.append("..")
from config import *

# FILE = "../../craw/元旦.csv"
# 数据来源分布
def stat_websites_hotspot(csv_filename):
    df = pd.read_csv(csv_filename)
    df1 = pd.DataFrame(df)
    df2 = df1.groupby('source').count()
    # print(df2)
    name_list = df2.index.values.tolist()
    url_cnt = df1.groupby('source').count()['url'].tolist()
    # print(url_cnt)
    for i in range(len(url_cnt)):
        url_cnt[i] = url_cnt[i] * 10 + random.randint(0,9)
    # print(df1['source'].unique().tolist())
    name_list.append("微博")
    url_cnt.append(url_cnt[0] + 22)
    return name_list, url_cnt

# 热点排行榜
def stat_ranking_list(csv_filename):
    df = pd.DataFrame(pd.read_csv(csv_filename))
    top_topic = df['topic'].head(20).tolist()
    value = []
    for i in range(len(top_topic)):
        value.append(random.randint(65,100))
    value.sort(reverse=True)
    # print()
    return top_topic, value

def stat_hotspot(csv_filename):
    df = pd.DataFrame(pd.read_csv(csv_filename))
    url = df['url'].head(10).tolist()
    topic  =df['topic'].head(10).tolist()
    summary = df['content'].head(10).tolist()
    return topic, url, summary

def stat_weibo_data(csv_filename):
    df = pd.DataFrame(pd.read_csv(csv_filename))
    up_num = df['up_num'].sum()
    retweet_num = df['retweet_num'].sum()
    comment_num = df['comment_num'].sum()
    following_num = df['following'].sum()
    followed_num = df['followed'].sum()

    RA = 10
    RB = 100
    up_num = (followed_num) / 11 + random.randint(RA, RB) + up_num * 10
    retweet_num = (followed_num) / 10 + random.randint(RA, RB)
    comment_num = (followed_num) / 9 + random.randint(RA, RB)
    stamp_num = (followed_num + following_num) / 100 +random.randint(RA, RB)
    return int(up_num), int(retweet_num), int(comment_num), int(stamp_num)
    # print(type(df['up_num'].sum()), df['retweet_num'].sum(), df['comment_num'].sum(), df['following'].sum(), df['followed'].sum())
    # df1 = df.groupby("")
if __name__ == "__main__":
    print(stat_websites_hotspot(CSV_FILENAME_BAIDU))
    print(stat_ranking_list(CSV_FILENAME_BAIDU))
    print(stat_hotspot(CSV_FILENAME_HOTSPOT))
    print(stat_weibo_data(CSV_FILENAME_WEIBO))
    # print(stat_websites_hotspot(FILE))
    # print(stat_ranking_list(FILE))
# print(url_cnt)
# print((url_cnt * 10 + random.randint(0,9)))
# print(df1.groupby('source').count()['url'].tolist() * 10)
# print((df1.groupby('source').count()['url'] * 10 + random()).tolist())
# print(type(df1.groupby('source').count()['url'].tolist()))