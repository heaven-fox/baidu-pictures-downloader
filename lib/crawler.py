# coding: utf8

import os
import pycurl
from StringIO import StringIO


# 伪装成iPad客户端
user_agent = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10' \
             ' (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'

# 伪造来源地址
_refer_path = "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%s"

# ajax request url
_ajax_url = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&" \
            "lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&" \
            "pn=180&rn=30&gsm=96&1473335095606="


def get_dlinks(search_target):
    """
    根据网页url图片的下载链接
    :param search_target: 目标文本
    :return 返回图片的真实下载链接
    """
    refer_url = _refer_path % search_target
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.REFERER, refer_url)

    result = []
    counter = 1
    ll = ''
    # record_start_cursor = get_record_start_cursor()
    print 'start'
    # 使用探测法拿到所有的图片资源
    while 1:
        print 'crawler the %d picture' % counter
        # 获取str类型的数据
        buffers = StringIO()
        target_url = _ajax_url % (search_target, search_target)
        curl.setopt(pycurl.URL, target_url)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()

        body = buffers.getvalue()
        body = body.replace('null', 'None')
        data = eval(body)
        if 'data' in data:
            for a_data in data['data']:
                print a_data['fromPageTitleEnc']
                break
                img_url = None
                if 'hasLarge' in a_data:
                    if a_data['hasLarge']:
                        img_url = a_data['largeTnImageUrl']
                    elif 'middleURL' in a_data:
                        img_url = a_data['middleURL']
                    elif 'thumbUrl' in a_data:
                        img_url = a_data['thumbURL']
                print img_url
        break

    print 'done'
    curl.close()
    # # 更新start_cursor
    # if ll:
    #     set_record_start_cursor(ll)

    return result


def save_to_file(d_links, file_name):
    """
    将图片链接存入文件
    :param d_links: 图片真实下载链接
    :param :file_name: 文件名
    :return
    """
    try:
        if not d_links:
            return
        base_dir = 'out/'
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        file_object = open(base_dir + file_name, 'a')

        for item in d_links:
            file_object.write(item)
            file_object.write('\n')
        file_object.close()
    except IOError:
        print 'file not exist!'
        exit()


def get_record_start_cursor():
    """
    从本地文件拿到最近一次的start_cursor
    :return
    """
    try:
        record_file = "cursor.txt"
        if not os.path.exists(record_file):
            return None
        file_object = open(record_file, "r")
        line = file_object.readline()
        file_object.close()
        if not line:
            return None

        return line
    except IOError:
        print 'file io error!'
        exit()


def set_record_start_cursor(start_cursor):
    """
    记录最近一次start_cursor
    :param start_cursor:
    :return
    """
    try:
        record_file = "cursor.txt"
        file_object = open(record_file, "w")
        file_object.write(start_cursor)
        file_object.close()
    except IOError:
        print 'file io error!'
        exit()
