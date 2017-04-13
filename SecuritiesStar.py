#coding=utf-8
import requests
import re

from module.UserAgent import getUserAgent as UserAgent
from module.Util import findCharset,currentTmpPath,currentDataPath,writeContent,getContent


def getUrlData():
    url = 'http://quote.stockstar.com'
    pageName = 'ranklist_a_3_1_1'
    url = url + '/stock/' + pageName + '.html'

    headers = {"User-Agent":UserAgent()} #伪装浏览器请求报头
    response = requests.get(url,headers=headers)
    charset = findCharset(response)
    pattern = re.compile('<tr[\s\S]*?</tr>')
    body = re.findall(pattern, str(response.content))

    Catalog = currentTmpPath('html/'+ pageName + '/')

    stock_all = []
    item_count = 0
    for i in range(0, body.__len__()):
        content = getContent(body[i], charset)

        #path = Catalog + str(i) + '.txt'
        #writeContent(content, path);

        pattern = re.compile('>(.*?)<')
        stock_page = re.findall(pattern,content)
        stock_last = []
        for data in stock_page:
            if data != '':
                stock_last.append(data)

        if item_count ==0 :
            item_count = stock_last.__len__()
        if item_count == stock_last.__len__():
            stock_all.append(stock_last)
        #else :
            #print i , stock_last.__len__()

    dataPath = currentDataPath('html/' + pageName + '/')
    data = '\n'.join('  '.join(str(item) for item in line) for line in stock_all)
    writeContent(data,dataPath + 'data.txt');
    return stock_all

if __name__ == '__main__':
    getUrlData()