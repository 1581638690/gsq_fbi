# /bin/python
# -*- coding: utf-8 -*- 


"""
net.py
基于风险模型的开发
#=========================
"""
import sys

sys.path.append("..")
sys.path.append("../")
sys.path.append("./lib")
import requests
import ujson
import time
import re
import pandas as pd
import numpy as np


def proof4(df, p=''):
    """
    @author： qh
    @date: 20230401
    @函数：proof
    @参数：df表, p->(srcip,url,b,srcip_count,pdbz)
    @描述：风险模型拼装证据字段
    @返回：证据
    """
    p = p.strip()
    srcip,url,b,srcip_count = p.split(',')
    proofs = {}
    proofs["判定标准"] = "终端频繁登陆验证：同一个IP或终端访问登录接口，超过设定阈值时发出告警"
    proofs["接口"] = url
    proofs["终端"] = srcip
    proofs["阈值"] = str(b) + '/分钟'
    proofs["结果"] = "终端在1分钟内访问登录接口" + srcip_count + "次"
    proofs["证据"] = {}
    proofs["证据"]["时间"] = "HTTP协议ID"
    for _, row in df.iterrows():
        proofs["证据"][str(row.timestamp)] = row.suid
    lens = 0
    n = 0
    proofs["证据"]["编号"] = "响应体内容"
    for _, row in df.iterrows():
        if lens > 10000:
            break
        proofs["证据"][n] = row.response
        lens = lens + len(str(row.response))
        n = n + 1
    proofs = ujson.dumps(proofs, ensure_ascii=False)
    list1 = []
    a = {}
    a["proofs"] = proofs
    list1.append(a)
    df1 = pd.DataFrame(list1)
    return df1


def proof2(df, p=''):
    """
    @author： qh
    @date: 20230401
    @函数：proof
    @参数：df表, p->(srcip,url,b,srcip_count,pdbz)
    @描述：风险模型拼装证据字段
    @返回：证据
    """
    p = p.strip()
    srcip,url,b,srcip_count = p.split(',')
    proofs = {}
    proofs["判定标准"] = "终端高频敏感访问：同一终端对敏感类型的数据接口访问超过设定阈值时发出告警"
    proofs["接口"] = url
    proofs["终端"] = srcip
    proofs["阈值"] = str(b) + '/分钟'
    proofs["结果"] = "终端在1分钟内访问敏感接口" + srcip_count + "次"
    proofs["证据"] = {}
    proofs["证据"]["时间"] = "HTTP协议ID"
    for _, row in df.iterrows():
        proofs["证据"][str(row.timestamp)] = row.suid
    proofs = ujson.dumps(proofs, ensure_ascii=False)
    list1 = []
    a = {}
    a["proofs"] = proofs
    list1.append(a)
    df1 = pd.DataFrame(list1)
    return df1


def proof3(df, p=''):
    """
    @author： qh
    @date: 20230401
    @函数：proof
    @参数：df表, p->(srcip,url,b,srcip_count,pdbz)
    @描述：风险模型拼装证据字段
    @返回：证据
    """
    p = p.strip()
    srcip,url,num,mean,n = p.split(',')
    proofs = {}
    proofs["判定标准"] = "终端访问接口数据波动过大：同一接口对所用终端单次提供敏感数据数量的月平均值为X，规则设定系数为n。当终端单次访问返回敏感类型数据的数量超过nX时发出告警"
    proofs["接口"] = url
    proofs["终端"] = srcip
    proofs["接口返回敏感数据数量月平均值"] = float(mean)/int(n)
    proofs["规则系数"] = n
    proofs["阈值"] = mean
    proofs["结果"] = "本次会话接口返回敏感数据数量" + num
    proofs["证据"] = {}
    proofs["证据"]["时间"] = "HTTP协议ID"
    for _, row in df.iterrows():
        proofs["证据"][str(row.timestamp)] = row.suid
    proofs = ujson.dumps(proofs, ensure_ascii=False)
    list1 = []
    a = {}
    a["proofs"] = proofs
    list1.append(a)
    df1 = pd.DataFrame(list1)
    return df1


def proof10(df, p=''):
    """
    @author： qh
    @date: 20230401
    @函数：proof
    @参数：df表, p->(srcip,url,b,srcip_count,pdbz)
    @描述：风险模型拼装证据字段
    @返回：证据
    """
    p = p.strip()
    srcip,url,srcip_count,srcs = p.split(',')
    proofs = {}
    proofs["判定标准"] = "疑似机器访问行为：同一终端对同一应用的数据接口访问数据超过设定阈值且每个接口的访问频率超过阈值时发出告警"
    proofs["接口"] = url
    proofs["终端"] = srcip
    proofs["接口数量阈值"] = srcs
    proofs["接口访问阈值"] = srcip_count
    proofs["结果"] = "终端在1分钟内访问敏感接口超过"+ srcs + "个，且访问频率都超过" + srcip_count + "/分钟，疑似机器访问行为"
    proofs["证据"] = {}
    proofs["证据"]["时间"] = "HTTP协议ID"
    for _, row in df.iterrows():
        proofs["证据"][str(row.timestamp)] = row.suid
    proofs = ujson.dumps(proofs, ensure_ascii=False)
    list1 = []
    a = {}
    a["proofs"] = proofs
    list1.append(a)
    df1 = pd.DataFrame(list1)
    return df1


def dropem(df):
    """
    @author： qh
    @date: 20230407
    @函数：dropem
    @参数：df表
    @描述：风险模型白名单去除空列,只能单行,否则容易报错
    @返回：去空后df
    """
    list1 = []
    a = {}
    columns = df.columns.values.tolist()
    for _, row in df.iterrows():
        for c in columns:
            if row[c] != '':
                a[c] = row[c]
    list1.append(a)
    df1 = pd.DataFrame(list1)
    return df1


def join2(df1, df2):
    """
    @author： qh
    @date: 20230407
    @函数：join2
    @参数：df表1,df表2
    @描述：风险模型按df1全字段合并
    @返回：合并后df
    """
    columns = df1.columns.values.tolist()
    df = pd.merge(df1, df2, left_on=columns, right_on=columns, how='inner')
    return df
