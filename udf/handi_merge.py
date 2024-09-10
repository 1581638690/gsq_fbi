# coding=gbk
import pandas as pd
import copy
def merge(df,p=""):
    """
    [
    {"gmt_create":"2023-02-28T11:37:20","gmt_modified":"2023-03-01T09:00:20","creator":"system","owner":"public","url":"http:\/\/205.174.165.68\/","api":"\/","parameter":"ZDNMU=PGOVB","protocol":"HTTP\/1.1","name":"","app":"205.174.165.68","dstip_num":1,"dstport":80,"api_type":0,"method":"GET","data_type":"HTML","first_time":"2023-02-28T11:32:24.522700+0800","last_time":"2023-03-01 08:59:45.206347","api_status":"0","risk_level":"2","risk_label":"API19-4;","risk_label_value":"API19-4\u7f3a\u4e4f\u8d44\u6e90\u548c\u901f\u7387\u9650\u5236;","req_label":"","res_llabel":"","srcip_num":1,"account_num":0,"visits_num":98467,"visits_flow":391379280,"app_type":0,"sensitive_label":"0","active":0,"auth_type":0,"scope":"","dstip":"","btn_show":"1,1,1,1,0"}
    ,{"gmt_create":"2023-02-28T11:57:00","gmt_modified":"2023-03-01T09:00:20","creator":"system","owner":"public","url":"http:\/\/205.174.165.68\/dv\/login.php","api":"\/dv\/login.php","parameter":"","protocol":"HTTP\/1.1","name":"","app":"205.174.165.68","dstip_num":1,"dstport":80,"api_type":1,"method":"GET","data_type":"\u52a8\u6001\u811a\u672c","first_time":"2023-02-28T11:54:34.477119+0800","last_time":"2023-03-01 08:58:19.662859","api_status":"0","risk_level":"2","risk_label":"API19-2;API19-4;","risk_label_value":"API19-2\u635f\u574f\u7684\u7528\u6237\u8eab\u4efd\u9a8c\u8bc1;API19-4\u7f3a\u4e4f\u8d44\u6e90\u548c\u901f\u7387\u9650\u5236;","req_label":"","res_llabel":"","srcip_num":1,"account_num":1,"visits_num":4059,"visits_flow":2985458,"app_type":0,"sensitive_label":"0","active":0,"auth_type":0,"scope":"","dstip":"192.168.10.50","btn_show":"1,1,1,1,0"}
    ]
    p：为一个列表，
    状态码：1为合并的 0为未合并
    状态码默认为
    :param df:
    :param p:
    :return:
    """
    #获取合并的列表 数据
    #df=pd.DataFrame(df1,index=[2,36])
    url_merges=df["url_merges"].tolist()
    url_merge=url_merges[0]
    api_status=df["api_status"].tolist()
    #取出数据中的接口,存储为被合并的接口
    url_list=df["url"].tolist()
    mege_url=";|".join(url_list)
    #对df表进行索引取值 取出第一个
    index=df.index.tolist()[0]
    del df["gmt_create"]
    del df["gmt_modified"]
    del df["creator"]
    del df["owner"]
    try:
        del df["btn_show"]
    except:
        pass
    #取出df表中的第一行,s
    df_=df.loc[index,:].to_frame()

    df_f=df_.T


    df_f.loc[index,'url_sum']=mege_url
    #df_f.loc[index,"url_merges"]=""
    df_f.loc[index,"url"]=url_merge
    df_f.loc[index,"merge_state"]=2
    df_f.loc[index, "parameter"] = ""
    df_f.loc[index, "api"] = ""
    df_f.loc[index,"name"]=""
    df_f.loc[index,"visits_flow"]=df["visits_flow"].sum(axis=0)
    df_f.loc[index,"visits_num"]=df["visits_num"].sum(axis=0)
    df_f.loc[index,"dstip_num"]=df["dstip_num"].sum()
    df_f.loc[index,"srcip_num"]=df["srcip_num"].sum()
    df_f.loc[index,"account_num"]=df["account_num"].sum()
    df_f.loc[index,"auth_type"] = df["auth_type"].max()
    df_f.loc[index,"active"] = df["active"].max()
    #获取敏感等级标签
    sensitive_label=df["sensitive_label"].tolist()
    a=[int(i) for i in sensitive_label]
    df_f.loc[index,"sensitive_label"]=str(max(a))
    df_f.loc[index,"api_type"]=df["api_type"].max()

    #审计状态
    df_f.loc[index,"api_status"]=max(api_status)

    #风险等级
    risk_level=df["risk_level"].tolist()
    r=[int(i) for i in risk_level]
    df_f.loc[index,"risk_level"]=str(max(r))

    #风险标签
    risk_label=df["risk_label"].tolist()
    #对其进行拼接然后利用;号分割 进行
    rl=""
    for i in risk_label:
        rl+=i
    rll=rl.split(";")
    rll=[i for i in rll if i!=""]#去掉空值
    rll=list(set(rll))#去重
    risk_l=";".join(rll)#连接
    df_f.loc[index,"risk_label"]=risk_l

    #risk_label_value 风险标签值
    risk_label_value=df["risk_label_value"].tolist()
    ri=""
    for i in risk_label_value:
        ri+=i
    rii=ri.split(";")
    rii = [i for i in rii if i != ""]  # 去掉空值
    rii = list(set(rii))  # 去重
    risk_i = ";".join(rii)  # 连接
    df_f.loc[index,"risk_label_value"] = risk_i

    #合并数据将被合并的数据和合并的数据进行处理
    df1=pd.concat([df,df_f])
    return df1


