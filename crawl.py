#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 11:00:12 2018

@author: hongyun
"""
import os
import re
import sys
import urllib
import requests

def mkdirr(path):
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False




def getPage(keyword,page,n):
    page=page*n
    keyword=urllib.parse.quote(keyword, safe='/')
    url_begin= "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin+ keyword + "&pn=" +str(page) + "&gsm="+str(hex(page))+"&ct=&ic=0&lm=-1&width=0&height=0"
    return url
def get_onepage_urls(onepageurl):
    try: html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return pic_urls
def down_pic(pic_urls,save_path):
    """给出图片链接列表, 下载所有图片"""
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=15)
            string = save_path + '/' + str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue

def crawl(keyword,save_path, page_begin, image_number, pages_number):
    save_path = save_path +'/' + keyword
    mkdirr(save_path)
    all_pic_urls = []
    while 1:
        if page_begin>pages_number:
            break
        print("第%d次请求数据",[page_begin])
        url=getPage(keyword,page_begin,image_number)
        onepage_urls= get_onepage_urls(url)
        page_begin += 1
        all_pic_urls.extend(onepage_urls)
    down_pic(list(set(all_pic_urls)),save_path)
'''
if __name__ == '__main__':
    keyword = '狗'
    save_path = '/Users/lhy/Photo_Montage/source_material'
    save_path = save_path +'/' + keyword
    mkdirr(save_path)
    page_begin=0
    image_number=30
    pages_number=3
    all_pic_urls = []
    while 1:
        if page_begin>pages_number:
            break
        print("第%d次请求数据",[page_begin])
        url=getPage(keyword,page_begin,image_number)
        onepage_urls= get_onepage_urls(url)
        page_begin += 1
        all_pic_urls.extend(onepage_urls)
    down_pic(list(set(all_pic_urls)),save_path)
'''
