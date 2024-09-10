#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_monitor.xlk
#datetime: 2024-08-30T16:10:58.415517
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

#LastModifyDate:　2024-07-26T15:57:55    Author:   rzc

#LastModifyDate:　2024-06-04T10:38:46    Author:   rzc

#LastModifyDate:　2024-05-10T09:51:02    Author:   rzc

#LastModifyDate:　2024-05-08T14:27:41    Author:   rzc

#LastModifyDate:　2024-04-28T16:27:22    Author:   pjb

#LastModifyDate:　2024-04-25T12:14:33    Author:   pjb

#LastModifyDate:　2024-04-25T11:35:33    Author:   pjb

#LastModifyDate:　2024-04-25T11:03:22    Author:   pjb

#LastModifyDate:　2024-04-25T10:59:58    Author:   pjb

#LastModifyDate:　2024-04-25T10:44:02    Author:   pjb

#LastModifyDate:　2024-04-07T12:14:18    Author:   pjb

#xlink脚本

# 处理urls的信息

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "审计数据存储数据库进程"
	stream["meta_desc"] = "从redis中消费数据，存入ckh数据库表api_monitor、api_business"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	#stream["source"]= {"link":stream["redis_link"]+":6381","topic":"http_monitor","redis":"list"}
	stream["source"]={"unix_udp":"/tmp/http-monitor"}
	#stream["source"]= {"link":"127.0.0.1:6381","topic":"http_monitor","redis":"list"}
	#stream["max_xlink"]=2
	stream["st"]["st_10s"]={"times":5,"fun":"print10"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	stream["max_mem"] = 4
	if "api_monitor" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	pool["http_business"] = []
	pool["monitors"] = []
	
	stream["perf_funs"]=[transate_ckh]
	stream["store_mon"]=0
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	o["ip_dep"] = ""
	o["account_dep"] = ""
	o["api_type"]=str(o["api_type"])
	del o["session_id"]
	#del o["user"]
	if "monitors_keys" not in stream:
		stream["monitors_keys"] = list(o.keys())
	o["time"] = iso_to_datetime(o["time"])
	o["request_body_json"] = ujson.dumps(o["request_body_json"])
	o["parameter_json"] = ujson.dumps(o["parameter_json"])
	o["request_headers"] = ujson.dumps(o["request_headers"])
	o["response_headers"] = ujson.dumps(o["response_headers"])
	o["info"] =  ujson.dumps(o["info"])
	o["key"] =  ujson.dumps(o["key"])
	stream["store_mon"] += 1
	to_pool("monitors",list(o.values()))
	if stream["sends"]:
		s = deepcopy(o)
		s["event_type"] = "api_monitor"
		#to_kfk(s)
		s["time"] = str(s["time"])
		to_json_file("/data/syslog_file/eve",s)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["store_mon"]))
	if "monitors_keys" in stream:
		store_ckh2(pool["monitors"],"api_monitor",stream["monitors_keys"])
#end 

#系统定时函数，st为时间戳 
def send60(st):
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_monitor" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
from copy import deepcopy
#end 

#udf

#end 
