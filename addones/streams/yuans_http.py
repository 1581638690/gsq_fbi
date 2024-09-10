#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: yuans_http.xlk
#datetime: 2024-08-30T16:10:58.244782
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

#LastModifyDate:　2024-08-16T12:10:58    Author:   rzc

#LastModifyDate:　2024-08-15T17:47:36    Author:   rzc

#LastModifyDate:　2024-08-15T17:20:43    Author:   rzc

#LastModifyDate:　2024-08-15T17:14:49    Author:   rzc

#LastModifyDate:　2024-08-15T17:12:29    Author:   rzc

#LastModifyDate:　2024-08-15T15:58:54    Author:   rzc

#LastModifyDate:　2024-08-15T11:23:25    Author:   rzc

#LastModifyDate:　2024-08-15T11:16:57    Author:   rzc

#LastModifyDate:　2024-08-15T10:59:23    Author:   rzc

#LastModifyDate:　2024-08-15T10:53:58    Author:   rzc

#LastModifyDate:　2024-08-15T10:52:14    Author:   rzc

#xlink脚本

#file: yuan_http.xlk

#name: 原始http协议数据

#描述： 从redis中取出分发的yuan_http数据,将原始的http存入ckh中

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "原始http协议数据"
	stream["meta_desc"] = "处理main_process分发的yuan_http数据,判断请求异常、域内域外判断、接口合并(可选)、识别账号"
	stream["max_mem"] = 4
	stream["st"]["st_10s"]={"times":30,"fun":"print10"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	#接口类型、账号识别
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["max_xlink"]=1
	#stream["source"]={"link":stream["redis_link"]+":16379","topic":"yuan_http","redis":"list"}
	stream["source"]= {"unix_udp":"/tmp/yuans_http"}
	stream["content"] = handle_content_type(a["setting"]["content_type"]["type"])
	##账号检索子项开关
	account1 = a["setting"]["account"]["account_key"]
	stream["account"] = []
	for account_key in account1:
		if account_key["off"]==1:
			stream["account"].append(account_key.get("name"))
	stream["api_merge1"]=load_ssdb_hall("api_merge1")
	stream["api_merge"]=load_ssdb_hall("api_merge")
	b = load_ssdb_kv("manage_type")
	stream["login"] = handle_login(b["mtype"]["login"]["table"])
	stream["logout"] = handle_login(b["mtype"]["logout"]["table"])
	stream["download"] = handle_login(b["mtype"]["download"]["table"])
	stream["upload"] = handle_login(b["mtype"]["upload"]["table"])
	#接口合并
	#stream["trie"] = Trie()
	event=load_ssdb_kv("protocol_data")["function"]["event"]
	stream["merge_off"]=event["merge_off"]
#Delete 注释 by rzc on 2024-01-18 16:42:04

#解除注释 by rzc on 2024-01-18 16:53:47

	if stream["merge_off"]=="true":
		stream["trie"] = Trie()
		#读取接口合并的数据
		try:
			stream["merge"]=remove_file("/dev/shm/merge.pkl","/data/xlink","merge.pkl")
		except:
			stream["merge"]={}
	#syslog开关
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_http" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	send = load_ssdb_kv("qh_send")["sends"].split(',')
	stream["sends2"] = send
	#域内域外
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["wd"]=jk_tf(stream["json_wdgl"])
	#功能开关
	a = load_ssdb_kv("protocol_data")
	stream["req_alm_store"] = a["function"]["event"]["req_alm_store"]
	stream["req_s"] = a["function"]["event"]["req_s"]
	stream["resources_off"] = a["function"]["event"]["resources_off"]
	##账户检索功能总开关
	stream["account_all_key"] = a["function"]["event"]["account_all_key"]
	#redis的链接
	stream["redis"]={"host":stream["redis_link"],"port":"6380","batch":500}
	#数据接口认证方式
	stream["auth_data"]=load_ssdb_kv("api_auth")["data"]
	owasp = load_ssdb_kv("qh_owasp")
	stream["token_rule"] = ""
	if owasp['setting']['API19-2']['API19-2-3-1']:
		for i in owasp['setting']['API19-2']['API19-2-3-1'].split('/'):
			stream["token_rule"] += i + "|"
	stream["token_rule"] = stream["token_rule"].strip("|")
	
	stream["ak_rule"] = ""
	if owasp['setting']['API19-2']['API19-2-3-2']:
		for i in owasp['setting']['API19-2']['API19-2-3-2'].split('/'):
			stream["ak_rule"] += i + "|"
	stream["ak_rule"] = stream["ak_rule"].strip("|")
	#stream["user_info"]=load_pkl("user_info.pkl")
	try:
		stream["user_info"]=remove_file("/dev/shm/user_info.pkl","/data/xlink","user_info.pkl")
	except:
		stream["user_info"]={}
	stream["mge_count"] =0
	stream["account_model"] = load_model_data("account_info")
	stream["urls"] = []
	
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#Delete 注释 by rzc on 2024-08-08 10:28:59
#user_infoss={}

#	for key,value in stream["user_info"].items():

#		ss = key.split(";")

#		user_infoss[ss[0]]=value

#	stream["user_info"] =user_infoss

	timestamp = o.get("timestamp")
	flow_id = o.get("flow_id", 0)
	http=o.get("http")
	http_port = http.get("http_port")
	http_url = http.get("url")
#Delete 注释 by rzc on 2024-08-12 14:40:36

	#if o.get("http").get("hostname") == "10.71.80.194" and o.get("http").get("http_port") == 8000:
	#if o.get("http").get("hostname") == "10.71.80.194":
#		

	#	stream["urls"].append(o)
	#	printf("urls",stream["urls"])
	http_url = unquote(http_url)
	http_url = unquote(http_url)
	app=http.get("hostname")
	dstip = o.get("dest_ip")
	destport = o.get("dest_port")
	src_ip = o.get("src_ip")
	src_port = o.get("src_port", 0)
	content_type=stream["content"]
	ht_type = http.get("http_content_type","")
	#d_timestamp = iso_to_datetime(timestamp)
	#t_timestamp = iso_to_timestamp(timestamp)
	if app == '127.0.0.1' or not app:
		app = dstip
	else:
		app=http.get("hostname").split(",")[0]
	if http_port:
		destport = http_port
	if destport != 80:
		app = app + ":" + str(destport)
	status1 = str(http.get("status","")).strip()
	end = http.get("end","")
	start = http.get("start","")
	age = str(http.get("age",""))
	if "?" in http_url:
	# 剔除参数
		suri = http_url.split('?')
		uri = suri[0]
		parameter = suri[1]
	else:
		uri = http_url
		parameter = ''
	
	if "1970-01-01" in start or "1970-01-01" in end or not status1.startswith("2") or len(uri)>=4000 or len(app)>=4000 or len(parameter)>=4000 or len(age)>=18:
		if stream["req_s"] == "true":
			# 异常请求
			url = "http://" + app + uri
			if stream["req_alm_store"] == "true":
				httpjson = ujson.dumps(o,ensure_ascii=False)
			else:
				httpjson = ""
			status = "状态码异常"
			status2 = "状态码异常:"+status1
			if status1 != "":
				if status1[0] == '1':
					info = '信息，服务器收到请求，需要请求者继续执行操作'
				elif status1[0] == '3':
					info = '重定向，需要进一步的操作以完成请求'
				elif status1[0] == '4':
					info = '客户端错误，请求包含语法错误或无法完成请求'
				elif status1[0] == '5':
					info = '服务器错误，服务器在处理请求的过程中发生了错误'
				else:
					info = status1
			else:
				status = "状态码丢失"
				status2 = "其他"
				info = "状态码丢失"
			if "1970-01-01" in end:
				status = "响应数据缺失"
				status2 = "其他"
				info = "响应数据缺失"
			if "1970-01-01" in start:
				status = "请求数据缺失"
				status2 = "其他"
				info = "请求数据缺失"
			if len(app) >= 4000:
				status = "应用过长"
				status2 = "其他"
				info = "超过" + str(len(app)) + '个字符'
			if len(uri) >= 4000:
				status = "uri过长"
				status2 = "其他"
				info = "超过" + str(len(uri)) + '个字符'
			if len(parameter) >= 4000:
				status = "参数过长"
				status2 = "其他"
				info = "超过" + str(len(parameter)) + '个字符'
			if len(age) >= 18:
				status = "age过长"
				status2 = "其他"
				info = "超过" + str(len(age)) + '个字符'
			a = {"timestamp":timestamp,"id":xlink_uuid(0),"src_ip":src_ip,"dest_ip":dstip,"dest_port":destport,"app":app,"url":url,"parameter":parameter,"httpjson":httpjson,"flow_id":flow_id,"src_port":src_port,"info":info,"status":status,"status2":status2}
			#to_redis("stat_req_alm",a)
			to_unix_udp(a,"/tmp/api_data_req_alm")
			if "api_req" in stream["sends2"]:
				s = deepcopy(a)
				s["event_type"] = "request"
				#to_kfk2("api_send",s)
				s["timestamp"] = str(s["timestamp"])
				to_json_file("/data/syslog_file/eve",s)
	else:
		yuw = yn(dstip,stream["wd"])
		if yuw:
			d_timestamp = iso_to_datetime(timestamp)
			if http_url.startswith('/'):
				data_type,counts=type_class(content_type,ht_type,uri,parameter)
				if stream["resources_off"] == "false":
					if data_type=="资源文件":
						o["http_response_body"] = ""
						o["http_request_body"] = ""
				o["http_response_body"] = unquote(base64_decode(o.get("http_response_body","")))
				o["http_request_body"] = unquote(base64_decode(o.get("http_request_body","")))
				o["http"]["url"] = unquote(http_url)
				#账号信息
				#user = ""
				user_info = ""
				#sess_id = ""
				#j_id = {}
				printf("user_info",stream["user_info"])
				try:
					response_body = json.loads(o["http_response_body"])
				except:
					response_body = o["http_response_body"]
				#通过JSESSIONID进行关联账户信息
				
				#Delete 注释 by rzc on 2024-08-15 15:57:29
#				for i in o["http"]["request_headers"]:

#					if i.get("name") == 'Cookie':

#						pattern = r"JSESSIONID=([A-Za-z0-9]+)"

#						match = re.findall(pattern, i.get("value"))

#						if len(match) >= 1:

#							for jsessionid in match:

#								if jsessionid in stream["user_info"]:

#									j_id = stream["user_info"][jsessionid]

#								sess_id = jsessionid

#				if j_id:

#					user = copy.copy(j_id)

#					del user["date"]

								
							#if j_id:
							#	for jsessionid in match:
							#		if jsessionid not in stream["user_info"]:
							#			stream["user_info"][jsessionid] = j_id
						#for jsessionid in match:
						#	if jsessionid in stream["user_info"]:
								#user = copy.copy(stream["user_info"][jsessionid])
								# 会话id
								#sess_id = jsessionid
								
				req_headers=o["http"]["request_headers"]
				#user,sess_id = Refresh_cookie(req_headers, o["http"]["response_headers"], stream["user_info"])
				if stream["merge_off"]=="true":
					#对原始的url进行判断
					if data_type in ["CSS","JS","资源文件"] or uri.lower().endswith((".gif",".png",".jpg")):
						#courl=0
						#直接对其最后一段进行合并,如果最后一段为空 则改原接口就是合并的接口
						an=uri.split("/")
						#先对长度进行判断
						if counts>2 and an[-1] == "":
							an[-2]="{dst}"
						elif an[-1]!="":
							an[-1]="{dst}"
						url_c="/".join(an)
					elif counts==2:
						#courl=0
						url_c=uri
					else:
						#进行接口规则对比
						url_c,courl=stream["trie"].match_url(stream["merge"],uri,counts,app)#从main_json出来的数据 进行对比处理
						if 0< courl <5:
							url_c=uri
					url_c,url=urlc(url_c,uri,app)
					###############对手工合并接口进行处理
				else:
					url_c=uri
					#拼接接口数据
					url_c,url=urlc(url_c,uri,app)
				#手动拆分 合并接口 可以保留  
				if url_c in stream["api_merge1"]:#判断接口是否存在于拆分得数据中
					url_c=url
				#判断接口是否合并
				if stream["api_merge"]: #合并的接口
					api_values=stream["api_merge"].values()
					for apis in api_values:
						api=apis.get("url_sum").split(";|")
						if url_c in api:#判断url_c是否存在
							url_c=apis.get("url")
				api_type=api_types(o,data_type, stream["logout"],uri)
				http_request_body=o.get("http_request_body","")
				auth_type=ats(status1, stream["token_rule"], stream["ak_rule"], parameter, http_request_body, req_headers, url_c, stream["auth_data"],app)
				#api_type=0
				#auth_type=0
				
				user,sess_id = Refresh_cookie(req_headers, o["http"]["response_headers"], stream["user_info"])
				#if stream["account_all_key"]=="true":
				#	try:
				#		re_acc, type= account_search(o,parameter,o["http_request_body"],stream["account"])
				#	except Exception as e:
				#		re_acc = ''
				#		type = ''
				#	if not re_acc:
				#		re_acc = ''
				#else:
				#	o["account"] = ""
				#	o["type"] = ""
				if user:
					#printf("ccc",user)
					re_acc = user.get("user","")
					if re_acc == "":
						re_acc = user.get("账户名","")
					user_info = json.dumps(user ,ensure_ascii=False)
				else:
					re_acc =""
				#Delete 注释 by pjb on 2024-04-30 17:41:28
				#sql语句base64解密
				newstr = ""
				if uri == "/dataasset/api/core/finddatasource/queryBySql":
					str1 = o["http_request_body"]
					if str1:
						sql = re.findall(r'sql=(.*?)&sqlDataRef=', str1)
						sqld = re.findall(r'sqlDataRef=(.*?)$', str1)
						#替换解密的sql语句
						if sql and sqld:
							newstr = str1.replace(sql[0],base64_decode(sql[0]))
							newstr = newstr.replace(sqld[0],base64_decode(sqld[0]))
				if newstr:
					o["http_request_body"] = newstr
				# 识别账户信息
				acc_o = {
					"app":app,
					"url":uri,
					"request_headers":o["http"]["request_headers"],
					"response_body" :response_body,
					"response_headers":o["http"]["response_headers"]
					}
				result = read_model_identify(stream["account_model"],acc_o)
				#printf("result",result)
				#rzcs,idr = header_token_model("会话ID",stream["user_info"],result)
				#printf("rzcs",rzcs)
				#printf("idr",idr)
				stream["user_info"] = session_retrieval(stream["user_info"],result)
				type = ""
				update_data = {
					"url_c": url_c,
					"url": url,
					"app": app,
					"parameter": parameter,
					"account": re_acc,
					"user_info": user_info,
					"type": type,
					"api_type": api_type,
					"auth_type": auth_type,
					"data_type": data_type,
					"counts": counts,
					"d_timestamp": d_timestamp,
					"session_id":sess_id
				}
				o.update(update_data)
				if stream["sends"]:
					s = deepcopy(o)
					s["event_type"] = "api_http"
					s["timestamp"] = str(s["timestamp"])
					s["d_timestamp"] = str(s["d_timestamp"])
					to_json_file("/data/syslog_file/eve",s)
				printf(o["event_type"],o)
				stream["mge_count"]+=1
				
				to_unix_udp_n(o,"/tmp/http-proto",2)
				#to_unix_udp(o,"/tmp/o_rules")
					#pass
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	stream["account_model"] = load_model_data("account_info")
	printf("总数","%s==sum==%d"%(st,stream["mge_count"]))
	#数据接口认证方式
	stream["auth_data"]=load_ssdb_kv("api_auth")["data"]
	#功能开关
	a = load_ssdb_kv("protocol_data")
	stream["req_alm_store"] = a["function"]["event"]["req_alm_store"]
	stream["req_s"] = a["function"]["event"]["req_s"]
	stream["resources_off"] = a["function"]["event"]["resources_off"]
	##账户检索功能总开关
	stream["account_all_key"] = a["function"]["event"]["account_all_key"]
	#接口类型、账号识别
	a = load_ssdb_kv("setting")
	##账号检索子项开关
	account1 = a["setting"]["account"]["account_key"]
	stream["account"] = []
	for account_key in account1:
		if account_key["off"]==1:
			stream["account"].append(account_key.get("name"))
	stream["content"] = handle_content_type(a["setting"]["content_type"]["type"])
	stream["api_merge1"]=load_ssdb_hall("api_merge1")
	stream["api_merge"]=load_ssdb_hall("api_merge")
	b = load_ssdb_kv("manage_type")
	stream["login"] = handle_login(b["mtype"]["login"]["table"])
	stream["logout"] = handle_login(b["mtype"]["logout"]["table"])
	stream["download"] = handle_login(b["mtype"]["download"]["table"])
	stream["upload"] = handle_login(b["mtype"]["upload"]["table"])
	#接口合并
	event=load_ssdb_kv("protocol_data")["function"]["event"]
	stream["merge_off"]=event["merge_off"]
	if stream["merge_off"]=="true":
		stream["trie"] = Trie()
		if os.path.exists("/data/xlink/merge.pkl"):
			try:
				with open("/data/xlink/merge.pkl",'rb')as fp:
					merge_json=pickle.load(fp)
					stream["merge"]=merge_json
			except:
				with open("/data/xlink/merge.pkl",'rb')as fp:
					merge_json=pickle.load(fp)
					stream["merge"]=merge_json
		else:
			stream["merge"]={}
#end 

#系统定时函数，st为时间戳 
def send60(st):
	user_info=copy.deepcopy(stream["user_info"])
	remove_key = []
	new_date = datetime.datetime.now()
	for key, value in user_info.items():
		if (new_date - value.get("date")).total_seconds() // 3600 >= 12:
			remove_key.append(key)
			del stream["user_info"][key]
	for key in remove_key:
		del user_info[key]
	dump_pkl("/data/xlink/user_info.pkl",user_info)
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["wd"]=jk_tf(stream["json_wdgl"])
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_http" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
#end 

#拼接接口

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def urlc(url_m,http_url,app):
	if not app:
		app=""
	# 然后进行接口合并
	url_c = "http://" + app + url_m
	url = "http://" + app + http_url
	return url_c,url
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def unquote(value):
	#if "%" in value:
	if value.find("%") != -1:
		return unquote2(value)
	return value
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def session_retrieval(user_dic,result):
	#result = read_model_identify(account_rule,acc_o)
	data = result.get("data",{})
	user_infos ={}
	JESSION = []
	if data:
		for http_pos,action_value in data.items():
			for action,value_lst in action_value.items():
				for name,value in value_lst.items():
					if name!="会话ID":
						if len(value) >=1:
							user_infos[name] = value[0]
					else:
						JESSION = value
		user_infos["date"] = datetime.datetime.now()
	if JESSION:
		for jsessionid in JESSION:
			user_dic.setdefault(jsessionid,user_infos)
	return user_dic
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def header_token_model(keyword,user_info,result):
	data = result.get("data",{})
	user ={}
	sess_id = ""
	for pos,action_value in data.items():
		for action,value_lst in action_value.items():
			for name,value in value_lst.items():
				if name == keyword:
					current_token = value[0] if len(value)>=1 else ""
					if current_token and current_token in user_info:
						user = user_info[current_token]
						sess_id = current_token
	if user and "data" in usr:
		del user["date"]
	return user,sess_id
	
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def Refresh_cookie(request_headers, request_body, user_info):
	# 初始化变量
	sessid, current_sessid, user = "", "", {}
	token_container = {}
	# 预编译正则表达式
	jsessionid_pattern = re.compile(r"JSESSIONID=([A-Za-z0-9]+)")
	# 提取当前的 JSESSIONID
	for header in request_headers:
		if header.get("name") == "Cookie":
			match = jsessionid_pattern.search(header.get("value", ""))
			if match:
				sessid = match.group(1)
				break
	# 从响应体中提取新生成的 JSESSIONID
	for body_item in request_body:
		if body_item.get("name") == "Set-Cookie":
			match = jsessionid_pattern.search(body_item.get("value", ""))
			if match:
				current_sessid = match.group(1)
				break
	# 处理用户信息
	if sessid and current_sessid:
		# 更新 user_info 字典
		token_container = user_info.get(sessid, {})
		if token_container:
			user_info[current_sessid] = token_container
	elif sessid:
		# 仅查找旧的 sessid
		token_container = user_info.get(sessid, {})
	# 复制用户信息并移除日期信息
	if token_container:
		user = copy.deepcopy(token_container)
		user.pop("date", None)
	return user, sessid
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import random
import json
import uuid
#from jk_ip import *
#import base64
from unix_utils import *
from stream_official_1119_sw import *
from url_merge import *
from urllib.parse import unquote as unquote2
from mondic import *
from model_information import *
from intell_analy_new import load_model_data
#from api_auth import *
#end 

#udf

#end 
