#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: event_counts.xlk
#datetime: 2024-08-30T16:10:58.316042
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

#LastModifyDate:　2024-08-07T16:27:37    Author:   rzc

#LastModifyDate:　2024-08-07T16:25:41    Author:   rzc

#LastModifyDate:　2024-08-07T16:18:16    Author:   rzc

#LastModifyDate:　2024-08-07T16:15:29    Author:   rzc

#LastModifyDate:　2024-08-07T15:29:26    Author:   rzc

#LastModifyDate:　2024-08-07T15:25:53    Author:   rzc

#LastModifyDate:　2024-08-05T19:08:31    Author:   pjb

#LastModifyDate:　2024-08-05T19:07:16    Author:   pjb

#LastModifyDate:　2024-08-05T18:56:52    Author:   pjb

#LastModifyDate:　2024-07-02T17:42:56    Author:   dwy

#LastModifyDate:　2024-05-31T18:12:56    Author:   dwy

#xlink脚本

#file: event_counts.xlk

#name: znsm事件统计

#描述： znsm事件实时统计

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with event_counts

#停止

#a = @udf FBI.x_finder3_stop with event_counts

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:event_counts,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::event_counts

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "znsm事件统计"
	stream["meta_desc"] = "znsm事件实时统计"
	stream["source"] = {"shm_name":"events"}
	
	#每分钟计数
	stream["stw"]["stw_event"]={"times":60,"fun":"total_events"}
	stream["stw"]["stw_csr_ip_event"]={"times":60,"fun":"csr_ip_events"}
	stream["stw"]["stw_znsm_ip_event"]={"times":60,"fun":"znsm_ip_events"}
	#stream["stw"]["stw_csr_config_event"]={"times":60,"fun":"csr_config_events"}
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#时间窗口，需要一个到秒时间戳
	k = o["k"]
	del o["k"]
	if o.get("http"):
		push_stw("stw_event",k,o)
	elif o.get("znsm_type"):
		push_stw("stw_znsm_ip_event",k,o)
		printf("aa",o)
	elif o.get("csr_type") == "csr":
		push_stw("stw_csr_ip_event",k,o)
	#Delete 注释 by pjb on 2024-05-21 18:05:32
#elif o.get("csr_type") == "csr_config":

#		printf("b",o)

#		push_stw("stw_csr_config_event",k,o)

	return [k]
#end 

#窗口函数，使用FBI的原语

#窗口函数，使用FBI语句块 
def total_events(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df_sum', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_sum'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[73]原语 df_sum = @udf df by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df_sum', 'to': 'redis', 'by': 'redis0', 'push': 'events:10s'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[75]原语 store df_sum to redis by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[76]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[78]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def csr_ip_events(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df_sum', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_sum'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[80]原语 df_sum = @udf df by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df_sum', 'to': 'redis', 'by': 'redis0', 'push': 'csr_ip_events:10s'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[81]原语 store df_sum to redis by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[82]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[84]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def znsm_ip_events(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df_sum', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_sum'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[87]原语 df_sum = @udf df by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df_sum', 'to': 'redis', 'by': 'redis0', 'push': 'znsm_ip_events:10s'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[88]原语 store df_sum to redis by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[89]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[event_counts.xlk]执行第[90]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#Delete 注释 by pjb on 2024-05-21 18:05:15

#csr_config_events => stw{

#	df_sum = @udf df by udf0.df_sum

#	store df_sum to redis by redis0 push csr_config_events:10s

#}

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
#end 

#udf

#end 
