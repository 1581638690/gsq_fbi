# /bin/python
# -*- coding: utf-8 -*-
"""
简化操作，方便使用
author : shb

"""
import random
import re
import subprocess
import sys
import os
import time
import pandas as pd
import numpy as np

sys.path.append("../")
sys.path.append("./lib")
sys.path.append("../lib")


# 将df1中的多个列通过 字典表df2 匹配转换，可写多列 例如df = @udf df1,df2 by DT.tag2dict with col1,col2
def tag2dict(df1, df2, p=''):
    df = df1.copy()
    p = p.strip()
    col_list = p.split(',')
    # dict1 = {}
    # if 'id' in df2:
    #     for index, rows in df2.iterrows():
    #         dict2 = {rows['id']: rows['value']}
    #         dict1.update(dict2)
    # else:
    #     for index, rows in df2.iterrows():
    #         dict2 = {index: rows['value']}
    #         dict1.update(dict2)

    for col_name in col_list:
        # dict3 = {col_name: dict1}
        for index, rows in df2.iterrows():
            # rows[col_name] = ','.join([dict1.get(int(y)) for y in rows[col_name].split(',')]) if rows[
            #                                                                                          col_name] != '' else ''
            if 'id' in df2:
                df.loc[:, col_name] = df.loc[:, col_name].apply(lambda x: x.replace(rows['id'], rows['value']) if x !='' else '')
            else:
                df.loc[:, col_name] = df.loc[:, col_name].apply(
                    lambda x: ','.join(x.replace(index, rows['value'])) if x != '' else '')

    return df


# 在linux服务器执行命令
def cmd(df, p=''):
    p = p.strip()
    try:
        tmp = subprocess.Popen(p, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        list1 = []
        for line in tmp.stdout.readlines():
            list1.append(line.strip())
        df1 = pd.DataFrame({'result': list1})
        # df1.columns = ['result']
    except Exception as e:
        return pd.DataFrame({'res': [e]}, index=[0])
    return True


# 判断列表与另一个列表的关系
def list_relation(df, p=''):
    p = p.strip()
    col1, col2, relation = p.split(',')
    df1 = df.copy()
    for index, rows in df1.iterrows():
        if relation == 'common':
            df_list2 = rows[col2].split(',')
            df_list1 = rows[col1].split(',')
            list1 = [x for x in df_list1 if x in df_list2]
            df1.at[index, 'common'] = ','.join(list1)
            # return df1
        elif relation == 'belong':
            df1.at[index, 'belong'] = True
            for col in col1.split("|"):
                df_list2 = rows[col2].strip().split(',')
                df_list1 = rows[col].strip().split(',') if rows[col].strip() != '' else []
                list1 = [x for x in df_list1 if x in df_list2]
                df1.at[index, 'belong'] *= True if df_list1 == list1 else False
            # return df1
        elif relation == 'diff':
            df_list2 = rows[col2].split(',')
            df_list1 = rows[col1].strip().split(',') if rows[col1].strip() != '' else []
            list1 = [x for x in df_list1 if x not in df_list2]
            df1.at[index, 'diff'] = list1
            # return df1
        else:
            raise KeyError("Wrong input args")
    return df1


if __name__ == '__main__':
    df1 = pd.DataFrame({'tag1': ['9,1,6', '', '3,3', '6,3'], 'tag2': ['a,b', 'b', 'c,d,e', 'd,b,c'],
                        'kind': ['a,b,c', 'd,c', 'c,d,e', 'a,d,b,e']}, index=[0, 1, 2, 3])
    df2 = pd.DataFrame({'value': ['银行', '企业', 'car', 'door'], 'id': ['1', '9', '6', '3']}, index=['1', '2', '3', '4'])
    df = tag2dict(df1, df2, p='tag1')
    # print(df)
    # tmp = cmd(df1, 'ls')
    # tmp = list_relation(df1, 'tag1,kind,belong')
    print(df)
