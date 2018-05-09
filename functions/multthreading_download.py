import os
import time
import logging
import threading
from functions.tools import *

from tqdm import tqdm

# 线程互斥锁（用于保证多线程安全）
mutexLock = threading.Lock()


# 传入设置好参数的图片列表, 进行多线程下载
def downloadPicByList(picList, download_func, maxThread=40, verbose=False) :
    succ = 0
    fail = 0
    # 将pic list 切分
    pbar = tqdm(total=len(picList))
    for ix in range(0, len(picList), maxThread) :
        picList_subset = picList[ix : ix+maxThread]
        threads = []

        # 遍历切分好的列表
        for _ix, pic in enumerate(picList_subset) :
            # 创建线程.. 调用下载资源API..
            threads.append(downloadThread(func=downloadPicByOne, args=(pic, ix+_ix, download_func)))

        # 并行开始
        for t in threads:
            time.sleep(0.3)
            t.start()

        # 主线程阻塞，等待全部子线程任务完成
        for _ix, t in enumerate(threads) :
            t.join()
            if t.get_result().status_code != 200:
                fail += 1
            else:
                succ += 1
            pbar.update(1)
        # 下载完一个picList_subset.. 休息2秒..
        time.sleep(1)

    # 返回下载成功和失败的数量
    return succ, fail

# 下载单个图片
def downloadPicByOne(pic, idx, download_func, verbose=False):
    # 输出资源地址和URL
    if verbose :
        # logging.info("resourcePath :"+pic.album)
        logging.info('第' + str(idx) + '张图片的 resourceURL :' + pic.URL)

    global mutexLock
    # 加锁
    if mutexLock.acquire():
        # 打开（可能创建）路径
        opendir(pic.album)
        mutexLock.release()

    # 真正的通过URL下载资源（不同站点需要修改的部分--------------------------------------------------------）
    ir = download_func(pic.URL, duplicate=5, timeout=20)
    # ir = _requests(pic.URL, duplicate=2)
    # logging.info('下载用时 ：'+str(ir.elapsed.microseconds))
    # logging.info('status_code : '+str(ir.status_code))

    if ir.status_code != 200 :
        if verbose:
            # 输出一下错误的pic信息
            logging.info('第' + str(idx) + '张图片下载失败....下载用时 ：'+str(ir.elapsed.microseconds/1000)+'毫秒...')
    else :
        # 保存资源
        open(os.path.join(pic.album, pic.name), 'wb').write(ir.content)
        if verbose:
            logging.info('第' + str(idx) + '张图片下载完毕....下载用时 ：'+str(ir.elapsed.microseconds/1000)+'毫秒...')
    # logging.info("resourcePath :" + pic.album)
    # logging.info("resourceURL :" + pic.URL)
    # logging.info("resourceName :" + pic.name)

    return ir

# 多线程...
class downloadThread(threading.Thread) :
    def __init__(self, func, args=()):
        super(downloadThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None
