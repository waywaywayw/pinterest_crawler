# -*- coding: utf-8 -*-
"""
@author: waywaywayw
@date: 2018/10/14
"""
import os

# 需要给定的超参数
# 1. 数据存储的文件夹路径（需要提前创建文件夹）
Rootpath = os.path.join('E:\\', '站点图片下载', 'pinterest', 'percylee1817')

# 2. 代理的端口号
location = 'way_dorm'    # way_company, way_dorm, Li
if location=='way_dorm':
    proxyPort = 54422    # 蓝灯
elif location=='way_company':
    proxyPort = 60562    # 蓝灯
else:
    pass

# 3. 执行模式
mode = 'username'   # username, URL
# username模式需要username ; 登录用的邮箱和密码
username = 'percylee1817'
email = 'wjwyhdz@126.com'
passwd = 'selinawjw23tl'