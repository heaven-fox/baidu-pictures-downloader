# coding: utf8

import os
import pycurl
from StringIO import StringIO


# 伪装成iPad客户端
_USER_AGENT = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10' \
              ' (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'

# 伪造来源地址
_REFER_URL = "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%s"

# ajax request url
_AJAX_URL = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&" \
            "lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&fr=&" \
            "pn=%d&rn=30&gsm=96&1473335095606="

# decode list
_REPLACE_DICT = {
    "w": "a",
    "k": "b",
    "v": "c",
    "1": "d",
    "j": "e",
    "u": "f",
    "2": "g",
    "i": "h",
    "t": "i",
    "3": "j",
    "h": "k",
    "s": "l",
    "4": "m",
    "g": "n",
    "5": "o",
    "r": "p",
    "q": "q",
    "6": "r",
    "f": "s",
    "p": "t",
    "7": "u",
    "e": "v",
    "o": "w",
    "8": "1",
    "d": "2",
    "n": "3",
    "9": "4",
    "c": "5",
    "m": "6",
    "0": "7",
    "b": "8",
    "l": "9",
    "a": "0",
    "_z2C$q": ":",
    "_z&e3B": ".",
    "AzdH3F": "/"
}


def get_dlinks(search_target):
    """
    根据网页url图片的下载链接
    :param search_target: 目标文本
    :return 返回图片的真实下载链接
    """
    refer_url = _REFER_URL % search_target
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, _USER_AGENT)
    curl.setopt(pycurl.REFERER, refer_url)

    result = []
    ll = 0
    record_start_cursor = get_record_start_cursor()
    if record_start_cursor:
        ll = int(record_start_cursor)
    print('start')
    # 使用探测法拿到所有的图片资源
    while 1:
        print('crawler pictures of page %d' % (ll / 30 + 1))
        # 获取str类型的数据
        buffers = StringIO()
        target_url = _AJAX_URL % (search_target, search_target, ll)
        curl.setopt(pycurl.URL, target_url)
        curl.setopt(pycurl.WRITEDATA, buffers)
        curl.perform()

        body = buffers.getvalue()
        body = body.replace('null', 'None')
        data = eval(body)
        if 'data' in data:
            has_data = False
            for a_data in data['data']:
                obj_url = None
                if 'objURL' in a_data:
                    obj_url = a_data['objURL']
                if obj_url:
                    has_data = True
                    result.append(obj_url)
            if not has_data:
                print('no more pic')
                break
            ll += 30
        else:
            print('no more pic')
            break

    print('done')
    curl.close()
    # 更新page_num
    if ll:
        set_record_start_cursor(str(ll))
    for index, data in enumerate(result):
        result[index] = decode_url(data)

    return result


def decode_url(source_url):
    """
    解密url
    :param source_url:
    :return:
    """
    result = ''
    if source_url:
        target_list = list()
        target_url = source_url.replace('_z2C$q', _REPLACE_DICT['_z2C$q'])
        target_url = target_url.replace('_z&e3B', _REPLACE_DICT['_z&e3B'])
        target_url = target_url.replace('AzdH3F', _REPLACE_DICT['AzdH3F'])
        length = len(target_url)
        for i in xrange(0, length):
            if target_url[i] in _REPLACE_DICT:
                tmp = _REPLACE_DICT[target_url[i]]
                if tmp:
                    target_list.append(tmp)
            else:
                target_list.append(target_url[i])
        if target_list:
            result = ''.join(target_list)

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
        print('file not exist!')
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
        print('file io error!')
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
        print('file io error!')
        exit()
