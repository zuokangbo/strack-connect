#!/usr/bin/env python
# coding=utf-8
'''
Author: zuokangbo
Date: 2022-01-05 22:32:50
'''
# :coding: utf-8
# :copyright: Copyright (c) 2021 strack

import os, sys
import copy
import yaml
import threading


class Config(object):
    _instance_lock = threading.Lock()
    config = {}

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            with Config._instance_lock:
                if not hasattr(Config, "_instance"):
                    Config._instance = object.__new__(cls)
        return Config._instance

    def load(self, name="config.yaml"):
        """ default file config.yaml"""
        if not bool(self.config):
            config_path = os.getenv('CONFIG_PATH')
            yaml_path = os.path.join(config_path, name)

            # read config yaml
            if sys.version_info == 3:
                f = open(yaml_path, 'r', encoding='utf-8')
            else:
                f = open(yaml_path, 'r')
            yaml_str = f.read()

            # convert dictionary with load method
            self.config = yaml.load(yaml_str, Loader=yaml.FullLoader)

    def get(self, name):
        # load yaml config file
        self.load()

        if isinstance(name, str) and '.' in name:
            param = copy.deepcopy(self.config)
            for key in name.split('.'):
                if isinstance(param, dict):
                    param = param.get(key)
                else:
                    param = ''
            return param
        elif name in self.config:
            return self.config.get(name)
        return ''


if __name__ == '__main__':
    from strack_connect.config.env import Env

    Env()

    obj = Config()
    print(obj.get('ws_server.port'))
