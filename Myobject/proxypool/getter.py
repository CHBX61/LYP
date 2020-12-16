import requests
from lxml import etree
#元类：创建类的类
#类：创建对象的类
#python中可以通过两种方法创建类
#第一种：class关键字
#第二种：type(
#       name,#类的名称
#       bases,#继承的元组
#       attrs)#属性字典
#type是Python提供给我们的唯一元类。
#一个类在实例化的时候：A()
#__new__:创建类
#__init__：创建对象

class ProxyMetaclass(type):
    def __new__(cls, name,bases,attrs):
        # print('元类启动！')
        # print('attr1:',attrs)
        #创建一个属性，这个属性是一个list，里面存放的是所有爬取免费代理方法的方法名字。
        attrs['__CrwalFunc__'] = []
        count = 0
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrwalFunc__'].append(k)
                count +=1
        attrs['__CrwalCount__'] = count
        # print('attrs2',attrs)
        return type.__new__(cls,name,bases,attrs)


class FreeProxyGetter(object,metaclass=ProxyMetaclass):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    }
    def get_raw_proxies(self,callback):
        '''

        :param callback: crawl_66ip
        :return:
        '''
        '''
        通过传入一个字符串的方法名，来调用这个方法，获取代理
        :param callback: 方法名的字符串格式--crawl_66ip
        :return: list-->代理
        '''
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
        # for proxy in self.crawl_66ip():
            proxies.append(proxy)
        return proxies

    #爬取代理方法，名称统一为crawl_
    def crawl_66ip(self):
        '''
        url:http://www.66ip.cn/
        :return:list[proxy]
        '''
        proxies = []
        base_url = 'http://www.66ip.cn/%s.html'
        for i in range(1, 20):
            response = requests.get(base_url % i, headers=self.headers)
            html = etree.HTML(response.text)
            ips = html.xpath('//tr[position()>1]/td[1]/text()')
            ports = html.xpath('//tr[position()>1]/td[2]/text()')
            if len(ips) == len(ports) and ips and ports:
                for i, ip in enumerate(ips):
                    port = ports[i]
                    # print(ip,port)
                    # proxies.append(ip.strip()+':'+port.strip())
                    yield ip.strip()+':'+port.strip()
        # return proxies
    def crawl_ip3366(self):
        '''
       url:http://www.ip3366.net/?stype=1&page=1
       :return:list[proxy]
       '''
        proxies = []
        base_url = 'http://www.ip3366.net/?stype=1&page=%s'
        for i in range(1, 11):
            response = requests.get(base_url % i, headers=self.headers)
            html = etree.HTML(response.text)
            ips = html.xpath('//tr/td[1]/text()')
            ports = html.xpath('//tr/td[2]/text()')
            if len(ips) == len(ports) and ips and ports:
                for i, ip in enumerate(ips):
                    port = ports[i]
                    # print(ip,port)
                    # proxies.append(ip.strip()+':'+port.strip())
                    yield ip.strip() + ':' + port.strip()
        # return proxies
if __name__ == '__main__':
    f = FreeProxyGetter()
    print(dir(f))
    # print(f.__CrwalFunc__)
    # print(f.crawl_66ip())
    # f.crawl_ip3366()