#coding=utf-8
import random

from bs4 import BeautifulSoup

from functions.historyDB import _historyDB
# from functions.tools import StringClean
from functions.multthreading_download import *

from model.pic import _pic

from standard.logger import *
from standard.requestsClient import _requestsClient

# 引入配置对象DesiredCapabilities
from crawler_myTools.selenium_tools.webdriver import webdriver_PhantomJS


# 需要给定的超参数
# 0、数据存储的文件夹路径（需要提前创建文件夹）
Rootpath = os.path.join('E:\\', '站点图片下载', 'pinterest', 'percylee1817')
# 1、给定的URL
# givenURL = 'https://www.pinterest.com/percylee1817/inspiration-giver/'
# givenURLs = [ 'https://www.pinterest.com/percylee1817/eastern-paint/'
#             , 'https://www.pinterest.com/percylee1817/machine/'
#              , 'https://www.pinterest.com/yuguenkim/sci-fi-conceptart/'
#             ]

# 2、代理的端口号
proxyPort = 60425    # 蓝灯


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

        global proxyPort
        self.client.setProxyPort(proxyPort) # 设置代理端口
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
            logging.warning('在线解析有问题 = = 暂时用不了')
            return
            logging.warning('正在发送URL请求, 准备获取资源列表...........')
            PageSource, status = self.getPageSource(givenURL)
            # 请求资源失败，直接return False
            if status == False :
                return False

        # 3 获取实际需要的图片数量picNum（不一定是源代码里面的所有图片）
        soup = BeautifulSoup(PageSource, "html.parser")
        Pins = soup.select('[class="_ta _s7 _s8 _s9 _tc _5l _sa _sk _si _sc"]')
        if Pins is not None:
            picNum = getPins(Pins[0].get_text())
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
        if len(picList) !=0 :
            logging.warning('\n............................................')
            # 只下载subsetLen张资源..(这里可以改小，用于测试)
            subsetLen = len(picList)
            succ, fail = downloadPicByList(picList[:subsetLen], self.client.requestsGet, maxThread=50)

            logging.warning('............................................')
            logging.warning('...总共下载成功'+str(succ)+'张图片 / 下载失败'+str(fail)+'张图片...')
        else :
            logging.warning('唔.. 不需要进行下载了..')

        # work 成功
        return True
        # 跳转到下一页
        # page += 1

    # 用模拟浏览器的方式，获取页面源代码
    def getPageSource(self, givenURL) :
        # 创建一个模拟浏览器
        driver = webdriver_PhantomJS()

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
        while True :
            Pins = None
            try :
                Pins = driver.find_element_by_css_selector("span:nth-child(1)>b")
            except :
                logging.warning('没有找到Pins属性..')
            # 正确的情况
            if Pins is not None :
                picNum = getPins(Pins.text)
                break
            else :
                if cnt !=0 and cnt %1 == 0 :
                    logging.warning('还是不行.. 尝试重头再来一次..')
                    # 退出模拟浏览器
                    driver.close()
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
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

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
        logging.warning('网页源代码一缓存只路径 : '+os.path.join(self.DBpath, self.album+'_page_source.html'))

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
        _pictList = soup.findAll("div", {"class": "_vz _2h _w0"})
        # logging.warning("从源代码中扫描到的图片资源数量 : "+str(len(_pictList)))
        if picNum >= 1000 :
            _pictList = _pictList[:len(_pictList)]
        else :
            _pictList = _pictList[:picNum]
        # logging.warning("Just need pic resources : "+str(picNum))
        for pic in _pictList:
            imgObj = pic.find("div", {"class": "_0 _3m _2q"})
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


# 程序入口
if __name__ == '__main__':
    # 初始化系统日志存储
    InitLogger()

    # 遍历所有给定的URL
    with open('givenURL.txt', 'r') as infile :
        for givenURL in infile.readlines() :
            logging.warning('---------------------------------------------------------------------------------------------------')
            logging.warning('givenURL is '+givenURL)

            # work
            while True :
                spider = spiderWay_picDownloader(Rootpath)
                # test
                # spider.client.requestsGet('https://i.pinimg.com/originals/65/23/66/65236656825be0adb17a2f1d54f3bfab.jpg')
                # spider.client.requestsGet('https://i.pinimg.com/originals/6c/36/2c/6c362c4906b447c6620c09c250001f93--black.jpg')

                # spider.client.requestsGet('https://i.pinimg.com/originals/e5/7a/21/e57a21d69608c9cdb9502cc680a85778.jpg')
                # work方法，成功运行，会返回True
                if spider.work(givenURL) :
                    break

    logging.warning('爬虫结束啦！')