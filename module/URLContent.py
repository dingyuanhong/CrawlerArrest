#coding=utf-8
import time
import urllib
import requests

from UserAgent import getUserAgent as UserAgent
from CacheFile import *

def GetCapacity(capacity):
    capacity = float(capacity)
    mode = ""
    if capacity >= 1024*1024:
        capacity = capacity/(1024*1024)
        mode = "mb"
    elif capacity >= 1024:
        capacity = capacity/(1024)
        mode = "kb"
    else:
        mode = "b"
    return {"cap":capacity,"mode":mode}

def GetTimeString(seconds):
    hours = seconds / 3600;
    minute = seconds / 60;
    second = seconds % 60;
    strRet = "";
    if(hours > 0 ):
        strRet += str(hours) + "h";
    if(minute > 0):
        strRet += str(minute) + "m";
    if(second > 0):
        strRet += str(second) + "s";
    if(len(strRet) == 0):
        strRet = "0s";
    return strRet;

def UpdateRate(total,block,time):
    if time == 0:
        time = 1;
    rate = float(block)/time
    rateObj = GetCapacity(rate)
    blockObj = GetCapacity(block)
    totalObj = GetCapacity(total)
    surplusTime = (total - block) / (block/time);
    strRet = "";
    if(total != 0):
        strRet += str("%.02f%s") % (totalObj["cap"],totalObj["mode"]);
        strRet += str(" %.0f%%") % (100*block/total);
    strRet += str(" %.0f%s") % (blockObj["cap"],blockObj["mode"]);
    strRet += str(" %.02f%s/s") % (rateObj["cap"],rateObj["mode"]);
    strRet += " eta " + GetTimeString(surplusTime);
    if(total != 0 and block == total):
        print "%s         "%(strRet);
    else:
        print "%s         \r"%(strRet),;
    return strRet;

def UpdateURLContent(url,option,file):
    # print("UpdateURLContent(\"" + url + "\")")
    headers={"User-Agent":UserAgent()}
    proxies = {};
    if option != None:
        if option.has_key('proxy') and \
         option['proxy'] != '':
            proxies = {type:option['proxy']};
    try:
        response=requests.get(url=url,headers=headers,proxies = proxies)
    except Exception as e:
        return 404;
    if response.status_code != 200:
        print("UpdateURLContent(\"" + url + "\")Failed." + str(response.status_code))
        return response.status_code
    WriteCacheFile(file,response.content);
    return response.status_code

def DownloadURL(url,option,file):
    print("DownloadURL(\"" + url + "\")")
    headers={"User-Agent":UserAgent()}
    try:
        response = requests.get(url=url, stream=True, headers=headers)
    except Exception as e:
        print e;
        return 404;
    if response.status_code != 200:
        print("DownloadURL(\"" + url + "\")Failed." + response.status_code)
        return response.status_code
    contentLength = response.headers.get('Content-Length')
    if contentLength == None:
        contentLength = 0;
    contentLength = int(contentLength);

    start_time = int(time.time())
    download_size = 0;
    with open(file, 'wb') as local_file:
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:
                local_file.write(chunk)
                local_file.flush()
                download_size += len(chunk)
            use_time = int(time.time()) - start_time
            UpdateRate(contentLength,download_size,use_time)
        local_file.close()
    return response.status_code

def GetCacheUrl(url,option):
    timeout = 0;
    if option != None:
        if option.has_key('timeout'):
            timeout = option['timeout'];
            timeout = int(timeout);

    cacheName = CreateCacheName(url);
    CacheFile = ChechCacheExpress(cacheName,timeout)
    if CacheFile == None :
        CacheFile = GetCahceFile(cacheName)
        ret = UpdateURLContent(url,option,CacheFile)
        if ret != 200:
            return None
    data = ReadCacheFile(CacheFile)
    if data == None:
        return None
    return {"url":url,"cache":CacheFile,"data":data}
