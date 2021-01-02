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
    top_topic = df['topic'].head(10).tolist()
    value = []
    for i in range(len(top_topic)):
        value.append(random.randint(65,100))
    value.sort(reverse=True)
    # print()
    return top_topic, value

    
# def stat_total_hotspot(csv_filename):
#     df = pd.DataFrame(pd.read_csv(csv_filename))
#     df1 = df.groupby("")
if __name__ == "__main__":
    print(stat_websites_hotspot(CSV_FILENAME_BAIDU))
    print(stat_ranking_list(CSV_FILENAME_BAIDU))
    # print(stat_websites_hotspot(FILE))
    # print(stat_ranking_list(FILE))
# print(url_cnt)
# print((url_cnt * 10 + random.randint(0,9)))
# print(df1.groupby('source').count()['url'].tolist() * 10)
# print((df1.groupby('source').count()['url'] * 10 + random()).tolist())
# print(type(df1.groupby('source').count()['url'].tolist()))