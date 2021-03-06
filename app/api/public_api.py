# -*- coding: utf-8 -*-

from flask import request, Blueprint, json
import functools

# from flask import flash
from flask import g
# from flask import render_template
from flask import session

import sys
sys.path.append("..")
sys.path.append("../craw/")
sys.path.append("../craw/Spider/")
# from config import *
import config as cfg

from craw.craw import craw_start, craw_topTen
# CSV_FILENAME_BAIDU = cfg.get_value("CSV_FILENAME_BAIDU", DEFAULT)
# CSV_FILENAME_HOTSPOT = cfg.get_value('CSV_FILENAME_HOTSPOT', DEFAULT)
# CSV_FILENAME_WEIBO = cfg.get_value("CSV_FILENAME_WEIBO", DEFAULT)

from analysis import data_analysis, bd_analysis
# module manage: buleprint
api_bp = Blueprint("api_bp", __name__, url_prefix="/api")


@api_bp.route('/hello/')
def hello_word():
    return 'hello world!'

global DEFAULT
DEFAULT = '科比'

def update_filename_path(key):
    DIR = cfg.get_value('CSV_FILENAME_BAIDU_DIR', 'NULL')
    cfg.set_value('CSV_FILENAME_BAIDU', DIR + key + '.csv')
    DIR = cfg.get_value('CSV_FILENAME_HOTSPOT_DIR', 'NULL')
    cfg.set_value('CSV_FILENAME_HOTSPOT', DIR + key + '_TOP10.csv')
    DIR = cfg.get_value('CSV_FILENAME_WEIBO_DIR', 'NULL')
    cfg.set_value('CSV_FILENAME_WEIBO', DIR + key + '_WEIBO.csv')

@api_bp.route('/search/', methods=['POST'])
def search_theme():
    '''
    搜索接口
    输入参数：
        @keywords：关键字
        @categories：类别
        @bgn_time: 开始时间
        @end_time: 结束时间
    '''
    if request.method == 'POST':
        # json_data = json.loads(request.data)
        # print(type(request.json))
        # 获取josn格式的数据
        json_data = request.json

        keywords = json_data.get('keywords')
        categories = json_data.get('categories')
        bgn_time = json_data.get('bgn_time')
        end_time = json_data.get('end_time')

        print(keywords, categories, bgn_time, end_time)
        # if cfg.get_value("KEYWORDS", "") != "":
        cfg.set_value('KEYWORDS', keywords)
        print('craw_topTen')
        # print(cfg.get_value('KEYWORDS'), cfg._global_dict)
        global DEFAULT
        DEFAULT = cfg.get_value('DEFAULT_NAME')
        KEYWORD_LIST = cfg.get_value('KEYWORD_LIST', [DEFAULT])

        print('[search KEYWORD_LIST]: ', KEYWORD_LIST)

        update_filename_path(keywords)

        if not keywords in KEYWORD_LIST:
            craw_topTen(keywords)
            print("-----CRAW TOPTEN------")


        return get_hotspot()
    else:
        return 'api_search_theme error'

@api_bp.route('/set_craw_start/')
def set_craw_start():
    DEFAULT = cfg.get_value('DEFAULT_NAME')
    KEYWORDS = cfg.get_value('KEYWORDS', DEFAULT)
    update_filename_path(KEYWORDS)

    print('set_craw_start=', KEYWORDS, cfg._global_dict)
    KEYWORD_LIST = cfg.get_value('KEYWORD_LIST', [DEFAULT])
    if not KEYWORDS in KEYWORD_LIST:
        craw_start(KEYWORDS)
    return "Start Craw OK"

