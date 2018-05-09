from selenium import webdriver
# 引入配置对象DesiredCapabilities
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def webdriver_PhantomJS() :
    # 模拟浏览器..获取页面...
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        dcap["phantomjs.page.settings.userAgent"] = ua
        # 不载入图片，爬页面速度会快很多
        dcap["phantomjs.page.settings.loadImages"] = False
        # 设置代理
        # service_args = ['--proxy=127.0.0.1:4860', '--proxy-type=socks5']

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