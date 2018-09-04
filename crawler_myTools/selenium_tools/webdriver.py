# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-04
"""

import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from crawler_myTools.common import UserAgent


class webdriver(object):
    """
    selenium官方中文文档：https://selenium-python-zh.readthedocs.io/en/latest/getting-started.html
    """

    def __init__(self, driver_type=2):
        """
        按照指定浏览器类型，创建一个浏览器。
        :param driver_type: 目前支持3种浏览器：0代表PhantomJS, 1代表Filefox, 2代表Chrome
        """
        # 浏览器类型（谷歌、火狐、或者其他啥）
        self._driver_type = int(driver_type)
        # 浏览器实体
        self._driver = None
        # 浏览器驱动的地址。之后默认放在'selenium_tools/Scripts'目录下
        self._executable_path = ""
        # 设置代理
        # self._service_args = ['--proxy=127.0.0.1:4860', '--proxy-type=socks5']
        self._service_args = []

        if driver_type == 0:
            self._driver = self.webdriver_PhantomJS()
        elif driver_type == 1:
            self._driver = self.webriver_Firefox()
        elif driver_type == 2:
            self._driver = self.webdriver_Chrome()
            self._executable_path = os.path.join('Scripts', 'chromedriver.exe')
        else:
            raise TypeError('没有找到需要的浏览器类型！')

        # 创建完浏览器后，设置一些通用的设置。（比如超时选项，屏幕分辨率等）
        self.set_something()

    def set_something(self):
        # 根据桌面分辨率来定，主要是为了抓到验证码的截屏
        # browser.set_window_size(configure.windowHeight, configure.windowWidth)

        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，不过driver.get()没有timeout选项
        self._driver.implicitly_wait(10)
        #  设置加载页面超时。以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        self._driver.set_page_load_timeout(60)
        # 设置10秒脚本超时时间
        self._driver.set_script_timeout(20)

    def get(self, url):
        response = self._driver.get(url)
        return response

    def webdriver_Chrome(self):
        # 开启配置项chrome_options
        chrome_options = webdriver.ChromeOptions()
        # 禁用加载图片
        # prefs = {"profile.managed_default_content_settings.images": 2}
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,  # 不加载图片
                'javascript': 2,  # 不加载JS
                "User-Agent": UserAgent.UA.get_random_ua()  # 随机UA
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # 无头模式
        chrome_options.add_argument('--headless')
        # 其他的可以参考：https://blog.csdn.net/zwq912318834/article/details/78933910

        # 创建浏览器
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=self._executable_path,
                                  service_args=self._service_args)
        return driver

    def webdriver_PhantomJS(self):
        # 引入配置对象DesiredCapabilities
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        # 开启配置项dcap
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 随机选取UA
        dcap["phantomjs.page.settings.userAgent"] = UserAgent.UA.get_random_ua()
        # 设置不载入图片
        dcap["phantomjs.page.settings.loadImages"] = False

        # 创建浏览器
        driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                     executable_path=self._executable_path)
        return driver

    def webriver_Firefox(self):
        profile = webdriver.FirefoxProfile()
        # profile.set_preference('permissions.default.image', 2)  # 某些firefox只需要这个
        # 设置下载地址
        profile.set_preference('browser.download.dir', 'E:\\')
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                               'application/rar;application/octet-stream;application/zip')
        # 禁用flash
        profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        driver = webdriver.Firefox(firefox_profile=profile,
                                   executable_path=self._executable_path)
        return driver

    def connect_test_0(self):
        """
        官方快速入门的测试代码。如果没有任何输出，说明一切正常。
        """
        driver = self._driver
        driver.get("http://www.python.org")
        assert "Python" in driver.title
        elem = driver.find_element_by_name("q")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source
        driver.close()

    def connect_test_1(self):
        """
        自己写的几个测试样例
        """
        driver = self._driver
        driver.get('http://1212.ip138.com/ic.asp')
        print('1: ', driver.session_id)
        print('2: ', driver.page_source)
        print('3: ', driver.get_cookies())
        print(driver.title)

    def connect_test_2(self):
        """
        自己写的几个测试样例
        """
        driver = self._driver
        driver.get('http://sahitest.com/demo/saveAs.htm')
        driver.find_element_by_xpath('//a[text()="testsaveas.zip"]').click()
        time.sleep(3)

    @property
    def driver(self):
        return self._driver


# 要兼容老版本代码，所有没有删掉这个函数
def webdriver_PhantomJS():
    # 引入配置对象DesiredCapabilities
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    dcap["phantomjs.page.settings.userAgent"] = ua
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    # 设置代理
    service_args = ['--proxy=127.0.0.1:4860', '--proxy-type=socks5']

    # 打开带配置信息的phantomJS浏览器
    PhantomJSPath = ''
    driver = webdriver.PhantomJS(desired_capabilities=dcap)
    # test driver
    # driver.get('http://1212.ip138.com/ic.asp')
    # print('1: ', driver.session_id)
    # print('2: ', driver.page_source)
    # print('3: ', driver.get_cookies())
    # logging.info(driver.title)
    driver.implicitly_wait(15)

    # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    #  以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    driver.set_page_load_timeout(30)
    # 设置10秒脚本超时时间
    driver.set_script_timeout(20)

    return driver
