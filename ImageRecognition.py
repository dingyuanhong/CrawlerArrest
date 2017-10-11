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
        'equ'#,
        #'osd'
    ]

    enhancer = ImageEnhance.Contrast(imgry)
    imgry = enhancer.enhance(4)

    print 'image', path, 'decode begin.'
    for language in languages:
        value = pytesser.image_to_string(imgry,language)
        print language,value.decode('utf8')
    print 'image',path,'decode end.'

import tesseract
import cv2.cv as cv

def decodeImage2(file):
    #https://www.oschina.net/p/python-tesseract?nocache=1492601195168
    #不知道怎么用
    api = tesseract.TessBaseAPI()
    api.Init('.','eng',tesseract.OEM_DEFAULT)
    api.SetPageSegMode(tesseract.PSM_AUTO)

    image = cv.LoadImage(file,cv.CV_LOAD_IMAGE_GRAYSCALE)
    tesseract.SetCvImage(image,api)
    text = api.GetUTF8Text()
    conf = api.MeanTextConf()
    print text
    print conf

def decodeImage3(file):
    #https://www.oschina.net/p/deep-ocr
    return

import ocrolib

def decodeImage4(file):
    #https://www.oschina.net/p/ocropus
    #https://github.com/tmbdev/ocropy
    #ocrolib.
    return

def decodeImage5(file):
    #Cuneiform
    return

#for i in range(0,20):
i = 0
decodeImage2('./data/'+ str(i) + '.png')

