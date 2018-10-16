# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-04
"""

import os
import time
import random
import logging
from selenium import webdriver

from atools_crawler.common.UserAgent import random_ua


class MyWebDriver(object):
    """
    selenium官方中文文档：https://selenium-python-zh.readthedocs.io/en/latest/getting-started.html
    """

    def __init__(self, driver_type=2, params=None):
        """
        创建一个模拟浏览器。

        :param driver_type: 浏览器类型。
            目前支持3种浏览器：0代表PhantomJS, 1代表Filefox, 2代表Chrome
        :param params: 创建浏览器时的参数。
            目前有如下参数：headless 无头模式,
                            images 禁止加载图片, js 禁止加载js,
                            UA 使用随机UA, proxy 代理地址
        """
        # 获取当前文件所在文件夹的地址
        current_path = os.path.dirname(os.path.abspath(__file__))
        # 浏览器类型（谷歌、火狐、或者其他啥）
        self._driver_type = int(driver_type)
        # 浏览器实体
        self._driver = None
        # 浏览器驱动的地址。之后默认放在'selenium_tools/Scripts'目录下
        self._executable_path = ""
        # 默认参数值
        self._params = {'headless': True,
                        'images': False, 'js': True,
                        'ua': False, 'proxy': None,
                        'local_config': False, 'profile_dir' : None}
        if params is not None:
            self._params.update(params)

        if driver_type == 0:
            self._driver = self.PhantomJS()
        elif driver_type == 1:
            self._driver = self.Firefox()
        elif driver_type == 2:
            self._executable_path = os.path.join(current_path, 'Scripts', 'chromedriver.exe')
            # self._executable_path = os.path.join(r'C:\Program Files (x86)\Google\Chrome\Application', 'chromedriver.exe')
            self._driver = self.Chrome()
        else:
            raise TypeError('没有找到需要的浏览器类型！')
        # 创建完浏览器后，设置一些通用的设置。（比如超时选项，屏幕分辨率等）
        self.set_something()

    def set_something(self):
        # 根据桌面分辨率来定，主要是为了抓到验证码的截屏
        # self._driver.set_window_size(configure.windowHeight, configure.windowWidth)
        # 窗口最大化
        # self._driver.maximize_window()

        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，不过driver.get()没有timeout选项
        self._driver.implicitly_wait(30)
        #  设置加载页面超时。以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        self._driver.set_page_load_timeout(60)
        # 设置10秒脚本超时时间
        self._driver.set_script_timeout(30)

    def get(self, url):
        response = self._driver.get(url)
        return response

    def Chrome(self):
        params = self._params
        # 开启配置项 chrome_options
        chrome_options = webdriver.ChromeOptions()

        if params['headless']:    # 无头模式
            chrome_options.add_argument('--headless')
        if params['proxy'] is not None:       # 设置代理  未试用过？！
            # chrome_options.add_argument("--proxy-server=http://127.0.0.1:10152")
            chrome_options.add_argument(params['proxy'])
        if params['local_config']:  # 测试报错！
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("user-data-dir=" + os.path.abspath(params['profile_dir']))
            pass

        config_prefs = {}
        if not params['images']:  # 禁止加载图片
            config_prefs['images'] = 2
        if not params['js']:      # 禁止加载javascript脚本
            config_prefs['javascript'] = 2
        if params['ua']:          # 使用随机UA
            config_prefs['User-Agent'] = random_ua()
        if config_prefs:
            prefs = {'profile.default_content_setting_values' : config_prefs}
            chrome_options.add_experimental_option("prefs", prefs)
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         # 'images': 2,  # 不加载图片
        #         'javascript': 2,  # 不加载JS
        #         # "User-Agent": random_ua()  # 随机UA
        #     }
        # }
        # 其他的可以参考：https://blog.csdn.net/zwq912318834/article/details/78933910
        # 还可参考：https://www.zhihu.com/question/35547395

        # 创建浏览器
        driver = webdriver.Chrome(chrome_options=chrome_options,
                                  executable_path=self._executable_path)
        return driver

    def login(self, login_url, username_elem, username, passwd_elem, passwd, login_button_elem, login_click_type=1, verbose=True):
        driver = self._driver
        if verbose:
            print('开始访问登录页面..')
        try:
            driver.get(login_url)
            driver.find_element_by_css_selector(username_elem).send_keys(username)
            driver.find_element_by_css_selector(passwd_elem).send_keys(passwd)

            if login_click_type==1: # 之前的做法1
                driver.find_element_by_css_selector(login_button_elem).click()
            elif login_click_type==2: # 之前的做法2
                button = driver.find_element_by_css_selector(login_button_elem)
                driver.execute_script("$(arguments[0]).click()", button)
            else:
                print('报错！')
            # 较新的做法。    据说可以适用于vue？ 不过需要定制.. 暂时只能根据class属性来找到元素..
            # js = 'document.getElementsByClassName("red SignupButton active")[0].click();'
            # driver.execute_script(js)

            time.sleep(1)
            if verbose:
                print('发送登录请求完毕..')
        except Exception as e:
            print(e)
            print('登录时出现错误！是否访问网页失败 或者 参数有误？')
            exit(1)
            
    def silde_down_until_stable(self, monitor_elem="", step_delay=0.2, until_num=-1, until_time=10, verbose=True):
        """
        不停模拟下滑页面，直到获取所有监控元素。

        :param step_delay: 每次下滑的间隔时间。
        :param monitor_elem: 需要监控的元素。（监控元素满足了条件，即跳出循环）
        :param until_num: 不停下滑，直到监控元素的数量达到until_num. （until_num>0 时，进入 until_num 模式。）
        :param until_time: 不停下滑，直到until_time秒之内监控元素的数量保持不变. （until_num<0 时，进入 until_time 模式。）
        :return: 无
        """
        driver = self._driver
        # 不停的滑啊滑啊
        same = 0
        pre_len = 0
        start_time = time.time()
        while True:
            # 下滑一次，并休息约step_delay秒
            self.slide_down()
            time.sleep(random.uniform(min(step_delay-0.1, 0.1), step_delay+0.1))

            # 找到监控元素
            elem_list = driver.find_elements_by_css_selector(monitor_elem)
            # 统计当前页面的资源数量
            cur_len = len(elem_list)
            if verbose:
                logging.warning('扫描到的资源数量 : {}'.format(cur_len))

            # 测试是否满足跳出条件
            if until_num >0:    # until_num模式
                pass
            else:   # until_time模式
                if cur_len == pre_len:
                    # 如果值满足条件，就跳出循环
                    if (time.time()-start_time) >= until_time:
                        break
                else:
                    # 重新开始统计一些值
                    start_time = time.time()

            pre_len = cur_len

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
        # 我之前的做法
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def page_to_file(self, output_path, encoding='utf8'):
        if self._driver.page_source is None or self._driver.page_source=="":
            print('页面源代码为空白！')
            return
        with open(output_path, 'w', encoding=encoding) as fout:
            fout.write(self._driver.page_source)
            print('已写入文件:', output_path)

    def real_driver(self):
        return self._driver

    def PhantomJS(self):
        # 引入配置对象DesiredCapabilities
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        # 开启配置项dcap
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 随机选取UA
        dcap["phantomjs.page.settings.userAgent"] = random_ua()
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

    def Firefox(self):
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



# 要兼容老版本代码，所有没有删掉这个函数
def PhantomJS():
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
