#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp_2_3.xlk
#datetime: 2024-08-30T16:10:58.528520
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

#LastModifyDate:　2024-01-06T21:16:26    Author:   superFBI

#LastModifyDate:　2024-01-06T16:18:16    Author:   superFBI

#LastModifyDate:　2024-01-05T11:05:51.582503    Author:   superFBI

#LastModifyDate:　2023-12-28T09:24:06.387495    Author:   superFBI

#LastModifyDate:　2023-12-27T15:19:15.079920    Author:   superFBI

#LastModifyDate:　2023-12-27T10:16:44.565362    Author:   superFBI

#LastModifyDate:　2023-12-26T09:51:45.696534    Author:   superFBI

#LastModifyDate:　2023-12-21T10:38:32.714088    Author:   superFBI

#LastModifyDate:　2023-12-18T10:32:52.726992    Author:   superFBI

#LastModifyDate:　2023-12-18T10:31:30.051451    Author:   superFBI

#LastModifyDate:　2023-11-27T14:54:22.930136    Author:   pjb

#xlink脚本

#file: api_owasp_2_3.xlk

#name: 数据接口无认证

#描述： 从owasp19中取出带敏感数据的数据进行处理

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with api_owasp_2_3

#停止

#a = @udf FBI.x_finder3_stop with api_owasp_2_3

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:api_owasp_2_3,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::api_owasp_2_3

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "数据接口无认证"
	stream["meta_desc"] = "从owasp19中取出带敏感数据的数据进行处理"
	a = load_ssdb_kv("setting")
	#stream["source"]= {"link":"127.0.0.1:16379","topic":"api_visit","redis":"pubsub"}
	#stream["source"]= {"link":stream["link"],"topic":stream["topic"],"group":"API19SEN","start-0":stream["reset"]}
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["redis"]={"host":stream["redis_link"],"port":"6382"}
	stream["stw"]["stw_flow"]={"times":10,"fun":"flow"}
	owasp = load_ssdb_kv("qh_owasp")
	stream["pwls"] = []
	
	if owasp['setting']['API19-2']['API19-2-2']:
		for i in owasp['setting']['API19-2']['API19-2-2'].split('/'):
			stream['pwls'].append(i)
	
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
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	# http 消息的主处理流程
	#http = ujson.loads(o["httpjson"])
	# 公共参数准备工作
	data_type=o.get("data_type")
	if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
		http=o.get("http")
		status = str(http.get("status","")).strip()
		url=o.get("url_c")
		cookie=o.get("http").get("cookie","")
		authorization=o.get("http").get("authorization","")
		#par
		dstip = str(o.get("dest_ip"))
		dest_port = int(o.get("dest_port"))
		method = o.get("http").get("http_method","")
		content_length = o.get("http").get('length',0)
		first_time = str(iso_to_datetime(o["timestamp"]))
		last_time = str(iso_to_datetime(o["timestamp"]))
		request_body=o.get("http_request_body","")
		response_body=o.get("http_response_body","")
		request_headers=o.get("http").get("request_headers")
		auth_type=o.get("auth_type")
		#时间窗口，需要一个到秒时间戳
		if o["api_type"] == 5 and request_body and response_body:
			if auth_type ==0:
				k = iso_to_timestamp(o["timestamp"])
				wz = {
					"url": url,
					"cookie": cookie,
					"authorization": authorization,
					"请求头": request_headers,
					"请求体": request_body,
					"响应体": response_body
				}
				#printf('http',http)
				temp = {
					'api': o.get('url_c', ''),
					'app': o['app'],
					'dest_ip': dstip,
					'dest_port': dest_port,
					'method': method,
					'length': content_length,
					'first_time': first_time,
					'last_time': last_time,
					'state': '待确认',
					'type': 'API19-2-3',
					'more': json.dumps({"数据接口无认证": wz}, ensure_ascii=False)
				}
				push_stw("stw_flow",k,temp)
			#printf("temp",temp)
			#to_redis("owasp_data",o)
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
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'API19', 'Action': 'distinct', 'distinct': 'df', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[130]原语 API19 = distinct df by (a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'API19', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[131]原语 size = eval API19 by (ind... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nAPI19 = @udf API19 by udf0.df_set with (state=\'待确认\')\na = load db by mysql1 with select api,type,id,state states,length lengths from api19_risk where type like \'API19-2%%\'\nAPI19 = join API19,a by [api,type],[api,type] with left\nAPI19 = @udf API19 by udf0.df_fillna with 0\nAPI19 = @udf API19 by udf0.df_set_index with id\nAPI191 = filter API19 by index == 0 and states !=\'忽略\'\nAPI191 = loc API191 drop states,lengths\n@udf API191 by CRUD.save_table with (mysql1,api19_risk)\nAPI192 = filter API19 by index != 0 and states !=\'忽略\'\n#API192_1 = filter API19 by type == \'API19-2-3\'\n#API192_1 = loc API192_1 by more,last_time,length,app,dest_ip,dest_port,method\n#@udf API192_1 by CRUD.save_table with (mysql1,api19_risk)\nalter API192.length as int\nalter API192.lengths as int\nAPI192 = @udf API192 by udf0.df_row_lambda with x: x["length"] if x["length"] > x["lengths"] else x["lengths"]\nAPI193 = loc API192 drop first_time,state,states,length,lengths\nAPI193= rename API193 as (\'lambda1\':\'length\')\n# 保存\n@udf API193 by CRUD.save_table with (mysql1,api19_risk,more,5)\nAPI194 = loc API192 by last_time\n@udf API194 by CRUD.save_table with (mysql1,api19_risk)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=132
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[132]原语 if $size > 0 with "API19 ... 出错,原因:'+e.__str__())

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
		errors.append('[api_owasp_2_3.xlk]执行第[155]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[156]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[157]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[158]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[159]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192_1'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[160]原语 drop API192_1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'a'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[161]原语 drop a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_2_3.xlk]执行第[163]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
import regex
#end 

#udf

#end 
