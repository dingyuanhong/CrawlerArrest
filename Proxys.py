#coding=utf-8
import requests
import re
import sys
import time
import random
import threading
from module.UserAgent import getUserAgent as UserAgetn
from module.Util import findCharset,getContent,currentTmpPath,currentDataPath,writeContent

def validateProxys(proxys):
    tmp = {'HTTP': [], 'HTTPS': []}
    lock = threading.Lock()

    def httpProxy(i):
        header = 'HTTP'
        url = "http://quote.stockstar.com/stock"  # 打算爬取的网址
        address = proxys[header][i]
        try:
            proxy_ip = {header: address}
            headers = {"User-Agent": UserAgetn()}
            response = requests.get(url=url, headers=headers, proxies=proxy_ip)
            if response.status_code == 200:
                lock.acquire()  # 获得锁
                tmp[header].append(address)
                lock.release()  # 释放锁
            else:
                lock.acquire()
                print(header, address, response.status_code)
                lock.release()
        except Exception as e:
            info = sys.exc_info()
            lock.acquire()
            print(header, address, info[0], info[1],e)
            lock.release()

    def httpsProxy(i):
        header = 'HTTPS'
        url = "https://www.baidu.com"  # 打算爬取的网址
        address = proxys[header][i]
        try:
            proxy_ip = {header: address}
            headers = {"User-Agent": UserAgetn()}
            response = requests.get(url=url, headers=headers, proxies=proxy_ip)
            if response.status_code == 200:
                lock.acquire()  # 获得锁
                tmp[header].append(address)
                lock.release()  # 释放锁
            else:
                lock.acquire()
                print(header, address, response.status_code)
                lock.release()
        except Exception as e:
            info = sys.exc_info()
            lock.acquire()
            print(header, address, info[0], info[1],e)
            lock.release()

    # 多线程验证
    threads = []
    for i in range(len(proxys['HTTP'])):
        thread = threading.Thread(target=httpProxy, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

    threads = []
    for i in range(len(proxys['HTTPS'])):
        thread = threading.Thread(target=httpsProxy, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()

    return tmp

def getProxys():
    url='http://www.xicidaili.com/nn/' #西刺代理

    ip_totle=[]  #所有页面的内容列表
    for page in range(2,6):
        url= url +str(page)
        headers={"User-Agent":UserAgetn()}
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

if __name__ == '__main__':
    data = getProxys()
    data = validateProxys(data)
    print data