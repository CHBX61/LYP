import requests,re,base64,io
from lxml import etree
from fontTools.ttLib import TTFont
import hashlib
from queue import Queue
import threading
import time,random
import os
from Myobject.excel_utils import write_to_excel,append_to_excel
class AnJuKe():
    def __init__(self):
        self.proxies = self.get_proxies()
        self.ajax_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        # 'cookie': 'login=flase; Hm_lvt_9007fab6814e892d3020a64454da5a55=1604653021,1604664055,1604711185; ASP.NET_SessionId=mi5gzudp2jtxammt0ke31pwd; wxopenid=defoaltid; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1604711960',
    }

    def get_proxies(self):
        '''
        获取代理字典
        :return:
        '''
        try:
            response = requests.get('http://127.0.0.1:5000/get')
            # print(response.text)
            proxies = {
                'https': 'https://' + response.text
            }
            return proxies
        except Exception:
            return None
    def get_xpath(self,url):
        '''
        发送请求，获取
        :param url:
        :return:
        '''
        try:
            print(self.proxies)
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
                # 'cookie': 'login=flase; login=flase; wxopenid=defoaltid; Hm_lvt_9007fab6814e892d3020a64454da5a55=1604653021,1604664055,1604711185,1605251746; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1605251748',
            }
            response = requests.get(url, headers=headers, proxies=self.proxies,timeout = 5)
            # print(response.text)
            page_content = self.base_decode(response.text)
            return page_content
        except Exception as e:
            print(e)
            #获取一个新的代理
            self.proxies = self.get_proxies()
            # time.sleep(1)
            return self.get_xpath(url)

    def base_decode(self,response):
        font_base64 = re.search(r'base64,(.*?)\'\) format',response,re.S).group(1)
        # print(font_base64)
        font_content = base64.b64decode(font_base64)
        font = TTFont(io.BytesIO(font_content))
        with open('font.woff','wb') as f:
            f.write(font_content)
        font.saveXML('font.xml')
        cm = font.getBestCmap()
        # print(cm)
        data = {str(hex(k))[2:]:str(int(v[-2:])-1) for k,v in cm.items()}
        # print(data)
        # print(data.items())
        for k,v in data.items():
            response = response.replace(f'&#x{k};',v)
        return response
    # def get_content(self,url):
    #     headers = {
    #         'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    #         # 'cookie': 'aQQ_ajkguid=74E25070-6792-A444-2851-6C2501857DDE; id58=e87rkF+rhXZn9kGJFcFNAg==; _ga=GA1.2.14466396.1605076322; 58tj_uuid=fadeb72f-a951-4cc0-80de-5e27f50fad29; new_uv=1; als=0; wmda_uuid=77f16aafcb98e3dc507d8aa7d71c497a; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; ctid=15; cmctid=102; sessid=DA7CA157-4E48-9858-B02B-BA3C5D060E9E; twe=2; lps=https%3A%2F%2Fcd.zu.anjuke.com%2F%7Chttps%3A%2F%2Fchengdu.anjuke.com%2F; wmda_session_id_6289197098934=1607648026266-2795029a-2fbc-1aad; obtain_by=2; xzfzqtoken=w2LR0zD3XbtTENwG26l0SQXQ9wpxQje0UMc51VjC3EbdVYfW7Sl8Bn8xGaVTosz2in35brBb%2F%2FeSODvMgkQULA%3D%3D',
    #         # 'cache-control': 'max-age=0',
    #         # 'referer': 'https://cd.zu.anjuke.com/fangyuan/x1/',
    #     }
    #     response = requests.get(url,headers=headers)
    #     time.sleep(5)
    #     page_content = self.base_decode(response.text)
    #     return page_content

    # def get_url():
    #     for i in range(1, 51):
    #         base_url = f'https://cd.zu.anjuke.com/fangyuan/x1-fx1-p{i}/'
    #         response = get_content(base_url)
    #         tree = etree.HTML(response)
    #         div_list = tree.xpath('//*[@id="list-content"]/div/div/h3/a/@href')
    #         return div_list
    def main(self):
        for i in range(35, 51):
            base_url = f'https://cd.zu.anjuke.com/fangyuan/x1-fx1-p{i}/'
            response = self.get_xpath(base_url)
            tree = etree.HTML(response)
            url_list = tree.xpath('//*[@id="list-content"]/div/div/h3/a/@href')
            house_info = []
            for url in url_list:
                try:
                    response = self.get_xpath(url)
                    tree = etree.HTML(response)
                    title = tree.xpath('/html/body/div[3]/h3/div/text()')
                    release_time = tree.xpath('/html/body/div[3]/div[2]/div[1]/div[2]/div/b/text()')
                    price = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[1]/span[1]/em/b/text()')
                    payment = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[1]/span[2]/text()')
                    house_model = '{}室{}厅{}卫'.format(*tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[2]/span[2]/b/text()'))
                    area = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[3]/span[2]/b/text()')
                    orientation = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[4]/span[2]/text()')
                    height = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[5]/span[2]/text()')
                    decoration = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[6]/span[2]/text()')
                    house_type = tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[7]/span[2]/text()')
                    address = '>'.join(tree.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[8]/a/text()'))
                    facility = '>'.join(tree.xpath('/html/body/div/div/div/ul/li[@class="peitao-item has"]/div/text()'))

                    # house_info = [title,release_time,price,payment,house_model,area,orientation,height,decoration,house_type,address,facility]
                    item = {}
                    item['标题'] = title
                    item['发布时间'] = release_time
                    item['价格'] = price
                    item['交租方式'] = payment
                    item['户型'] = house_model
                    item['面积'] = area
                    item['朝向'] = orientation
                    item['楼层'] = height
                    item['装修'] = decoration
                    item['类型'] = house_type
                    item['小区'] = address
                    item['设施'] = facility
                    # print(item)
                    house_info.append(item)
                except:
                    print('程序出错')
                    time.sleep(3)
                    continue
            if not os.path.exists(filename):
                write_to_excel(house_info, filename)
            # 第二次调用追加方法
            else:
                append_to_excel(house_info, filename)
                # j = random.randint(5,20)
                # time.sleep(1)
            print(f'第{i}页爬取完成')


if __name__ == '__main__':
    filename = './anjuke.xlsx'
    pc = AnJuKe()
    pc.main()