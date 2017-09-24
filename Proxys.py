#coding=utf-8
import requests
import re
import sys
import time
import random
import threading
import string
from module.Charset import getCharset as Charset
from module.UserAgent import getUserAgent as UserAgent
from module.ValidateProxy import *
from module.Util import *
from module.URLContent import *
from module.CacheFile import *

def getProxys():
    url='http://www.xicidaili.com/nn/' #西刺代理

    ip_totle=[]  #所有页面的内容列表
    for page in range(2,6):
        url= url +str(page)
        headers={"User-Agent":UserAgent()}
        response=requests.get(url=url,headers=headers)
        if response.status_code != 200:
            continue

        charset = findCharset(response.content)
        content = getContent(response.content,charset);
        pattern=re.compile('(?:<td>(\d.*?)</td>)')  #截取<td>与</td>之间第一个数为数字的内容
        ip_page=re.findall(pattern,str(content))
        ip_totle.extend(ip_page)
        time.sleep(random.choice(range(1,3)))

    proxys = {'HTTP':[],'HTTPS':[]}
    #打印抓取内容
    #print('代理IP地址     ','\t','端口','\t','速度','\t','验证时间')
    for i in range(0,len(ip_totle),4):
        #print(ip_totle[i],ip_totle[i+1],ip_totle[i+2],ip_totle[i+3])
        proxys['HTTP'].append(ip_totle[i] + ':' + ip_totle[i+1])
    return proxys

#验证代理可用性
validateURL = {'HTTP':'http://www.csdn.net/company/contact.html','HTTPS':'https://www.baidu.com/'};

# home = 'http://www.xicidaili.com/nn/'  # 西刺代理

#解析代理地址
def parseProxyContent(data,key):
    proxys = {
        'HTTP':[],
        'HTTPS':[]
        }
    hasData = False;
    for item in data:
        if item.__len__() <= key:
            continue;
        if item[key] == 'HTTP':
            proxys['HTTP'].append(item[0] + ':' + item[1])
            hasData = True;
        elif item[key] == 'HTTPS':
            proxys['HTTPS'].append(item[0] + ':' + item[1])
            hasData = True;
        else:
            print item
    if hasData == False:
        return None;
    return proxys

#获取页面最大值
def parsePageMax(content):
    pattern = re.compile(r'/nn/\d+.>(\d+)\<')
    page = re.findall(pattern,str(content))
    if page.count > 0 :
        max = 1
        for a in page:
            if string.atoi(a) > max:
                max = string.atoi(a)
        if isinstance(max,int):
            return max
    return 1

#解析页面代理信息数组
def parsePageProxy(content):
    pattern = re.compile(r'(?:<tr[\s\S]*?>([\s\S]*?)</tr>)')
    page = re.findall(pattern, str(content))
    data = []
    index = 0
    if page.__len__() > 0:
        rule0 = '([\s\S]*?)'
        for item in page:
            rule = rule0
            pattern = re.compile('(?:<td[\s\S]*?\>' + rule + '</td\>)')
            packet = re.findall(pattern,str(item));
            if packet.__len__() > 0:
                for i in range(0,packet.__len__()):
                    if i == 0:
                        packet[i] = ''
                        continue
                    elif i != 3 and i != 6 and i != 7:
                        continue
                    rule3 = '(?:\>(.*)<)'
                    rule6 = '(?:title="(.*?)")'
                    if i == 3:
                        rule = rule3
                    elif i == 6 or i == 7:
                        rule = rule6
                    pattern = re.compile(rule)
                    value = re.findall(pattern,str(packet[i]))
                    if value.__len__()  == 1:
                        packet[i] = value[0]
                    elif i == 3:
                        packet[i] = ''
                packet.remove("");
                data.append(packet)
            index = index + 1
    return data

