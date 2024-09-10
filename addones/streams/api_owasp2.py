#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp2.xlk
#datetime: 2024-08-30T16:10:58.345463
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

#LastModifyDate:　2024-01-08T09:19:07    Author:   superFBI

#LastModifyDate:　2024-01-06T16:06:03    Author:   superFBI

#LastModifyDate:　2024-01-05T10:08:31.700410    Author:   superFBI

#LastModifyDate:　2024-01-05T10:02:57.715988    Author:   superFBI

#LastModifyDate:　2024-01-05T10:02:38.002294    Author:   superFBI

#LastModifyDate:　2023-12-28T09:22:41.040593    Author:   superFBI

#LastModifyDate:　2023-12-27T15:18:26.583282    Author:   superFBI

#LastModifyDate:　2023-12-27T10:15:14.948515    Author:   superFBI

#LastModifyDate:　2023-12-26T09:51:00.310150    Author:   superFBI

#LastModifyDate:　2023-12-21T10:39:13.127102    Author:   superFBI

#LastModifyDate:　2023-12-18T10:57:10.031600    Author:   superFBI

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "OWASP_API19-2处理进程"
	stream["meta_desc"] = "从api_visit主题中消费数据，更新mariadb数据库表api19_risk"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["max_mem"]=4
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/owp_2"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["redis"]={"host":stream["redis_link"],"port":"6382"}
	#stream["source"]= {"link":stream["link"],"topic":stream["topic"],"group":stream["group"],"start-0":stream["reset"]}
	#stream["source"]= {"link":stream["link"],"topic":"lhq_test","group":stream["group"],"start-0":stream["reset"]}
	# 定时函数
	stream["stw"]["stw_flow"]={"times":30,"fun":"flow"}
	stream["st"]["st_60s"]={"times":60,"fun":"print60"}
	owasp = load_ssdb_kv("qh_owasp")
	
	stream["pwls"] = []
	
	if owasp['setting']['API19-2']['API19-2-2']:
		for i in owasp['setting']['API19-2']['API19-2-2'].split('/'):
			stream['pwls'].append(i)
	if owasp['setting']['API19-7']['API19-7-2']:
		for i in owasp['setting']['API19-7']['API19-7-2'].split('/'):
			if i not in stream["pwls"]:
				stream["pwls"].append(i)
	stream["token_rule"] = ""
	if owasp['setting']['API19-2']['API19-2-3-1']:
		for i in owasp['setting']['API19-2']['API19-2-3-1'].split('/'):
			stream["token_rule"] += i + "|"
	stream["token_rule"] = '(' + stream["token_rule"].strip("|") + ')'
	
	stream["ak_rule"] = ""
	if owasp['setting']['API19-2']['API19-2-3-2']:
		for i in owasp['setting']['API19-2']['API19-2-3-2'].split('/'):
			stream["ak_rule"] += i + "|"
	stream["ak_rule"] = '(' + stream["ak_rule"].strip("|") + ')'
	stream["basic_rule"] = "(?<=https://)([\w\W]*:[\w\W]*)(?=@)"
	stream["soap_rule"] = "<(soap|soapenv):Envelope[\w\W]*<(soap|soapenv):Body"
	
	# 加载本地ip列表
	stream['lan_ip'] = []
	lan_ip_list = a["setting"]["lan"]["network"]
	for ip in lan_ip_list:
		stream['lan_ip'].append(ip['name'])
	#printf('lan_ip',stream['lan_ip'])
	# 加载cookie中保存密码配置项
	owasp = load_ssdb_kv("qh_owasp")
	stream["rules"] = ""
	if owasp['setting']['API19-7']['API19-7-4']:
		for i in owasp['setting']['API19-7']['API19-7-4'].split('/'):
			stream["rules"] += i.replace('.', '\.') + "|"
	stream["rules"] = '\.(' + stream["rules"].strip("|") + ')'
	
	#登录错误提示不合理
	err_prompt="\\b("
	if owasp["setting"]["API19-2"]["API19-2-5"]:
		for i in owasp['setting']['API19-2']['API19-2-5'].split('/'):
			err_prompt+=i+"|"
	stream["err_prompt"]=err_prompt.rstrip("|")
	stream["err_prompt"]+=")\\b"
	
	# 加载ip库
	stream["ipdb"] = IPIPDatabase('/opt/openfbi/workspace/ipdb.datx')
	
	stream["ruo_list"]=[]
	for i in open("/opt/openfbi/pylibs/ruo.csv",'r',encoding='utf-8'):
		stream["ruo_list"].append(i.replace("\n",""))
	weak_password=owasp["setting"]["weak_password"]
	if weak_password:
		pwd_list=weak_password.get("password")
		for dic in pwd_list:
			if dic not in stream["ruo_list"]:
				stream["ruo_list"].append(dic["password"])
		
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	data_type=o.get("data_type")
	if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
		k = iso_to_timestamp(o["timestamp"])
		parameter = o["parameter"]
		dstip = o["dest_ip"]
		dest_port = o["dest_port"]
		method = o.get("http").get("http_method","")
		content_length = o.get("http").get('length',0)
		first_time = str(iso_to_datetime(o["timestamp"]))
		last_time = str(iso_to_datetime(o["timestamp"]))
		request_body=o.get("http_request_body")
		response_body=o.get("http_response_body")
		request_headers = o.get("http").get("request_headers")
		# 判断是否有basic认证
		# 初始化
		have_basic = False
		for i in request_headers:
			if i.get("name") == "Authorization" and i.get("value") != "":
				find_res = i.get("value")
				if isinstance(find_res,str):
				#对Authorization进行basic认证匹配
					matchs=regex.findall('(?<=Basic\s)[\w\W]*',find_res,regex.I)
					if matchs:
						have_basic = True
						have_site = "请求头authorization中"
						break
		#有base认证和返回数据包 API19-2-1与API19-7-3
		if have_basic :
			ip_is,res = ip_lookup(o["src_ip"])
			ip_is2,res2 = ip_lookup(o["dest_ip"])
			# API19-7-3 basic认证在公网暴露 判断是否有basic认证
			if ip_is and ip_is2:
				# 准备数据
				temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-7-3")
				temp['type'] = 'API19-7-3'
				more_base = {
					"存在位置": have_site,
					"具体信息": matchs[0],
					"请求头": request_headers
				}
				temp['more'] = ujson.dumps(more_base, ensure_ascii=False)#json.dumps({"访问来源":res,"认证信息":str(find_res)}, ensure_ascii=False)
				push_stw("stw_flow",k,temp)
				#to_redis("owasp_data",o)
			#内网API19-2-1
			else:
				# 准备数据
				#printf('authorization',base64.urlsafe_b64decode(res[0]))
				temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-2-1")
				more_base = {
					"存在位置": have_site,
					"具体信息": matchs[0],
					"请求头": request_headers
				}
				temp['more'] = ujson.dumps(more_base, ensure_ascii=False)#json.dumps({"存在位置":have_site,"具体信息":str(find_res)}, ensure_ascii=False)
				push_stw("stw_flow",k,temp)
		#API19-2-2判断登陆接口是否含有明文密码 API19-2-4 OR API19-2-5
		if o["api_type"] == 1 or o["api_type"] == 5:
			weak_msg={}
			plain_msg={}
			par = {}
			plain_pwd = {}
			weak_res={}
			weak_pwd=[]
			pwd_where = []
			if response_body:
				res_match=regex.findall(stream["err_prompt"],response_body)
				if res_match:
					temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-2-5")
					temp["more"]=ujson.dumps({"存在位置":"响应体","提示信息":res_match,"证据样例":response_body}, ensure_ascii=False)
					push_stw("stw_flow",k,temp)
			if request_body :
				data=extract_username_password(request_body,response_body,stream["pwls"])
				if data:
					if "请求体" in data:
						#取出密码
						pwl=data["请求体"]["pwls"]
						password=data["请求体"]["密码"]
						pos="请求体"
						en_pos="http_request_body"
						weak_res,weak_pwd,weak_msg,plain_pwd,pwd_where,plain_msg=pwd_msgs(password,pwl,stream["ruo_list"],weak_res,weak_pwd,weak_msg,plain_pwd,pwd_where,plain_msg,request_body,pos,en_pos)
			if parameter:
				pwl_pwd=extract_password_from_parameter(stream["pwls"],parameter)
				if pwl_pwd:
					pwl=pwl_pwd[0]
					pwd=pwl_pwd[1]
					pos="参数"
					en_pos="parameter"
					weak_res,weak_pwd,weak_msg,plain_pwd,pwd_where,plain_msg=pwd_msgs(pwd,pwl,stream["ruo_list"],weak_res,weak_pwd,weak_msg,plain_pwd,pwd_where,plain_msg,parameter,pos,en_pos)
			if weak_res:
				temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-2-4")
				temp['more'] = ujson.dumps({"存在位置":str(weak_pwd),"密码信息":str(weak_res),"证据样例":weak_msg}, ensure_ascii=False)
				push_stw("stw_flow",k,temp)
			if plain_pwd:
				temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-2-2")
				temp['more'] = ujson.dumps({"存在位置":str(pwd_where),"密码信息":str(plain_pwd),"证据样例":plain_msg}, ensure_ascii=False)
				push_stw("stw_flow",k,temp)
		# API19-7-2 cookie中存在密码
		if "cookie" in o["http"]:
			cookie=o['http']['cookie']
			weak_cookie={}
			weak_pwd=[]
			weak_msg={}
			cookie_msg={}
			res_lst = []
			pwl_pwd=extract_username_password_from_cookie(cookie,stream["pwls"])
			if pwl_pwd:
				pwl=pwl_pwd[0]
				pwd=pwl_pwd[1]
				if len(pwd)<15 and pwd !="":
					res=pwl+"="+pwd
					if pwd in stream["ruo_list"]:
						#弱口令
						weak_cookie["cookie"]=res
						weak_pwd.append("cookie")
						weak_msg["cookie"]=o["http"]["cookie"]
					#cookie保存密码
					res_lst.append(res)
					cookie_msg["cookie"]=o["http"]["cookie"]
			#存储mysql
			if res_lst!=[]:
				# 准备数据
				temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-7-2")
				temp['more'] =ujson.dumps({"具体信息":cookie,"密码信息":res_lst,"证据样例":cookie_msg}, ensure_ascii=False)
				push_stw("stw_flow",k,temp)
			if weak_cookie:
				temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-2-4")
				temp['more'] = ujson.dumps({"存在位置":str(weak_pwd),"密码信息":str(weak_cookie),"证据样例":weak_msg}, ensure_ascii=False)
				push_stw("stw_flow",k,temp)
		# API19-7-4 不安全的直接对象访问
		if request_body and response_body:
			if parameter:
				msg_7_4={}
				#msg_7_4["原始ID"]=id
				msg_7_4["参数"]=parameter
				res = regex.search(stream["rules"],parameter)
				if res:
					# 准备数据
					temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-7-4")
					#temp['type'] = 'API19-7-4'
					req = "http://" + o.get("app",dstip) + ":" + str(dest_port) + o["http"]["url"]
					temp['more'] =ujson.dumps({"不安全的直接对象访问":"直接对象访问","弱点请求":req,"证据样例":msg_7_4}, ensure_ascii=False)
					push_stw("stw_flow",k,temp)
				# API19-7-1 跨域访问
				if '?' in o['http']['url']:
					api = o['http']['url'].split('?')
					http_uri = api[0]
					parameter = api[1]
					if http_uri != '/':
						response_headers = o.get("http").get('response_headers')
						risk_tissue = owasp_seven(response_headers, parameter)
						if risk_tissue:
							# 准备数据
							temp=store_result(o,dstip,dest_port,method,content_length,first_time,last_time,"API19-7-1")
							temp['more'] =ujson.dumps({"弱点类型":"跨域访问","存在原因":"响应头中Access-Control-Allow-Origin的值为*","证据样例":response_headers}, ensure_ascii=False)
							push_stw("stw_flow",k,temp)
							#to_redis("owasp_data",o)
					
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print60(st):
	owasp = load_ssdb_kv("qh_owasp")
	stream["ruo_list"]=[]
	for i in open("/opt/openfbi/pylibs/ruo.csv",'r',encoding='utf-8'):
		stream["ruo_list"].append(i.replace("\n",""))
	weak_password=owasp["setting"]["weak_password"]
	if weak_password:
		pwd_list=weak_password.get("password")
		for dic in pwd_list:
			if dic not in stream["ruo_list"]:
				stream["ruo_list"].append(dic["password"])
	stream["pwls"] = []
	if owasp['setting']['API19-2']['API19-2-2']:
		for i in owasp['setting']['API19-2']['API19-2-2'].split('/'):
			stream['pwls'].append(i)
	if owasp['setting']['API19-7']['API19-7-2']:
		for i in owasp['setting']['API19-7']['API19-7-2'].split('/'):
			if i not in stream["pwls"]:
				stream["pwls"].append(i)
	#登录错误提示不合理
	err_prompt="\\b("
	if owasp["setting"]["API19-2"]["API19-2-5"]:
		for i in owasp['setting']['API19-2']['API19-2-5'].split('/'):
			err_prompt+=i+"|"
	stream["err_prompt"]=err_prompt.rstrip("|")
	stream["err_prompt"]+=")\\b"
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def store_result(o,dstip,dest_port,method,content_length,first_time,last_time,type):
	temp = {
		'api': o.get('url_c', ''),
		'app': o["app"],
		'dest_ip': dstip,
		'dest_port': dest_port,
		'method': method,
		'length': content_length,
		'first_time': first_time,
		'last_time': last_time,
		'state': '待确认',
		'type': type
	}
	return temp
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def pwd_msgs(password,pwl,ruo_list,weak_res,weak_pwd,weak_msg,pwd_plain,pwd_pos,pwd_msg,message,pos,en_pos):
	if len(password) < 15 and password != "":
		res = pwl + "=" + password
		if password in ruo_list:
			# 弱口令
			weak_res[pos] = res
			weak_pwd.append(en_pos)
			weak_msg[pos] = message
		pwd_plain[pos] = res
		pwd_pos.append(en_pos)
		pwd_msg[pos] = message
	return weak_res,weak_pwd,weak_msg,pwd_plain,pwd_pos,pwd_msg
