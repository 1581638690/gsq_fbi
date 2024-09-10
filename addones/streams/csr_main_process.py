#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: csr_main_process.xlk
#datetime: 2024-08-30T16:10:58.467083
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

#LastModifyDate:　2024-07-31T16:07:13    Author:   rzc

#LastModifyDate:　2024-07-31T16:00:18    Author:   rzc

#LastModifyDate:　2024-07-31T15:55:31    Author:   rzc

#LastModifyDate:　2024-05-13T16:33:04    Author:   rzc

#LastModifyDate:　2024-05-08T14:35:52    Author:   rzc

#LastModifyDate:　2024-04-25T11:37:12    Author:   pjb

#LastModifyDate:　2024-04-24T11:15:07    Author:   pjb

#LastModifyDate:　2024-04-07T17:10:07    Author:   pjb

#LastModifyDate:　2024-04-07T12:16:01    Author:   pjb

#LastModifyDate:　2024-04-07T11:48:35    Author:   pjb

#LastModifyDate:　2024-04-07T11:32:45    Author:   pjb

#xlink脚本

#file: main_process.xlk

#name: 分发主流程

#描述： 分发数据到Redis

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with main_process

#停止

#a = @udf FBI.x_finder3_stop with main_process

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:main_process,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::main_process

#断点调试

#debug_on(1)

# 初始化

# Delete 注释 by superFBI on 2024-03-26 18:58:14

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "[CSR]主分发流程"
	stream["meta_desc"] = "处理/tmp/csr_main数据，分发到unix_udp"
	#stream["source"]= {"link":stream["link"],"topic":stream["topic"],"group":stream["group"],"start-0":stream["reset"]}
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"] = {"files":"/data/znsm/eve-*.{}.json"}
	stream["max_xlink"]=9
	#stream["source"]= {"unix_udp":"/tmp/znsm_main"}
	stream["source"]= {"unix_udp":"/tmp/csr_main"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_1s"]={"times":1,"fun":"print1"}
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["protocol"]=load_ssdb_kv("protocol_data")["protocol"]["event"]
	stream["dns_count"]=0
	stream["http_count"]=0
	#redis的链接
	stream["redis"]={"host":stream["redis_link"],"port":"16379","batch":1000}
	#stream["redis"]={"host":"192.168.124.221","port":"16379","batch":1000}
	stream["se_http"] = 0
	stream["urls"]=[]
#end 

#事件处理函数

#Delete 注释 by superFBI on 2024-03-26 18:57:34

#事件处理函数
def Events(o,topic=''):
	if o["event_type"]=="http" and stream["protocol"]["http_key"]=="true":
		#url = base64_decode(o.get("http").get("url",""))
		stream["http_count"]+=1
		url = o.get("http").get("url")
		stream["urls"].append(url)
		printf("urls",stream["urls"])
		if url:
			#to_redis_n("yuan_http",o,8)
			#to_unix_udp(o,"/tmp/yuans_http")
			stream["se_http"]+=1
			
			printf(o["event_type"],o)
			
	elif o["event_type"]=="fileinfo" and stream["protocol"]["fileinfo_key"]=="true":
		if o.get("fileinfo"):
			files = o.get('fileinfo').get("filename", "")
			try:
				decoded = files.encode('latin1').decode('gb2312')
			except:
				decoded = files
			o["fileinfo"]["filename"] = urllib.parse.unquote(decoded)
			if o.get("fileinfo").get("file_path")!="files/":
				#to_redis("fileinfo_proto",o)
				to_unix_udp_n(o,"/tmp/fileinfo_proto",5)
				#to_redis("model_file",o)
				to_unix_udp(o,"/tmp/model_file")
				#to_redis("fileinfo1_proto",o)
				#to_redis("proto",o)
				to_unix_udp(o,"/tmp/proto")
	elif o["event_type"]=="ftp" and stream["protocol"]["ftp_key"]=="true":
		#to_redis("proto",o)
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"]=="pop3" and stream["protocol"]["pop3_key"]=="true":
		#to_redis("proto",o)
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"]=="tftp" and stream["protocol"]["tftp_key"]=="true":
		#to_redis("proto",o)
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"]=="dns" and stream["protocol"]["dns_key"]=="true":
		stream["dns_count"]+=1
		if stream["dns_count"] %5 !=0: return -1
		#to_redis("dns_proto",o)
		to_unix_udp(o,"/tmp/dns_proto")
	elif o["event_type"]=="smtp" and stream["protocol"]["smtp_key"]=="true":
		#to_redis("proto",o)
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"]=="imap" and stream["protocol"]["imap_key"]=="true":
		#to_redis("proto",o)
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"]=="smb" and stream["protocol"]["smb_key"]=="true":
		#to_redis("proto",o)
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"] == "dbms":
		to_unix_udp_n(o,"/tmp/yuan_dbms",2)
	elif o["event_type"]=="flow":
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"] == "ssh":
		to_unix_udp(o,"/tmp/proto")
		printf(o["event_type"],o)
	elif o["event_type"] == "telnet":
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"] == "tls":
		to_unix_udp(o,"/tmp/proto")
	elif o["event_type"] == "rdp":
		to_unix_udp(o,"/tmp/proto")
	else:
		to_unix_udp(o,"/tmp/proto")
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("接收到http事件","%s==sum==%d"%(st,stream["http_count"]))
	printf("发出到http事件","%s==sum==%d"%(st,stream["se_http"]))
	#c = load_ssdb_kv("alarm")
	stream["protocol"]=load_ssdb_kv("protocol_data")["protocol"]["event"]
	#stream["request_status"] = c["setting"]["request_status_alarm"]["request_status"]
	stream["dns_count"]=0
	
#end 

#系统定时函数，st为时间戳 
def print1(st):
	#c = load_ssdb_kv("alarm")
	stream["protocol"]=load_ssdb_kv("protocol_data")["protocol"]["event"]
	#stream["request_status"] = c["setting"]["request_status_alarm"]["request_status"]
	
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
import uuid
import urllib
from urllib import parse
#end 

#udf

#end 
