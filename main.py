# coding: utf8

"""
项目入口
"""

import os
# 切换工作目录到项目根目录
project = os.path.split(os.path.realpath(__file__))[0]
os.chdir(project)

import lib.crawler as cl


if __name__ == '__main__':
    # 测试用例
    search_target = "kde"
    d_links = cl.get_dlinks(search_target)
    cl.save_to_file(d_links, '%s.txt' % search_target)
