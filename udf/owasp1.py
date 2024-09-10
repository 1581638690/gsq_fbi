# /bin/python
# -*- coding: utf-8 -*-


"""
owasp1.py
owasp1
#=========================
"""
import difflib
import sys

sys.path.append("..")
sys.path.append("../")
sys.path.append("./lib")
import pandas as pd
import numpy as np
import requests
import json
import time
#import re
import regex as re
#import orjson as json
import socket
from avenger.fsys import get_key

__workSpace = "../workspace/"


def search(df, p=''):
    """
    @author： qh
    @date: 20221115
    @函数：search
    @参数：df表, p->(a)
    @描述：owasp1-1参数可遍历识别
    @返回：识别结果df表
    """
    p = p.strip()
    a = p.split('|')
    s = {}
    ss = {}
    end = {"参数可遍历": "", "类似参数": {}}
    sss = []
    for item in a:
        s[item] = []
        for _, row in df.iterrows():
            if item in row["parameter"]:
                page = re.findall(r'%s=[0-9]+' % item, row["parameter"])
                if page:
                    s[item].append(page[0])
    for k, v in s.items():
        v = list(set(v))
        if len(v) > 1:
            end["参数可遍历"] = end["参数可遍历"] + k + ","
            end["类似参数"][k] = v
    if end["参数可遍历"]:
        # ss["g"] = "1"
        end = json.dumps(end, ensure_ascii=False).encode("utf-8")
        ss["more"] = end
    else:
        # ss["g"] = "0"
        ss["url"] = "bucun"
    sss.append(ss)
    df1 = pd.DataFrame(sss)
    return df1


def search2(df):
    risk_urls = []
    uris = []
    urls = []
    end = {"对象可猜测": "", "类似接口": {}}
    try:
        for _, row in df.iterrows():
            a = re.findall(r'(?:http://)(?:.*?/)(.*)', row["url_a"])
            if a:
                uris.append(a[0])
                urls.append(row["url_a"])
        for m in range(len(uris)):  # 依次不重复的对比
            for n in range(m + 1, len(uris)):
                s = difflib.SequenceMatcher(None, uris[m], uris[n]).quick_ratio()  # 相似度对比
                if s > 0.8:
                    # 相似度超过0.8视为相似
                    a_d = []  # 临时存储筛选后内容的列表
                    b_d = []
                    a_az = []
                    a_r = []
                    # print("相同接口?")
                    split_m = re.split(r'/', uris[m])  # 按/切割
                    # print(a)
                    split_n = re.split(r'/', uris[n])
                    # print(b)
                    if len(split_m) == len(split_n):  # 判断长度是否相同,长度不同的不是同接口
                        for i in range(len(split_m)):
                            if split_m[i] == split_n[i]:  # 去除相同的部分
                                continue
                            a_d.append(re.sub(r'[^\d]', '', split_m[i]))  # 去除不相同部分的字母并存储
                            b_d.append(re.sub(r'[^\d]', '', split_n[i]))
                            a_az.append(re.sub(r'[\d]', '', split_m[i]))  # 去除不相同部分的数字并存储
                            a_r.append(split_m[i])
                            a_r.append(split_n[i])
                        if len(a_d) == 1 and len(b_d) == 1 and a_d[0] != '' and b_d[0] != '':  # 只剩一个参数且不为空
                            sab = difflib.SequenceMatcher(None, str(a_d), str(b_d)).quick_ratio()
                            # print(sab)
                            if sab > 0.8 and len(a_az[0]) < 10:  # 剩余参数相似度超过0.8且字母不超过10个视为不安全
                                # print("不安全！")
                                # print(a_az[0])
                                # print(len(a_az[0]))
                                risk_urls.append(urls[m])
                                end["对象可猜测"] = end["对象可猜测"] + urls[m] + ","
                                end["类似接口"][urls[m]] = a_r
                                break
            if len(risk_urls) > 20:
                break
    except:
        pass  # print("比对超时跳过")
    ss = {}
    if end["对象可猜测"]:
        # ss["g"] = "1"
        end = json.dumps(end, ensure_ascii=False).encode("utf-8")
        ss["more"] = end
    else:
        # ss["g"] = "0"
        ss["url"] = "bucun"
    sss = []
    sss.append(ss)
    df1 = pd.DataFrame(sss)
    return df1

