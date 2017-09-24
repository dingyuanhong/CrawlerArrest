# coding:utf-8
import requests
import sys
import threading
import random
from UserAgent import getUserAgent as UserAgent
import json

def DefaultContent(url):
    headers = {"User-Agent": UserAgent()}
    try:
        response = requests.get(url, headers=headers)
    except:
        return ''
    if response.status_code != 200:
        return ''
    return response.content

def ProxyContent(url,proxy,timeout=0):
    headers = {"User-Agent": UserAgent()}
    try:
        if timeout > 0:
            response = requests.get(url, headers=headers, proxies=proxy,timeout=timeout)
        else:
            response = requests.get(url, headers=headers, proxies=proxy)
    except:
        info = sys.exc_info()
        return ''

    if response.status_code != 200:
        return ''
    return response.content

class ProxyValidate:
    def __init__(self):
        self.http = {};
        self.http.content = '';
        self.https = {};
        self.https.content = '';
        self.result = {'HTTP':[],'HTTPS':[]};

    def checkContent(self,type,content):
        if(type == 'HTTP'):
            if(content == self.http.content):
                return True;
        elif(type == 'HTTPS'):
            if(content == self.https.content):
                return True;
        return False;

    def default(self,url,type,proxys):
        self[type] = {};
        self[type].content = DefaultContent(url);
        for proxy in proxys[type]:
            proxies = {type:proxy};
            content = ProxyContent(url,proxies);
            ret = self.checkContent(type,content);
            if ret == True:
                self.result[type].append(proxy);
        return self.result[type];

    def http(self,url,proxys):
        self.http.content = DefaultContent(url);
        for proxy in proxys['HTTP']:
            content = ProxyContent(url,proxy);
            ret = self.checkContent('HTTP',content);
            if ret == True:
                self.result['HTTP'].append(proxy);
        return self.result['HTTP'];

    def https(self,url,proxys):
        self.https.content = DefaultContent(url);
        for proxy in proxys['HTTPS']:
            content = ProxyContent(url,proxy);
            ret = self.checkContent('HTTPS',content);
            if ret == True:
                self.result['HTTPS'].append(proxy);
        return self.result['HTTPS'];

    def multity(url,type,proxys):
        result = [];
        source_content = DefaultContent(url);
        lock = threading.Lock()  # 建立一个锁
        def checkContent(content):
            if(source_content == content):
                return True;
            return False;

        def validate(i):
            proxy = proxys[i]
            proxies = {type:proxy};
            content = ProxyContent(url,proxies);
            ret = checkContent(content);
            if ret == True:
                lock.acquire()
                result.append(proxy)
                lock.release()

        threads = []
        for i in range(len(proxys)):
            thread = threading.Thread(target=validate, args=[i])
            threads.append(thread)
            thread.start()
        # 阻塞主进程，等待所有子线程结束
        for thread in threads:
            thread.join()

        return result;

    def multitHttp(url,proxys):
        return multity(url,'http',proxys['HTTP']);

    def multitHttps(url,proxys):
        return multity(url,'https',proxys['HTTPS']);

    #高匿检查
    def multitHTTPHighhiding(proxys):
        url = "http://ip.chinaz.com/getip.aspx";
        result = [];
        source_content = DefaultContent(url);
        source_obj = json.loads(source_content);

        lock = threading.Lock()  # 建立一个锁

        def checkContent(content):
            the_obj = json.loads(content);
            if(source_obj.ip !== the_obj.ip):
                return True;
            return False;

        def validate(i):
            proxy = proxys['HTTP'][i]
            proxies = {'http':proxy};
            content = ProxyContent(url,proxies);
            ret = checkContent(content);
            if ret == True:
                lock.acquire()
                result.append(proxy)
                lock.release()

        threads = []
        for i in range(len(proxys['HTTP'])):
            thread = threading.Thread(target=validate, args=[i])
            threads.append(thread)
            thread.start()
        # 阻塞主进程，等待所有子线程结束
        for thread in threads:
            thread.join()

        return result;
