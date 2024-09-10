#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_mege.xlk
#datetime: 2024-08-30T16:10:58.158318
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

#LastModifyDate:　2024-08-15T10:44:55    Author:   rzc

#LastModifyDate:　2024-08-09T14:03:50    Author:   rzc

#LastModifyDate:　2024-08-08T17:51:45    Author:   rzc

#LastModifyDate:　2024-08-06T14:18:10    Author:   rzc

#LastModifyDate:　2024-07-31T16:15:00    Author:   rzc

#LastModifyDate:　2024-07-31T15:46:28    Author:   rzc

#LastModifyDate:　2024-07-31T15:17:21    Author:   rzc

#LastModifyDate:　2024-07-31T15:13:58    Author:   rzc

#LastModifyDate:　2024-07-31T15:13:48    Author:   rzc

#LastModifyDate:　2024-07-31T15:05:52    Author:   rzc

#LastModifyDate:　2024-07-26T15:57:26    Author:   rzc

#xlink脚本

#file: api_mege.xlk

#name: 接口合并数据

#描述： 对接口进行合并

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "审计数据处理，敏感数据处理"
	stream["meta_desc"] = "处理yuan_http分发的http_proto数据,处理审计数据处理、敏感数据处理"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"]= {"link":stream["redis_link"]+":6380","topic":"http_proto","redis":"list"}
	#stream["max_xlink"]=12
	stream["max_xlink"]=2
	stream["source"]= {"unix_udp":"/tmp/http-proto"}
	stream["redis"]={"host":stream["redis_link"],"port":"6382"}
	stream["redis2"]={"host":stream["redis_link"],"port":"6381"}
	
	stream["pubshm"] = {"shm_name":"httpub", "size": 256*1024*1024}
	
	stream["perf_funs"]=[to_unix_udp,to_unix_udp_n,pub_unix_udp]
	#stream["con_rules"] = load_model_data("gsqevent")
	stream["st"]["st_12m"]={"times":600,"fun":"print10m"}
	stream["st"]["st_10f"]={"times":30,"fun":"print5f"}
	stream["st"]["st_20s"]={"times":30,"fun":"print20"}
	
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_visit" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	if "api_model" in a:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
	
	#白名单 NLP识别
	white=load_ssdb_kv("writelist")
	name_switch=white.get("name_switch")
	#敏感数据正则配置
	try:
		sensitive1=load_ssdb_kv("sensitive")["data"]
		stream["sensitive"]=[]
		for data in sensitive1:
			if data["off"]==1:
				if data["rekey"]=="姓名" or data["rekey"]=="地址":
					if name_switch!="0":
						data["name"]=re.compile(data["name"])
						stream["sensitive"].append(data)
				else:
					data["name"]=re.compile(data["name"])
					stream["sensitive"].append(data)
	except:
		stream["sensitive"]=load_ssdb_kv("sensitive")["data"]
	#for data in stream["sensitive"]:
	#	data["name"]=re.compile(data["name"])
		
	stream["sensitive_alarm"] = load_ssdb_kv("dd:reqs_label")["data"]
	
	stream["app_merge"]= load_ssdb_hall("app_merge")
	event=load_ssdb_kv("protocol_data")["function"]["event"]
	#敏感识别总开关
	stream["sen_identify"]=event["sen_identify"]
	stream["app_sj"] = event["app_sj"]
	#stream["sw_or_ordinary"]=event["sw_or_ordinary"]
	# 空字典 用来保存含有监控标签的接口（合并） 不保存ssdb
	stream["monitor"] = {}
	#字典 app与应用名映射
	stream["map_apps"] = {}
	monitor_local=load_pkl("/data/xlink/api_mon.pkl")
	stream["monitor"]=monitor_local
	app_local=load_pkl("/data/xlink/app_mon.pkl")
	stream["map_apps"]=app_local
	#敏感信息白名单
	stream["whitelist"]={}
	with open("/opt/openfbi/pylibs/wrong_name.csv","r",encoding="utf-8")as fp:
		name_con=fp.readlines()
	name_list=[i.strip() for i in name_con if len(i.strip())>1]
	wrong_name=name_list
	write_list=white["write_list"]
	if "name_list" in write_list:
		name_list=write_list.get("name_list").get("name")
		for name in name_list:
			wrong_name.append(name["data"])
	stream["whitelist"]["姓名"]=wrong_name
	wrong_moblie=[]
	if "moblie_list" in write_list:
		moblie_list=write_list.get("moblie_list").get("moblie")
		for moblie in moblie_list:
			wrong_moblie.append(moblie["data"])
	stream["whitelist"]["手机号"]=wrong_moblie
	#铁路
	stream["fid_mch_off"]=event["field_off"]
	field_data=load_ssdb_kv("field_sen")["data"]
	stream["sen_dic"]=get_data(field_data)
	
	name_list = load_ssdb_kv("writelist")
	not_name = []
	if "name_list" in name_list["write_list"]:
		for item in name_list["write_list"]["name_list"]["name"]:
			not_name.append(item["data"])
		stream["name_lsit"] = not_name
	else:
		stream["name_list"]=[]
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
	stream["sen_url"]={}
	sen_path="/data/xlink/sen_dic.pkl"
	if not os.path.exists(sen_path):
		stream["sen_url"]={}
	else:
		stream["sne_url"]=load_pkl(sen_path)
	
	stream["mon_count"] = 0
	stream["obj_count"] = 0
	
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#printf(o["event_type"],o)
	#printf("sen_dic",stream["sen_dic"])
	suid = xlink_uuid(1)
	#printf("suid",suid)
	http = o["http"]
	qlength=http.get("qlength",0)
	length=http.get("content_length","0")
	cookie=http.get("cookie","")
	age=http.get("age")
	destport = o["dest_port"]
	srcport=o["src_port"]
	request_headers=http.get("request_headers","")
	response_headers=http.get("response_headers","")
	response_body=o["http_response_body"]
	request_body=o["http_request_body"]
	timestamp=o["timestamp"]
	d_timestamp = o["d_timestamp"]
	srcip = o['src_ip']
	flow_id = o['flow_id']
	http_method=http["http_method"]
	content_length = http.get('length', 0)
	dstip = o["dest_ip"]
	url = o["url"]
	url_c = o["url_c"]
	app = o["app"]
	app_dst=app
	account = o["account"]
	type = o["type"]
	parameter = o["parameter"]
	api_type = o["api_type"]
	data_type = o["data_type"]
	counts = o["counts"]
	realip, agent_ip = real_ip(request_headers,srcip)
	content_type=http.get("content_type")
	if srcip == '127.0.0.1':
		if realip:
			srcip = realip
			o['src_ip'] = realip
	if stream["app_merge"]:
		app_values=stream["app_merge"].values()
		for apps in app_values:
			if app in apps.get("app_sum").split(","):
				if apps.get("app"):
					app_dst=apps.get("app")
	
	if url_c in stream["monitor"] or app_dst in stream["map_apps"] or stream["app_sj"] == "true":
		
			#stream["urls"]["event"] = "识别前"
		if url_c in stream["monitor"]:
			risk_leve = stream["monitor"][url_c][0]  # "2"
			api_type = stream["monitor"][url_c][1]  # 4
			# 接口名
			name = stream["monitor"][url_c][2]  # ""
			data_type=stream["monitor"][url_c][3]
			try:
				app_name = stream["map_apps"][app_dst]
			except:
				app_name = ''
		else:
			risk_leve = '0'
			name = ""
			app_name = ''
		response = response_body
		re_data = request_body
		
		total_info ={}
		total_count={}
		info={}
		if data_type in ["XML","数据文件","JSON","动态脚本"] and stream["sen_identify"]=="true":
		#判断敏感接口
			if url_c not in stream["sen_url"]:
				response,re_data,total_info,total_count,info = monitor_data(response,re_data,stream["sensitive"],stream["whitelist"],stream["fid_mch_off"],stream["sen_dic"],url_c)
				
				#根据得出的结果来判断 url_c是否为敏感接口
				# 根据total_info的值选择分类键
				stream["sen_url"][url_c]={}
				category_key = "1" if total_info else "0"
				stream["sen_url"][url_c]["count"]=1
				stream["sen_url"][url_c]["yn_sen"]=category_key
			else:
				#url_c存在与字典中
				#获取是否存在敏感
				cay_key=stream["sen_url"][url_c]["yn_sen"]
				if cay_key =="1":
					response,re_data,total_info,total_count,info = monitor_data(response,re_data,stream["sensitive"],stream["whitelist"],stream["fid_mch_off"],stream["sen_dic"],url_c)
				else:
					stream["sen_url"][url_c]["count"]+=1
					url_count=stream["sen_url"][url_c]["count"]
					if url_count % 10==0:
						response,re_data,total_info,total_count,info = monitor_data(response,re_data,stream["sensitive"],stream["whitelist"],stream["fid_mch_off"],stream["sen_dic"],url_c)
		
		count = 0
		#判断响应体是否为JSON数据 且 是否存在敏感数据信息
		#if is_json_string(response) and "响应体" in info:
		if content_type == "application/json" and "响应体" in info:
			#存储原始信息
			s = re.findall(r"\[.+?\]", str(response))
			#count = 0
			pa = []
			if s:
				for i in range(len(s)):
					sa = re.findall(r'\{.+?\}', s[i])
					count = count + len(sa)
					pa = pa + sa
			dict1 = {}
			dict1["bsxx"] = []
			for i in range(len(pa)):
				try:
					dict1["bsxx"].append(ujson.loads(pa[i]))
				except:
					count = count - 1
			if count>0:
				key=dict1
				yw_count=count
			else:
				key=""
				yw_count=0
		else:
			key=""
			yw_count=0
		request_body_json = str_json(re_data)
		parameter_json = str_json(parameter)
		monitors = {"url":url,"urld":url_c,"time":timestamp,"auth_type":o.get("auth_type"),"length":length,"age":age,"qlength":qlength,"cookie":cookie,"flow_id":str(o.get("flow_id","")),"app":app_dst,"srcip":srcip,"account":account,"content_type":data_type,"risk_level":risk_leve,"api_type":api_type,"name":name,"parameter":parameter,"content_length":content_length,"app_name":app_name,"real_ip":realip,"http_method":http_method,"request_headers":request_headers,"response_headers":response_headers,"status":http.get('status',0),"response_body":response,"request_body":re_data,"info":info,"key":key,"yw_count":yw_count,"id":suid,"dstip":dstip,"dstport":destport,"srcport":o.get("src_port"),"user_info": o.get("user_info"),"request_body_json":request_body_json,"session_id":o.get("session_id"),"parameter_json":parameter_json}
		stream["mon_count"]+=1
		
		to_unix_udp(monitors,"/tmp/http-monitor")
		
		#to_unix_udp(monitors,"/tmp/duck_http")
		#to_unix_udp_n(monitors,"/tmp/yuan_dbms",8)
		#to_redis_n("http_monitor", monitors,4,"redis2")
		#if name!="":
		#to_unix_udp(monitors,"/tmp/operation_events")
		#to_unix_udp(monitors,"/tmp/operation_events_new")
		to_unix_udp(monitors,"/tmp/operation_events_oper")
		
		if count > 0:
			#to_redis("bs_monitor",monitors)
			to_unix_udp(monitors,"/tmp/bs_monitor")
		if total_info:
			c={
				"timestamp":d_timestamp,
				"flow_id":flow_id,
				"src_ip":srcip,
				"dest_ip":dstip,
				"dest_port":destport,
				"http_method":http_method,
				"uuid": suid,
				"url": url_c,
				"url_c": url,  # 未合并的
				"app": app_dst,
				"account": account,
				"parameter": parameter,
				"request_bodys": re_data,
				"response_bodys": response,
				"cookie": http.get("cookie", ""),
				"request_count": total_count.get("请求体",""),
				"response_count": total_count.get("响应体",""),
				"msg_total": total_info,
				"sen_type_count": total_count,
				"real_ip": realip,
				"srcport": srcport}
			#to_redis("sen_count",c,"redis2")
			to_unix_udp(c,"/tmp/sen_count")
	else:
	##########处理敏感数据监控(6381)############
		total_info={}
		XML = "XML"
		DATA_FILE = "数据文件"
		JSON = "JSON"
		DYNAMIC_SCRIPT = "动态脚本"
		if data_type in (XML, DATA_FILE, JSON, DYNAMIC_SCRIPT):
			if (stream["addr_switch"] == 0 and stream["name_switch"] == 0) or stream["ai_switch"] != "0":
				pass
			else:
				#to_redis("http_nlp",o,"redis2")
				to_unix_udp(o,"/tmp/http_nlp")
			if url_c not in stream["sen_url"]:
				total_info=sen_con_dete(response_body,request_body,url_c)
				stream["sen_url"][url_c]={}
				category_key = "1" if total_info else "0"
				stream["sen_url"][url_c]["count"]=1
				stream["sen_url"][url_c]["yn_sen"]=category_key
			else:
				#url_c存在与字典中
				#获取是否存在敏感
				cay_key=stream["sen_url"][url_c]["yn_sen"]
				if cay_key =="1":
					total_info=sen_con_dete(response_body,request_body,url_c)
				else:
					stream["sen_url"][url_c]["count"]+=1
					url_count=stream["sen_url"][url_c]["count"]
					if url_count % 10==0:
						total_info=sen_con_dete(response_body,request_body,url_c)
			if total_info:
				a = sen_datas(total_info)
				if a.get("sen_type_count") != {}:
					c={
					"timestamp":d_timestamp,
					"flow_id":flow_id,
					"src_ip":srcip,
					"dest_ip":dstip,
					"dest_port":destport,
					"http_method":http_method,
					"uuid": suid,
					"url": url_c,
					"url_c": url,  # 未合并的
					"app": app_dst,
					"account": account,
					"parameter": parameter,
					"request_bodys": request_body,
					"response_bodys": response_body,
					"cookie": http.get("cookie", ""),
					"request_count": a.get("sen_type_count", {}).get("请求体",""),
					"response_count": a.get("sen_type_count", {}).get("响应体",""),
					"msg_total": a.get("msg_total"),
					"sen_type_count": a.get("sen_type_count"),
					"real_ip": realip,
					"srcport": srcport
				}
					to_unix_udp(c,"/tmp/sen_count")
		
