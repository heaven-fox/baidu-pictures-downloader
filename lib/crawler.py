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
            "pn=%d&rn=30&gsm=96&1473335095606="

# decode list
_replace_dict = {
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
    refer_url = _refer_path % search_target
    curl = pycurl.Curl()
    curl.setopt(pycurl.USERAGENT, user_agent)
    curl.setopt(pycurl.REFERER, refer_url)

    result = []
    ll = 0
    record_start_cursor = get_record_start_cursor()
    if record_start_cursor:
        ll = int(record_start_cursor)
    print 'start'
    # 使用探测法拿到所有的图片资源
    while 1:
        print 'crawler pictures of page %d' % (ll / 30 + 1)
        # 获取str类型的数据
        buffers = StringIO()
        target_url = _ajax_url % (search_target, search_target, ll)
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
                    # decode url
                    has_data = True
                    result.append(decode_url(obj_url))
            if has_data:
                ll += 30
            else:
                print 'no more pic'
                break
        else:
            print 'no more pic'
            break
        print ll

    print 'done'
    curl.close()
    # 更新page_num
    if ll:
        set_record_start_cursor(str(ll))

    return result


def decode_url(source_url):
    """
    解密url
    :param source_url:
    :return:
    """
    if source_url:
        source_url = source_url.replace('_z2C$q', _replace_dict['_z2C$q'])
        source_url = source_url.replace('_z&e3B', _replace_dict['_z&e3B'])
        source_url = source_url.replace('AzdH3F', _replace_dict['AzdH3F'])
        length = len(source_url)
        for i in xrange(0, length):
            if source_url[i] in _replace_dict:
                tmp = _replace_dict[source_url[i]]
                if tmp:
                    source_url = source_url[:i] + tmp + source_url[i+1:]

    return source_url


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
