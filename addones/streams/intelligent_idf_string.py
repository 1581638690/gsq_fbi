#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: intelligent_idf_string.xlk
#datetime: 2024-08-30T16:10:58.463061
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

#LastModifyDate:　2024-03-26T16:34:32    Author:   rzc

#LastModifyDate:　2024-03-26T16:24:56    Author:   rzc

#LastModifyDate:　2024-03-26T15:16:14    Author:   rzc

#LastModifyDate:　2024-03-26T15:15:31    Author:   rzc

#LastModifyDate:　2024-03-26T11:35:06    Author:   rzc

#LastModifyDate:　2024-03-25T17:41:11    Author:   rzc

#LastModifyDate:　2024-03-25T17:27:09    Author:   rzc

#LastModifyDate:　2024-03-25T17:25:54    Author:   rzc

#LastModifyDate:　2024-03-25T15:56:27    Author:   rzc

#LastModifyDate:　2024-03-25T09:34:37    Author:   rzc

#LastModifyDate:　2024-03-22T16:51:29    Author:   rzc

#xlink脚本

#file: intelligent_idf_string.xlk

#name: 智能识别字符串信息

#描述： 从字符串信息中标识出来数据,并根据形成的规则对数据进行精准识别

#创建时间: 2024-03-21T17:16:51.289137

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with intelligent_idf_string

#停止

#a = @udf FBI.x_finder3_stop with intelligent_idf_string

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:intelligent_idf_string,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::intelligent_idf_string

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "智能识别字符串信息"
	stream["meta_desc"] = "从字符串信息中标识出来数据,并根据形成的规则对数据进行精准识别"
	stream["source"]= {"unix_udp":"/tmp/o_rules"}
	
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_120s"]={"times":120,"fun":"send120"}
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	stream["rules"] = load_pkl("/data/xlink/intell_rules.pkl")
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	
	http = o.get("http")
	http_method = http.get("http_method")
	dest_ip = o.get("dest_ip")
	dest_port = o.get("dest_port")
	status = http.get("status")
	request_headers = http.get("request_headers")
	response_headers = http.get("response_headers")
	http_response_body = o.get("http_response_body")
	http_request_body = o.get("http_request_body")
	uri = http.get("url")
	if "?" in uri:
		uri = uri.split("?")[0]
	else:
		uri = uri
	urlc = o.get("url_c")
	url = o.get("url")
	
	
	app = o.get("app")
	parameter = o.get("parameter","")
	key = f"Method:{http_method}, App:{app},DestIP:{dest_ip}, DestPort:{dest_port}, Status:{status}"
	
	req_headers = header_handle(http)
	if key in stream["rules"]:
		rules_data = stream["rules"][key]
		if uri in rules_data["urls"]:
		 # 通过这两层判断 才能进行下面操作
			imp_rules = rules_data["rule"]
			 # 数据存储
			data_storage = {}
			for ch_name, t_rules in imp_rules.items():
				# 修改将rules规则改为 列表
				for rules in t_rules:
					for http_pos, pos_rules in rules.items():
						if http_pos == "request_headers":
							data_storage = headers_exract(ch_name, pos_rules, req_headers, data_storage)
						if http_pos == "parameter":
							pos="参数"
							data_storage = par_body(ch_name, pos_rules, parameter, data_storage,pos)
						if http_pos == "request_body":
							pos="请求体"
							data_storage = par_body(ch_name, pos_rules, http_request_body, data_storage,pos)
			if url=="http://100.78.1.125/ebus/00000000000_nw_dzfpfwpt/SJCS_FPJF_ZJ_MRJK":
				printf("da",data_storage)
				#printf("oo",o)
			if data_storage:
				printf("data",data_storage)
				
				
				stream["count"] +=1
				a = {"time":o.get("timestamp"),"id":xlink_uuid(0),"app":app,"url":urlc,"dest_ip":dest_ip,"dest_port":str(dest_port),"parameter":parameter,"request_body":http_request_body,"response_body":http_response_body,"request_headers":req_headers,"response_headers":response_headers,'account_info':data_storage}
				
				to_unix_udp(a,"/tmp/storages")
				
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	
#end 

#系统定时函数，st为时间戳 
def send120(st):
	
	rules = load_pkl("/data/xlink/intell_rules.pkl")
	stream["rules"] = rules
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def par_body(ch_name, pos_rules, data_source, data_storage,pos):
	# 获取偏移量
	start_offset = pos_rules["start"].get("offset_pos",0)
	end_offset = pos_rules["end"].get("offset_pos",0)
	# pos_rules 为 {start:{},end:{}}
	start_str = pos_rules["start"]["str"]
	end_str = pos_rules["end"]["str"]
	# 根据两者信息 从数据中提取出重要信息
	start_pos = data_source.find(start_str) + len(start_str)
	end_pos = data_source.find(end_str, start_pos)
	if start_pos != -1 and end_pos != -1:
		current_start = start_pos + start_offset
		current_end = end_pos - end_offset
		res = data_source[current_start:current_end].strip()
		
		if res !="":
			data_storage.setdefault(pos,{}).setdefault(ch_name, []).append(res)
	return data_storage
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def headers_exract(ch_name, pos_rules, request_headers, data_storage):
	for key, rule in pos_rules.items():
		for item in request_headers:
			if item["name"].lower() == key.lower():
				# 获取偏移量
				start_offset = rule["start"].get("offset_pos",0)
				end_offset = rule["end"].get("offset_pos",0)
				# 如果相等，就开始让规则从该数据中取出重要信息
				start_str = rule["start"]["str"]
				end_str = rule["end"]["str"]
				# 根据两者信息 从数据中提取出重要信息
				start_pos = item["value"].find(start_str) + len(start_str)
				end_pos = item["value"].find(end_str, start_pos)
				# 如果找到了起始字符串和结束字符串
				if start_pos != -1 and end_pos != -1:
					current_start = start_pos + start_offset
					current_end = end_pos - end_offset
					res = item["value"][current_start:current_end].strip()
					
					if res !="":
						data_storage.setdefault("请求头",{}).setdefault(ch_name, []).append(res)
						continue
	return data_storage
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def header_handle(http):
	req_headers=[]
	if "request_headers" in http:
		for item in http["request_headers"]:
			ii={}
			for k,v in item.items():
				ii[k]=unquote(v)
			req_headers.append(ii)
	return req_headers
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def unquote(value):
	#if "%" in value:
	if value.find("%") != -1:
		return unquote2(value)
	return value
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
from mondic import *
from urllib.parse import unquote as unquote2
#end 

#udf

#end 