#Delete 注释 by superFBI on 2024-01-02 20:48:31

	##########处理pubsub数据(首次发现接口数据,弱点，wrf,对象管理 都从此取出 6382)############
	o["url"]=url
	o["url_c"]=url_c
	o["app"]=app_dst
	#if total_info!={}:
		#printf("total_info",total_info)
	o["total_info"]=total_info
	
	o["id"]= suid
	o["realip"]= realip
	#pub_redis("api_visit1",o)
	to_unix_udp(o,"/tmp/main_json")
	stream["obj_count"]+=1
	#pub_unix_udp(o,["/tmp/owp_1_1","/tmp/owp_1_2","/tmp/owp_2","/tmp/owp_2_3","/tmp/owp_4","/tmp/owp_sen_data","/tmp/owp_model","/tmp/mod","/tmp/object_active","/tmp/model","/tmp/ip","/tmp/risk_event","/tmp/req_alm"])
	pub_shm(o,"httpub")
	tab={"id":suid,"url":url_c,"app":app_dst,"dstip":dstip,"srcip":srcip,"account":account,"ll":content_length,"time":d_timestamp}
	#to_redis("hx_data",tab,"redis2")
	to_unix_udp(tab,"/tmp/hx_data")
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10m(st):
	field_data=load_ssdb_kv("field_sen")["data"]
	stream["sen_dic"]=get_data(field_data)