#end 

#窗口函数，使用FBI语句块 
def flow(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df', 'Action': 'distinct', 'distinct': 'df', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[313]原语 df = distinct df by (api,... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[314]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nAPI19 = @udf df by udf0.df_set with (state=\'待确认\')\na = load db by mysql1 with select api,type,id,state states,length lengths from api19_risk where type like \'API19-2%%\' or type like \'API19-7%%\'\nAPI19 = join API19,a by [api,type],[api,type] with left\nAPI19 = @udf API19 by udf0.df_fillna with 0\nAPI19 = @udf API19 by udf0.df_set_index with id\nAPI191 = filter API19 by index == 0 and states !=\'忽略\'\nAPI191 = loc API191 drop states,lengths\n@udf API191 by CRUD.save_table with (mysql1,api19_risk)\nAPI192 = filter API19 by index != 0 and states !=\'忽略\'\n#API192_1 = filter API19 by type == \'API19-2-3\'\n#API192_1 = loc API192_1 by more,last_time,length,app,dest_ip,dest_port,method\n#@udf API192_1 by CRUD.save_table with (mysql1,api19_risk)\nalter API192.length as int\nalter API192.lengths as int\nAPI192 = @udf API192 by udf0.df_row_lambda with x: x["length"] if x["length"] > x["lengths"] else x["lengths"]\nAPI193 = loc API192 drop first_time,state,states,length,lengths\nAPI193= rename API193 as (\'lambda1\':\'length\')\n# 保存\n@udf API193 by CRUD.save_table with (mysql1,api19_risk,more,5)\nAPI194 = loc API192 by last_time\n@udf API194 by CRUD.save_table with (mysql1,api19_risk)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=315
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[315]原语 if $size > 0 with "API19 ... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[338]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[339]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[340]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[341]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[342]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192_1'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[343]原语 drop API192_1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'a'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[344]原语 drop a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[345]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp2.xlk]执行第[346]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ip_lookup(ip):
	try:
		result = stream["ipdb"].lookup(ip).split('	')[0]
		if result not in ["局域网","本地链路","共享地址","本机地址","保留地址"]:
			a = True
		else:
			a = False
	except Exception as e:
		pass
	return a,result
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def owasp_seven(response_headers, parameter):
	if response_headers:
		for x, response in enumerate(response_headers):
			for response_values in response.values():
				if response_values == 'Access-Control-Allow-Origin':
					access = response_headers[x].values()
					if list(access)[1] == '*':
						return 1
	else:
		return 0
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def searchpwd(cookie):
	ow2 = 0
	pwls = stream["pwls"]
	for i in range(len(pwls)):
		if re.findall(r'%s' % pwls[i], cookie, re.I):
			pw = re.findall('%s=([a-zA-Z0-9]+);' % pwls[i], cookie, re.I)
			if not pw:
				pw = re.findall('&%s=([a-zA-Z0-9]+)&' % pwls[i], cookie, re.I)
			if not pw:
				pw = re.findall('\"%s\"\s*:\s*\"([a-zA-Z0-9]+)\"' % pwls[i], cookie, re.I)
			if not pw:
				pw = re.findall('\'%s\'\s*:\s*\'([a-zA-Z0-9]+)\'' % pwls[i], cookie, re.I)
			if pw:
				ow2 = pw[0]
				return ow2,pwls[i]
			else:
				return ow2,pwls[i]
	return ow2,""
#end 

#需要额外引入的包

#需要引入的包 
import regex
import sys
import gc
import uuid
import html
from pyipip import IPIPDatabase
from API19_1_2 import *
import ujson

#end 

#udf

#end 
