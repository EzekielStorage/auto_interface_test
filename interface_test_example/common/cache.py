# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
    缓存文件，就是本地的一个数据字典
"""
from collections import UserDict


class CachePool(UserDict):
    """全局变量池"""

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value=None):
        self.data.setdefault(key, value)

    def has(self, key):
        return key in self.data

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(self.data)


cache = CachePool()

if __name__ == '__main__':
    cache.set('name', 'Chris')
    print(len(cache))
    print(cache.get('name'))
