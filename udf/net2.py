# /bin/python
# -*- coding: utf-8 -*- 


"""
net.py
基于网络接口的开发
#=========================
"""
import sys

sys.path.append("..")
sys.path.append("../")
sys.path.append("./lib")
import pandas as pd
import numpy as np
import requests
import json
import time
import re
import socket
import avenger.fsys
#import get_key

__workSpace = "../workspace/"
from avenger.fsys import New_encrypt, New_decrypt

protocol = 'http'
ip_port = {
    'ip': '103.79.24.59',
    'port': 18080
}
json_header = {
    'Content-Type': 'application/json'
}

error_message = '请求证书套件服务出现错误!'


# 设置请求协议
def set_protocol_type(pro_type):
    if pro_type == 'http' or pro_type == 'https':
        global protocol
        protocol = pro_type


# 设置请求IP和端口号
def set_ip_port(ip, port):
    global ip_port
    if ip:
        ip_port['ip'] = ip
    if port:
        ip_port['port'] = port


# 发送post请求
def request_post(api, params, fail_res):
    req_url_pre = protocol + '://' + ip_port['ip'] + ':' + str(ip_port['port'])
    req_url = req_url_pre + api
    res = requests.post(req_url, verify=False, data=json.dumps(params), headers=json_header)
    if res.status_code == requests.codes.ok:
        return res.json()
    else:
        fail_res['errCode'] = res.status_code
        # return json.dumps(fail_res, ensure_ascii=False)
        return fail_res


# 客户端身份认证1
def auth1(str_ip_or_id):
    api = '/auth1'
    params = {
        'strIPorID': str_ip_or_id
    }
    fail_res = {
        'errMsg': error_message,
        'clientHello': None
    }
    return request_post(api, params, fail_res)


# 客户端身份认证2
def auth2(str_ip_or_id, server_hello):
    api = '/auth2'
    params = {
        'strIPorID': str_ip_or_id,
        'serverHello': server_hello
    }
    fail_res = {
        'errMsg': error_message,
        'clientAuth': None
    }
    return request_post(api, params, fail_res)


# 读取证书
def read_cert(str_ip_or_id, cert_num):
    api = '/readCert'
    params = {
        'strIPorID': str_ip_or_id,
        'dwCertNum': cert_num
    }
    fail_res = {
        'errMsg': error_message,
        'cert': None
    }
    return request_post(api, params, fail_res)


# 签名
def sign_data(str_ip_or_id, sign_data):
    api = '/signData'
    params = {
        'strIPorID': str_ip_or_id,
        'signData': sign_data
    }
    fail_res = {
        'errMsg': error_message,
        'signResult': None
    }
    return request_post(api, params, fail_res)


# 验签
def verify_sign(str_ip_or_id, sign_data, sign_result):
    api = '/verifySign'
    params = {
        'strIPorID': str_ip_or_id,
        'signData': sign_data,
        'signResult': sign_result
    }
    fail_res = {
        'errMsg': error_message
    }
    return request_post(api, params, fail_res)


# 加密
def enc_data(str_ip_or_id, data):
    api = '/encData'
    params = {
        'strIPorID': str_ip_or_id,
        'data': data
    }
    fail_res = {
        'errMsg': error_message,
        'enData': None
    }
    return request_post(api, params, fail_res)


# 解密
def dec_data(str_ip_or_id, enc_data):
    api = '/decData'
    params = {
        'strIPorID': str_ip_or_id,
        'enData': enc_data
    }
    fail_res = {
        'errMsg': error_message,
        'data': None
    }
    return request_post(api, params, fail_res)


def soc_request_post(ip, port, api, params):
    req_url = 'https://' + ip + ':' + port + api
    res = requests.post(req_url, verify=False, data=json.dumps(params), headers={'Content-Type': 'application/json'})
    if res.status_code == requests.codes.ok:
        return res.json()
    else:
        fail_res = {}
        fail_res['errCode'] = res.status_code
        # return json.dumps(fail_res, ensure_ascii=False)
        return fail_res


def cert(df, p=''):
    """
    @author： qh
    @date: 20221201
    @函数：cert
    @参数：p->(ip, port, socip, socport, protocol)
    @描述：SDK和SOC平台对接
    @返回：认证结果
    """
    p = p.strip()
    ip_or_id, ip, port, protocol, socip, socport = p.split(',')
    list1 = []
    set_protocol_type(protocol)
    set_ip_port(ip, port)
    a1 = auth1(ip_or_id)
    # print("a1", a1)
    if a1["errCode"] == 0:
        ch = {}
        ch['clientHello'] = a1["clientHello"]
        # print(ch)
        s1 = soc_request_post(socip, socport, "/iscjcrypt/auth/serverHello", ch)
        # print("s1", s1)
        if s1["statusCode"] == 0:
            a2 = auth2(ip_or_id, s1["data"]["serverHello"])
            # print("a2", a2)
            if a2["errCode"] == 0:
                sa = {}
                sa['clientAuth'] = a2["clientAuth"]
                sa['random'] = s1["data"]["random"]
                s2 = soc_request_post(socip, socport, "/iscjcrypt/auth/serverAuth", sa)
                # print("s2", s2)
                if s2["statusCode"] == 0:
                    d = {"a": "1"}
                    list1.append(d)
                    df1 = pd.DataFrame(list1)
                    return df1
            else:
                d = {"a": "0"}
                list1.append(d)
                df1 = pd.DataFrame(list1)
                return df1
        else:
            d = {"a": "0"}
            list1.append(d)
            df1 = pd.DataFrame(list1)
            return df1
    else:
        d = {"a": "0"}
        list1.append(d)
        df1 = pd.DataFrame(list1)
        return df1


def enc(str_ip_or_id, data):
    while True:
        s = enc_data(str_ip_or_id, data)
        if s["errCode"] == 0:
            return s["enData"]


def send_tcp_syslog(df, p=''):
    """
    @author： cj
    @date: 20201110
    @函数：send_tcp_syslog
    @参数：df表, p->(ip,port,charset)
    @描述：使用tcp发送syslog
    @返回：
    """
    p = p.strip()
    ip, port, key, charset, sdk , ip_or_id, sdke = p.split(',')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))
    try:
        for _, row in df.iterrows():
            s = row["data"]
            if key:
                s = New_encrypt(key, s)
            if sdk == '1':
                while True:
                    s1 = sign_data(ip_or_id, s)
                    if s1["errCode"] == 0:
                        s2 = {}
                        s2["signature"] = s1.get("signResult")
                        s2["log"] = s
                        s = json.dumps(s2)
                        break
            if sdke != '0':
                s = enc(ip_or_id, s)
            sock.sendto(s.encode(charset), (ip, int(port)))
    finally:
        sock.close()


def send_udp_syslog(df, p=''):
    """
    @author： cj
    @date: 20201110
    @函数：send_udp_syslog
    @参数：df表, p->(ip,port,charset)
    @描述：使用udp发送syslog
    @返回：
    """
    p = p.strip()
    ip, port, key, charset, sdk , ip_or_id, sdke = p.split(',')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        for _, row in df.iterrows():
            s = row["data"]
            if key:
                s = New_encrypt(key, s)
            if sdk == '1':
                while True:
                    s1 = sign_data(ip_or_id, s)
                    if s1["errCode"] == 0:
                        s2 = {}
                        s2["signature"] = s1.get("signResult")
                        s2["log"] = s
                        s = json.dumps(s2)
                        break
            if sdke != '0':
                s = enc(ip_or_id, s)
            sock.sendto(s.encode(charset), (ip, int(port)))
    finally:
        sock.close()
