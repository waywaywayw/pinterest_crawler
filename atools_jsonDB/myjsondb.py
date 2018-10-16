# -*- coding: utf-8 -*-
"""
@author: weijiawei
@date: 2018-09-06
"""

import os, re
import json


class MyjsonDB(object):
    def __init__(self, db_path):
        """
        初始化数据库，初始化res列表
        :param db_path:
        """
        # self._db_name = db_name
        self._db_path = db_path
        self._resource_dict = {}

        # 没找到数据库文件
        if not os.path.isfile(db_path):
            open(db_path, 'w', encoding='utf8').close()
            print('json文件 {} 不存在，已新建该文件'.format(db_path))
        else:
            self.load_from_file(db_path)
            print('发现json文件 {} ，已读取内容'.format(db_path))

    def load_from_file(self, db_path, encoding='utf8'):
        """从json_db中读取resource_dict
        """
        with open(db_path, 'r', encoding=encoding) as fin:
            self._resource_dict = json.load(fin)

    def load_from_dict(self, data_dict):
        self._resource_dict = data_dict

    def write_to_file(self, write_mode='w', encoding='utf8', verbose=False):
        """
        将json列表格式的resource_dict写入db, 遇到重复的自动不添加
        :param db_path:
        :param resource_dict:
        :return: 写入成功，返回True
        """
        save_path = self._db_path
        resource_dict = self._resource_dict
        # 写入数据库
        with open(save_path, write_mode, encoding=encoding) as fout:
            # 有中文需要：ensure_ascii=False
            json.dump(self._resource_dict, fout, ensure_ascii=False)
            # for res in resource_dict:
            #     res_json = json.dumps(res, ensure_ascii=False, sort_keys=True)
            #     db_file.write(res_json + '\n')
            #     if verbose:
            #         print(res_json)
        return True

    def is_duplicate(self, key_name, resource, res_db=None):
        """
        判重
        :param res: 需要判重的数据
        :param res_db: 资源数据库
        :param key_name: 判重的关键key的name
        :return:
        """
        if not res_db:
            res_db = self._resource_dict

        # resource里没有key_name属性的情况
        if not resource.get(key_name):
            return False

        ret = False
        for r in res_db:
            # print(r)
            # print(r[key_name])
            if resource[key_name] == r[key_name]:
                ret = True
        return ret

    @property
    def resource_dict(self):
        return self._resource_dict

    def extend_resource_dict(self, resource_dict):
        """扩展resource_dict, 参数为resource of list"""
        self._resource_dict.update(resource_dict)