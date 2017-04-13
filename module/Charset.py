

charsets = [
["gb2312","gbk"],
["gbk","gbk"],
["utf","utf"],
["big5","unicode"],
["unicode","unicode"],
]

def getCharset(name):
    name = name.lower()
    for item in charsets:
        if name.find(item[0]) != -1:
            return item[1]
    return ""

def  CharsetDecode(value,charset):
    if charset == 'gbk':
        return value.decode('gbk')
    elif  charset == 'utf':
        return value.decode('utf')
    else :
        return str(value)