@api_bp.route('/get_hotspot/')
def get_hotspot():
    '''
    返回热点消息列表：{url,summary}
    '''
    # test_data = {"hotspot": [{"url":"http://www.baidu.com", "summary":"热点时间列表"}, {"url":"http://www.baidu.com", "summary":"热点时间列表"}]}
    # test_data = {"url":['url1', 'url2'], "summary":['text1', 'text2']}
    CSV_FILENAME_HOTSPOT = cfg.get_value('CSV_FILENAME_HOTSPOT', DEFAULT)
    topic, url, summary = data_analysis.stat_hotspot(CSV_FILENAME_HOTSPOT)
    data = []
    for i in range(len(url)):
        data.append({
            "topic" : topic[i],
            "summary" : summary[i],
            "url": url[i]
        })
    # data = {
    #     "topic" : topic,
    #     "url": url,
    #     "summary": summary
    # }
    return json.dumps(data)

@api_bp.route('/get_ranking_list/')
def get_ranking_list():
    '''
    获取热搜排行榜

    '''
    # data = {
    #     "title" : ['坚守岗位过元旦', "欢庆元旦 祝福新年", "这个元旦，我们守望平安！", "新疆：元旦佳节 官兵迎风踏雪巡逻在祖国边陲",
    #     "中国元旦节都有哪些习俗", "元旦的来历及习俗 人民是怎样庆祝这个节日", "古诗里的元旦节"],
    #     "hot_value" : ['99', '89', "80", "78", "76", "75", "74"]
    # }
    CSV_FILENAME_BAIDU = cfg.get_value("CSV_FILENAME_BAIDU", DEFAULT)
    print('===ranking_list====', CSV_FILENAME_BAIDU)
    title, hot_value = data_analysis.stat_ranking_list(CSV_FILENAME_BAIDU)

    data = {"title" : title, "hot_value": hot_value}
    return json.dumps(data)

@api_bp.route('/get_website_hotspot/')
def get_website_hotspot():
    '''
    获取网站热度排行榜
    统计每个网站所爬取的网页数量
    '''
    # data = {
    #     "website" : ['人民网', "腾讯网", "军事网", "微博"],
    #     "hot_value" : ['99', '89', "80", "78"]
    # }
    CSV_FILENAME_BAIDU = cfg.get_value("CSV_FILENAME_BAIDU", DEFAULT)
    print('===website_hotspot====', CSV_FILENAME_BAIDU)
    website, hot_value = data_analysis.stat_websites_hotspot(CSV_FILENAME_BAIDU)
    # data = {"name" : website, "value" : hot_value}
    data = {"website" : website, "hot_value" : hot_value}
    return json.dumps(data)

@api_bp.route('/get_sentiment/')
def get_sentiment():
    '''
    情感分析结果
    0:负向，1:中性，2:正向
    '''
    CSV_FILENAME_BAIDU = cfg.get_value("CSV_FILENAME_BAIDU", DEFAULT)
    data = bd_analysis.stat_sentiment(CSV_FILENAME_BAIDU)
    trans = {0:"消极", 1:"中立", 2:"积极"}
    ret_data = {}
    for (k,v) in data.items():
        ret_data[trans[k]] = v
    return json.dumps(ret_data)

class jsonObj:
    def __init__(self, name, value):
        self.name = name
        self.value = value

@api_bp.route('/get_word_cloud/')
def get_word_cloud():
    '''
    获取话题关键词云
    先NLP抽取关键词，再统计词频
    '''
    data = []
    # for i in range(5):
    #     data.append(jsonObj("关键词"+str(i), str(i)).__dict__)
    CSV_FILENAME_BAIDU = cfg.get_value("CSV_FILENAME_BAIDU", DEFAULT)
    tags, values = bd_analysis.stat_keyword(CSV_FILENAME_BAIDU)

    for i in range(len(tags)):
        # data.append(jsonObj(tags[i], str(values[i])).__dict__)
        data.append({"name": tags[i], "value": values[i]})
    # data = {
    #     'x':['2020-02-08','2020-04-09'],
    #     'y':[10,99]
    # }

    return json.dumps(data)

