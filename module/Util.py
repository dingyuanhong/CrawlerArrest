import re
import os
from Charset import getCharset as Charset
import hashlib

def findCharset(content):
    pattern = re.compile('(?:<meta[\s\S]*?charset[ ="\']*?([\w_-]+?)[ ="\']*?/>)')
    body = re.findall(pattern, str(content))
    if body.__len__() == 0:
        return 'urf'
    return Charset(body[0])

def isAString(obj):
    return isinstance(obj,basestring)

def currentTmpPath(file = None):
    path = './tmp/'
    if isAString(file):
        path = path + file

    dirname, basename = os.path.split(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return path

def currentDataPath(file = None):
    path = './data/'
    if isAString(file):
        path = path + file

    dirname, basename = os.path.split(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return path

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return None;
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

def writeContent(line, path):
    fd = os.open(path, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    os.write(fd, str(line))
    os.close(fd)

def writeBinary(line,path):
    fd = open(path,'wb')
    fd.write(line)
    fd.close()

def getContent(content,charset):
    if charset == 'utf':
        return content
    content = content.decode(charset).encode('utf')
    return content
