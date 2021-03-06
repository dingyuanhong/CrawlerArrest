#coding=utf-8


import os

def AddPath(path):
    #获取当前模块路径名
    #path =  str(__file__)
    #找到路径分割
    index = path.rfind('\\')
    #分割全路径为模块路径
    if index != -1:
        path = path[0:index]
    #获取PATH环境变量
    sysPath = str(os.environ["PATH"])
    #检查环境变量是否已存在路径,不存在则添加
    if sysPath.find(path) == -1:
        os.environ["PATH"] = path + ";" + os.environ["PATH"]
    #设置TESS数据扩展路径环境变量
    os.environ['TESSDATA_PREFIX'] = path
