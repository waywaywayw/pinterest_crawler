import logging
import os
import time


# 定义历史数据库
# 目的是判重，不下载重复资源
class _historyDB :
    # 类初始化
    def __init__(self, RootPath=""):
        # self.contentFolder = u"抓取内容"
        self.RootPath = RootPath
        '''
        self.dbName = os.path.join(RootPath, "url.db")              # 1、定义数据库文件名
        # self.createFolder(self.contentFolder)    # 2、创建内容存储目录
        self.urlDB = set()                 # 3、创建内存数据库
        self.pathDB = set()                 # 4、创建路径数据库（适合资源有明确的文件名的情况）
        '''

     # 读取URL数据库以获取爬过的网页地址
    # def loadURLDatabase(self):
    #      isExists = os.path.exists(self.dbName)    # 4、首先判断是否是首次运行，如果数据库文件不存在则创建一下
    #      if not isExists:
    #          logging.info(u"创建URL数据库文件：'" + self.dbName + u"'")
    #          f = open(self.dbName, 'w+')
    #          f.write("#Create time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + '\n')
    #          f.close()
    #          return
    #      db = open(self.dbName, 'r')          # 5、从磁盘中加载数据库
    #      for line in db.readlines():
    #          if not line.startswith('#'):    # 注释性的信息
    #              self.urlDB.add(line.strip('\n'))    # 读取文件中的URL, 保存进数据库
    #      db.close()
    #      logging.info(u"URL数据库加载完成！")

     # 获取所有已经获取爬过的网页图片的路径
    # def loadPathDatabase(self):
    #     for parent, dirnames, filenames in os.walk(self.RootPath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    #         for dirname in dirnames :   # 遍历每个相册
    #             for _parent, _dirnames, _filenames in os.walk(os.path.join(self.RootPath, dirname)) :  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    #                 for filename in _filenames: # 遍历相册里每个资源
    #                     # 将路径信息, 保存进数据库
    #                     self.pathDB.add(os.path.join(self.RootPath, dirname, filename))
    #
    #     logging.info(u"路径数据库加载完成！")

     # 追加URL数据, 写入URL数据库 和 当前内存中的URL数据库
    # def writeToDatabase(self, url):         # 6、在系统运行过程中，如需记录日志，追加日志内容即可
    #      # logging.info('有新追加的URL..')
    #      db = open(self.dbName, 'a', encoding='utf-8')
    #      # 如果是list ，那么就是pic的List
    #      if isinstance(url, list) :
    #          for urlData in url :
    #              db.write(urlData.URL + '\n')
    #              self.urlDB.add(urlData.URL)
    #              # 更新path数据库
    #              self.pathDB.add(os.path.join(urlData.album, urlData.name))

        # 单个的只是URL
        #  else :
        #     db.write(url + '\n')
        #     self.urlDB.add(url)
        #  db.close()

     # 判断资源是否已存在
    def IsExists (self, pic) :
         isExists = False

         # 先判断是否在路径数据库中（实体已经存在文件夹中）
         isExists = os.path.exists( os.path.join(pic.album, pic.name) )
         return isExists

         # if os.path.join(pic.album, pic.name) in self.pathDB :
         #     pass
             # 判断文件是否过小
             # fileSize = os.path.getsize(os.path.join(self.RootPath, pic.album, pic.name)) / 1024
             # logging.info('the file size is : %.3f KB' % (fileSize))
             # if( fileSize < 2 ) :
             #     isExists = False
             # # 文件大小正常
             # else :
             # isExists = True
             # # 在路径数据库中存在（实体已经存在文件夹中），但是没有存入路径的情况
             # if pic.URL not in self.urlDB :
             #     self.writeToDatabase(pic.URL)

         # 资源不存在的情况
         # elif pic.URL in self.urlDB :
             # logging.DEBUG("??? 应该是不会出现的情况：存在URL数据库中，但是实体文件不存在")
             # isExists = True
         #     isExists = False
         # else :
         #     isExists = False

         # 返回结果
         return isExists

    # 外界API
    def removeDuplicate(self, picList) :
        # 待删除的列表（这个删除方式感觉不太方便）
        delList = []

        raw_len = len(picList)
        cnt = 0
        for ix, pic in enumerate(picList):
            # 图片过滤（过滤重复）
            if self.IsExists(pic):
                delList.append(pic)
                cnt += 1
        logging.info('判重操作完毕.. 需要的'+str(raw_len)+'张图片中,有'+str(cnt)+'张图片已存在..')

        # 删掉列表中的元素
        for pic in delList :
            picList.remove(pic)

        return picList
