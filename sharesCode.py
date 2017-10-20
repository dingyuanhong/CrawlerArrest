#coding=utf-8
from module.URLContent  import *
import re
from bs4 import BeautifulSoup
import json

def parseContent(content):
    soup = BeautifulSoup(content,'lxml');
    # param = soup.find_all("re.compile('id=\"szseWebReport_pageinfo')");
    param = soup.find_all(attrs={"id":re.compile(r"szseWebReport_pageinfo*")});
    param = param[0]['url'];
    # print param;
    ret = soup.select('table[id=REPORTID_tab1]');
    for tag in ret:
        tagTRS = tag.find_all('tr');
        for tagTR in tagTRS:
            tagTDS = tagTR.find_all('td');
            if len(tagTDS) <= 0:
                continue;
            tagTD = tagTDS[0];
            # print tagTD.a.u.string;
            tagTD = tagTDS[1];
            # print tagTD.a.u.string;
            tagTD = tagTDS[2];
            # print tagTD.string;
            tagTD = tagTDS[3];
            # print tagTD.string;
            tagTD = tagTDS[4];
            # print tagTD.string;
            tagTD = tagTDS[5];
            # print tagTD.a;
            refreshData = tagTD.a['onclick'];
            # print tagTD.a['onclick'];
            # print refreshData;
            rule = "(?:\'(.*)\')";
            pattern = re.compile(rule)
            command = re.findall(pattern,refreshData)
            command = command[0];
            print command;
            print param;
            result = os.popen('node ./javascript/szseURLAndParam.js -c ' + command + ' -p ' + param).readlines();
            print result;
            result = result[0];
            print result;
            obj = json.loads(str(result));
            print obj;
            break;
            # for tagTD in tagTDS:
                # print tagTD.prettify();
    return ret;

def GetCode():
    url = "http://www.szse.cn/main/marketdata/jypz/colist/";
    data = GetCacheUrl(url,{});
    print data["cache"];
    parseContent(data['data']);


if __name__ == "__main__":
    GetCode();
