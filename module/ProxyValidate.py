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

def ProxyContent(url,proxyIP,timeout=0):
    headers = {"User-Agent": UserAgent()}
    proxy = {type: proxyIP}  # 想验证的代理IP
    try:
        if timeout > 0:
            response = requests.get(url, headers=headers, proxies=proxy,timeout=timeout)
        else:
            response = requests.get(url, headers=headers, proxies=proxy_ip)
    except:
        info = sys.exc_info()
        return ''

    if response.status_code != 200:
        return ''
    return response.content

def threadProxytValidate(self,i):

class Proxy:
    def __init(self):

    class Validate:
        def __init__(self):
            self.http = {};
            self.http.content = '';
            self.https = {};
            self.https.content = '';
            self.result = {'HTTP':[],'HTTPS':[]};
        def checkContent(self,type,content):
            if(type == 'http'):
                if(content == self.http.content):
                    return True;
            elif(type == 'https'):
                if(content == self.https.content):
                    return True;
            return False;

        def http(self,url,proxys):
            self.http.content = DefaultContent(url);
            for proxy in proxys['HTTP']:
                content = ProxyContent(url,proxy);
                ret = self.checkContent('http',content);
                if ret == True:
                    self.result['HTTP'].append(proxy);
            return self.result;

        def https(url,proxys):
            self.https.content = DefaultContent(url);
            for proxy in proxys['HTTPS']:
                content = ProxyContent(url,proxy);
                ret = self.checkContent('https',content);
                if ret == True:
                    self.result['HTTPS'].append(proxy);
            return self.result;

        def multitHttp(url,proxys):
            self.http.content = DefaultContent(url);
            lock = threading.Lock()  # 建立一个锁

            def validate(i):
                proxy = proxys['HTTP'][i]
                content = ProxyContent(url,proxy);
                ret = self.checkContent('http',content);
                if ret == True:
                    lock.acquire()
                    self.result['HTTP'].append(proxy)
                    lock.release()

            threads = []
            for i in range(len(proxys['HTTP'])):
                thread = threading.Thread(target=validate, args=[i])
                threads.append(thread)
                thread.start()
            # 阻塞主进程，等待所有子线程结束
            for thread in threads:
                thread.join()

            return self.result;

        def multitHttps(url,proxys):
            self.https.content = DefaultContent(url);
            lock = threading.Lock()  # 建立一个锁
            def validate(i):
                proxy = proxys['HTTPS'][i]
                content = ProxyContent(url,proxy);
                ret = self.checkContent('https',content);
                if ret == True:
                    self.result['HTTPS'].append(proxy);

            threads = []
            for i in range(len(proxys['HTTP'])):
                thread = threading.Thread(target=validate, args=[i])
                threads.append(thread)
                thread.start()
            # 阻塞主进程，等待所有子线程结束
            for thread in threads:
                thread.join()
            return self.result;

        #http://ip.chinaz.com/getip.aspx
        #高匿检查
        def checkHighhiding(url,proxyIP):
            content = DefaultContent(url);
            obj = json.loads(content);
            #本地IP
            selfIP  = obj.ip;
            content = ProxyContent(url,proxyIP,0);
            obj = json.loads(content);
            theIP = obj.ip;
            if(selfIP == theIP):
                return false;
            else:
                return true;
