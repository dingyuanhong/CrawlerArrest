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

def defaultCheckContent(sourceContent,proxyContent):
    if(sourceContent == proxyContent):
            return True;
    return False;

def default(url,proxys,checkContent = defaultCheckContent):
    defaultContent = DefaultContent(url)
    result = []
    for proxy in proxys:
        content = ProxyContent(url,proxy);
        if content == '':
            # print proxy,' Error';
            continue;
        ret = checkContent(defaultContent,proxyContent);
        if ret == True:
            result.append(proxy)
    return result;

# http = "http://www.csdn.net/company/contact.html"
# https = "https://www.baidu.com/"
#验证代理
def defaultValidateProxys(urls,proxys):
    http = default(urls['HTTP'],proxys['HTTP']);
    https = default(urls['HTTPS'],proxys['HTTPS']);
    return {'HTTP': http, 'HTTPS': https}

def multit(url,proxys,checkContent = defaultCheckContent):
    result = [];
    content = DefaultContent(url)

    lock = threading.Lock()
    def validate(i):
        proxy = proxys[i]
        content = ProxyContent(url,proxy);
        if content == '':
            # lock.acquire()
            # print proxy,' Error';
            # lock.release()
            return;
        ret = checkContent(content,content);
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

#验证代理
def multitValidateProxys(urls,proxys):
    http = multit(urls['HTTP'],proxys['HTTP']);
    https = multit(urls['HTTPS'],proxys['HTTPS']);
    return {'HTTP': http, 'HTTPS': https}

#http://ip.chinaz.com/getip.aspx
#高匿检查
def checkHighhidingValidate(sourceContent,proxyContent):
    if (proxyContent == ''):
        return False;
    the = json.loads(sourceContent);
    obj = json.loads(proxyContent);
    if (the.ip == obj.ip):
        return False;
    return True;

#验证代理高匿
def multitHighhidingValidateProxys(proxys):
    result = {'HTTP': [], 'HTTPS': []}
    http = multit(urls['HTTP'],proxys['HTTP'],checkHighhidingValidate);
    result['HTTP'] = http;
    # result['HTTPS'] = https;
    return result;

def randomProxy(proxys):
    if proxys.__len__() <= 0:
        return '';
    proxy = -1
    proxy = random.choice(range(0, proxys.__len__() ))
    if proxy != -1:
        return proxys[proxy];

#随机代理信息
def randomProxysIP(proxys):
    http = randomProxys(proxys['HTTP']);
    https = randomProxys(proxys['HTTPS']);
    if(http == '' and　https == ''):
        return {}
    else if(http == ''):
        return {'HTTPS':https};
    else if(https == ''):
        return {'HTTP':http};
    return {'HTTP':http,'HTTPS':https};