#解析代理信息
def parseProxy(url,option):
    timeout = 0;
    if option != None:
        if option.has_key('timeout'):
            timeout = option['timeout'];
            timeout = int(timeout);

    file = ChechCacheFileExpress(GetCacheURLFile("Result:" + url),timeout);
    if(file == None):
        content = GetCacheUrl(url,option);
        if content == None:
            return None;
        data = parsePageProxy(content["data"])
        value = '\n'.join('  '.join(i) for i in data)

        WriteCacheFile(GetCacheURLFile("Result:" + url),value);
        content = value;
    else:
        content = ReadCacheFile(file);

    content = content.decode('utf8');
    data = [];
    packet = content.split('\n');
    for row in packet:
        data.append(row.split('  '));
    ret = parseProxyContent(data,4);
    return ret;

#Obsolete
def GetDefaultPages(url,path=None):
    headers = {"User-Agent": UserAgent()}
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return 0

    charset = Charset(response.content)
    content = response.content.decode(charset).encode('utf8')
    maxPages = parsePageMax(content)

    if path != None:
        data = parsePageContent(content)
        value = '\n'.join('  '.join(i) for i in data)

        if os.path.exists(path):
            os.remove(path);
        writeContent(str(value).decode(charset).encode('utf'),path)
    return maxPages

#Obsolete
def GetUrlResponse(url,headers,proxys = None):
    proxy = {}
    response = ''
    useProxys = False
    success = False
    for i in range(0, 5):
        if useProxys:
            proxy = randomProxysIP(proxys)
            if proxy == {}:
                continue
            print '使用代理:', proxy
        if headers == None:
            headers = {"User-Agent": UserAgent()}
        else:
            headers["User-Agent"] = UserAgent()
        err = False
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
        except:
            info = sys.exc_info()
            print url, info[0], ":", info[1]
            err = True
            if proxys != None:
                useProxys = True
        if err:
            continue
        # s失败
        if response.status_code != 200:
            print url, response.status_code
            if proxys != None:
                useProxys = True
            continue
        success = True
        break

    return response,success

_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Host": "www.xicidaili.com",
    "Referer": "http://www.xicidaili.com/nn/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": UserAgent()
}

_cookies = None

#获取代理地址列表
def getProxysList():
    home = 'http://www.xicidaili.com/nn/'  # 西刺代理

    proxysList = parseProxy(home,{'timeout':-1});
    proxys = multitHighhidingValidateProxys(validateURL,proxysList);

    content = GetCacheUrl(home,{'timeout':-1});
    # print content['cache'];
    maxPages = parsePageMax(content);
    if maxPages <= 1:
        maxPages = 1
    # 待验证的代理IP
    pageCharset = Charset(findCharset(content));

    ip_totle = {
        'HTTP':[],
        'HTTPS':[]
        }
    page = 0
    successPage = 0
    while True:
        url = home
        if page > 0:
            url= home +str(page)

        if page >= maxPages:
            break

        #print 'index:', page
        page = page + 1

        proxysList = parseProxy(url,{'timeout':-1,'proxy':randomProxysIP(proxys)['HTTP']});
        if proxysList == None:
            continue;
        proxysList = multitHighhidingValidateProxys(validateURL,proxysList);
        proxys['HTTP'].extend(proxysList['HTTP']);
        proxys['HTTPS'].extend(proxysList['HTTPS']);

    return proxys

#获取页面最大值
def parsePageMax2(content):
    pattern = re.compile(r'>(\d+?)\</a>')
    page = re.findall(pattern,str(content))
    if page.count > 0 :
        max = 1
        for a in page:
            if string.atoi(a) > max:
                max = string.atoi(a)
        if isinstance(max,int):
            return max
    return 1

def downloadImage(url,name):
    file = currentDataPath(name)
    if not os.path.exists(file):
        DownloadURL(url,{},file);
        return {file:0};
    return None;

