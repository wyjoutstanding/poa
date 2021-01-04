import csv

def write_csv(file, info = None):
    """将爬取的信息写入csv文件"""
    try:
        result_headers = [
            'source',           #来源
            'public_time',      #发布时间
            'content',          #正文
            'topic',            #标题
            'url',              #网页链接
        ]
        if info == None:
            file.writerows([result_headers])
        else:
            file.writerows([info])   
    except Exception as e:
        print('Error: ', e)
        traceback.print_exc()