@api_bp.route('/get_weibo_data/')
def get_weibo_data():
    '''
    获取微博数据：转发，评论，点赞，拉踩量
    '''
    # data = []
    # for i in range(5):
    #     data.append(jsonObj("微博分析量关键词"+str(i), str(i)).__dict__)
    # data = {
    #     'x':['2020-02-08','2020-04-09'],
    #     'y':[10,99]
    # }
    CSV_FILENAME_WEIBO = cfg.get_value("CSV_FILENAME_WEIBO", DEFAULT)
    up_num, retweet_num, comment_num, stamp_num = data_analysis.stat_weibo_data(CSV_FILENAME_WEIBO)

    data = {
        "点赞量": up_num,
        "转发量": retweet_num,
        "评论量": comment_num,
        "拉踩量": stamp_num
    }
    return json.dumps(data)


@api_bp.route('/get_analysis_data/')
def get_analysis_data():
    '''
    返回分析数据
    '''
    x, y  = data_analysis.get7days()
    data = {"total_hotspot_change":{'x':x, 'y':y}}
    return json.dumps(data)

@api_bp.route('/get_report/')
def get_report():
    '''
    返回简报
    '''
    pass
# @auth_bp.route('/login/', methods=['POST'])
# def login():
#     print("hello")
#     username = request.form.get('username')
#     password = request.form.get('password')
#     # print(username, password)
#     return username+password




# # decorator: https://www.runoob.com/w3cnote/python-func-decorators.html
# # *args,**kwargs: https://www.cnblogs.com/cwind/p/8996000.html
# def login_required(view):
#     """View decorator that redirects anonymous users to the login page."""

#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             # return redirect(url_for("auth.login"))
#             pass

#         return view(**kwargs)

#     return wrapped_view



# # reference url: https://www.cnblogs.com/zhangjunkang/p/10240270.html
# # this function will be execute before any requests
# @auth_bp.before_app_request
# def load_logged_in_user():
#     """If a user id is stored in the session, load the user object from
#     the database into ``g.user``."""
#     user_id = session.get("user_id")

#     if user_id is None:
#         # g only valid in current request
#         g.user = None
#     else:
#         pass
#         # g.user = (
#         #     get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
#         # )


# @auth_bp.route("/register/", methods=("GET", "POST"))
# def register():
#     """Register a new user.

#     Validates that the username is not already taken. Hashes the
#     password for security.
#     """
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # db = get_db()
#         error = None

#         if not username:
#             error = "Username is required."
#         elif not password:
#             error = "Password is required."
#         # elif (
#         #     # db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
#         #     # is not None
#         #     pass
#         # ):
#         #     error = f"User {username} is already registered."

#         if error is None:
#             # the name is available, store it in the database and go to
#             # the login page
#             # db.execute(
#             #     "INSERT INTO user (username, password) VALUES (?, ?)",
#             #     (username, generate_password_hash(password)),
#             # )
#             # db.commit()
#             # return redirect(url_for("auth.login"))
#             pass

#         # flash(error)

#     # return render_template("auth/register.html")
#     return 'register success'


# @auth_bp.route("/login/", methods=("GET", "POST"))
# def login():
#     """Log in a registered user by adding the user id to the session."""
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         # db = get_db()
#         error = None
#         # user = db.execute(
#         #     "SELECT * FROM user WHERE username = ?", (username,)
#         # ).fetchone()

#         # if user is None:
#         #     error = "Incorrect username."
#         # elif not check_password_hash(user["password"], password):
#         #     error = "Incorrect password."

#         # if error is None:
#         #     # store the user id in a new session and return to the index
#         #     session.clear()
#         #     session["user_id"] = user["id"]
#         #     return redirect(url_for("index"))

#         # flash(error)

#     # return render_template("auth/login.html")
#     return 'login success'


# @auth_bp.route("/logout/")
# def logout():
#     """Clear the current session, including the stored user id."""
#     session.clear()
#     # return redirect(url_for("index"))
#     return 'logout success'
