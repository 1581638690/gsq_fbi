#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_ai_nlp.xlk
#datetime: 2024-08-30T16:10:58.432910
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

#LastModifyDate:　2023-08-24T09:29:48.555718    Author:   superFBI

#LastModifyDate:　2023-08-17T15:51:27.771881    Author:   qh

#LastModifyDate:　2023-08-17T14:57:49.731344    Author:   qh

#LastModifyDate:　2023-08-17T14:23:04.555225    Author:   qh

#LastModifyDate:　2023-08-17T14:07:33.654694    Author:   qh

#LastModifyDate:　2023-08-17T11:49:11.158572    Author:   qh

#LastModifyDate:　2023-08-17T11:43:44.717009    Author:   qh

#LastModifyDate:　2023-08-17T11:33:26.733132    Author:   qh

#LastModifyDate:　2023-08-14T09:24:58.052996    Author:   qh

#LastModifyDate:　2023-08-11T16:22:19.470991    Author:   qh

#LastModifyDate:　2023-08-11T15:21:05.705185    Author:   qh

#LastModifyDate:　2023-08-11T15:19:05.873086    Author:   superFBI

#LastModifyDate:　2023-08-11T14:34:45.137680    Author:   qh

#LastModifyDate:　2023-08-11T14:31:37.434279    Author:   qh

#LastModifyDate:　2023-08-11T14:12:15.597834    Author:   qh

#LastModifyDate:　2023-08-11T14:02:41.521678    Author:   qh

#LastModifyDate:　2023-08-11T09:47:24.990697    Author:   qh

#LastModifyDate:　2023-08-11T09:42:16.136584    Author:   qh

#LastModifyDate:　2023-08-10T17:37:17.693870    Author:   qh

#LastModifyDate:　2023-08-10T17:35:40.139247    Author:   qh

#LastModifyDate:　2023-08-10T17:33:58.839264    Author:   qh

#LastModifyDate:　2023-08-10T17:32:36.292274    Author:   qh

#LastModifyDate:　2023-08-09T11:55:46.852291    Author:   qh

#LastModifyDate:　2023-08-09T11:51:46.231165    Author:   qh

#LastModifyDate:　2023-08-09T11:42:16.569122    Author:   qh

#LastModifyDate:　2023-08-09T11:29:40.644371    Author:   qh

#LastModifyDate:　2023-08-09T11:24:53.959307    Author:   qh

#LastModifyDate:　2023-08-09T11:16:04.701904    Author:   qh

#LastModifyDate:　2023-08-09T11:03:54.399410    Author:   qh

#LastModifyDate:　2023-08-09T11:02:34.242703    Author:   qh

#LastModifyDate:　2023-08-09T10:48:32.398545    Author:   qh

#LastModifyDate:　2023-08-09T10:34:00.574008    Author:   qh

#LastModifyDate:　2023-08-09T10:13:50.986941    Author:   qh

#LastModifyDate:　2023-08-09T10:00:27.577850    Author:   qh

#LastModifyDate:　2023-08-09T09:58:05.921961    Author:   qh

#LastModifyDate:　2023-08-09T09:48:02.518701    Author:   qh

#LastModifyDate:　2023-08-08T17:20:10.658927    Author:   qh

#LastModifyDate:　2023-08-08T17:17:44.241759    Author:   qh

#LastModifyDate:　2023-08-08T17:11:38.381215    Author:   qh

#LastModifyDate:　2023-08-08T16:50:01.855055    Author:   qh

#LastModifyDate:　2023-08-08T16:49:46.940509    Author:   qh

#LastModifyDate:　2023-08-08T16:48:32.691825    Author:   qh

#LastModifyDate:　2023-08-08T16:20:08.523191    Author:   qh

#LastModifyDate:　2023-07-25T11:34:32.987219    Author:   qh

#LastModifyDate:　2023-07-25T11:09:54.065087    Author:   qh

#xlink脚本

#file: a1_hanlp_test.xlk

#name: 中文分词测试

#描述： 6666666666

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with a1_hanlp_test

#停止

