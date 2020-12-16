#密码：如果为空，就没有密码
PASSWORD = ''
#主机ip和端口号
HOST = 'localhost'
PORT = 6379

#代理池的名称
PROXIES = 'proxies_new'
#测试代理的网址
TSET_API = 'http://www.baidu.com/'
#配置测试网址的请求头
TEST_REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
}
#测试代理的超时时间
TSET_TIME_OUT = 30
#循环校验时间
CYCLE_VALID_TIME = 100
#代理池代理数量的最小值
LOWER_THRESHOLD = 10
#代理池代理的最大值
UPPER_THRESHOLD = 100
#循环检查时间
CYCLE_CHECK_TIME = 100