#end 

#系统定时函数，st为时间戳 
def print5f(st):
	event=load_ssdb_kv("protocol_data")["function"]["event"]
	#stream["con_rules"] = load_model_data("gsqevent")
	#敏感识别总开关
	stream["sen_identify"]=event["sen_identify"]
	# 应用全部审计
	stream["app_sj"] = event["app_sj"]
	#字段匹配
	stream["fid_mch_off"]=event["field_off"]
	b = load_ssdb_kv("manage_type")
	stream["login"] = handle_login(b["mtype"]["login"]["table"])
	stream["app_merge"]= load_ssdb_hall("app_merge")
	stream["api_merge1"]=load_ssdb_hall("api_merge1")
	stream["api_merge"]=load_ssdb_hall("api_merge")
	
	
	name_list = load_ssdb_kv("writelist")
	not_name = []
	if "name_list" in name_list["write_list"]:
		for item in name_list["write_list"]["name_list"]["name"]:
			not_name.append(item["data"])
		stream["name_lsit"] = not_name
	else:
		stream["name_list"]=[]
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

#系统定时函数，st为时间戳 
def print20(st):
	printf("审计总数","%s==sum==%d"%(st,stream["mon_count"]))
	printf("对象管理总数","%s==sum==%d"%(st,stream["obj_count"]))
	#白名单 NLP识别
	white=load_ssdb_kv("writelist")
	name_switch=white.get("name_switch")
	write_list=white["write_list"]
	#敏感信息白名单
	stream["whitelist"]={}
	with open("/opt/openfbi/pylibs/wrong_name.csv","r",encoding="utf-8")as fp:
		name_con=fp.readlines()
	name_list=[i.strip() for i in name_con if len(i.strip())>1]
	wrong_name=name_list
	if "name_list" in write_list:
		name_list=write_list.get("name_list").get("name")
		for name in name_list:
			wrong_name.append(name["data"])
	stream["whitelist"]["姓名"]=wrong_name
	wrong_moblie=[]
	if "moblie_list" in write_list:
		moblie_list=write_list.get("moblie_list").get("moblie")
		for moblie in moblie_list:
			wrong_moblie.append(moblie["data"])
	stream["whitelist"]["手机号"]=wrong_moblie
	#敏感数据正则配置
	try:
		sensitive1=load_ssdb_kv("sensitive")["data"]
		stream["sensitive"]=[]
		for data in sensitive1:
			if data["off"]==1:
				if data["rekey"]=="姓名" or data["rekey"]=="地址":
					if name_switch!="0":
						data["name"]=re.compile(data["name"])
						stream["sensitive"].append(data)
				else:
					data["name"]=re.compile(data["name"])
					stream["sensitive"].append(data)
	except:
		stream["sensitive"]=load_ssdb_kv("sensitive")["data"]
	#for data in stream["sensitive"]:
		#data["name"]=re.compile(data["name"])
	monitor_local=load_pkl("/data/xlink/api_mon.pkl")
	stream["monitor"]={}
	stream["monitor"]=monitor_local
	app_local=load_pkl("/data/xlink/app_mon.pkl")
	stream["map_apps"]={}
	stream["map_apps"]=app_local
	#存储 敏感接口信息
	file_path="/data/xlink/sen_dic.pkl"
	res=temp_dic(stream["sen_url"],file_path)
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def sen_con_dete(response_body,request_body,url_c):
	total_info={}
	if response_body != "":
		sen_data,response_body = process_data(response_body, stream["sen_dic"], stream["sensitive"], stream["whitelist"],stream["fid_mch_off"],url_c)
		if sen_data != {}:
			total_info["响应体"] = sen_data
	if request_body != "":
		sen_data,request_body= process_data(request_body, stream["sen_dic"], stream["sensitive"], stream["whitelist"],stream["fid_mch_off"],url_c)
		if sen_data != {}:
			total_info["请求体"] = sen_data
	return total_info
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def is_json_string(s):
	return (s.strip().startswith("{") and s.strip().endswith("}")) or (s.strip().startswith("[") and s.strip().endswith("]"))
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def str_json(data_source):
	data_dic = {}
	if isinstance(data_source,str) and "&" in data_source:
		result = data_source.split("&")
		
		for i in result:
			i_lst = i.split("=")
			if len(i_lst) >1:
				key = i_lst[0]
				value = i_lst[1]
				try:
					if is_json_string(value):
						value = ujson.loads(value)
				except:
					pass
				data_dic[key] = value
			elif len(i_lst) ==1:
				data_dic[i_lst[0]] = ""
		return data_dic
	else:
		return data_dic
