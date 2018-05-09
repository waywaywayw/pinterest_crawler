import requests

# 定义会话客户端类
class _sessionClient :
    # 参数
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # connection = 'keep-alive'
    # session
    session = ""

    # 构造方法
    def __init__(self):
        # 初始化session
        self.session = requests.session()

        # 设置请求头
        self.session.headers.update({'User-Agent': self.agent
                                    ,'Connection': 'keep-alive'
                                    ,'Host': 'i.pinimg.com'
                                    ,'Accept': 'text / html, application / xhtml + xml, application / xml;    q = 0.9, image / webp, * / *;q = 0.8'
                                    # , 'Cookie': '__cfduid=dd47fd076c3e54cc53a5d1054db82d6121505225609; PHPSESSID=j31c7qsbkqi22p0019vide6ih0; AGREE_CONSENT=1; _popfired=20; _gat=1; _ga=GA1.2.1458835411.1504142140; _gid=GA1.2.1307652668.1505225547'
                                     })
        pass