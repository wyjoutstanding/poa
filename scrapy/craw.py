import  threading
from Spider.TieBa import tieba_crawl
from Spider.WeiBo import sina_crawl
from Spider.ZhongQing import youth_crawl




class MyThread(threading.Thread):

    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

# 爬取所有数据的接口
def craw_data(key):
    out = []

    t = []
    t.append( MyThread(tieba_crawl, args=(key,10)) )
    t.append( MyThread(youth_crawl, args=(key,10)) )
    t.append( MyThread(sina_crawl, args=(key,4)) )
    
    for ti in t:
        ti.start()

    for ti in t:
        ti.join()
        out.append(ti.get_result())
        print( ti.get_result())
        print("_______________________________________")
    
    return out

if __name__ == "__main__":
    key = input("关键词: ")

    out = []

    t = []
    t.append( MyThread(tieba_crawl, args=(key,10)) )
    t.append( MyThread(youth_crawl, args=(key,10)) )
    t.append( MyThread(sina_crawl, args=(key,4)) )
    

    for ti in t:
        ti.start()

    for ti in t:
        ti.join()
        print( ti.get_result())
        print("_______________________________________")


    