def dispose(df):
    df["y_url"] = df["y_url"].apply(lambda x: x.replace("\\", ""))
    df["url"] = df["url"].apply(lambda x: x.replace("\\", ""))
    # 判断接口中是否存在p1 p2
    #filter_df = df[df["url"].str.contains("{p1}") | df["url"].str.contains("{p2}")]
    # 对url进行分组
    # grouped=filter_df.groupby('url').agg({"y_url":'count'})
    grouped = df.groupby('url')
    # 取出
    # filter_df=grouped[grouped["y_url"]>=10]
    result = grouped.aggregate(lambda x: ';|'.join(x))
    #result = result[result["y_url"].apply(lambda x: len(x.split(";|")) < 10)]

    return result
def limit_ten(df):
    df["y_url"] = df["y_url"].apply(lambda x: x.replace("\\", ""))
    df["url"] = df["url"].apply(lambda x: x.replace("\\", ""))
    # 判断接口中是否存在p1 p2
    filter_df = df[df["url"].str.contains("{p1}") | df["url"].str.contains("{p2}")]
    # 对url进行分组
    # grouped=filter_df.groupby('url').agg({"y_url":'count'})
    grouped = filter_df.groupby('url')
    # 取出
    # filter_df=grouped[grouped["y_url"]>=10]
    result = grouped.aggregate(lambda x: ';|'.join(x))
    result = result[result["y_url"].apply(lambda x: len(x.split(";|")) < 10)]
    return result
def id_drop(df):
    filter_df=df[df["ltten_url"].str.contains("{dst}")]
    #判断{dst}中是否存在  找出两个相等的
    grouped=filter_df.groupby("ltten_url")
    #找到相等的和不等的 判断相等的url是否存在与 y_url

    return grouped
def aaa(df):
    filter_df = df[df["ltten_url"].str.contains("{p1}") | df["ltten_url"].str.contains("{p2}")]
    return filter_df
def filter_ten(df):
    # 判断接口中是否存在p1 p2
    filter_df = df[df["ltten_url"].str.contains("{p1}") | df["ltten_url"].str.contains("{p2}")]
    #筛选出ltten_url存在{p1}和{p2}的url与ltten_url不同的接口
    df_filtered=filter_df[filter_df["ltten_url"] != filter_df["url"]]
    #然后对齐进行连接
    #grouped=df_filtered.groupby("ltten_url")["url"].agg(["count"])
    #filterdf=df_filtered[df_filtered["ltten_url"].isin(grouped[grouped["count"]>=8].index)]
    return df_filtered
