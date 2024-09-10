from avenger.fsys import b64
from driver.pyssdb import Client
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from numpy import nan
import sys
from datetime import datetime, timedelta
import math
import re
import time
import random
import json
import ipaddress
import IPy


###连接ssdb链接
def db_conn(server="127.0.0.1", port=8888):
    conn = Client(server, port)
    return conn


# 建立数据链接 返回key的字符串
def get_ssdb_data1(key):
    conn = db_conn()
    a = conn.get(b64(key))
    if a:
        b = json.loads(a)
    else:
        b = {}
    return b


# 检验ip是否存在
def jk_tf(df, p=""):
    dict1 = get_ssdb_data1("json_wdgl")
    # dict1 = {"wd_table":
    #                  [
    #                      {"wd": "62.6.*.*", "wd1_name": "内部网C段", "wd2_name": "", "wd3_name": "", "yn": "true"},
    #                   {"wd": "168.*.*.*", "wd1_name": "内部网C段", "wd2_name": "", "wd3_name": "", "yn": "true"},
    #                  {"wd": "72.14.204.149", "wd1_name": "内部网C段", "wd2_name": "", "wd3_name": "", "yn": "true"}]}
    wd_list = dict1.get("wd_table")  # 获取到网段地址
    total_ip = df[p.strip()].tolist()
    if wd_list:

        for wd in wd_list:
            start_list = []
            end_list = []
            ip_segment = wd["wd"]
            yn = wd["yn"]
            seg_list = ip_segment.split(".")
            for seg in seg_list:
                if "-" in seg:
                    seg1 = seg.split("-")
                    start_list.append(seg1[0])
                    end_list.append(seg1[1])
                elif "*" == seg:
                    start_list.append("0")
                    end_list.append("255")
                elif "0" == seg:
                    start_list.append("0")
                    end_list.append("255")
                else:
                    start_list.append(seg)
                    end_list.append(seg)
            if start_list != [] and end_list != []:
                start_str = ".".join(start_list)
                end_str = ".".join(end_list)
                    # loc[row_index, 'new_column'] = new_value
                for ips in total_ip:#所有的ip
                    index = df[df.ip == ips].index.tolist()[0]
                    ip_list = ips.split(",")
                    if len(ip_list) > 1:
                        for ip in ip_list:
                            if IPy.IP(start_str) <= IPy.IP(ip) <= IPy.IP(end_str) and yn == "true":
                                df.loc[index, "yn"] = True
                                break
                    else:
                        if IPy.IP(start_str) <= IPy.IP(ip_list[0]) <= IPy.IP(end_str) and yn == "true":
                            df.loc[index, "yn"] = True

    #将为NAN的值都给成False
    df=df.fillna(False)

    return df


if __name__ == '__main__':
    json_ip = [{"id": 1,
                "ip": "72.14.204.149,172.217.11.6,172.217.10.230,216.58.219.198,172.217.12.134,172.217.10.6,72.14.204.148,172.217.12.198,216.58.219.230,172.217.10.38,172.217.6.198,172.217.9.230,172.217.12.166,172.217.6.230,172.217.10.134,72.14.204.149,172.217.11.38"},
               {"id": 2, "ip": "72.21.91.29"}, {"id": 3, "ip": "203.73.24.75"}, {"id": 4, "ip": "192.168.10.50"},
               {"id": 5, "ip": "202.41.220.218"}, {"id": 6, "ip": "178.255.83.1"}, {"id": 7, "ip": "192.168.5.122"},
               {"id": 8, "ip": "142.176.121.86,142.166.14.77,142.176.121.79,142.166.14.70,142.166.14.80"},
               {"id": 9, "ip": "210.188.195.42"}, {"id": 10, "ip": "68.178.178.97,68.178.178.33"}]
    df = pd.DataFrame(json_ip)

    df=jk_tf(df, p="ip")
    print(df)