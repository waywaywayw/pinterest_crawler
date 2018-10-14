# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-04
"""

import os, time
from selenium import webdriver

from atools_crawler.common.UserAgent import get_random_UA


class MyWebDriver(object):
    """
    selenium官方中文文档：https://selenium-python-zh.readthedocs.io/en/latest/getting-started.html
    """

    def __init__(self, driver_type=2):
        """
        按照指定浏览器类型，创建一个浏览器。
        :param driver_type: 目前支持3种浏览器：0代表PhantomJS, 1代表Filefox, 2代表Chrome
        """
        # 获取当前文件所在文件夹的地址
        current_path = os.path.dirname(os.path.abspath(__file__))
        # 浏览器类型（谷歌、火狐、或者其他啥）
        self._driver_type = int(driver_type)
        # 浏览器实体
        self._driver = None
        # 浏览器驱动的地址。之后默认放在'selenium_tools/Scripts'目录下
        self._executable_path = ""

        if driver_type == 0:
            self._driver = self.webdriver_PhantomJS()
        elif driver_type == 1:
            self._driver = self.webriver_Firefox()
        elif driver_type == 2:
            self._executable_path = os.path.join(current_path, 'Scripts', 'chromedriver.exe')
            self._driver = self.webdriver_Chrome()
        else:
            raise TypeError('没有找到需要的浏览器类型！')

        # 创建完浏览器后，设置一些通用的设置。（比如超时选项，屏幕分辨率等）
        self.set_something()

    def set_something(self):
        # 根据桌面分辨率来定，主要是为了抓到验证码的截屏
        # self._driver.set_window_size(configure.windowHeight, configure.windowWidth)

        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，不过driver.get()没有timeout选项
        self._driver.implicitly_wait(30)
        #  设置加载页面超时。以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        self._driver.set_page_load_timeout(60)
        # 设置10秒脚本超时时间
        self._driver.set_script_timeout(30)

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
                # 'javascript': 2,  # 不加载JS
                "User-Agent": get_random_UA()  # 随机UA
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # 无头模式
        chrome_options.add_argument('--headless')
        # 设置代理  未试用？！
        # chrome_options.add_argument("--proxy-server=http://202.20.16.82:10152")
        # 其他的可以参考：https://blog.csdn.net/zwq912318834/article/details/78933910
        # 还可参考：https://www.zhihu.com/question/35547395

        # 创建浏览器
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=self._executable_path)
        return driver

    def webdriver_PhantomJS(self):
        # 引入配置对象DesiredCapabilities
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        # 开启配置项dcap
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 随机选取UA
        dcap["phantomjs.page.settings.userAgent"] = get_random_UA()
        # 设置不载入图片
        dcap["phantomjs.page.settings.loadImages"] = False
        # 设置代理
        # service_args = ['--proxy=127.0.0.1:4860', '--proxy-type=socks5']  # socks5 ?? 还是http??
        service_args = []

        # 创建浏览器
        driver = webdriver.PhantomJS(desired_capabilities=dcap,
                                     executable_path=self._executable_path,
                                     service_args=service_args)
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

    def slide_down(self):
        """向下滑动窗口
        """
        driver = self._driver
        # 将滚动条移动到页面的底部
        js = "var q=document.documentElement.scrollTop=99100000"
        driver.execute_script(js)
        # time.sleep(3)
        # 将滚动条移动到页面的顶部
        # js = "var q=document.documentElement.scrollTop=0"
        # driver.execute_script(js)
        # time.sleep(3)
        # 若要对页面中的内嵌窗口中的滚动条进行操作，要先定位到该内嵌窗口，在进行滚动条操作
        # js = "var q=document.getElementById('id').scrollTop=100000"
        # driver.execute_script(js)
        # time.sleep(3)
        # js = "var q=document.body.scrollTop=99100000"   # 实测Chrome用这个设置没用~
        # driver.execute_script(js)
        # time.sleep(3)

    def page_to_file(self, output_path, encoding='utf8'):
        if self._driver.page_source is None or self._driver.page_source=="":
            print('页面源代码为空白！')
            return
        with open(output_path, 'w', encoding=encoding) as fout:
            fout.write(self._driver.page_source)
            print('已写入文件:', output_path)

    def real_driver(self):
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
