
import sys
sys.path.append('..')

from atools_crawler.common.UserAgent import get_random_UA


class MyRequestsConfig(object):
    proxies = {
        'http': 'http://127.0.0.1:54422',
        'https': 'https://127.0.0.1:54422',
    }
    headers = {'Connection': 'Keep-Alive'
               # ,'host': 'zhannei.baidu.com'
               # ,'ref??': ''
                , 'User-Agent': get_random_UA()
    }
