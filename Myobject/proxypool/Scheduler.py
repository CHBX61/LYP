import time
from multiprocessing import Process
from threading import Thread
import aiohttp
from Myobject.proxypool.setttings import *

import asyncio
from Myobject.proxypool.db import Reids_Client
from Myobject.proxypool.getter import FreeProxyGetter

class VaildityTester(object):
    def __init__(self):
        #篮子
        self._raw_proxies = []

    #向篮子放东西
    def set_raw_proxies(self,proxies):
        self._raw_proxies = proxies
        # 数据的所有连接，用的时候在创建。
        self._conn = Reids_Client()
    #校验代理，要使用异步 请求
    async def test_single_proxy(self,proxy):
        try:
            # 创建一个session对象
            # session = aiohttp.ClientSession()
            async with aiohttp.ClientSession() as session:
                # 参数校验,如果proxy参数是一个bytes类型，就给他转成字符串
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                try:
                    async with session.get(TSET_API,
                                           headers=TEST_REQUEST_HEADERS,
                                           proxy=real_proxy,
                                           timeout=TSET_TIME_OUT) as response:
                        if response.status == 200:
                            # 该代理可用
                            # 添加到代理池
                            self._conn.put(proxy)
                            print('有效代理！', proxy)
                except Exception:
                    print('无效代理！',proxy)
        except Exception as e:
            print(e)
    #校验器的校验方法
    def test(self):
        print('代理池开始启动！')

        #创建一个loop（任务执行链）
        loop = asyncio.get_event_loop()
        #执行任务
        tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
        #启动loop
        loop.run_until_complete(asyncio.wait(tasks))

#添加器
class PoolAdder(object):
    #threshold--阈值--代理池最大值
    def __init__(self,threshold):
        self._threshold = threshold
        #校验
        self._tester = VaildityTester()
        #db
        self._conn = Reids_Client()
        self._crawler =FreeProxyGetter()
    #判断代理池数量是否达到最大值
    def is_over_threshold(self):
        '''

        :return: True:达到 False不能
        '''
        if self._conn.queue_len>=self._threshold:
            return True
        return False
    #添加代理到代理池的方法
    def add_to_queue(self):
        #代理的获取是从getter组件组件中获取的。
        print('添加器开始工作....')
        while True:
            #当添加到代理池数量达到最大值，就不添加了。
            if self.is_over_threshold():
                break
            proxy_count = 0
            #1、先从网上获取免费代理
            #问题：现在只能调用单一的爬取代理的方法，无法从各个网站都获取代理
            #如何实现？
            # for crawl in [crawl_ip3366,crawl_66ip]:
            # proxies  = self._crawler.crawl_ip3366()
            for crawl_name in self._crawler.__CrwalFunc__:
                try:
                    proxies = self._crawler.get_raw_proxies(crawl_name)
                    # 2、调度校验器校验
                    self._tester.set_raw_proxies(proxies)
                    self._tester.test()
                    proxy_count += len(proxies)

                except Exception:
                    print(crawl_name,'该网站异常！')
                    pass


            if proxy_count==0:
                print('所有的代理网站都是异常！请求更换代理网站')


class Scheduler(object):
    @staticmethod
    def vaild_proxy(cycle = CYCLE_VALID_TIME):
        conn = Reids_Client()
        tester = VaildityTester()
        while True:
            print('循环校验器开始启动！')
            count = int(conn.queue_len*0.5)
            if count ==0:
                print('代理池数量不足！正在添加...')
                time.sleep(cycle)
            #从代理池头部取出count个代理，进行校验
            raw_proxies = conn.get(count)
            #调用校验器
            # 2.1先把代理放到篮子
            tester.set_raw_proxies(raw_proxies)
            # 2.2test方法就自动从篮子中获取代理校验
            tester.test()
            time.sleep(cycle)
    @staticmethod
    def check_pool_add(lower_threshold = LOWER_THRESHOLD,
                       upper_threshold = UPPER_THRESHOLD,
                       cycle=CYCLE_CHECK_TIME):
        conn = Reids_Client()
        adder = PoolAdder(upper_threshold)
        while True:
            #如果代理池数量小于最小值，调用添加器添加
            if conn.queue_len<lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)
    def run(self):
        vaild_process =Process(target=Scheduler.vaild_proxy)
        check_process =Process(target=Scheduler.check_pool_add)
        vaild_process.start()
        check_process.start()
