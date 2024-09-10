#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: csr_1.xlk
#datetime: 2024-08-30T16:10:58.403627
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

#LastModifyDate:　2024-08-15T11:42:21    Author:   rzc

#LastModifyDate:　2024-08-09T15:40:13    Author:   rzc

#LastModifyDate:　2024-08-08T16:50:38    Author:   rzc

#LastModifyDate:　2024-08-08T16:37:24    Author:   rzc

#LastModifyDate:　2024-08-08T10:27:25    Author:   rzc

#LastModifyDate:　2024-08-07T16:25:35    Author:   rzc

#LastModifyDate:　2024-08-07T14:36:15    Author:   rzc

#LastModifyDate:　2024-08-07T11:29:18    Author:   rzc

#LastModifyDate:　2024-08-07T11:28:11    Author:   rzc

#LastModifyDate:　2024-08-07T11:17:53    Author:   rzc

#LastModifyDate:　2024-08-06T15:52:09    Author:   rzc

#xlink脚本

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "[CSR]收集流程，根据页面配置"
	stream["meta_desc"] = "处理redis数据到/tmp/csr_main"
	stream["redis_l"] = load_ssdb_kv("agent")["redis"]
	try:
		stream["header"] = load_ssdb_kv("agent")["header"]
	except:
		stream["header"] = []
	#取第一个topic
	try:
		stream["topic1"] = load_ssdb_kv("agent")["header"][0]["topic"]
	except:
		stream["topic1"] = ""
	#字典 key-topic:value-destip
	stream["cfg"] = {}
	for flag in stream["header"]:
		stream["cfg"][flag["topic"]] = flag["destip"]
	stream["topics"] = []
	stream["pubshm"] = {"shm_name":"events", "size": 2048*2048}
	for tp in stream["header"]:
		topic = tp.get("topic")
		stream["topics"].append(topic)
	#stream["pubshm"] = {"shm_name":"events","size":}
	#stream["topics"].pop(0)
	stream["source"]= {"link":stream["redis_l"],"topic":stream["topic1"],"redis":"list_json","topics":stream["topics"]}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	#stream["st"]["st_20s"]={"times":20,"fun":"print20"}
	#Delete 注释 by rzc on 2024-08-08 16:29:14
	#stream["stw"]["stw_cpu"]={"times":10,"fun":"stw_cpu"}
	#	stream["stw"]["stw_mem"]={"times":10,"fun":"stw_mem"}
	#	stream["stw"]["csr_sum"]={"times":10,"fun":"csr_sum"}
	#	stream["stw"]["csr_los"]={"times":10,"fun":"csr_los"}
	#stream["st"]["st_60s"]={"times":20,"fun":"print60"}
	stream["count_scrip"] = {"csr_type":"csr"}
	stream["csr_info"] = {}
	stream["count_scrip"] = {}
	stream["urls"] = []
	stream["http_c"]=0
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	k = iso_to_timestamp(o["timestamp"])
	#目的ip
	dest_ip = stream["cfg"][topic]
	# 计算事件数
	if dest_ip in stream["count_scrip"]:
		stream["count_scrip"][dest_ip] += 1
	else:
		stream["count_scrip"][dest_ip] = 1
	if o.get("event_type") == "stats" and o.get("basic"):
		# 探针状态信息 cpu、内存使用率
		#总包数，丢失数，丢包率
		if o.get("stats") and o.get("stats").get("capture"):
			stream["csr_info"][dest_ip] = {}
			stream["csr_info"][dest_ip]["IP"] = dest_ip
			stream["csr_info"][dest_ip]["CPU使用率"] = float(o.get("basic").get("os_cpu",0))
			stream["csr_info"][dest_ip]["内存使用率"] = float(o.get("basic").get("os_mem",0))
			stream["csr_info"][dest_ip]["总包数"] = o.get("stats").get("capture").get("kernel_packets")
			stream["csr_info"][dest_ip]["丢包数"] = o.get("stats").get("capture").get("kernel_drops")
			stream["csr_info"][dest_ip]["丢包率"] = str(round(o.get("stats").get("capture").get("kernel_drops")/o.get("stats").get("capture").get("kernel_packets"),4) * 100) + '%'
			stream["csr_info"][dest_ip]["事件总数"] = stream["count_scrip"][dest_ip] if stream["count_scrip"].get(dest_ip) else 0
	#修改dest_ip
	if o.get("dest_ip") == '127.0.0.1':
		o["dest_ip"] = stream["cfg"][topic]
	if o.get("http"):
		url = o.get("http").get("url")
		#stream["urls"]["url"] =[]
		if o.get("http").get("hostname") == "10.71.80.194" and o.get("http").get("http_port") == 11022:
			stream["urls"].append(url)
		
			printf("urls",stream["urls"])
			#stream["http_c"] += 1
		if o.get("http").get("hostname") == "localhost" or o.get("http").get("hostname") == '127.0.0.1':
			o.get("http")["hostname"] = stream["cfg"][topic]
		
		
		if url:
			#to_redis_n("yuan_http",o,8)
			to_unix_udp(o,"/tmp/yuans_http")
	to_unix_udp_n(o,"/tmp/csr_main",9)
#end 

#系统定时函数，st为时间戳 
def print10(st):
	push_dict_to_df(stream["csr_info"],"csr_info")
	save()
#end 

#系统定时函数

#自定义批处理函数，使用FBI语句块 
def save(k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'csr_info', 'Action': '@udf', '@udf': 'csr_info', 'by': 'udf0.clone_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[csr_1.xlk]执行第[108]原语 csr_info = @udf csr_info ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'csr_info', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'csr_info:10s'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[csr_1.xlk]执行第[109]原语 store csr_info to ssdb by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[csr_1.xlk]执行第[110]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
#end 

#udf

#end 