#解析页面代理信息数组
def parsePageProxy2(content):
    pattern = re.compile(r'(?:(<td[\s\S]*?>[\s\S]*?)</tr>)')
    page = re.findall(pattern, str(content))
    data = []
    index = 0
    if page.__len__() > 0:
        rule0 = '([\s\S]*?)'
        for item in page:
            rule = rule0
            pattern = re.compile('(?:<td[\s\S]*?\>' + rule + '</td\>)')
            packet = re.findall(pattern,str(item));
            if packet.__len__() > 0:
                for i in range(0,packet.__len__()):
                    if i == 0:
                        packet[i] = ''
                        continue
                    elif i != 5 and i != 7 and i != 8:
                        continue
                    rule5 = '(?:\>(.*)<)'
                    rule7 = '(?:title="(.*?)")'
                    if i == 5:
                        rule = rule3
                    elif i == 7 or i == 8:
                        rule = rule7
                    pattern = re.compile(rule)
                    value = re.findall(pattern,str(packet[i]))
                    if value.__len__()  == 1:
                        packet[i] = value[0]
                    elif i == 5:
                        packet[i] = value
                packet.remove("");
                print packet;
                data.append(packet)
            index = index + 1
    return data

def parseProxy2(url,option):
    file = ChechCacheFileExpress(GetCacheURLFile("Result:" + url),5);
    if(file == None):
        content = GetCacheUrl(url,option);
        if content == None:
            return None;
        data = parsePageProxy2(content["data"])
        value = '\n'.join('  '.join(i) for i in data)

        WriteCacheFile(GetCacheURLFile("Result:" + url),value);
        content = value;
    else:
        content = ReadCacheFile(file);

    content = content.decode('utf8');
    data = [];
    packet = content.split('\n');
    for row in packet:
        data.append(row.split('  '));
    ret = parseProxyContent(data,4);
    return ret;

def parsePageImage(content):
    #<img src=common/ygrandimg.php?id=1&port=MmjiMm4vMpDgO0O />
    pattern = re.compile('<img src[=" ]*?(common/[\W\w/.?&=]+?)[ "/]*?>')  # 截取<td>与</td>之间第一个数为数字的内容
    ip_page = re.findall(pattern, str(content))
    print ip_page.__len__()
    for i in range(ip_page.__len__()):
        downloadImage("http://proxy.mimvp.com/" + ip_page[i],str(i) + '.png')
    return ip_page

def getProxysList2():
    proxys = {'HTTP': [], 'HTTPS': []}

    home = 'https://proxy.mimvp.com/free.php'  # 西刺代理
    proxysList = parseProxy2(home,{'timeout':-1});
    print proxysList;
    return;

    proxys = multitHighhidingValidateProxys(validateURL,proxysList);

    home = 'http://proxy.mimvp.com/free.php?proxy=in_hp'
    pageCharset = ''
    ip_totle = []  # 所有页面的内容列表
    page = 1
    maxPages = 1
    successPage = 0
    while True:
        url = home
        if page >= 1:
            url = home + '&sort=&page=' + str(page)
        if page > maxPages:
            break
        if successPage >= 100:
            break;
        page = page + 1

        response, success = GetUrlResponse(url, {}, proxys)
        if not success:
            continue

        if pageCharset == '':
            pageCharset = Charset(response.content)
        content = response.content.decode(pageCharset).encode('utf')
        if maxPages <= 1:
            maxPages = getPageMax3(content);

        ip_page = getPageContent3(content)
        ip_page = []
        ip_totle.extend(ip_page)

        if ip_page.__len__() > 0:
            successPage = successPage + 1
        break

    proxys = {
        'HTTP': [],
        'HTTPS': []
    }
    for i in ip_totle:
        proxys['HTTP'].append(str(i[0] + ':' + i[1]));

    proxys = validateProxys(validateURLS,proxys);
    return proxys

if __name__ == '__main__':
    data = getProxysList()
    # print data['HTTP'].__len__()
    # print data
