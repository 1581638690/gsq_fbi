#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: aopera_monitoring.xlk
#datetime: 2024-08-30T16:10:58.145809
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

#LastModifyDate:　2024-06-17T15:08:55    Author:   rzc

#LastModifyDate:　2024-06-17T15:06:45    Author:   rzc

#LastModifyDate:　2024-06-17T15:04:04    Author:   rzc

#LastModifyDate:　2024-06-17T15:02:03    Author:   rzc

#LastModifyDate:　2024-06-17T15:01:07    Author:   rzc

#LastModifyDate:　2024-06-17T14:55:09    Author:   rzc

#LastModifyDate:　2024-06-17T14:14:30    Author:   rzc

#LastModifyDate:　2024-06-17T10:28:36    Author:   rzc

#LastModifyDate:　2024-06-17T10:27:58    Author:   rzc

#xlink脚本

#file: aopera_monitoring.xlk

#name: 操作行为日志监控

#描述： 根据用户操作行为进行日志监控行为

#创建时间: 2024-06-17T10:21:51.601653

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with aopera_monitoring

#停止

#a = @udf FBI.x_finder3_stop with aopera_monitoring

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:aopera_monitoring,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::aopera_monitoring

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "操作行为日志监控"
	stream["meta_desc"] = "根据用户操作行为进行日志监控行为"
	stream["source"]= {"unix_udp":"/tmp/monitor_opera"}
	
	stream["stw"]["stw_mon"]={"times":10,"fun":"stw_mon"}
	#stream["stw"]["stw_http"]={"times":60,"fun":"http"}
	#stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	
	
	#创建ckh的pool
	pools["ckh"] = []
	
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	printf("oo",o)
	# mon = {}
	timestamp = o.get("time")
	k = iso_to_timestamp(timestamp)
	datetime_str = datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%f%z")
	
	# 提取年月日
	date_part = datetime_str.date()
	date_str = date_part.strftime("%Y-%m-%d")
	# 提取时分
	time_part = datetime_str.time()
	time_str = time_part.strftime("%H-%M")
	
	appName = o.get("app_name")
	userName = o.get("account")
	interface =o.get("name")
	type = o.get("action")
	mon = {"time":time_str,"year":date_str,"type":type,"userName":userName,"appName":appName,"interface":interface}
	push_stw("stw_mon",k,mon)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
	stream["count-10"] = 0
	
	
#end 

#窗口函数，使用FBI的原语

#窗口函数，使用FBI语句块 
def stw_mon(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'apps', 'Action': 'loc', 'loc': 'df', 'by': 'appName'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[86]原语 apps = loc df by appName... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'app_distinct', 'Action': 'distinct', 'distinct': 'apps', 'by': 'appName'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[87]原语 app_distinct = distinct a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'users', 'Action': 'loc', 'loc': 'a', 'by': 'userName'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[88]原语 users = loc a by userName... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'user_distinct', 'Action': 'distinct', 'distinct': 'users', 'by': 'userName'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[89]原语 user_distinct = distinct ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'app_distinct', 'with': 'app = $1', 'run': '""\ntt = filter df by appName == \'@app\'\nstore tt to redis by redis0 push log:app:@app:user:全部\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[92]原语 foreach app_distinct run ... 出错,原因:'+e.__str__())

#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'user_distinct', 'with': 'user = $1', 'run': '""\ntt = filter df by userName == \'@user\'\nstore tt to redis by redis0 push log:app:全部:user:@user\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[98]原语 foreach user_distinct run... 出错,原因:'+e.__str__())

#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df', 'to': 'redis', 'by': 'redis0', 'push': 'log:app:全部:user:全部'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[102]原语 store df to redis by redi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[103]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[aopera_monitoring.xlk]执行第[104]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#base64字符串的解码,处理被截断的情况

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def base64_decode(x):
	try:
		a =  base64.b64decode(x).decode("utf-8")
	except Exception as e:
		a = base64.b64decode(x)[0:e.start].decode("utf-8")
	return a
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
#end 

#udf

#end 