#a = @udf FBI.x_finder3_stop with a1_hanlp_test

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:a1_hanlp_test,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::a1_hanlp_test

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "基于深度学习识别姓名、地址、机构"
	stream["meta_desc"] = "99999999999"
	stream["source"]= {"link":"127.0.0.1:6381","topic":"http_nlp","redis":"list"}
	#stream["source"]= {"link":"127.0.0.1:6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"link":"127.0.0.1:6381","topic":"test","redis":"list_json"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["redis"]={"host":stream["redis_link"],"port":"6381"}
	#自定义的统计变量
	stream["count"] = 0
	# 自定义的词语
	# stream["ltp"].add_words(words=["郑州云智信安安全技术有限公司"])
	stream["max_mem"] = 10
	stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
	stream["m"] = 1
	stream["redis_list_depth"]= 100000
	name_list = load_ssdb_kv("writelist")
	stream["name_list"] = []
	for item in name_list["write_list"]["name_list"]["name"]:
		stream["name_list"].append(item["data"])
	stream["ai_switch"] = name_list["name_switch"] # "0"是AI识别
	ai_cpu = name_list["AI_cpu"]
	torch.set_num_threads(ai_cpu)
	switch = load_ssdb_kv("sensitive")["data"]
	for item in switch:
		if item["rekey"] == "地址":
			if item["off"] == 1:
				stream["addr_switch"] = 1
			else:
				stream["addr_switch"] = 0
		if item["rekey"] == "姓名":
			if item["off"] == 1:
				stream["name_switch"] = 1
			else:
				stream["name_switch"] = 0
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	if (stream["addr_switch"] == 0 and stream["name_switch"] == 0) or stream["ai_switch"] != "0":
		pass
	else:
		if stream["m"]:
			stream["ltp"] = LTP("/data/base1")
			stream["m"] = 0
		response_body=o["http_response_body"]
		request_body=o["http_request_body"]
		fcount = {}
		f2count = {}
		if response_body:
			fcount, finfo = ltp_find(response_body)
		if request_body:
			f2count, f2info = ltp_find(request_body)
		if fcount or f2count:
			#printf("敏感统计",fcount)
			#printf("敏感内容",finfo)
			suid = xlink_uuid(1)
			srcip = o['src_ip']
			request_headers=o.get("http").get("request_headers","")
			realip, agent_ip = real_ip(request_headers,srcip)
			c={}
			c["timestamp"]= iso_to_datetime(o["timestamp"])
			c["flow_id"]=o.get("flow_id")
			c["src_ip"]= srcip
			c["dest_ip"]= o.get("dest_ip")
			c["dest_port"]=o.get("dest_port")
			if o.get("http").get("http_method"):
				c["http_method"]=o["http"]["http_method"]
			else:
				c["http_method"]=''
			c["uuid"]=suid
			c["url"] = o["url_c"]
			c["url_c"] = o["url"] #未合并的
			c["app"]=o["app"]
			c["account"]=o["account"]
			c["parameter"]=o["parameter"]
			c["request_bodys"]=request_body
			c["response_bodys"]=response_body
			c["cookie"]=o.get("http").get("cookie","")
			c["request_count"]=f2count
			c["response_count"]=fcount
			sfinfo = {}
			sfcount = {}
			sfinfo["识别"] = "AI"
			if fcount:
				sfinfo["响应体"] = finfo
				sfcount["响应体"] = fcount
			if f2count:
				sfinfo["请求体"] = f2info
				sfcount["请求体"] = f2count
			c["msg_total"]=sfinfo
			c["sen_type_count"]=sfcount
			c["real_ip"]=realip
			c["srcport"]=o["src_port"]
			to_redis("sen_count",c)
			stream["count"] += 1
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	#store_ckh(table,"test_ltp")
	printf("敏感统计",stream["count"])
	name_list = load_ssdb_kv("writelist")
	not_name = []
	for item in name_list["write_list"]["name_list"]["name"]:
		not_name.append(item["data"])
	stream["name_lsit"] = not_name
	switch = load_ssdb_kv("sensitive")["data"]
	for item in switch:
		if item["rekey"] == "地址":
			if item["off"] == 1:
				stream["addr_switch"] = 1
			else:
				stream["addr_switch"] = 0
		if item["rekey"] == "姓名":
			if item["off"] == 1:
				stream["name_switch"] = 1
			else:
				stream["name_switch"] = 0
	stream["ai_switch"] = name_list["name_switch"] # 0是AI识别
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ltp_find(a):
	a = re.sub(r'[^\w]','',a)
	s = ""
	s = a
	nh = []
	ni = []
	ns = []
	for dd in range(10):
		result = stream["ltp"].pipeline(s, tasks=["cws", "ner"])
		if result.ner:
			for i in result.ner:
				if stream["name_switch"] and i[0] == "Nh" and 5 > len(i[1]) > 1 and not re.findall(r'[A-Za-z_\W]+', i[1]) and i[1] not in stream["name_lsit"]:
					nh.append(i[1])
				if i[0] == "Ni":
					if len(i[1]) > 6 and re.findall(r'(公司|集团|学院|学校|法院|公安|政府|局)', i[1]):
						ni.append(i[1])
				if stream["addr_switch"] and i[0] == "Ns" and len(i[1]) > 6:
					ns.append(i[1])
			s = result.cws[-1]
		else:
			break
	#ni2 = []
	for i in ni:
		if len(i) > 16:
			result = stream["ltp"].pipeline(i, tasks=["cws", "ner"])
			if result.ner:
				for r in result.ner:
					#if r[0] == "Ni":
						#if len(r[1]) > 6 and re.findall(r'(公司|集团|学院|学校|法院|公安|政府|局)', r[1]):
							#ni2.append(r[1])
					if stream["name_switch"] and r[0] == "Nh" and 5 > len(r[1]) > 1 and not re.findall(r'[A-Za-z_\W]+',r[1]) and r[1] not in stream["name_lsit"]:
						nh.append(r[1])
					if stream["addr_switch"] and r[0] == "Ns" and len(r[1]) > 6:
						ns.append(r[1])
		#else:
			#ni2.append(i)
	finfo = {}
	fcount = {}
	#if ni2:
		#finfo["机构"] = list(set(ni2))
		#fcount["机构"] = len(set(ni2))
	if nh:
		finfo["姓名"] = list(set(nh))
		fcount["姓名"] = len(set(nh))
	if ns:
		finfo["地址"] = list(set(ns))
		fcount["地址"] = len(set(ns))
	return fcount,finfo
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def real_ip(request_headers,srcip):
	real_ip = ''
	agent_ip = ''
	try:
		#request_headers = element.get('http').get('request_headers')
		for i in request_headers:
			if i['name'] == 'X-Forwarded-For':
				ip = i['value'].split(',')
				ip2 = []
				for i in ip:
					ip2.append(i.strip())
				real_ip = ip2[0]
				agent_ip = ip2[1:]
				agent_ip.append(srcip)
	except:
		pass
	return real_ip, agent_ip
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
 return "%d-%7f-%3f" % (x,time.time(), random.random())
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
import os
import re
from ltp import LTP
import torch
import datetime
#end 

#udf

#end 
