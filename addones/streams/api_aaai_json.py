#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_aaai_json.xlk
#datetime: 2024-08-30T16:10:58.418315
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

#LastModifyDate:　2024-04-30T16:30:37    Author:   pjb

#LastModifyDate:　2024-03-04T17:58:23    Author:   pjb

#LastModifyDate:　2024-03-04T17:45:54    Author:   pjb

#LastModifyDate:　2024-01-09T15:43:38    Author:   zwl

#LastModifyDate:　2024-01-05T09:32:05.556688    Author:   superFBI

#LastModifyDate:　2023-12-28T10:19:28.048222    Author:   superFBI

#LastModifyDate:　2023-12-28T10:07:14.626893    Author:   superFBI

#LastModifyDate:　2023-10-08T16:04:14.834360    Author:   superFBI

#LastModifyDate:　2023-09-13T15:01:29.057230    Author:   superFBI

#LastModifyDate:　2023-09-13T11:31:37.215206    Author:   rzc

#LastModifyDate:　2023-08-08T11:43:18.694906    Author:   pjb

#xlink脚本

#4主体信息

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "对象管理:终端、接口、应用、账户"
	stream["meta_desc"] = "从redis中消费数据，存入mariadb数据库data_*_new等4个表"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["source"]= {"unix_udp":"/tmp/api_object"}
	stream["count"] = 0
	stream["count-10"] = 0
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	stream["sends"] = load_ssdb_kv("qh_send")["sends"].split(',')
	pool["app"] = []
	pool["api"] = []
	pool["account"] = []
	pool["ip"] = []
	stream["scw"]["scw_api"] = {"count":20,"fun":"flow"}
	stream["scw"]["scw_app"] = {"count":20,"fun":"flow1"}
	stream["scw"]["scw_account"] = {"count":20,"fun":"flow2"}
	stream["scw"]["scw_ip"] = {"count":20,"fun":"flow3"}
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	account = o.get("account") # account
	srcip =o.get("srcip") # ip
	api = o.get("api") # api
	app_title =o.get("app_title")
	#if topic == "http_app":
	if app_title or app_title == "":
		o["last_time"]=o.get("first_time")
		push_scw("scw_app",o)
		#to_pool("app",o)
		if "api_app" in stream["sends"]:
			s = deepcopy(o)
			s["event_type"] = "app"
			#to_kfk(s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	#elif topic == "http_api":
	elif api or api =="":
		#to_pool("api",o)
		push_scw("scw_api",o)
		if "api_url" in stream["sends"]:
			s = deepcopy(o)
			s["event_type"] = "api"
			#to_kfk(s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	#elif topic == "http_account":
	elif account or account == "":
		#to_pool("account",o)
		push_scw("scw_account",o)
		if "api_account" in stream["sends"]:
			s = deepcopy(o)
			s["event_type"] = "account"
			#to_kfk(s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	#elif topic == "http_ip":
	elif srcip or srcip == "":
		#to_pool("ip",o)
		push_scw("scw_ip",o)
		if "api_ip" in stream["sends"]:
			s = deepcopy(o)
			s["event_type"] = "ip"
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	push_arrays_to_df(pool["app"],"apps")
	push_arrays_to_df(pool["api"],"apis")
	push_arrays_to_df(pool["account"],"accounts")
	push_arrays_to_df(pool["ip"],"ips")
	save()
#end 

#系统定时函数，st为时间戳 
def send60(st):
	stream["sends"] = load_ssdb_kv("qh_send")["sends"].split(',')
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
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'apis', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[105]原语 apis = @udf df by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'apis', 'Action': '@udf', '@udf': 'apis', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[106]原语 apis = @udf apis by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'apis', 'Action': 'add', 'add': 'name', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[107]原语 apis = add name by ("")... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'apis.first_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[108]原语 alter apis.first_time as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'apis.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[109]原语 alter apis.last_time as s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'apis', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[110]原语 aa = @udf apis by CRUD.sa... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'apis'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[111]原语 drop apis... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[112]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[113]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow1(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'apps', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[116]原语 apps = @udf df by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'apps', 'Action': '@udf', '@udf': 'apps', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[117]原语 apps = @udf apps by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'apps', 'Action': 'add', 'add': 'name', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[118]原语 apps= add name by ("")... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'apps.first_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[119]原语 alter apps.first_time as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'apps.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[120]原语 alter apps.last_time as s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'apps', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[121]原语 @udf apps by CRUD.save_ta... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'apps'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[122]原语 drop apps... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[123]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[124]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow2(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'accounts', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[126]原语 accounts = @udf df by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'accounts', 'Action': '@udf', '@udf': 'accounts', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[127]原语 accounts = @udf accounts ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'accounts.firsttime', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[128]原语 alter accounts.firsttime ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'accounts.lasttime', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[129]原语 alter accounts.lasttime a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'accounts', 'by': 'CRUD.save_table', 'with': 'mysql1,data_account_new'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[130]原语 @udf accounts by CRUD.sav... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'accounts'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[131]原语 drop accounts... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[132]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[133]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow3 (k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'ips', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[135]原语 ips = @udf df by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'ips', 'Action': '@udf', '@udf': 'ips', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[136]原语 ips = @udf ips by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'ips.firsttime', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[137]原语 alter ips.firsttime as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'ips.lasttime', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[138]原语 alter ips.lasttime as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'ips', 'by': 'CRUD.save_table', 'with': 'mysql1,data_ip_new'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[139]原语 @udf ips by CRUD.save_tab... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'ips'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[140]原语 drop ips... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[141]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_aaai_json.xlk]执行第[142]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
from copy import deepcopy
#end 

#udf

#end 
