#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/26 9:51 上午
# @Author : WOLF
# @File : get_bing_wallpaper.py
# @desc: 这里填写文件的描述信息

import calendar
import datetime
import os
import time
import requests
import json


# https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1611072000000&pid=hp
# 其中参数：
# idx=0 表示今天开始，1表示昨天，以此类推，最大为7；
# n=1 表示要返回包括idx及前面几天的数据，每天1张 ，最大值为8；
# nc= 当前13位时间戳
# 综合：最多可以提取到最近16天的图。
#
#
#


# '2000-01-01 12:34:00'
def string_to_times(_str):
    return calendar.timegm(time.strptime(_str, '%Y-%m-%d %H:%M:%S'))


def get_b_w():
    ts = calendar.timegm(time.gmtime())
    # print(f'当前时间戳: {ts}')
    api_url = f'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8&nc={ts}&pid=hp'
    # print(f'当前API: {api_url}')
    res = requests.get(api_url)
    # _json是 dict 类型
    _json = res.json()
    # print(_json)

    # print(_json['images'][0])
    for item in _json['images']:
        _urlbase = item['urlbase']
        _copyright = item['copyright']

        # print(f'urlbase : {_urlbase}')
        # print(f'copyright : {_copyright}')
        image_url = f'https://cn.bing.com{_urlbase}_UHD.jpg'
        # print(image_url)
        a = (os.path.dirname(__file__))  # 获取当前路径

        # 接着把图片保存下来，再提前准备一个Photo目录用来存放
        # name = str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day) + '.jpg'
        # _time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # _time = datetime.datetime.now().strftime('%Y%m%d')
        _time = item['enddate']
        name = _time + '0900.jpg'
        file = a + '/Photo' + '/' + name  # 建立保存的绝对地址
        # print(file)
        while True:
            try:
                fp = open(file, 'wb')
                fp.write(requests.get(image_url).content)
                fp.close()  # 保存图片到Photo这个文件夹
                print('已将图片保存于', file)
                with open(a + '/Photo/' + _time + "0900.txt", "w+") as f:
                    f.write(_copyright)  # 自带文件关闭功能，不需要再写f.close()
                    f.write('\r\n')
                    f.write(image_url)
                    f.write('\r\n')
                break
            except:
                print('发生错误！！请检查是否在', a, '中创建Photo名称的文件夹')
                b = input('创建确定请输入1:')
                # 保存图片到
