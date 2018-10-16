# -*- coding: utf-8 -*-
"""
@author: waywaywayw
@date: 2018/10/14
"""
import os

# 需要给定的超参数
location = 'way_company'  # way_company, way_dorm, Li
if location == 'way_dorm':
    profile_dir = r'C:\Users\way\AppData\Local\Google\Chrome\User Data'  # 谷歌浏览器的用户数据文件夹。字符串中的duoyi估计要改为你自己的电脑名
    Rootpath = os.path.join('E:\\', '站点图片下载', 'pinterest', 'percylee1817')  # 数据存储的文件夹路径（需要提前创建文件夹）
    proxyPort = 54422  # 蓝灯的端口号
elif location == 'way_company':
    profile_dir = r'C:\Users\duoyi\AppData\Local\Google\Chrome\User Data'
    Rootpath = os.path.join('D:\\', 'percylee1817')
    proxyPort = 60562
elif location == 'Li':
    profile_dir = r'C:\Users\???\AppData\Local\Google\Chrome\User Data'
    Rootpath = os.path.join('D:\\', '???', 'percylee1817')
    proxyPort = '???'
else:
    pass


# 选择执行模式
"""
URL模式：
    只需要给定 givenURL.txt
username模式：
    需要给定 givenUserName.txt
    需要给定 登录用的邮箱和密码
only_username模式：
    只下载 givenUserName.txt 中所有用户名的板子列表，不下载板子
"""
mode = 'only_username'   # username, URL, only_username
# 只username模式需要给定email和passwd
email = ''
passwd = ''


# 一些小参数
headless = True    # 浏览器无头模式
threading_num = 10     # 下载资源时，开启的多线程数量
