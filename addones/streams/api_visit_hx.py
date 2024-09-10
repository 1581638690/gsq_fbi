#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_visit_hx.xlk
#datetime: 2024-08-30T16:10:58.324166
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

#LastModifyDate:　2024-01-22T11:59:09    Author:   zwl

#LastModifyDate:　2024-01-19T19:05:40    Author:   zwl

#LastModifyDate:　2024-01-19T14:33:17    Author:   superFBI

#LastModifyDate:　2024-01-18T14:16:56    Author:   zwl

#LastModifyDate:　2024-01-11T18:24:06    Author:   zwl

#LastModifyDate:　2024-01-11T17:14:06    Author:   rzc

#LastModifyDate:　2024-01-09T16:20:33    Author:   zwl

#xlink脚本

#file: api_visit_hx.xlk

#name: zzzz

#描述： 

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with api_visit_hx

#停止

#a = @udf FBI.x_finder3_stop with api_visit_hx

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:api_visit_hx,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::api_visit_hx

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "画像分层"
	stream["meta_desc"] = "从api_visit1消费数据，存入ckh：api_visit_hour(存储每小时的流量访问次数)、api_visit_day(存储每天的流量访问次数)"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"] = {"link":stream["redis_link"]+":6381","topic":"hx_data","redis":"list"}
	stream["source"]= {"unix_udp":"/tmp/hx_data"}
	#窗口
	#stream["stw"]["stw_http"] = {"times":60,"fun":"flow"}
	stream["scw"]["http_100k"] = {"count":100000,"fun":"flow"}
	##定时函数
	#stream["st"]["st_day"] = {"times":86400,"fun":"print_day"}
	###存储内存
	stream["max_mem"] = 8
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	push_scw("http_100k",o)
#end 

##系统定时函数    一天调用一次

#系统定时函数，st为时间戳 
def print_day(st):
	save_day()
#end 

#窗口函数，使用FBI的原语     一分钟:60s调用一次

#窗口函数，使用FBI语句块 
def flow(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df1', 'Action': 'group', 'group': 'df', 'by': 'app,url,srcip,dstip,account', 'agg': 'id:count,ll:sum,time:max'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_visit_hx.xlk]执行第[62]原语 df1 = group df by app,url... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_visit_hx.xlk]执行第[63]原语 df1 = @udf df1 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df1', 'to': 'pq', 'by': 'xlink/api_visit_hx_min/min_@k.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_visit_hx.xlk]执行第[66]原语 store df1 to pq by xlink/... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df1'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_visit_hx.xlk]执行第[67]原语 drop df1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_visit_hx.xlk]执行第[68]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
#end 

#udf

#end 
