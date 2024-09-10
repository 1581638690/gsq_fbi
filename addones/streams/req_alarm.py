#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: req_alarm.xlk
#datetime: 2024-08-30T16:10:57.588464
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

#LastModifyDate:　2024-01-09T10:22:49    Author:   rzc

#LastModifyDate:　2024-01-08T09:47:10    Author:   superFBI

#LastModifyDate:　2024-01-06T15:39:10    Author:   superFBI

#LastModifyDate:　2024-01-06T14:05:53    Author:   superFBI

#LastModifyDate:　2023-12-29T10:06:59.058711    Author:   superFBI

#LastModifyDate:　2023-12-28T09:35:01.750064    Author:   superFBI

#LastModifyDate:　2023-12-27T13:55:54.173940    Author:   superFBI

#LastModifyDate:　2023-08-08T18:34:57.394570    Author:   pjb

#LastModifyDate:　2023-08-02T16:24:00.824722    Author:   pjb

#LastModifyDate:　2023-08-02T16:20:38.084917    Author:   pjb

#LastModifyDate:　2023-07-27T16:27:58.917113    Author:   superFBI

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "异地访问、耗时告警告警、境外访问风险告警"
	stream["meta_desc"] = "从api_visit1主题中消费数据，处理异地访问、耗时告警告、境外访问"
	#b = load_ssdb_kv("setting")
	#stream["link"] = b["kfk"]["visit"]["link"]
	#stream["topic"] = b["kfk"]["visit"]["topic"]
	#stream["group"] = b["kfk"]["visit"]["group"] + "reqalarm"
	#stream["reset"] = b["kfk"]["visit"]["reset"]
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["redis"]={"host":stream["redis_link"],"port":"16379"}
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["redis"],"topic":stream["topic1"],"redis":"list","topics":stream["topics"]}
	#stream["source"] = {"link":"10.99.20.105:9092","topic":"zichan","group":"hs","start-0":True}
	#stream["source"] = {"link":stream["link"],"topic":stream["topic"],"group":stream["group"],"start-0":stream["reset"]}
	#stream["source"]= {"link":"127.0.0.1:16379","topic":"api_visit","redis":"pubsub"}
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/req_alm"}
	stream["source"] = {"shm_name":"httpub","count":8}
	#stream["source"]= {"link":"127.0.0.1:16379","topic":"api_visit","redis":"list"}
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	stream["content"] = handle_content_type(load_ssdb_kv("setting")["setting"]["content_type"]["type"])
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	stream["sends"] = a
	if "api_req" in a:
		stream["send1"] = 1
	else:
		stream["send1"] = 0
	if "api_place" in a:
		stream["send2"] = 1
	else:
		stream["send2"] = 0
	#add by by gjw 增加文件的kafka队列和IP地域库
	#stream["kfk"]={"link":stream["link"],"topic":"api_send","key":""}
	stream["ipdb"] = IPIPDatabase( '/opt/openfbi/workspace/ipdb.datx')
	
	#stream["kfk"]={"link":stream["link"],"topic":"api_send","key":""}
	stream["st"]["ip"]={"times":10,"fun":"store_ip"}
	#stream["st"]["port"]={"times":10,"fun":"store_port"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	stream["st"]["abroad"]={"times":10,"fun":"abroad_store"}
	
	stream["sight"] = []
	stream["sign"] = []
	stream["severity"] = []
	stream["t_cons_app"] = ""
	c = load_ssdb_kv("alarm")
	if c.get("setting").get("delay_time"):
		#延迟定义
		stream["sight"] = c["setting"]["delay_time"]["sight"]
		stream["sign"] = c["setting"]["delay_time"]["sign"]
		stream["severity"] = c["setting"]["delay_time"]["severity"]
		app = c.get("setting").get("delay_time").get("app")
		if app:
			stream["t_cons_app"] = app.split('/')
		else:
			stream["t_cons_app"] = ""
	
	
	stream["ip_white"] = []
	stream["vi_status"] = {}
	stream["app_temp"] = []
	stream["ip_app"] = {}
	stream['vi_app'] = []
	# 异地访问告警准备数据
	if c.get("setting").get("remote_access_alarm"):
		r_alarm_ip = c.get("setting").get("remote_access_alarm").get("remote_alarm_ip")
		if r_alarm_ip:
			# 将所有应用去重后，创建对应的字典
			for ip in r_alarm_ip:
				for i in ip.get('app').split('/'):
					stream["app_temp"].append(i)
			stream["app_temp"] = list(set(stream["app_temp"]))
			for app in stream["app_temp"]:
				stream["ip_app"][app] = []
			# 将对应的ip插入相应的元组中
			for ip in r_alarm_ip:
				for i in ip.get('app').split('/'):
					stream["ip_app"][i].append(ip.get('ip'))
			# 去重stream["ip_app"]中的值
			for key in stream["ip_app"]:
				stream["ip_app"][key] = list(set(stream["ip_app"][key]))
	pool["ip"] = []
	pool["port"] = []
	pool["abroad"] = []
	stream["api_abroad"] = load_ssdb_kv("protocol_data")["function"]["event"]["api_abroad"]
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	if stream["api_abroad"] == "true":
		ip_is,res = ip_lookup(o.get('src_ip'))
		if ip_is:
			printf("res",res)
			b = {}
			b["id"] = xlink_uuid(0)
			b["timestamp"] = iso_to_datetime(o.get("timestamp"))
			b["srcip"] = o.get('src_ip')
			b["srcport"] = int(o.get('src_port'))
			b["dstip"] = o.get('dest_ip')
			b["dstport"] = o.get('dest_port')
			b["address"] = res
			#event_type = o.get("event_type")
			#b["type"] = event_type
			b["data"] = o.get("id")
			to_pool("abroad",b)
			if "api_abroad" in stream["sends"]:
				s = deepcopy(b)
				s["event_type"] = "external"
				#to_kfk(s)
				s["timestamp"] = str(s["timestamp"])
				to_json_file("/data/syslog_file/eve",s)
	# 异地访问告警
	app = o.get('app')
	if stream["ip_app"]:
		in_white = 0
		in_white1 = 0
		for ip_app in stream["ip_app"]:
			# 过滤ipv6
			# if o.get("proto") == "IPv6-ICMP":
			# 	break
			# 比对应用是否在监控列表中
			if app == ip_app:
				in_white = 1
				# 比对是否在白名单中
				for ip in stream["ip_app"][ip_app]:
					ip_len = len(ip)
					if o.get("src_ip")[0:ip_len] == ip:
						in_white1 = 1
						break
				if in_white1 == 1:
					break
		if in_white == 1 and in_white1 == 0 :
			temp = {}
			temp["timestamp"] = iso_to_datetime(o.get("timestamp"))
			temp["src_ip"] = str(o.get("src_ip"))
			temp["src_port"] = int(o.get("src_port"))
			temp["url"] = o.get("url_c")
			temp["dest_ip"] = str(o.get("dest_ip"))
			temp["dest_port"] = o.get("dest_port")
			to_pool("ip",temp)
			if stream["send2"]:
				s = deepcopy(temp)
				s["event_type"] = "outside"
				#to_kfk(s)
				s["timestamp"] = str(s["timestamp"])
				to_json_file("/data/syslog_file/eve",s)
	det = time.time()
	if o.get("app") in stream["t_cons_app"]:
		url_c = o.get("url_c")
		#http = ujson.loads(o.get("httpjson"))
		delay_am = delay_alarm(o, url_c, stream["sight"], stream["sign"], stream["severity"])
		if delay_am:
			delay_am["time"]= o.get("timestamp")
			delay_am["id"] = xlink_uuid(0)
			delay_am["srcip"] = o.get('src_ip')
			#to_redis("delay_time", delay_am)
			to_unix_udp(delay_am,"/tmp/delay_time")
