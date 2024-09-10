# -*- coding:utf-8 -*-
# @FileName  :mondic.py
# @Time      :2023-06-30 17:12
# @Author    :Rzc
import os.path
import pickle
import shutil

import pandas as pd


def mon_dic_api(df,p=""):
    """
    :param df:url,risk_level,api_type,name,app,data_type
    :param p:
    :return:
    """
    try:

        #对df进行遍历
        monitor_dict_api={}
        #写入副本文件
        file_path="/data/xlink/api_mon.pkl"
        temp_file_path=file_path+".temp"
        for index,row in df.iterrows():
            api=[]
            urls=row["url"]
            api.append(row["risk_level"])
            api.append(row["api_type"])
            api.append(row["name"])
            #api.append(row["app"])
            api.append(row["data_type"])
            monitor_dict_api[urls]=api
        #将pkl存储到dev/shm中
        with open(temp_file_path,'wb')as fp:
            pickle.dump(monitor_dict_api,fp)
        #写入完成后替换原文件
        shutil.move(temp_file_path,file_path)
        return pd.DataFrame(["创建成功"])
    except Exception as e:
        return pd.DataFrame(["创建失败"+e.__str__()])
def mon_dic_app(df,p=""):
    """
    :param df:app,name
    :param p:
    :return:
    """
    try:
        monitor_dict_app={}
        file_path = "/data/xlink/app_mon.pkl"
        temp_file_path = file_path + ".temp"
        for index,row in df.iterrows():
            #apps=[]
            app=row["app"]
            #apps.append(row["name"])
            #单个应用等于应用名
            monitor_dict_app[app]=row["name"]
        # 将pkl存储到dev/shm中
        with open(temp_file_path, 'wb') as fp:
            pickle.dump(monitor_dict_app, fp)
        # 写入完成后替换原文件
        shutil.move(temp_file_path, file_path)
        #return pd.DataFrame(monitor_dict_app)
        return pd.DataFrame(["存储成功"])
    except Exception as e:
        return pd.DataFrame(["存储失败"+e.__str__()])


def load_pkl(fp):
    """
    :param fp:文件名
    :return:
    """
    #创建备份文件
    #temp_file_path=fp+".temp"
    #读取pkl文件
    try:
        if os.path.exists(fp):
            with open(fp,'rb')as f:
                dic=pickle.load(f)
        else:
            dic={}
    except:
        dic={}
    return dic
def dump_pkl(fp,dic):
    """
    :param fp:文件名
    :return:
    """
    #创建备份文件
    #temp_file_path=fp+".temp"
    with open(fp,'wb')as f:
        pickle.dump(dic,f)
    #写入完成后替换原文件名称
    #shutil.move(temp_file_path,fp)

#查看对象是否存储在文件中

def FF_app(df,p=''):
    """
    :param df:读取对象文件信息
    :param p:
    :return:
    api=@udf udf0.new_df with aa
    df=@udf api by mondic.FF_app with '192.168.5.122'
    """
    app_dic=load_pkl('/dev/shm/FF_app2.pkl')
    app=p.strip()
    if app in app_dic:
        return pd.DataFrame([True])
    else:
        return pd.DataFrame([False])
def FF_api(df,p=''):
    """
    :param df:读取接口信息
    :param p:
    :return:
    """
    api_dic=load_pkl('/dev/shm/FF_url2.pkl')
    api=p.strip()
    if api in api_dic:
        return pd.DataFrame([True])
    else:
        return pd.DataFrame([False])
def FF_ip(df,p=''):
    """
    :param df:读取IP信息
    :param p:
    :return:
    """
    ip_dic=load_pkl("/dev/shm/FF_ip2.pkl")
    ip=p.strip()
    if ip in ip_dic:
        return pd.DataFrame([True])
    else:
        return pd.DataFrame([False])

def FF_account(df,p=''):
    """
    :param df:读取IP信息
    :param p:
    :return:
    """
    acc_dic=load_pkl("/dev/shm/FF_user3.pkl")
    acc=p.strip()
    if acc in acc_dic:
        return pd.DataFrame([True])
    else:
        return pd.DataFrame([False])

def url_n_y(url,total_info,sen_url):
    """
    :param url: 当前接口
    :param total_info:  敏感识别数据
    :param sen_url: 接口字典
    :return:
    {
        “url”:{"count":1,"yn_sen":"1"}#表示存在敏感识别
        ”url_c“:{"count":1,"yn_sen":"0"}#表示不存在敏感识别
    }
    1.首先判断 url存在于sen_url中，不存在，则进行 敏感识别 sen_data
    """
    pass
def temp_dic(data,file_path):
    """
    :param df:app,name
    :param p:
    :return:
    """
    try:

        temp_file_path = file_path + ".temp"
        # 将pkl存储到dev/shm中
        with open(temp_file_path, 'wb') as fp:
            pickle.dump(data, fp)
        # 写入完成后替换原文件
        shutil.move(temp_file_path, file_path)
        #return pd.DataFrame(monitor_dict_app)
        return pd.DataFrame(["存储成功"])
    except Exception as e:
        return pd.DataFrame(["存储失败"+e.__str__()])
def load_set_pkl(fp):
    # 创建备份文件
    # temp_file_path=fp+".temp"
    # 读取pkl文件
    try:
        if os.path.exists(fp):
            with open(fp, 'rb') as f:
                my_set = pickle.load(f)
        else:
            my_set = set()
    except:
        my_set=set()
    return my_set
def remove_file(file_path,target_path,files):
    """
    :param target_path:当前目录文件
    :return:
    """

    if os.path.exists(file_path):
        #读取文件
        with open(file_path,'rb')as file:
            loaded_data=pickle.load(file)
        #移动文件到目标路径
        new_file_path=os.path.join(target_path,os.path.basename(file_path))
        shutil.move(file_path,new_file_path)
        return loaded_data
    else:
        path=target_path+"/"+files
        with open(path,'rb')as file:
            loaded_data=pickle.load(file)
        return loaded_data
def df_rever(df,p=""):
    url=p.strip()
    urllst=df[url].to_list()
    df=pd.DataFrame({"urls":[urllst]})
    return df
if __name__ == '__main__':
    loaded_data=remove_file("E:\code\company_project\Data_Analyze\FF_app3.pkl","E:\code\company_project\monitor_project","FF_app3.pkl")
