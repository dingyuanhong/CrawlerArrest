import re
import os
from Charset import getCharset as Charset

def findCharset(response):
    pattern = re.compile('(?:<meta[\s\S]*?charset[ ="\']*?([\w_-]+?)[ ="\']*?/>)')
    body = re.findall(pattern, str(response.content))
    if body.__len__() == 0:
        return 'urf'
    return Charset(body[0])

def isAString(obj):
    return isinstance(obj,basestring)

def currentTmpPath(file = None):
    path = './tmp/'
    if isAString(file):
        path = path + file

    if not os.path.exists(path):
        os.makedirs(path)
    return path

def currentDataPath(file = None):
    path = './data/'
    if isAString(file):
        path = path + file

    if not os.path.exists(path):
        os.makedirs(path)
    return path

def writeContent(line, path):
    fd = os.open(path, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    os.write(fd, str(line))
    os.close(fd)

def getContent(content,charset):
    if charset == 'utf':
        return content
    content = content.decode(charset).encode('utf')
    return content