#end 

#Delete 注释 by rzc on 2024-01-09 16:40:34

#filter_data =>(cfg,data,whitelist){

#	da={}

#	for re_match in cfg:

#		an=re.findall(re_match["name"],data)

#		if an:

#			if re_match["rekey"] in whitelist:

#				worng_name=whitelist.get(re_match["rekey"])

#				an=list(set(an)-set(worng_name))

#				if not an:

#					continue

#			da[re_match["rekey"]]=an

#	return da

#}

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def sen_datas(total_info):
	#ds=[]
	pos_info={}#监控
	msg_info={}#信息汇总
	c={}
	for pos,sen_data in total_info.items():
		if sen_data:
			#如果存在匹配的敏感数据则进行处理
			type_info={}
			msg={}
			for key,data in sen_data.items():
				value_count=0
				detail_msg=[]
				#key 为纳税人什么的，data为匹配的数据信息
				val_list=list(set(data))
				for val in val_list:
					value_count+=1
					detail_msg.append(val)
					#ds.append(http_sen)
				if value_count !=0:
					type_info[key]=value_count
					msg[key]=detail_msg
			if type_info !={}:
				pos_info[pos]=type_info
			if msg!={}:
				msg_info[pos]=msg
	c["msg_total"]=msg_info
	c["sen_type_count"]=pos_info
	return c
