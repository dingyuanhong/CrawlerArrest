#coding=UTF-8

#PIL 图像处理库
#http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
#x64 pip install Pillow
#tesseract 字符识别库
#项目地址 https://github.com/tesseract-ocr/tesseract
#下载页面 https://github.com/UB-Mannheim/tesseract/wiki
#字符库页面 https://github.com/tesseract-ocr/tesseract/wiki/Data-Files

from PIL import Image,ImageEnhance
from pytesser import pytesser

def decodeImage(path):
    img = Image.open(path)
    imgry = img.convert('L')
    #imgry.show()

    imgry.convert('1')

    languages=[
        'chi_sim',
        'eng',
        'enm',
        'equ',
        'osd'
    ]

    enhancer = ImageEnhance.Contrast(imgry)
    imgry = enhancer.enhance(4)

    print 'image', path, 'decode begin.'
    for language in languages:
        value = pytesser.image_to_string(imgry,language)
        print language,value.decode('utf8')
    print 'image',path,'decode end.'

for i in range(0,20):
    decodeImage('./data/'+ str(i) + '.png')