def drop_dst(df):
    filter_df=df[df["ltten_url"].str.contains("{dst}")]
    #山选出url与ltten_url不同的数据
    df_filter=filter_df[filter_df["ltten_url"]!=filter_df["url"]]
    return df_filter
def delete_df(df):
    del_df=df[df["ltten_url"] != df["url"]]
    return del_df

def ApiMerging(df):
    filter_df = df[df["ltten_url"].str.contains("{p1}")]
    equal_url = filter_df[filter_df["ltten_url"] == filter_df["url"]]
    no_equal = filter_df[filter_df["ltten_url"] != filter_df["url"]]
    merge = pd.merge(equal_url, no_equal, on="ltten_url", suffixes=("_df1", "_df2"))
    merge = merge.drop(["id_df1", "url_df1", "api_df1"], axis=1)
    merge = merge.rename(columns={"id_df2": "id", "url_df2": "url", "api_df2": "api"})
    return merge

if __name__ == '__main__':
    data = [
        {
            "gmt_create": "2023-02-28T11:57:00",#
            "gmt_modified": "2023-03-01T11:00:24",#
            "creator": "system",#
            "owner": "public",#
            "url": "http://205.174.165.68/dv/login.php",#
            "api": "/dv/login.php",
            "parameter": "", #
            "protocol": "HTTP/1.1",#
            "name": "",#
            "app": "205.174.165.68",#
            "dstip_num": 1,#
            "dstport": 80,#
            "api_type": 0,#
            "method": "GET",#
            "data_type": "动态脚本",
            "first_time": "2023-02-28T11:54:34.477119+0800",#
            "last_time": "2023-03-01 10:55:20.644695",#
            "api_status": "0",#
            "risk_level": "2",#
            "risk_label": "API19-2;API19-4;",#
            "risk_label_value": "API19-2损坏的用户身份验证;API19-4缺乏资源和速率限制;",
            "req_label": "",
            "res_llabel": "",
            "srcip_num": 1,#
            "account_num": 1,#
            "visits_num": 4165,#
            "visits_flow": 3064365,#
            "app_type": 0,#
            "sensitive_label": "1",
            "active": 0,#
            "auth_type": 0,#
            "scope": "",
            "dstip": "192.168.10.50",
            "btn_show": "1,1,1,1,0",
            "url_merges": "http://205.174.165.68/dv/{dst}",
            "merge_state": 1,
            "url_sum": ""
        },
        {
            "gmt_create": "2023-02-28T11:57:00",
            "gmt_modified": "2023-03-01T11:00:24",
            "creator": "system",
            "owner": "public",
            "url": "http://205.174.165.68/dv/vulnerabilities/xss_r/",
            "api": "/dv/vulnerabilities/xss_r/",
            "parameter": "",
            "protocol": "HTTP/1.1",
            "name": "",
            "app": "205.174.165.68",
            "dstip_num": 1,
            "dstport": 80,
            "api_type": 1,
            "method": "GET",
            "data_type": "HTML",
            "first_time": "2023-02-28T11:54:34.499339+0800",
            "last_time": "2023-03-01 10:52:07.630901",
            "api_status": "1",
            "risk_level": "3",
            "risk_label": "API19-7;API19-4;",
            "risk_label_value": "API19-7安全性配置错误;API19-4缺乏资源和速率限制;",
            "req_label": "",
            "res_llabel": "",
            "srcip_num": 1,
            "account_num": 0,
            "visits_num": 211,
            "visits_flow": 149644,
            "app_type": 0,
            "sensitive_label": "0",
            "active": 0,
            "auth_type": 0,
            "scope": "",
            "dstip": "192.168.10.50",
            "btn_show": "1,1,1,1,0",
            "url_merges": "http://205.174.165.68/dv/{dst}",
            "merge_state": 1,
            "url_sum": ""
        }
    ]
    p="url_merges"
    df = pd.DataFrame(data, index=[2, 36])
    df=merge(df, p)
    print(df)

