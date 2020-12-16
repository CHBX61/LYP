"""
-*- coding:utf-8 -*-
@Time : 2020/12/10 0010 20:22
@Author : 陆一平
@File : lianjiapc.py
@Software: PyCharm
"""
import requests
from lxml import etree
import re
import pandas as pd
import time
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    # 'Cookie': 'select_city=510100; lianjia_ssid=c344dd68-1387-43f3-9756-12fc7cdefb65; lianjia_uuid=44c04b6d-0ad4-4d4c-8bb2-3ef6d622ddf4; _smt_uid=5fd20c25.4508b035; UM_distinctid=1764c7f71d015c-085bb76396d615-3b3d5308-15f900-1764c7f71d11a1; CNZZDATA1253492306=46495905-1607601243-https%253A%252F%252Fwww.baidu.com%252F%7C1607601243; CNZZDATA1254525948=1672795922-1607599450-https%253A%252F%252Fwww.baidu.com%252F%7C1607599450; CNZZDATA1255633284=736884263-1607600261-https%253A%252F%252Fwww.baidu.com%252F%7C1607600261; CNZZDATA1255604082=5202409-1607600261-https%253A%252F%252Fwww.baidu.com%252F%7C1607600261; _jzqa=1.4012999721179016000.1607601190.1607601190.1607601190.1; _jzqc=1; _jzqy=1.1607601190.1607601190.1.jzqsr=baidu.-; _jzqckmp=1; _qzja=1.2090439920.1607601189808.1607601189808.1607601189808.1607601189808.1607601189808.0.0.0.1.1; _qzjc=1; _qzjto=1.1.0; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221764c7f740351f-0a4028ab54ba8c-3b3d5308-1440000-1764c7f740454f%22%2C%22%24device_id%22%3A%221764c7f740351f-0a4028ab54ba8c-3b3d5308-1440000-1764c7f740454f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; _ga=GA1.2.333639289.1607601191; _gid=GA1.2.376778721.1607601191; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiOGE2ZGRiNGRhYjU4MWE1YWY2ZjlkOWJjZTQ0NGQzNWUyNTMzMjMyYTdmMDkzMzI4NDAzMjNhZDQzMWFmYjQ2ZmY3NDg2Y2FmOWIzZTQwOTk2Yjc3NWMyZjAyZTRiZTc1MzZlNDUxM2IzNzM4ZmFmMjk2NDE2OTNhOGFiNTU1ZjU4ZTM3NjM0NzAxNmQxMmJjMTRlZGFkOWZkY2E5MDg4Y2ViYjFhZDk2NWJhMTBlN2U3YTMyOTBhMGM2MjAxMmQ0OGYwMDJkNzIxYmQ5M2I2NTk0NjUzNGQzNTVmNjI2Mzc4ZGM4MmJhNTg4M2IzZTgxYTk4YjVlOGEwZjA4Mzk5OWMyMmM4OGJmNDM2ZmVhYTY1MWVhMDUwZGUyMjRmZTZjNDNiMWJiODBjM2Q1Mjg2OGJmYzI0NmFlNmViM2E3ZWRjOWVjZWM4NWQ3MzMwY2I2N2I3ZGY0ZWUwZjY1ZmIwOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIzOTdiZTk0ZlwifSIsInIiOiJodHRwczovL2NkLmxpYW5qaWEuY29tL3p1ZmFuZy9wZzMiLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
    'Host': 'm.lianjia.com',
    'Referer': 'https://cd.lianjia.com/',
}
def parse_url(url):
    html = requests.get(url,headers=headers)
    if html.status_code ==200:
        get_html(html)
    else:
        print(html.status_code)
def get_html(html):
    content = html.text
    soup = etree.HTML(content)
    href = soup.xpath('//div/a[@data-el ="jumpDetailEl"]/@href')
    title = soup.xpath('//div/p[@class="content__item__title"]/text()')
    nerong = soup.xpath('//div/p[@class="content__item__content"]/text()')
    prices = soup.xpath('//div/p[@class="content__item__bottom"]/text()')
    prices = str(prices)
    prices_list = re.findall(r"\d+\.?\d*",prices)
    tag = soup.xpath('//div/p[@class="content__item__tag--wrapper"]')
    biaoqian_list = []
    for t in tag:
        biaoqian = t.xpath('./i/text()')
        tag = '|'.join(biaoqian)
        biaoqian_list.append(tag)
    print(prices_list,href,title,nerong,biaoqian_list)
    downloads(title,nerong,prices_list,href)

def downloads(title,nerong,prices_list,href):
    df = pd.DataFrame()
    df['标题'] = title
    df['内容'] = nerong
    # df['标签'] = biaoqian_list
    df['价格'] = prices_list
    df['链接'] = href
    try:
        df.to_csv("链家广州租房信息.csv", mode="a+", header=None, index=None, encoding="gbk")
        print("写入成功")
    except:
        print("当页数据写入失败")
    time.sleep(1)
if __name__ == '__main__':
    for i in range(1,2):
        url = 'https://cd.lianjia.com/zufang/pg{}'.format(i)
        parse_url(url)