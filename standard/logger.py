# -*- coding:utf-8 -*-

import logging
import time

# 输出信息（加入时间元素）
# def _print(message) :
#     print(time.strftime("%m.%d %T") + ' -- ' + message)

def InitLogger():
    logFileName = 'logs/log_' + time.strftime("%Y-%m-%d_%H%M%S", time.localtime(time.time())) + '.txt'
    logging.basicConfig(level=logging.WARNING,
                        format='[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s',
                        filename=logFileName,
                        filemode='w')

    # 定义一个StreamHandler将INFO级别以上的信息打印到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
