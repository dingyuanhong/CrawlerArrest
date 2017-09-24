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
    proxy_ip = {type: proxyIP}  # 想验证的代理IP
    try:
        if timeout > 0:
            response = requests.get(url, headers=headers, proxies=proxy_ip,timeout=timeout)
        else:
            response = requests.get(url, headers=headers, proxies=proxy_ip)
    except:
        info = sys.exc_info()
        return ''

    if response.status_code != 200:
        return ''
    return response.content

# url = "http://quote.stockstar.com/stock"  # 打算抓取内容的网页
# url = "https://www.baidu.com/"  # 打算抓取内容的网页
def defaultValidateProxys(urls,proxys):
    url = urls["http"];
    content = DefaultContent(url)
    def validateProxy(url,type,proxy, content):
        headers = {"User-Agent": UserAgent()}
        proxy_ip = {type: proxy}  # 想验证的代理IP
        try:
            response = requests.get(url, headers=headers, proxies=proxy_ip, timeout=5)
        except:
            info = sys.exc_info()
            print proxy, type + ' Error',info[0]
            return False

        if response.status_code != 200:
            print proxy, type + ' Error',response.status_code
            return False
        if content == response.content:
            return True
        return False

    tmp = {'HTTP':[],'HTTPS':[]}
    for proxy in proxys['HTTP']:
        ret = validateProxy(url,'http',proxy,content);
        if ret == True:
            tmp['HTTP'].append(proxy)

    url = urls["https"];
    if(url == None):
        return tmp;
    content = DefaultContent(url)
    for proxy in proxys['HTTPS']:
        ret = validateProxy(url,'https',proxy,content);
        if ret == True:
            tmp['HTTPS'].append(proxy)

    return tmp

# url = "http://www.csdn.net/company/contact.html"  # 打算抓取内容的网页
# url = "https://www.baidu.com/"  # 打算抓取内容的网页
def multitValidateProxys(urls,proxys):
    tmp = {'HTTP': [], 'HTTPS': []}
    lock = threading.Lock()  # 建立一个锁

    def validateProxy(url,type,proxy, content):
        headers = {"User-Agent": UserAgent()}
        proxy_ip = {type: proxy}  # 想验证的代理IP
        try:
            response = requests.get(url, headers=headers, proxies=proxy_ip, timeout=5)
        except:
            info = sys.exc_info()
            lock.acquire()
            print proxy, type + ' Error',info[0]
            lock.release()
            return False

        if response.status_code != 200:
            lock.acquire()
            print proxy, type + ' Error',response.status_code
            lock.release()
            return False
        if content == response.content:
            return True
        return False

    url = urls["http"];
    content = DefaultContent(url)

    def httpValidate(i):
        proxy = proxys['HTTP'][i]
        ret = validateProxy(url,'http',proxy,content)
        if ret == True:
            lock.acquire()
            tmp['HTTP'].append(proxy)
            lock.release()

    threads = []
    for i in range(len(proxys['HTTP'])):
        thread = threading.Thread(target=httpValidate, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

    url = urls["https"];
    if(url == None):
        return tmp;

    content = DefaultContent(url)
    threads = []
    def httpsValidate(i):
        proxy = proxys['HTTPS'][i]
        ret = validateProxy(url,'https',proxy,content)
        if ret == True:
            lock.acquire()
            tmp['HTTPS'].append(proxy)
            lock.release()

    for i in range(len(proxys['HTTPS'])):
        thread = threading.Thread(target=httpsValidate, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

    return tmp

def validateProxys(urls,proxys):
    tmp = {'HTTP': [], 'HTTPS': []}
    lock = threading.Lock()
    def validateProxy(url,type,proxy):
        try:
            proxy_ip = {type: proxy}
            headers = {"User-Agent": UserAgent()}
            response = requests.get(url=url, headers=headers, proxies=proxy_ip)
            if response.status_code == 200:
                lock.acquire()  # 获得锁
                tmp[type].append(proxy)
                lock.release()  # 释放锁
            else:
                lock.acquire()
                print(type, proxy, response.status_code)
                lock.release()
        except Exception as e:
            info = sys.exc_info()
            lock.acquire()
            print(type, proxy, info[0], info[1], e)
            lock.release()

    def httpProxy(i):
        # url = "http://quote.stockstar.com/stock"  # 打算爬取的网址
        url = urls["http"];
        header = 'HTTP'
        proxy = proxys[header][i]
        validateProxy(url,header,proxy);

    def httpsProxy(i):
        # url = "https://www.baidu.com"  # 打算爬取的网址
        url = urls["https"];
        header = 'HTTPS'
        proxy = proxys[header][i]
        validateProxy(url, header, proxy);

    # 多线程验证
    threads = []
    for i in range(len(proxys['HTTP'])):
        thread = threading.Thread(target=httpProxy, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

    if(urls["https"] == None):
        return tmp;

    threads = []
    for i in range(len(proxys['HTTPS'])):
        thread = threading.Thread(target=httpsProxy, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

    return tmp

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

#随机代理信息
def randomProxysIP(proxys):
    needHttp = False
    needHttps = False
    if proxys['HTTP'].__len__() > 0:
        #print 'HTTP PROXYS',proxys['HTTP'].__len__()
        needHttp = True
    if proxys['HTTPS'].__len__() > 0:
        #print 'HTTPS PROXYS', proxys['HTTPS'].__len__()
        needHttps = True
    http = -1
    https = -1
    if needHttp:
        http = random.choice(range(0, proxys['HTTP'].__len__() ))
    if needHttps:
        https = random.choice(range(0, proxys['HTTPS'].__len__() ))
    if  http != -1 and https != -1:
        proxy_ip = {'HTTP':proxys['HTTP'][http],
                    'HTTPS':proxys['HTTPS'][https]}
        return proxy_ip
    elif http != -1:
        proxy_ip = {'HTTP': proxys['HTTP'][http]}
        return proxy_ip
    elif https != -1:
        proxy_ip = {'HTTPS': proxys['HTTPS'][https]}
        return proxy_ip
    else:
        return {}
