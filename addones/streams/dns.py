#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: dns.xlk
#datetime: 2024-08-30T16:10:58.455732
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

#LastModifyDate:　2024-01-09T10:27:18    Author:   rzc

#LastModifyDate:　2024-01-06T16:35:19    Author:   superFBI

#LastModifyDate:　2024-01-06T15:41:44    Author:   superFBI

#LastModifyDate:　2024-01-06T14:01:35    Author:   superFBI

#LastModifyDate:　2024-01-05T11:24:38.081331    Author:   superFBI

#LastModifyDate:　2023-12-27T14:07:47.008807    Author:   superFBI

#LastModifyDate:　2023-09-27T17:45:18.855540    Author:   superFBI

#LastModifyDate:　2023-08-08T18:34:07.234278    Author:   pjb

#LastModifyDate:　2023-07-27T16:23:29.025567    Author:   superFBI

#LastModifyDate:　2023-07-21T09:56:24.594496    Author:   qh

#LastModifyDate:　2023-07-20T10:27:18.463257    Author:   qh

#xlink脚本

#file: dns.xlk

#name: 协议处理

#描述： 从redis中取出dns数据

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with dns

#停止

#a = @udf FBI.x_finder3_stop with dns

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:dns,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::dns

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "协议处理"
	stream["meta_desc"] = "从redis中取出dns数据"
	#a = load_ssdb_kv("setting")
	#stream["link"] = a["kfk"]["origin"]["link"]
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]={"link":stream["redis_link"]+":16379","topic":"dns_proto","redis":"list"}
	stream["source"]={"unix_udp":"/tmp/dns_proto"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["sends"] = load_ssdb_kv("qh_send")["sends"].split(',')
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	#chk的链接
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	pool["dns"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	stream["count-10"] +=1
	if stream["count-10"] %2 !=0: return -1 #2分之一采样
	a = {
		"id": xlink_uuid(0),
		"flow_id": str(o.get("flow_id", "")),
		"timestamp": iso_to_datetime(o.get("timestamp")),
		"srcip": o.get('src_ip'),
		"srcport": o.get('src_port'),
		"dstip": o.get('dest_ip'),
		"dstport": o.get('dest_port'),
		"ID": str(o.get('dns').get("id", "")),
		"rrname": o.get('dns').get("rrname", ""),
		"type": o.get('dns').get("type", ""),
		"version": str(o.get('dns').get("version", "")),
		"groupedA": str(o.get('dns').get("grouped", {}).get("A", "")).replace("[", "").replace("]", "").replace("'", ""),
		"groupedCNAME": str(o.get('dns').get("grouped", {}).get("CNAME", "")),
		"qr": str(o.get('dns').get("qr", "")),
		"ra": str(o.get('dns').get("ra", "")),
		"rd": str(o.get('dns').get("rd", "")),
		"rrtype": o.get('dns').get("rrtype", ""),
		"flags": o.get('dns').get("flags", ""),
		"rcode": str(o.get('dns').get("rcode", ""))
	}
	to_pool("dns",a)
	if "api_dns" in stream["sends"]:
		s = deepcopy(a)
		s["event_type"] = "dns"
		#to_kfk2("api_send",s)
		#to_redis("api_send",s)
		s["timestamp"] = str(s["timestamp"])
		to_json_file("/data/syslog_file/eve",s)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
	stream["count-10"] = 0
	ret = len(pool["dns"])
	store_ckh(pool["dns"],"api_dns")
	return ret
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
#end 

#udf

#end 
