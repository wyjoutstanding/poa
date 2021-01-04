# 网页去重工具--布隆过滤器 安装命令: pip install pybloom_live
from pybloom_live import ScalableBloomFilter, BloomFilter


# 可自动扩容的布隆过滤器
bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)
#####################################
## 博隆过滤器使用方法 ##
# url1 = 'http://www.baidu.com'
# url2 = 'http://qq.com'
#
# bloom.add(url1) # 添加 url
#
# url in bloom 即可判断 url 是否重复
# print(url1 in bloom)
# print(url2 in bloom)
#####################################

DEFAULT_START_TIME = datetime.now() - timedelta(days=30)
DEFAULT_END_TIME = datetime.now()