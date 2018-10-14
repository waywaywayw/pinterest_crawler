# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018/10/8
"""

import os
import re
import time
import numpy as np
import pandas as pd
import atools_crawler.requests
from pprint import pprint
from bs4 import BeautifulSoup

from atools_crawler.requests.common_config import MyRequestsConfig
from atools_crawler.common.UserAgent import get_random_UA

from atools_crawler.selenium.webdriver import MyWebDriver


def selenium_main():
    driver = MyWebDriver(driver_type=2)
    # url = "http://www.baidu.com"
    url = 'https://www.pinterest.com/percylee1817/machine/'
    driver.get(url)

    # while True:
    for i in range(30):
        soup = BeautifulSoup(driver.driver().page_source, 'html.parser')
        # soup.findAll('div', {'class':'_uc _4h _ud'})
        pic_cnt = len(soup.findAll('div', {'class':'Grid__Item'}))
        print('找到的图片数：', pic_cnt)
        driver.slide_down()
        print('模拟下滑执行完毕')
        time.sleep(1)

def main():
    # 1. 设置请求参数
    proxies = {
        'http': 'http://127.0.0.1:54422',
        'https': 'https://127.0.0.1:54422',
    }
    headers = {'Connection': 'Keep-Alive'
               # ,'host': 'zhannei.baidu.com'
               # ,'ref??': ''
                , 'User-Agent': get_random_UA()
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