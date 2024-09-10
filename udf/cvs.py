# /bin/python
# -*- coding: utf-8 -*-


"""
cvs.py
转码工具
#=========================
"""
import sys

sys.path.append("..")
sys.path.append("../")
sys.path.append("./lib")
import base64
from datetime import datetime
from urllib import parse
import pandas as pd

__workSpace = "../workspace/"


def cvs(df, p=''):
    """
    @author： qh
    @date: 20230630
    @函数：cvs
    @参数：df表, p->(ms, cv, base64d)
    @参数：ms:输入的信息
    @参数：cv:需要转换的类型
    @参数：base64d:base64转换的编码
    @描述：转换格式为易读
    @返回：a:转换完成的值
    """
    p = p.strip()
    ms, cv, base64d = p.split(',')
    a = ""
    if cv == "base64解码":
        if base64d == "自动":
            try:
                a = base64.b64decode(ms).decode("utf-8")
            except:
                try:
                    a = base64.b64decode(ms).decode("gbk")
                except:
                    a = ms
        else:
            try:
                a = base64.b64decode(ms).decode(base64d)
            except Exception as e:
                try:
                    a = base64.b64decode(ms)[0:e.start].decode(base64d)
                except:
                    a = ms
        a = parse.unquote(a)
    if cv == "url解码":
        a = parse.unquote(ms)
    if cv == "时间戳转时间" or cv == "id转时间":
        time1 = str(ms).split('-')
        if len(time1) > 1:
            time1 = time1[1]
        else:
            time1 = time1[0]
        time2 = time1.split('.')[0]
        try:
            dt = datetime.fromtimestamp(int(time2))
            a = dt.astimezone()
        except:
            a = ms
    list1 = []
    s = {}
    s["a"] = a
    list1.append(s)
    df1 = pd.DataFrame(list1)
    return df1