#end 

#系统定时函数，st为时间戳 
def store_ip(st):
	store_ckh(pool["ip"],"r_req_alm")
#end 

#Delete 注释 by pjb on 2023-02-07 15:59:20

#store_port => {

#	store_ckh(pool["port"],"stat_req_alm")

#}

#系统定时函数，st为时间戳 
def abroad_store(st):
	store_ckh(pool["abroad"],"api_abroad")
#end 

#系统定时函数，st为时间戳 
def send60(st):
	#延迟定义
	c = load_ssdb_kv("alarm")
	stream["t_cons_app"] = ""
	if c.get("setting").get("delay_time"):
		#延迟定义
		stream["sight"] = c["setting"]["delay_time"]["sight"]
		stream["sign"] = c["setting"]["delay_time"]["sign"]
		stream["severity"] = c["setting"]["delay_time"]["severity"]
		app = c.get("setting").get("delay_time").get("app")
		if app:
			stream["t_cons_app"] = app.split('/')
		else:
			stream["t_cons_app"] = ""
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	stream["sends"] = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_req" in a:
		stream["send1"] = 1
	else:
		stream["send1"] = 0
	if "api_place" in a:
		stream["send2"] = 1
	else:
		stream["send2"] = 0
	# 异地访问告警准备数据
	r_alarm_ip = load_ssdb_kv("alarm")["setting"]["remote_access_alarm"]["remote_alarm_ip"]
	if r_alarm_ip:
		# 将所有应用去重后，创建对应的字典
		for ip in r_alarm_ip:
			for i in ip.get('app').split('/'):
				stream["app_temp"].append(i)
		stream["app_temp"] = list(set(stream["app_temp"]))
		for app in stream["app_temp"]:
			stream["ip_app"][app] = []
		# 将对应的ip插入相应的元组中
		for ip in r_alarm_ip:
			for i in ip.get('app').split('/'):
				stream["ip_app"][i].append(ip.get('ip'))
		# 去重stream["ip_app"]中的值
		for key in stream["ip_app"]:
			stream["ip_app"][key] = list(set(stream["ip_app"][key]))
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ip_lookup(ip):
	try:
		ip_is = False
		result = stream["ipdb"].lookup(ip).split('	')[0]
		if result not in ["中国","局域网","本地链路","共享地址","本机地址","保留地址"]:
			ip_is = True
	except Exception as e:
		ip_is = False
		result = ''
	return ip_is,result
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#需要额外引入的包

#需要引入的包 
import base64
from stream_official import *
from copy import deepcopy
import json
from pyipip import IPIPDatabase
#end 

#udf

#end 
