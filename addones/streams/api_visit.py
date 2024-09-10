#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_visit.xlk
#datetime: 2024-08-30T16:10:58.533318
#copyright: OpenFBI

import sys 
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/pylibs")
sys.path.append("../")
import json
from . import *
import threading
try:
	import numpy as np 
	import  pandas as pd
	from avenger.fbiprocesser import *
	from avenger.fglobals import *

except:
	pass



#流和批共享的函数：

#数组到DF
def push_arrays_to_df(arrays,name=""):
	if len(arrays)==0:
		return 0
		
	try:
		#lockP.acquire()
		b  = arrays.copy()
		del arrays[0:len(b)]
		#arrays.clear()
		#lockP.release()

		df = pd.DataFrame(b)
		#设置index 为0
		df['seq19821221'] = 0
		df.set_index('seq19821221',inplace=True)
		if fbi_global.runtime.is_have(name):
			o = fbi_global.runtime.get(name)
			dfs=[o.df,df]
			dfz = pd.concat(dfs,sort=True)
			o.df = dfz
		else:
			o = FbiTable(name,df)
			fbi_global.runtime.put(o)
		if stream["pm_ssdb_printf"]:#用于调试
			o.df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_arrays_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
#end push_arrays_to_df

#字典到DF
def push_dict_to_df(d,name=""):
	try:
		dd = d.copy() #浅复制，保持不变
		df = pd.DataFrame(data=list(dd.values()),index=list(dd.keys()))
		o = FbiTable(name,df)
		fbi_global.runtime.put(o)
		if stream["pm_ssdb_printf"]:#用于调试
			df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_dict_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
#end push_dict_to_df


#mysql到DF
def mysql_to_df(a,cols,name=""):
	try:
		df = pd.DataFrame(data=a,columns=cols)
		if stream["pm_ssdb_printf"]:#用于调试
			df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_mysql_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
	return df
#end mysql_to_df

#参数替换
def replace_ps(p,runtime):	
	for k in runtime.keys:
		p = p.replace(k,runtime.ps[k])	
	return p

#处理单值变量的替换
def deal_sdf(work_space="",prmtv=""):	
	if prmtv.find("$")==-1: #未找到需要替换的变量
		return prmtv

	#仅适用当前工作区
	d = fbi_global.get_runtime().get_cur_ws().workspace	
	
	#处理单值$,不能跨区 add by gjw on 20220507
	keys = list(d.keys())
	#倒序，越长的越在最前面
	keys.sort(key=len,reverse = True)
	
	for k in keys:
		if d[k].type==2:
			try:
				if isinstance(d[k].vue,str):
					prmtv = prmtv.replace("$%s"%(k),d[k].vue)
				else:
					prmtv = prmtv.replace("$%s"%(k),str(d[k].vue))
			except:
				try:
					if isinstance(d[k].vue,str):
						prmtv = prmtv.replace("$%s"%(k),str(d[k].vue,"utf-8"))
				except:
					prmtv = prmtv.replace("$%s"%(k),str(d[k].vue,"gbk"))
	return prmtv

#LastModifyDate:　2024-01-09T10:23:26    Author:   rzc

#LastModifyDate:　2024-01-08T09:38:41    Author:   superFBI

#LastModifyDate:　2024-01-06T16:25:07    Author:   superFBI

#LastModifyDate:　2024-01-06T15:42:04    Author:   superFBI

#LastModifyDate:　2024-01-06T14:00:16    Author:   superFBI

#LastModifyDate:　2024-01-05T11:19:46.689746    Author:   superFBI

#LastModifyDate:　2023-08-08T18:31:57.316818    Author:   pjb

#LastModifyDate:　2023-05-31T09:48:57.634546    Author:   rzc

#LastModifyDate:　2023-05-24T15:51:19.833329    Author:   rzc

#LastModifyDate:　2023-05-24T15:14:56.425260    Author:   rzc

#LastModifyDate:　2023-05-24T11:44:23.098578    Author:   rzc

#xlink脚本

#file: api_visit.xlk

#name: 用来存储单一的http协议数据

#描述： 将http协议进行去重进行单一存储

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with api_visit

#停止

#a = @udf FBI.x_finder3_stop with api_visit

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:api_visit,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::api_visit

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "存储首次发现数据"
	stream["meta_desc"] = "将http协议进行去重进行单一存储"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["st"]["st_1s"]={"times":1,"fun":"print1"}
	stream["st"]["st_30s"]={"times":30,"fun":"print10"}
	#从ssdb中加载一个hashmap的字典，用于比对去重等
	stream["url_dis"] = load_ssdb_hall("FF:urldis")
	stream["api_merge1"] = load_ssdb_hall("FF:api_merge1")
	pool["http_visit"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	url=o.get("url")
	if url not in stream["url_dis"]:
	#解除注释 by superFBI on 2023-05-12 10:10:20
		#hp = ujson.loads(o.get("httpjson"))
		http=o.get("http")
		url_c=o.get("url_c")
		if url_c in stream["api_merge1"]:
			url_c=url
		data = {
			"id": xlink_uuid(0),
			"url": url_c,
			"urld": o.get("url"),
			"time": iso_to_datetime(o.get('timestamp')),
			"app": o.get("app"),
			"srcip": o.get("src_ip"),
			"account": o.get("account"),	"content_type": o.get("data_type"),
			"api_type": str(o.get("api_type")),
			"content_length": o.get("http").get('length', 0),
			"parameter": o.get("parameter"),
			"http_method": http.get('http_method'),
			"request_headers": http.get('request_headers'),
			"response_headers": http.get('response_headers'),
			"status": http.get('status'),
			"response_body": o.get('http_response_body'),
			"request_body": o.get('http_request_body'),
			"dstip": o.get("dest_ip"),
			"dstport": o.get("dest_port"),
			"srcport": o.get("src_port")
		}
		to_pool("http_visit",data)
		stream["url_dis"][url] = True
		to_ssdb_h("FF:urldis", url, True)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print1(st):
	store_ckh(pool["http_visit"],"api_httpdata")
#end 

#窗口函数，使用FBI的原语

#系统定时函数，st为时间戳 
def print10(st):
	stream["api_merge1"] = load_ssdb_hall("FF:api_merge1")
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64

#end 

#udf

#end 
