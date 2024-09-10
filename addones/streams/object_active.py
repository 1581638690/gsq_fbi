#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: object_active.xlk
#datetime: 2024-08-30T16:10:58.150567
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

#LastModifyDate:　2024-01-08T09:41:49    Author:   superFBI

#LastModifyDate:　2023-12-28T09:34:08.244580    Author:   superFBI

#LastModifyDate:　2023-12-27T15:20:22.205728    Author:   superFBI

#LastModifyDate:　2023-12-27T10:22:54.296727    Author:   superFBI

#LastModifyDate:　2023-08-09T10:41:11.076201    Author:   pjb

#LastModifyDate:　2023-08-08T12:23:05.950900    Author:   pjb

#LastModifyDate:　2023-05-25T16:21:23.069556    Author:   pjb

#LastModifyDate:　2023-05-25T15:15:51.361564    Author:   pjb

#LastModifyDate:　2023-05-25T14:12:16.344686    Author:   pjb

#LastModifyDate:　2023-05-25T14:09:05.338396    Author:   pjb

#LastModifyDate:　2023-05-25T14:05:17.928336    Author:   pjb

#xlink脚本

#file: object_active.xlk

#name: 对象活跃值

#描述： 计算对象的活跃值

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with object_active

#停止

#a = @udf FBI.x_finder3_stop with object_active

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:object_active,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::object_active

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "对象活跃值"
	stream["meta_desc"] = "计算对象的活跃值"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"]= {"link":stream["link"],"topic":stream["topic"],"group":"object_active","start-0":True}
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]={"unix_udp":"/tmp/object_active"}
	stream["source"] = {"shm_name":"httpub","count":8}
	#stream["source"]= {"link":"127.0.0.1:16379","topic":"api_visit","redis":"pubsub"}
	stream["st"]["st_10s"]={"times":60,"fun":"print10"}
	
	stream["stw"]["flow_app2"]={"times":10,"fun":"flow_app2"}
	stream["stw"]["flow_api2"]={"times":10,"fun":"flow_api2"}
	stream["stw"]["flow_ip2"]={"times":10,"fun":"flow_ip2"}
	stream["stw"]["flow_account2"]={"times":10,"fun":"flow_account2"}
	#从ssdb中加载一个hashmap的字典，用于比对去重等
	#Delete 注释 by pjb on 2023-01-07 09:32:49
	#当前访问时间
	stream["app_date"] = load_ssdb_hall("FF:app_date")
	stream["api_date"] = load_ssdb_hall("FF:api_date")
	stream["ip_date"] = load_ssdb_hall("FF:ip_date")
	stream["account_date"] = load_ssdb_hall("FF:account_date")
	#上次访问时间
	stream["app_date2"] = load_ssdb_hall("FF:app_date2")
	stream["api_date2"] = load_ssdb_hall("FF:api_date2")
	stream["ip_date2"] = load_ssdb_hall("FF:ip_date2")
	stream["account_date2"] = load_ssdb_hall("FF:account_date2")
	#stream["break"]= True
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#当前时间
	the_day = str(datetime.datetime.now()).split(" ")[0]
	date = str(o.get("timestamp")).split("T")[0]
	if the_day == date :
		k = iso_to_timestamp(o.get("timestamp"))
		printf("date",date)
		app = o.get("app")
		api = o.get("url_c")
		ip = o.get("src_ip")
		account = o.get("account")
		if app not in stream["app_date"] :
			stream["app_date"][app] = date
			to_ssdb_h("FF:app_date", app, date)
			stream["app_date2"][app] = date
			to_ssdb_h("FF:app_date2", app, date)
		else:
			if stream["app_date"][app] != date:
				stream["app_date2"][app] = stream["app_date"][app]
				to_ssdb_h("FF:app_date2", app, stream["app_date"][app])
				stream["app_date"][app] = date
				to_ssdb_h("FF:app_date", app, date)
		if api not in stream["api_date"] :
			stream["api_date"][api] = date
			to_ssdb_h("FF:api_date", api, date)
			stream["api_date2"][api] = date
			to_ssdb_h("FF:api_date2", api, date)
		else:
			if stream["api_date"][api] != date:
				stream["api_date2"][api] = stream["api_date"][api]
				to_ssdb_h("FF:api_date2", api, stream["api_date"][api])
				stream["api_date"][api] = date
				to_ssdb_h("FF:api_date", api, date)
		if ip not in stream["ip_date"] :
			stream["ip_date"][ip] = date
			to_ssdb_h("FF:ip_date", ip, date)
			stream["ip_date2"][ip] = date
			to_ssdb_h("FF:ip_date2", ip, date)
		else:
			if stream["ip_date"][ip] != date:
				stream["ip_date2"][ip] = stream["ip_date"][ip]
				to_ssdb_h("FF:ip_date2", ip, stream["ip_date"][ip])
				stream["ip_date"][ip] = date
				to_ssdb_h("FF:ip_date", ip, date)
		if account not in stream["account_date"] and account !='' :
			stream["account_date"][account] = date
			to_ssdb_h("FF:account_date", account, date)
			stream["account_date2"][account] = date
			to_ssdb_h("FF:account_date2", account, date)
		elif account !='':
			if stream["account_date"][account] != date:
				stream["account_date2"][account] = stream["account_date"][account]
				to_ssdb_h("FF:account_date2", account, stream["account_date"][account])
				stream["account_date"][account] = date
				to_ssdb_h("FF:account_date", account, date)
