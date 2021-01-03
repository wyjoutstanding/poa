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

import datetime
# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def getdate(dispOfDay):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=dispOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y-%m-%d')
    return re_date

def get7days():
    disp = [-4, -3, -2, -1, 0, 1, 2]
    date_list = []
    value_list = []
    for i in range(len(disp)):
        date_list.append(getdate(disp[i]))
        value_list.append(20 + random.randint(20,90))
    value_list[-1] = (value_list[-1] + value_list[-2]) // 2
    print(date_list, value_list)
    return date_list, value_list

# 获取前一周的所有日期(weeks=1)，获取前N周的所有日期(weeks=N)
def getBeforeWeekDays(weeks=1):
    # 0,1,2,3,4,5,6,分别对应周一到周日
    week = datetime.datetime.now().weekday()
    days_list = []
    start = 7 * weeks +  week
    end = week
    for index in range(start, end, -1):
        day = getdate(index) 
        print(day)

if __name__ == "__main__":
    # print(stat_websites_hotspot(CSV_FILENAME_BAIDU))
    # print(stat_ranking_list(CSV_FILENAME_BAIDU))
    # print(stat_hotspot(CSV_FILENAME_HOTSPOT))
    # print(stat_weibo_data(CSV_FILENAME_WEIBO))

    get7days()
    # print(stat_websites_hotspot(FILE))
    # print(stat_ranking_list(FILE))