#end 

#克隆一个新事件,创建一个新的变量，并返回

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	if o.get("http").get("http_method"):
		http_method=o["http"]["http_method"]
	else:
		http_method=''
	c={"timestamp":iso_to_datetime(o["timestamp"]),"flow_id":o.get("flow_id"),"src_ip":o.get("src_ip"),"dest_ip":o.get("dest_ip"),"dest_port":o.get("dest_port"),"http_method":http_method}
	return c
#end 

#Delete 注释 by rzc on 2024-01-09 16:41:04

#re_rules =>(rule_list,message,sen_data,whitelist):

#	#正则匹配

#	for rule in rule_list:

#		if rule.get("off")==1:

#			an=re.findall(rule["name"], message)

#			if an:

#				#判断识别名称是否存在与白名单中 ，如果存在则取出改键值的白名单 进行剔除

#				if rule["rekey"] in whitelist:

#					worng_name=whitelist.get(rule["rekey"])

#					an=list(set(an)-set(worng_name))

#					if not an:

#						continue

#				if rule["rekey"] not in sen_data:

#					sen_data[rule["rekey"]]=an

#				else:

#					sen_data[rule["rekey"]].extend(an)

#	return sen_data

#base64字符串的解码,处理被截断的情况

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def urlc(url_m,http_url,destport,app):
	if not app:
		app=""
	if destport == 80:
		# 然后进行接口合并
		url_c = "http://" + app + url_m
		url = "http://" + app + http_url
	else:
		url_c = "http://" + app + ":" + str(destport) + url_m
		url = "http://" + app + ":" + str(destport) + http_url
	return url_c,url
#end 

#定义处理敏感数据监控函数

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def process_data(body, sen_dic, sensitive, whitelist,fid_mch_off,url):
	#if stream["sw_or_ordinary"] == "false":
	if fid_mch_off == "true":
		sen_data,body = match_data(body, sen_dic, url)
	else:
		# 普通识别
		sen_data = filter_data(sensitive, body, whitelist)
	return sen_data,body
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import random
import uuid
import copy
from stream_official_1119_sw import *
#from sen_match_identify import *
from compile_sen_match import *
import IPy
from url_merge import *
from jk_ip import jk_tf
import pickle
from un_file import *
import regex as re
from mondic import *

#end 

#udf

#end 
