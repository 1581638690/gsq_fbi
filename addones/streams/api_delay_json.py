#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_delay_json.xlk
#datetime: 2024-08-30T16:10:58.320402
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

#LastModifyDate:　2024-01-05T09:35:11.615746    Author:   superFBI

#LastModifyDate:　2023-12-27T13:56:18.427189    Author:   superFBI

#LastModifyDate:　2023-08-08T18:33:28.634967    Author:   pjb

#LastModifyDate:　2023-07-27T11:21:33.574582    Author:   superFBI

#LastModifyDate:　2023-07-19T16:02:37.580131    Author:   qh

#LastModifyDate:　2023-04-04T12:42:59.890636    Author:   rzc

#LastModifyDate:　2023-04-04T11:56:02.744613    Author:   rzc

#LastModifyDate:　2022-12-10T14:47:40.719478    Author:   qh

#LastModifyDate:　2022-12-08T16:21:51.257791    Author:   qh

#LastModifyDate:　2022-11-21T18:32:18.700379    Author:   hs

#LastModifyDate:　2022-11-21T18:01:43.701449    Author:   qh

#xlink脚本

# 处理urls的信息

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "耗时数据存储数据库进程"
	stream["meta_desc"] = "从api_delay主题中消费数据，存入ckh数据库api_delay表"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["redis_link"]+":16379","topic":"delay_time","redis":"list"}
	stream["source"]= {"unix_udp":"/tmp/delay_time"}
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	stream["st"]["st_10s"]={"times":20,"fun":"print10"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_delay" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	o["warn_level"] = str(o["warn_level"])
	o["time"] = iso_to_datetime(o["time"])
	to_table(o)
	if stream["sends"]:
		s = deepcopy(o)
		s["event_type"] = "delay"
		#to_kfk(s)
		to_json_file("/data/syslog_file/eve",s)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	store_ckh(table,"api_delay")
#end 

#系统定时函数，st为时间戳 
def send60(st):
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_delay" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
#end 

#自定义批处理函数，使用FBI语句块, 可以在系统定时函数中调用

#自定义批处理函数，使用FBI语句块 
def save (k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 't2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_delay_json.xlk]执行第[65]原语 t2 = @sdf sys_now... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 't1', 'Action': 'eval', 'eval': 'delays', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[api_delay_json.xlk]执行第[66]原语 t1 = eval delays by index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'delays', 'Action': '@udf', '@udf': 'delays', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_delay_json.xlk]执行第[68]原语 delays = @udf delays by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'delays', 'to': 'ckh', 'by': 'ckh', 'with': 'api_delay'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_delay_json.xlk]执行第[69]原语 store delays to ckh by ck... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'delays'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_delay_json.xlk]执行第[71]原语 drop delays... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_delay_json.xlk]执行第[73]原语 drop df... 出错,原因:'+e.__str__())

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
