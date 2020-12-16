import redis
from Myobject.proxypool.setttings import PASSWORD,HOST,PORT,PROXIES
class Reids_Client(object):
    def __init__(self,host=HOST,port = PORT):
        #判断是否有密码：
        if PASSWORD:
            self._db =redis.Redis(host=host,port=port,password=PASSWORD)
        else:
            self._db = redis.Redis(host=host,port=port)
    #将代理添加到代理池的尾部
    def put(self,proxy):
        self._db.rpush(PROXIES,proxy)

    #从头部获取count个代理,并将其删除
    def get(self,count=1):
        #lrange：获取指定范围的内容
        #ltrim :保留指定范围内的内容，其他删除
        proxies = self._db.lrange(PROXIES,0,count-1)
        self._db.ltrim(PROXIES,count,-1)
        return proxies

    #从尾部获取一个最新代理
    def pop(self):
        #从redis中获取处来的数据是bytes
        return self._db.rpop(PROXIES).decode('utf-8')

    #计算代理池长度
    @property
    def queue_len(self):
        return self._db.llen(PROXIES)

    def flush(self):
        self._db.flushall()

if __name__ == '__main__':
    r = Reids_Client()
    print(r.queue_len)