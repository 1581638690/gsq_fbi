#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: modsecurity.xlk
#datetime: 2024-08-30T16:10:58.470361
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

#LastModifyDate:　2024-01-09T10:26:59    Author:   rzc

#LastModifyDate:　2024-01-06T20:59:46    Author:   superFBI

#LastModifyDate:　2024-01-06T15:56:35    Author:   superFBI

#LastModifyDate:　2024-01-06T15:40:11    Author:   superFBI

#LastModifyDate:　2024-01-06T14:05:04    Author:   superFBI

#LastModifyDate:　2023-12-28T09:33:55.490381    Author:   superFBI

#LastModifyDate:　2023-12-27T15:20:08.366904    Author:   superFBI

#LastModifyDate:　2023-12-27T10:17:34.589303    Author:   superFBI

#LastModifyDate:　2023-08-11T17:12:03.389651    Author:   zwl

#LastModifyDate:　2023-08-08T18:31:40.100268    Author:   pjb

#LastModifyDate:　2023-05-26T16:57:30.642692    Author:   pjb

#xlink脚本

#file: modsecurity.xlk

#name: modsecurity安全事件

#描述： modsecurity安全事件

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with modsecurity

#停止

#a = @udf FBI.x_finder3_stop with modsecurity

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:modsecurity,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::modsecurity

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "modsecurity安全事件"
	stream["meta_desc"] = "modsecurity安全事件"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/mod"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["libCalc"] = modsecurity_init()
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	stream["modsecurity_store"] = load_ssdb_kv("protocol_data")["function"]["event"]["modsecurity_store"]
	stream["modsecurity_key"] = load_ssdb_kv("protocol_data")["function"]["event"]["modsecurity_key"]
	with open("/opt/openfbi/pylibs/modsecurity_id.json",encoding='utf-8')as f:
		stream["modsecurity_id"] = ujson.load(f)
	with open("/opt/openfbi/pylibs/modsecurity_all.json",encoding='utf-8')as f:
		stream["modsecurity_all"] = ujson.load(f)
	with open("/opt/openfbi/pylibs/modsecurity_class.json",encoding='utf-8')as f:
		stream["modsecurity_class"] = ujson.load(f)
	pool["modsecurity"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	if stream["modsecurity_key"]=="true":
		#printf("httpjson",httpjson)
		sjt=time.time()
		mod = stream["libCalc"].modsecurity(o)
		printf("安全检查", '{:.3f}'.format((time.time() - sjt) * 1000))
		st = ""
		level = ""
		cla = ""
		of = False
		for id in mod:
			id = str(id)
			if id in stream["modsecurity_id"]:
				of = True
				st += stream["modsecurity_id"].get(id)
				st +='，'
			else:
				if id in stream["modsecurity_all"]:
					of = True
					if stream["modsecurity_all"].get(id).get("msg"):
						st += stream["modsecurity_all"].get(id).get("msg")
						st +='，'
		if str(mod[0]) in stream["modsecurity_all"]:
			if stream["modsecurity_all"].get(str(mod[0])).get("severity"):
				level += stream["modsecurity_all"].get(str(mod[0])).get("severity")
		if str(mod[0])[:3] in stream["modsecurity_class"]:
			cla = stream["modsecurity_class"].get(str(mod[0])[:3])
		else:
			if str(mod[0])[:4] in stream["modsecurity_class"]:
				cla = stream["modsecurity_class"].get(str(mod[0])[:4])
		if of:
			if st:
				st = st[0:-1]
			if stream["modsecurity_store"] == "true":
				httpjson = ujson.dumps(o, ensure_ascii=False)
			else:
				httpjson = ""
			a = {
				"timestamp": iso_to_datetime(o.get("timestamp")),
				"id": xlink_uuid(0),
				"srcip": o.get("src_ip"),
				"srcport": o.get("src_port"),
				"dstip": o.get("dest_ip"),
				"dstport": o.get("dest_port"),
				"app": o.get("app"),
				"url": o.get("url_c"),
				"content_length": o.get("http").get("length", 0),
				"url_a": o.get("url"),
				"method": o.get("http").get("http_method"),
				"modsecurity_id": str(mod),
				"modsecurity_str": st,
				"flow_id": o.get("flow_id"),
				"level": level,
				"class": cla,
				"httpjson": httpjson
			}
			to_pool("modsecurity",a)
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	stream["modsecurity_store"] = load_ssdb_kv("protocol_data")["function"]["event"]["modsecurity_store"]
	stream["modsecurity_key"] = load_ssdb_kv("protocol_data")["function"]["event"]["modsecurity_key"]
	store_ckh(pool["modsecurity"],"api_modsecurity")
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
from modsecurity import *
#end 

#udf

#end 