#end 

#系统定时函数，st为时间戳 
def print10(st):
	#复活
	k = iso_to_timestamp(str(datetime.datetime.now()))
	#当前访问时间
	app_2 = stream["app_date"].copy()
	api_2 = stream["api_date"].copy()
	ip_2 = stream["ip_date"].copy()
	account_2 = stream["account_date"].copy()
	#上次访问时间
	app_1 = stream["app_date2"].copy()
	api_1 = stream["api_date2"].copy()
	ip_1 = stream["ip_date2"].copy()
	account_1 = stream["account_date2"].copy()
	for key,value in app_2.items():
		if value != app_1[key] :
			app_date = (datetime.datetime.strptime(value, '%Y-%m-%d') - datetime.datetime.strptime(app_1[key], '%Y-%m-%d')).days
			if app_date > 30 :
				app3 = {}
				app3["app"] = key
				app3["active"] = 2
				push_stw("flow_app2",k,app3)
				printf("app3",app3)
	for key,value in api_2.items():
		if value != api_1[key] :
			api_date = (datetime.datetime.strptime(value, '%Y-%m-%d') - datetime.datetime.strptime(api_1[key], '%Y-%m-%d')).days
			if api_date > 30 :
				printf("value",value)
				printf('app_1[key]',api_1[key])
				printf("api_date",api_date)
				printf("key",key)
				api3 = {}
				api3["url"] = key
				api3["active"] = 2
				push_stw("flow_api2",k,api3)
	for key,value in ip_2.items():
		if value != ip_1[key] :
			ip_date = (datetime.datetime.strptime(value, '%Y-%m-%d') - datetime.datetime.strptime(ip_1[key], '%Y-%m-%d')).days
			if ip_date > 30 :
				ip3 = {}
				ip3["srcip"] = key
				ip3["active"] = 2
				push_stw("flow_ip2",k,ip3)
	for key,value in account_2.items():
		if value != account_1[key] :
			account_date = (datetime.datetime.strptime(value, '%Y-%m-%d') - datetime.datetime.strptime(account_1[key], '%Y-%m-%d')).days
			if account_date > 30 :
				account3 = {}
				account3["account"] = key
				account3["active"] = 2
				push_stw("flow_account2",k,account3)
#end 

#窗口函数，使用FBI语句块 
def flow_app2(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
#Delete 注释 by pjb on 2023-01-12 14:20:56

#	set param by xlink as k with flow_stat

#	t2 = @sdf format_timestamp with (@k,"%Y-%m-%dT%H:%M:%S")

#	assert True as xlink to 调度成功[$t2] with 调度失败

#	store df to pkl by flow_stat30.pkl

#	df = load pkl by flow_stat30.pkl

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[191]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\napp = load db by mysql1 with select app,id from data_app_new where app_type = 1 and active != 2\napp = join app,df by app,app\nsize = eval app by (index.size)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=192
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[192]原语 if $size > 0 with "app = ... 出错,原因:'+e.__str__())

#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\napp = @udf app by udf0.df_set_index with id\n@udf app by CRUD.save_table with (mysql1,data_app_new)\ndrop df\ndrop app\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=197
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[197]原语 if $size > 0 with "app = ... 出错,原因:'+e.__str__())

#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[203]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow_api2(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[207]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nurl = load db by mysql1 with select url,id from data_api_new where active != 2\nurl = join url,df by url,url\nsize = eval url by (index.size)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=208
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[208]原语 if $size > 0 with "url = ... 出错,原因:'+e.__str__())

#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nurl = @udf url by udf0.df_set_index with id\n@udf url by CRUD.save_table with (mysql1,data_api_new)\ndrop df\ndrop url\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=213
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[213]原语 if $size > 0 with "url = ... 出错,原因:'+e.__str__())

#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[219]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow_ip2(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[223]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nip = load db by mysql1 with select srcip,id from data_ip_new where active != 2\nip = join ip,df by srcip,srcip\nsize = eval ip by (index.size)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=224
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[224]原语 if $size > 0 with "ip = l... 出错,原因:'+e.__str__())

#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nip = @udf ip by udf0.df_set_index with id\n@udf ip by CRUD.save_table with (mysql1,data_ip_new)\ndrop df\ndrop ip\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=229
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[229]原语 if $size > 0 with "ip = @... 出错,原因:'+e.__str__())

#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[235]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow_account2(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[239]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\naccount = load db by mysql1 with select account,id from data_account_new where active != 2\naccount = join account,df by account,account\nsize = eval account by (index.size)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=240
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[240]原语 if $size > 0 with "accoun... 出错,原因:'+e.__str__())

#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\naccount = @udf account by udf0.df_set_index with id\n@udf account by CRUD.save_table with (mysql1,data_account_new)\ndrop df\ndrop account\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=245
		if_fun(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[245]原语 if $size > 0 with "accoun... 出错,原因:'+e.__str__())

#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[object_active.xlk]执行第[251]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import datetime
from time import strftime
#end 

#udf

#end 
