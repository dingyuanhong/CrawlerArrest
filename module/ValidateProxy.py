# coding:utf-8
import requests
import sys
import threading
import random
from UserAgent import getUserAgent as UserAgent
import json
import demjson

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
    # {'http': ip}  # 想验证的代理IP
    # {'https': ip}  # 想验证的代理IP
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

def defaultCheckContent(sourceContent,proxyContent):
    if(sourceContent == proxyContent):
            return True;
    return False;

def default(url,type,proxys,checkContent = defaultCheckContent):
    if len(url) == 0:
        return [];
    defaultContent = DefaultContent(url)
    result = []
    for proxy in proxys:
        proxies = {type:proxy};
        content = ProxyContent(url,proxies);
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
    if proxys == None:
        return {'HTTP': [], 'HTTPS': []};
    http = default(urls['HTTP'],'http',proxys['HTTP']);
    https = default(urls['HTTPS'],'https',proxys['HTTPS']);
    return {'HTTP': http, 'HTTPS': https}

def multit(url,type,proxys,checkContent = defaultCheckContent):
    if len(url) == 0:
        return [];
    result = [];
    defaultcontent = DefaultContent(url)
    lock = threading.Lock()
    def validate(i):
        proxy = proxys[i]
        proxies = {type:proxy};
        content = ProxyContent(url,proxies,5);
        if content == '':
            # lock.acquire()
            # print proxy,' Error';
            # lock.release()
            return;
        ret = checkContent(defaultcontent,content);
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
    if proxys == None:
        return {'HTTP': [], 'HTTPS': []};
    http = multit(urls['HTTP'],'http',proxys['HTTP']);
    https = multit(urls['HTTPS'],'https',proxys['HTTPS']);
    return {'HTTP': http, 'HTTPS': https}

#http://ip.chinaz.com/getip.aspx
#高匿检查
def checkHighhidingValidate(sourceContent,proxyContent):
    if (proxyContent == ''):
        return False;
    # the = json.loads(sourceContent);
    # obj = json.loads(proxyContent);
    # print sourceContent.decode('utf8')
    # print proxyContent.decode('utf8')
    try:
        the = demjson.decode(sourceContent);
        obj = demjson.decode(proxyContent);
    except Exception,e:
        # print e;
        return False
    if (the['ip'] == obj['ip']):
        return False;
    return True;

#验证代理高匿
def multitHighhidingValidateProxys(urls,proxys):
    result = {'HTTP': [], 'HTTPS': []}
    if proxys == None:
        return result;
    http = multit('http://ip.chinaz.com/getip.aspx','http',proxys['HTTP'],checkHighhidingValidate);
    https = multit('http://ip.chinaz.com/getip.aspx','https',proxys['HTTP'],checkHighhidingValidate);
    result['HTTP'] = http;
    result['HTTPS'] = https;
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
    http = randomProxy(proxys['HTTP']);
    https = randomProxy(proxys['HTTPS']);
    if(http == '' and https == ''):
        return {'HTTP':'','HTTPS':''}
    elif(http == ''):
        return {'HTTP':'','HTTPS':https};
    elif(https == ''):
        return {'HTTP':http,'HTTPS':''};
    return {'HTTP':http,'HTTPS':https};
