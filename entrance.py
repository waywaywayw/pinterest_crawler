# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-10-15
"""
from pprint import pprint
import random
from bs4 import BeautifulSoup

from functions.historyDB import _historyDB
# from functions.tools import StringClean
from functions.multthreading_download import *
from model.pic import _pic
from standard.logger import *
from standard.requestsClient import _requestsClient

from atools_crawler.selenium.webdriver import MyWebDriver
from atools_jsonDB.myjsondb import MyjsonDB
import config


# 1、给定的URL
# test
# givenURLs = [ 'https://www.pinterest.com/percylee1817/eastern-paint/'
#             , 'https://www.pinterest.com/percylee1817/machine/'
#              , 'https://www.pinterest.com/yuguenkim/sci-fi-conceptart/'
#             ]


# 用到的超参数
# 0、网址
raw_URL = 'https://www.pinterest.com/'
# 1、目标网站的编码
SiteCode = 'utf-8'


# 爬虫主体
class spiderWay_picDownloader :
    client = ""

    # 构造方法。初始化client会话对象
    def __init__(self, Rootpath):
        self.client = _requestsClient()
        self.client.setProxyPort(config.proxyPort) # 设置代理端口
        # DBpath路径就是用户目录
        self.DBpath = Rootpath

    # 工作流程主体
    def work(self, givenURL) :
        # 0 从givenURL中解析出album
        scannedAlbum = StringClean(givenURL.split('/')[-2])
        # logging.warning('对应的album name is ' + scannedAlbum)
        # album是资源存放的具体文件夹名
        self.album = scannedAlbum

        # 1 确认用户目录存在
        try :
            opendir(self.DBpath)
        except Exception :
            logging.warning('指定目录Rootpath 不存在啊不存在！')

        # 创建album文件夹
        opendir(os.path.join(self.DBpath, self.album))

        # 载入历史数据库（路径数据库+URL数据库）
        self.historyData = _historyDB(self.DBpath)
        # self.historyData.loadURLDatabase()
        # self.historyData.loadPathDatabase()

        # 2 获取（或载入）页面源代码, 保存在PageSource变量....
        if os.path.exists(os.path.join(self.DBpath, self.album+'_page_source.html')):
            logging.warning('发现对应album的缓存源代码.. 准备加载..')
            PageSource = open(os.path.join(self.DBpath, self.album+'_page_source.html'), 'r', encoding=SiteCode).read()

        else:
            # logging.warning('在线解析有问题 = = 暂时用不了')
            # return
            logging.warning('正在发送URL请求, 准备获取资源列表...........')
            PageSource, status = self.getPageSource(givenURL)
            # 请求资源失败，直接return False
            if status == False :
                return False

        # 3 获取实际需要的图片数量picNum（不一定是源代码里面的所有图片）
        soup = BeautifulSoup(PageSource, "html.parser")
        Pins_elem = soup.find('div', {'class': '_w6 _0 _1 _2 _w9 _2y _3 _d _b _6'})
        if Pins_elem is not None:
            picNum = getPins(Pins_elem.get_text())
        else:
            logging.warning('在缓存源代码中没找到Pins 属性?')
            picNum = 0
            exit(1)

        # 4 通过页面源代码和picNum获取资源列表..
        picList = self.getPicListByPageSource(PageSource, picNum)
        logging.warning('需要的图片数量 :'+str(len(picList)))
        # logging.warning([pic for pic in picList])

        # 5 去重API
        self.historyData.removeDuplicate(picList)

        # 6 下载API
        logging.warning('准备正式下载资源.. 需要下载的资源数量 : %d' %len(picList))
        if len(picList) != 0:
            logging.warning('\n............................................')
            # 只下载subsetLen张资源..(这里可以改小，用于测试)
            subsetLen = len(picList)
            succ, fail = downloadPicByList(picList[:subsetLen], self.client.requestsGet, maxThread=config.threading_num, verbose=True)
            logging.warning('............................................')
            logging.warning('...总共下载成功'+str(succ)+'张图片 / 下载失败'+str(fail)+'张图片...')
        else:
            logging.warning('唔.. 不需要进行下载了..')

        # work 成功
        return True
        # 跳转到下一页
        # page += 1

    # 用模拟浏览器的方式，获取页面源代码
    def getPageSource(self, givenURL) :
        # 创建一个模拟浏览器
        my_driver = MyWebDriver()
        driver = my_driver.real_driver()

        # 访问givenURL
        try :
            # givenURL = 'https://www.pinterest.com/percylee1817/deer/'
            driver.get(givenURL)
            time.sleep(1)
        except Exception as e :
            print("异常原因 %s" %e)
            driver.get_screenshot_as_file('test.png')

        # 取得图片数量Pins...
        cnt = 0
        # my_driver.page_to_file('temp_html.html')
        while True :
            Pins = None
            try :
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                Pins_elem = soup.find('div', {'class': '_w6 _0 _1 _2 _w9 _2y _3 _d _b _6'})
                Pins = Pins_elem.get_text()
            except :
                logging.warning('没有找到Pins属性..')
            # 正确的情况
            if Pins is not None :
                picNum = getPins(Pins)
                break
            else :
                if cnt !=0 and cnt %1 == 0 :
                    logging.warning('还是不行.. 尝试重头再来一次..')
                    # 退出模拟浏览器
                    # driver.close()
                    driver.quit()
                    return None, False
                else :
                    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(1)
                    logging.warning('滑一下.. 然后等待1秒...')
                    cnt += 1

        logging.warning('album picNum : '+str(picNum))

        # 不停的滑啊滑啊
        same = 0
        pre_len = 0
        while True:
            # 给浏览器发送滑的操作
            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            js = "var q=document.documentElement.scrollTop=99100000"
            driver.execute_script(js)
            # 滑一次休息0.5-0.6秒
            time.sleep(random.uniform(0.4, 0.6))

            # 找最新的picNum
            # list = driver.find_elements_by_css_selector("div.wsh8N")
            list = driver.find_elements_by_css_selector("div.Grid__Item")

            # 统计当前页面的资源数量
            cur_len = len(list)
            logging.warning('scanned pic resource : ' + str(cur_len))
            if picNum < 1000 and cur_len >= picNum :
                break
            if picNum >=1000 and cur_len+5 >= picNum :  # 大于1000的，显示不了个位数，给一个补偿量5
                picNum = cur_len
                break

            # 一直刷不出来.. 就跳出循环吧...
            if cur_len == pre_len :
                same += 1
                if same >= 10 :
                    break
            else :
                same = 0

            pre_len = cur_len

        # page_source = driver.page_source
        page_source = driver.page_source.split('More ideas')[0]

        # 保存页面源代码 (encoding 很重要)
        with open(os.path.join(self.DBpath, self.album+'_page_source.html'), 'w', encoding=SiteCode) as file :
            file.write(page_source)
        logging.warning('网页源代码缓存至路径 : '+os.path.join(self.DBpath, self.album+'_page_source.html'))

        # 退出模拟浏览器
        driver.close()
        driver.quit()
        # 返回页面源代码和运行状态
        return page_source, True

    # 通过页面源代码 获取资源列表...（不同站点需要修改的部分-----------------------------）
    # pageSource 是页面源代码, 直接用BeautifulSoup载入
    # picNum是指定需要下载的图片数量
    def getPicListByPageSource(self, pageSource, picNum=-1) :
        # BeautifulSoup 解析
        soup = BeautifulSoup(pageSource, "html.parser")
        # soup = BeautifulSoup(open(os.path.join(self.DBpath, 'html.txt'), 'rb').readline(),  "html.parser")
        #print(soup)

        # 解析得到的页面，获取帖子列表... beautifulSoup各种找...（不同站点需要修改的部分-----------------------------）
        picList = []
        _pictList = soup.findAll("div", {"class": "Grid__Item"})
        # logging.warning("从源代码中扫描到的图片资源数量 : "+str(len(_pictList)))
        if picNum >= 1000:
            _pictList = _pictList[:len(_pictList)]
        else :
            _pictList = _pictList[:picNum]
        # logging.warning("Just need pic resources : "+str(picNum))
        for pic in _pictList:
            imgObj = pic.find("div", {"class": "GrowthUnauthPinImage"})
            # textObj = pic.find("div", {"class": "list-item-desc-title"})
            # print(imgObj)
            # print(textObj)
            if imgObj is None:
                logging.warning('没找到图片对象..?')
                continue
            else :
                __pic = _pic()
                # 获取图片链接...（不同站点需要修改的部分--------------------------------------------------------）
                __pic.URL = imgObj.find('img').attrs['src']
                # logging.warning("imgURL :"+__pic.URL)
                # 获取更高分辨率的图片链接
                # __pic.URL = __pic.URL.split(' ')[-2]
                list = __pic.URL.split('/')
                list[3] = 'originals'
                __pic.URL = "/".join(list)
                # print("biggest imgURL :" + __pic.URL)
                # 没有名字，将网站随机生成的URL中的值作为名字
                __pic.name = __pic.URL.split('/')[-1]
                # print("imgName :" + __pic.name)
                # 构造并清洗图片album
                __pic.album = os.path.join(self.DBpath, self.album)
                # print("imgAlbum :" + __pic.album)
                # 将图片加入列表
                picList.append(__pic)

        # 返回帖子列表（pic类列表）
        return picList


def get_board_list(username):
    borad_list = []
    output_path = os.path.join('cache', 'username', username + '.txt')

    if os.path.exists(output_path): # 已存在，直接读取
        logging.warning('发现缓存文件.. 直接载入..')
        with open(output_path, 'r', encoding='utf8') as fin:
            for line in fin:
                borad_list.append(line.strip())
        logging.warning('用户名{} 下共有 {} 个board.'.format(username, len(borad_list)))
    else:   # 通过请求 获取板子列表
        db_path = os.path.join('cache', 'login_cookie.json')
        my_json = MyjsonDB(db_path)

        if not my_json.resource_dict:   # 登录。拿到cookie
            my_driver = MyWebDriver(params={'headless' : config.headless, 'local_config': True, 'profile_dir': config.profile_dir})
            # my_driver = MyWebDriver(params={'headless': False})   # 为啥这样获取的cookie不能用？
            driver = my_driver.real_driver()
            # 登录
            # my_driver.login(
            #     login_url='https://www.pinterest.com/login/?referrer=home_page',
            #     username_elem="#email",
            #     username=config.email,
            #     passwd_elem="#password",
            #     passwd=config.passwd,
            #     login_button_elem='button[class="red SignupButton active"]',
            #     login_click_type=1
            # )
        else:
            my_driver = MyWebDriver(params={'headless': config.headless})
            driver = my_driver.real_driver()
            # 访问主页
            driver.get('https://www.pinterest.com/')
            # 添加cookie到浏览器
            cookie_dict = my_json.resource_dict
            for cookie in cookie_dict:
                driver.add_cookie(cookie)
            print('cookie已添加到浏览器中：\ncookie_dict = {}'.format(cookie_dict))

        # 再次访问主页，可能会得到新的cookie
        driver.get('https://www.pinterest.com/')
        # 保存/更新 cookie
        cookie_dict = driver.get_cookies()
        print('cookie已保存：\ncookie_dict = {}'.format(cookie_dict))
        my_json.load_from_dict(cookie_dict)
        my_json.write_to_file()

        # 获取board列表
        logging.warning('开始访问指定用户名{}的主页'.format(username))
        driver.get(raw_URL+username)
        # my_driver.page_to_file('temp.html')
        # 下滑直到页面稳定
        my_driver.silde_down_until_stable(monitor_elem='div[class="_49 _6s _7j _h _xt _4q"]')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        borad_elem_list = soup.findAll('div', {'class': "_49 _6s _7j _h _xt _4q"})
        for board_elem in borad_elem_list:
            board_href = raw_URL[:-1] + board_elem.find('a')['href']
            borad_list.append(board_href)
        logging.warning('用户名{} 下共有 {} 个board.'.format(username, len(borad_list)))
        # 保存board列表
        with open(output_path, 'w', encoding='utf8') as fout:
            for board in borad_list:
                fout.write(board+'\n')
        logging.warning('已将板子列表写入缓存')
        driver.quit()
    return borad_list


def work(board_URL):
    logging.warning(
        '---------------------------------------------------------------------------------------------')
    logging.warning('board_URL : ' + board_URL)
    while True:
        spider = spiderWay_picDownloader(config.Rootpath)
        # spider.client.requestsGet('https://i.pinimg.com/originals/65/23/66/65236656825be0adb17a2f1d54f3bfab.jpg')
        # work方法，成功运行，会返回True
        if spider.work(board_URL):
            break


# 程序入口
if __name__ == '__main__':
    # 初始化系统日志存储
    InitLogger()

    if config.mode == 'URL':
        # 读取 givenURL.txt 所有的URL, 并开始下载
        with open('givenURL.txt', 'r') as infile:
            for board_URL in infile.readlines():
                work(board_URL)

    elif config.mode.endswith('username'):
        with open('givenUserName.txt', 'r') as fin:     # 读取 givenUserName.txt 所有的用户名
            for username in fin:
                # 获取指定用户名的板子列表（会保存板子列表）
                board_list = get_board_list(username.strip())
                if config.mode != 'only_username':
                    # 遍历并下载所有板子
                    for board_URL in board_list:
                        work(board_URL)
    else:
        logging.warning('执行模式错误！请检查config.py里的mode项')

    logging.warning('爬虫执行完毕！')