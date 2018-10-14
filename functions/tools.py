# -*- coding:utf-8 -*-

import time
import os
import requests
import logging

# 清洗字符串（因为是从网上下来的数据）
def StringClean(str) :
    str = str.replace('&', '')
    # str = str.strip()
    # # 清洗标题，防止不符合文件名的规定
    # str = str.replace('/', '')
    # str = str.replace('\\', '')
    # str = str.replace(':', '')
    # str = str.replace('*', '')
    # str = str.replace('?', '')
    # str = str.replace('"', '')
    # str = str.replace('|', '')
    # # str = str.replace(' ', '')
    # # str = str.replace('.', '')
    # str = str.replace('>', '')
    # str = str.replace('<', '')
    # str = str.replace('\xa0', '')
    # str = str.replace('\x14', '')
    # # 去掉空白字符
    # str = "".join( ch for ch in str if ord(ch)> 0 )
    #
    # # 去掉str末尾出现的...字符（window系统的规定...）
    # # str = "abc..."
    # while len(str)>0 and str[-1] == '.' :
    #     str = str[:-1]
    # # 测试过滤
    # for ch in str:
    #     print("ch : "+ch +", ch : ")
    #     print(ord(ch))
    return str

# # 输出信息（加入时间元素）
# def _print(message) :
#     print(time.strftime("%m.%d %T") + ' -- ' + message)

# 根据资源的URL，返回资源的后缀
def suffix(URL) :
    list = URL.split('.')
    return list[-1]

# 创建路径
def opendir(path) :
    if os.path.exists(path) is False:  # 判断是否已存在该资源路径, 不存在就新建一个路径
        os.mkdir(path)

# 如果后面带k..就去掉然后*1000
def getPins(string) :
    string = string.strip()
    if string.endswith('k') :
        string = string[0:-1]
        ret = int(float(string) *1000)
    else :
        ret = string.split(' ')[0]
        ret = ret.replace(',', '')
        ret = int(ret)

    # logging.info('str = ' + str(ret))
    return ret
