# -*- coding: utf-8 -*-
'''
爬取浏览器
'''
import ssl
import socket
import requests
# import urllib.request
# import urllib.parse
import urllib2
import urlparse
from datetime import datetime
from bs4 import BeautifulSoup
# from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
# from sys import argv
import datetime
import traceback


class Monitor_tronscan(object):
    @classmethod
    def send_msg(cls, mobile, item_name):
        """
         钉钉机器人API接口地址:
         https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1
         :param mobile:
         :param itemName:
         :return:
        """
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + "961d0856cbde6105db99a399cfae5bfb6b238b19745f9d8cd90a3627f404a8b5"
        context = ssl._create_unverfed_context()
        data = {
            "msgtype": "text",
            "text": {
                "content": item_name
            },
            "at": {
                "atMobiles": [
                    mobile
                ],
                "isAtAll": "false"
            }
        }
        # 设置编码格式
        json_data = json.dumps(data).encode(encoding='utf-8')
        print(json_data)
        header_encoding = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                           "Content-Type": "application/json"}
        req = urllib2.Request(url=url, data=json_data, headers=header_encoding)
        res = urllib2.urlopen(req)
        res = res.read()
        print(res.decode(encoding='utf-8'))

    @classmethod
    def Get_web_info(cls, url):
        '''
        :param url: website
        '''
        # 请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        request = requests.get(url='https://tronscan.org/#/en/', headers=headers, timeout=3)
        # request = urllib.request.Request(url=url, headers=headers,timeout=3)
        # 爬取结果
        response = urllib2.urlopen(request)
        data = response.read()
        # 设置解码方式
        data = data.decode('utf-8')
        # # 打印结果
        print('----------------------------------------------')
        print(data)
        return data

    @classmethod
    def Add_Link(cls, link_list, pre_url, uri):
        if uri in link_list:
            print(uri + ' has in the list,ignore')
            return link_list
        if uri == None:
            return link_list
        if uri.startswith('http') and 'github' not in uri:
            print(pre_url, uri)
            link_list.append(uri)
            return link_list
        if not uri.startswith('/'):
            return link_list
        # print('uri is ' + uri)
        link_list.append(pre_url + uri)
        return link_list

    @classmethod
    def Get_link_list(cls, url, pre_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        link_list = []
        try:
            driver.get(url)
        except:
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
            mobile = 17631360443
            item_name = nowTime + ', the chrome driver cannot get The url is ' + url
            cls.send_msg(mobile, item_name)
            print(' the chrome driver cannot get the url normally')
            driver.close()
            return link_list

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        img_ = soup.find_all(name='img')
        link_list = []
        for each in img_:
            link_list = Monitor_tronscan.Add_Link(link_list, pre_url, each.get('src'))

        script_ = soup.find_all(name='script')
        for each in script_:
            link_list = Monitor_tronscan.Add_Link(link_list, pre_url, each.get('src'))

        link_ = soup.find_all(name='link')
        for each in link_:
            link_list = Monitor_tronscan.Add_Link(link_list, pre_url, each.get('href'))
        driver.close()
        return link_list

    @classmethod
    def Get_Multilevel_Link(cls, url, pre_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        multilevel_linklist = []
        try:
            driver.get(url)
        except:
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
            mobile = 17631360443
            item_name = nowTime + ', the chrome driver cannot get the url normally. The url is ' + url
            cls.send_msg(mobile, item_name)
            print(' the chrome driver cannot get the url normally')
            return multilevel_linklist
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        multilevel = soup.find_all(name='a')
        multilevel_linklist = []
        for each in multilevel:
            if each.get('href') in multilevel:
                print(each.get('href') + ' has in the list,ignore')
                continue
            if each.get('href') == None:
                continue
            if each.get('href').startswith('#'):
                multilevel_linklist.append(pre_url + each.get('href'))
            if each.get('href').startswith('/'):
                multilevel_linklist.append(pre_url + each.get('href'))
            if each.get('href').startswith('http') and '.js' in each.get('href'):
                multilevel_linklist.append(each.get('href'))
        driver.close()
        return multilevel_linklist

    @classmethod
    def Assert_link_get_available(cls, url):
        if 'tron' not in url:
            return 1
        global requested_list
        index = 0
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        while (index < 2):
            index = index + 1
            try:
                request = urllib2.Request(url=url, headers=headers)
            except:
                try:
                    request = urllib2.Request(url=url, headers=headers)
                except:
                    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
                    mobile = 17631360443
                    item_name = nowTime + ', the url ' + url + ' request timeout,please check'
                    cls.send_msg(mobile, item_name)
                    # print(item_name + ' 168')
                    return 0
            try:
                response = urllib2.urlopen(request)
                requested_list.append(url)
                if response.getcode() == 200:
                    # print(url + ' can access')
                    return 1
            except:
                # traceback.print_exc()
                if index == 2:
                    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
                    mobile = 17631360443
                    item_name = nowTime + ' ' + url + ' cannot access'
                    cls.send_msg(mobile, item_name)
                    # print(item_name + ' 183')
            time.sleep(2)
        return 0

    @classmethod
    def check(cls, url, pre_url):
        link_list = Monitor_tronscan.Get_link_list(url, pre_url)
        global requested_list
        for link in link_list:
            if link in requested_list:
                pass
            if Monitor_tronscan.Assert_link_get_available(link):
                pass
            else:
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
                mobile = 17631360443
                item_name = nowTime + ' ' + link + ' cannot access'
                # Monitor_tronscan.send_msg(mobile, item_name)
                print(link + ' cannot access')

    @classmethod
    def list_check(cls, list_link):
        for link in list_link:
            global requested_list
            if link in requested_list:
                pass
            if Monitor_tronscan.Assert_link_get_available(link):
                pass
            else:
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
                mobile = 17631360443
                item_name = nowTime + ' ' + link + ' cannot access'
                # Monitor_tronscan.send_msg(mobile, item_name)
                print(link + ' cannot access')

    @classmethod
    def Get_Pre_Uri(cls, url):
        host = urlparse.urlparse(url).hostname
        scheme = urlparse.urlparse(url).scheme
        uri = scheme + '://' + host
        return uri


if __name__ == '__main__':
    s = Monitor_tronscan()
    socket.setdefaulttimeout(10.0)
    requested_list = []
    start = datetime.datetime.now()
    site_list = ['https://tronscan.org/#/']
    local_json_list = ['nodes', 'representatives', 'markets', 'votes', 'votes-live', 'account', '', '', '',
                       '', '']
    # local_json_list = ['common','trx','wallet','tronpg','index','resources','about','faq','bug','personalcenter',
    # 'tronpgawards','carrers','showcarrer']
    for json_content in local_json_list:
        local_url = 'https://tronscan.org/#/en/' + json_content + '.json'
        a = s.Assert_link_get_available(local_url)
    for site in site_list:
        s.check(site, s.Get_Pre_Uri(site))
        site_mutilevel_list = s.Get_Multilevel_Link(site, s.Get_Pre_Uri(site))
        s.list_check(site_mutilevel_list)
        # for link in site_mutilevel_list:
        #    Monitor_tronscan.check(link, Monitor_tronscan.Get_Pre_Uri(link))
    print(requested_list)
    end = datetime.datetime.now()
    print(len(requested_list))
    print((end - start).seconds)
