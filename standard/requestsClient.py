import requests
import logging
import time


# 定义会话客户端类
class _requestsClient :
    # 参数
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

    # 蓝灯的代理端口 60425
    # port = 60425
    port = 60425 # 默认端口
    proxies = {
        'https': 'https://127.0.0.1:'+str(port),
        'http': 'http://127.0.0.1:'+str(port)
    }
    headers = {
        'user-agent': agent
        , 'Connection': 'keep-alive'
        , 'Host': 'i.pinimg.com'
        ,'Accept': 'text / html, application / xhtml + xml, application / xml;    q = 0.9, image / webp, * / *;q = 0.8'
        # ,'Cookie': '__cfduid=dd47fd076c3e54cc53a5d1054db82d6121505225609; PHPSESSID=j31c7qsbkqi22p0019vide6ih0; AGREE_CONSENT=1; _popfired=20; _gat=1; _ga=GA1.2.1458835411.1504142140; _gid=GA1.2.1307652668.1505225547'
    }

    # 构造方法
    def __init__(self):
        # 初始化
        pass

    def setProxyPort(self, port) :
        self.proxies = {
            'https': 'https://127.0.0.1:' + str(port),
            'http': 'http://127.0.0.1:' + str(port)
        }

    # 发送requests请求，如果不成功，尝试duplicate次(-1表示一直尝试）,请求超时时间timeout，请求失败睡眠时间sleep
    def requestsGet(self, URL, params={}, timeout=10, sleepTime=3, duplicate=2, pic=None):
        cnt = 0
        ir = None
        try_png = False
        try_736x = False
        while True:
            # 是否异常的标识
            ERROR = False
            try:
                # logging.info('准备下了..')
                # 真正的通过URL下载资源
                ir = requests.get(URL, params=params, headers=self.headers, proxies=self.proxies, timeout=timeout)
                # logging.info('搞完了.. 时间'+str(ir.elapsed.microseconds/1000)+'毫秒..')
                # logging.info('status_code = '+str(ir.status_code))
                cnt += 1

                # 成功获取，直接返回
                if ir.status_code == 200:
                    return ir
                # 所有尝试都不成功.. 返回403
                if try_png==True and try_736x==True :
                    logging.info('服务器拒绝访问.....')
                    return ir

                # 改变一下后缀..改为png试试？
                if try_png==False and ir.status_code == 403:
                    list = URL.split('.')
                    list[-1] = 'png'
                    URL = ".".join(list)
                    # logging.info('更换后缀png，再次进行尝试..')
                    # logging.info(URL)
                    try_png = True

                # 改变一下清晰度..改为736x试试？
                if try_736x==False and ir.status_code == 403:
                    # 先换回jpg
                    list = URL.split('.')
                    list[-1] = 'jpg'
                    URL = ".".join(list)
                    # 再切换736x
                    list = URL.split('/')
                    list[3] = '736x'
                    URL = "/".join(list)
                    # logging.info('更换低清736x版本，再次进行尝试..')
                    # logging.info(URL)
                    try_736x = True

            except requests.exceptions.ConnectTimeout:
                logging.info('资源连接超时.. ' + URL + str(params))
                ERROR = True
            except requests.exceptions.Timeout:
                logging.info('资源获取' + str(timeout) + '秒超时.. ' + URL + str(params))
                ERROR = True
            except Exception :
                logging.info('捕获到异常..估计是没开代理 或者 代理端口不对？')
                ERROR = True
            finally:
                # 如果捕获到异常
                if ERROR is True:
                    # 结束条件
                    if duplicate != -1 and cnt >= duplicate:
                        logging.info('不继续下载资源了？ cnt = ' + str(cnt) + 'duplicate = ' + str(duplicate))
                        return ir
                    # 两次请求失败才给出错误提示
                    if cnt >= 2 :
                        logging.info('URL:'+URL+'请求资源失败，等待' + str(cnt * sleepTime) + '秒后发送第' + str(cnt + 1) + '次请求..')
                    # 睡眠几秒..
                    time.sleep(cnt * sleepTime)

        # ir = requests.get('wwwwwwwww.com')
        return ir
