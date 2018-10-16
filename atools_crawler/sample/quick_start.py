# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/8
"""

import os
import re
import numpy as np
import pandas as pd
import atools_crawler.requests
from pprint import pprint
from bs4 import BeautifulSoup

from atools_crawler.requests.common_config import MyRequestsConfig
from atools_crawler.common.UserAgent import random_ua

from atools_crawler.selenium.webdriver import MyWebDriver


def selenium_main():
    driver = MyWebDriver(driver_type=2)
    # url = "http://www.baidu.com"
    url = 'https://www.pinterest.com/percylee1817/machine'
    driver.get(url)
    driver.real_driver()
    driver.slide_down()


def main():
    # 1. 设置请求参数
    proxies = {
        'http': 'http://127.0.0.1:54422',
        'https': 'https://127.0.0.1:54422',
    }
    headers = {'Connection': 'Keep-Alive'
               # ,'host': 'zhannei.baidu.com'
               # ,'ref??': ''
                , 'User-Agent': random_ua()
    }
    params = {
    }
    # 2. 发送请求
    url = "http://www.baidu.com"
    # requests.get(url, headers=headers, proxies=proxies, params=params)
    response = atools_crawler.requests.get(url, headers=headers)
    # 3. 解析回复
    page_source = response.content.decode('utf8')
    # 将页面源代码写到临时html文件
    # with open('temp.html', 'r', encoding='utf8') as fout:
    #     fout.write(page_source)
    # or 直接输出页面源代码
    pprint(page_source)


if __name__ == "__main__":
    # main()
    selenium_main()