#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_business.xlk
#datetime: 2024-08-30T16:10:57.774968
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

#LastModifyDate:　2024-01-09T10:31:35    Author:   rzc

#LastModifyDate:　2024-01-09T10:30:03    Author:   rzc

#LastModifyDate:　2024-01-06T15:49:25    Author:   superFBI

#LastModifyDate:　2024-01-06T13:48:55    Author:   superFBI

#LastModifyDate:　2024-01-05T09:34:24.346376    Author:   superFBI

#LastModifyDate:　2023-12-27T09:50:00.824178    Author:   superFBI

#LastModifyDate:　2023-12-13T14:33:06.174436    Author:   superFBI

#LastModifyDate:　2023-12-12T16:57:01.356266    Author:   superFBI

#LastModifyDate:　2023-12-12T16:02:39.164131    Author:   superFBI

#LastModifyDate:　2023-12-12T15:34:37.236177    Author:   superFBI

#LastModifyDate:　2023-12-12T15:30:30.570661    Author:   superFBI

#xlink脚本

#file: api_business.xlk

#name: 业务审计

#描述： redis取过滤审计数据进行业务审计

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with api_business

#停止

#a = @udf FBI.x_finder3_stop with api_business

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:api_business,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::api_business

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "业务审计"
	stream["meta_desc"] = "redis取过滤审计数据进行业务审计"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"bs_monitor","redis":"list"}
	stream["source"]= {"unix_udp":"/tmp/bs_monitor"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_60s"]={"times":20,"fun":"send60"}
	stream["st"]["st_100s"]={"times":1800,"fun":"bssearch"}
	#stream["kfk"]={"link":"127.0.0.1:9092","topic":"api_send","key":""}
	stream["redis"]={"host":stream["redis_link"],"port":"6381"}
	stream["redis2"]={"host":stream["redis_link"],"port":"6382"}
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	d = load_ssdb_kv("model_config")
	stream["bscount"] = d["setting"]["model201"]["count"]
	stream["model_url"] = d["setting"]["model201"]["urls"].split(",")
	stream["model201_on"] = d["setting"]["switch"]["model201"]
	stream["bsfirsttime"] = ""
	stream["bsmessage"] = {}
	stream["bss"] = {}
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_model" in a:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	resbody = o.get("response_body")
	url_c = o.get("urld")
	url = o.get("url")
	dstip = o.get("dstip")
	account = o.get("account")
	o["time"] = iso_to_datetime(o["time"])
	count = o.get("yw_count")
	if stream["model201_on"] and url_c in stream["model_url"] and count > stream["bscount"]:
		dict1 = o.get("key")
		srcip = o.get("srcip")
		real_ip = o.get("real_ip")
		http_api = {}
		http_api["url"] = url_c
		http_api["srcip"] = srcip
		http_api["srcport"] = o.get("srcport")
		http_api["dstip"] = dstip
		http_api["dstport"] = o.get("dstport")
		http_api["timestamp"] = o["time"]
		http_api["url_a"] = url
		http_api["account"] = account
		http_api["real_ip"] = real_ip
		http_api["app"] = o.get("app")
		http_api["id"] = xlink_uuid(0)
		http_api["type"] = 201
		http_api["level"] = 1
		http_api["proof"] = o.get("id")
		http_api["desc"] = "终端通过接口获取重要信息"
		proofs = {}
		proofs["判定标准"] = "重要信息获取行为：对重要接口（人工指定）的返回体进行JSON数组进行数量识别"
		proofs["接口"] = http_api["url"]
		if real_ip:
			srcs = real_ip
			http_api["message"] = "终端" + srcs + "（XFF地址）通过" + srcip + "（代理地址）在接口" + http_api["url"] + "中获取了信息" + str(count) + "条"
			proofs["终端"] = srcs + "（XFF地址）"
		else:
			srcs = srcip
			http_api["message"] = "终端“" + srcs + "”在接口" + http_api["url"] + "中获取了信息" + str(count) + "条"
			proofs["终端"] = srcs
		proofs["终端"] = srcs
		proofs["单次获取阈值"] = stream["bscount"]
		proofs["本次获取数量"] = count
		proofs["结果"] = "终端通过接口获取重要信息"
		proofs["证据"] = {}
		proofs["证据"]["时间"] = "HTTP协议ID"
		proofs["证据"][str(o.get("time"))] = o.get("id")
		if count > 5:
			dict1["bsxx"] = dict1["bsxx"][:5]
		proofs["证据"]["信息"] = dict1
		proofs = ujson.dumps(proofs, ensure_ascii=False)
		http_api["proofs"] = proofs
		to_table(http_api)
		if stream["sends2"]:
			ssss = deepcopy(http_api)
			ssss["event_type"] = "model"
			#to_kfk(ssss)
			ssss["timestamp"] = str(ssss["timestamp"])
			to_json_file("/data/syslog_file/eve",ssss)
		if stream["bsfirsttime"] == "":
			stream["bsfirsttime"] = str(o.get("time"))
		srcurl = srcs + "|" + http_api["url"]
		if srcurl in stream["bss"]:
		#if stream["fps"][srcurl]:
			stream["bss"][srcurl] = stream["bss"][srcurl] + count
		else:
			stream["bss"][srcurl] = count
		subs = deepcopy(http_api)
		del subs["proofs"]
		stream["bsmessage"][srcurl] = subs
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	store_ckh(table,"api_model")
#end 

#窗口函数，使用FBI的原语

#系统定时函数，st为时间戳 
def send60(st):
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_model" in a:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
	d = load_ssdb_kv("model_config")
	stream["bscount"] = d["setting"]["model201"]["count"]
	stream["model_url"] = d["setting"]["model201"]["urls"].split(",")
	stream["model201_on"] = d["setting"]["switch"]["model201"]
#end 

#系统定时函数，st为时间戳 
def bssearch(st):
	if stream["bsfirsttime"]:
		c = load_ssdb_kv("model_config")
		bstime = c["setting"]["model201"]["times"]
		bsft = int(stream["bsfirsttime"][11:13])
		t1 = int(time.strftime("%H"))
		t2 = bsft + bstime
		if t2 > 24:
			t2 = t2 - 24
		if t1 > t2:
			bsc = c["setting"]["model201"]["timec"]
			for k in stream["bss"]:
				if stream["bss"][k] > bsc:
					s = stream["bsmessage"][k]
					srcip = s.get("srcip")
					real_ip = s.get("real_ip")
					s["id"] = xlink_uuid(1)
					s["proof"] = ""
					s["desc"] = "终端通过接口段时间获取重要信息"
					proofs = {}
					proofs["判定标准"] = "对重要接口（人工指定）的返回体进行JSON数组进行数量识别"
					proofs["接口"] = s["url"]
					if real_ip:
						s["message"] = "终端" + real_ip + "（XFF地址）通过" + srcip + "（代理地址）在接口" + s["url"] + "中" + str(bstime) + "小时内获取了信息" + str(stream["bss"][k]) + "条"
						proofs["终端"] = real_ip + "（XFF地址）"
					else:
						s["message"] = "终端“" + srcip + "”在接口" + s["url"] + "中" + str(bstime) + "小时内获取了信息" + str(stream["bss"][k]) + "条"
						proofs["终端"] = srcip
					proofs["时间段（小时）"] = bstime
					proofs["段时间获取阈值"] = bsc
					proofs["段时间获取数量"] = stream["bss"][k]
					proofs["结果"] = "终端通过接口段时间获取重要信息"
					s["proofs"] = proofs
					to_table(s)
					if stream["sends2"]:
						ssss = deepcopy(s)
						ssss["event_type"] = "model"
						printf("ssss",ssss)
						#to_kfk(ssss)
						ssss["timestamp"] = str(ssss["timestamp"])
						to_json_file("/data/syslog_file/eve",ssss)
			stream["bsfirsttime"] = ""
			stream["bsmessage"] = {}
			stream["bss"] = {}
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
from copy import deepcopy
import ujson
import re
#end 

#udf

#end 
