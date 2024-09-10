#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: csrtokafka.xlk
#datetime: 2024-08-30T16:10:58.234110
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

#LastModifyDate:　2022-10-20T14:26:21.067149    Author:   gsp

#LastModifyDate:　2022-10-20T14:19:29.486841    Author:   gsp

#xlink脚本

#file: csrtokafka.xlk

#name: 云探针到Kafka

#描述： 云探针到Kafka

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with csrtokafka

#停止

#a = @udf FBI.x_finder3_stop with csrtokafka

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:csrtokafka,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::csrtokafka

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "云探针到Kafka"
	stream["meta_desc"] = "云探针到Kafka"
	stream["link"] = load_ssdb_kv("setting")["kfk"]["origin"]["link"]
	stream["topic"] = load_ssdb_kv("setting")["kfk"]["origin"]["topic"]
	stream["redis"] = load_ssdb_kv("agent")["redis"]
	stream["header"] = load_ssdb_kv("agent")["header"]
	#取第一个topic
	stream["topic1"] = load_ssdb_kv("agent")["header"][0]["topic"]
	#字典 key-topic:value-destip
	stream["cfg"] = {}
	for flag in stream["header"]:
		stream["cfg"][flag["topic"]] = flag["destip"]
		#value = list(flag.values())
		#stream["cfg"].setdefault("{}".format(value[0]), "{}".format(value[1]))
	#把剩下的topic生成一个列表
	stream["topics"] = []
	for tp in stream["header"]:
		topic = tp.get("topic")
		stream["topics"].append(topic)
	stream["topics"].pop(0)
	
	stream["source"]= {"link":stream["redis"],"topic":stream["topic1"],"redis":"list","topics":stream["topics"]}
	#stream["source"]= {"link":stream["redis"],"topic":"csr-data-1","redis":"list","topics":["csr-data-2"]}
	#stream["cfg"] = {"csr-data-1":"192.168.1.175","csr-data-2":"192.168.1.86","csr-data-3":"192.168.1.187"}
	#stream["kfk"]={"link":stream["link"],"topic":stream["topic"],"key":""}
	stream["kfk"]={"link":"192.168.1.190:9092","topic":"csrtest","key":""}
	stream["stw"]["stw_flow"]={"times":60,"fun":"flow"}
	stream["stw"]["stw_http"]={"times":60,"fun":"http"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["count"] = 0
	stream["count-10"] = 0
	#chk的链接
	#stream["CKH"] = CKH_Client(host="192.168.1.192",port=19999,user="default",password="client")
	#chk创建表
	#stream["CKH"].execute("CREATE TABLE test2 (x Int32) ENGINE = MergeTree() order by x")
	#创建pool
	pool["ckh"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	k = iso_to_timestamp(o["timestamp"])
	#o["test"] = ss(o["event_type"],o["event_type"],o["event_type"])
	#k =  int(o["time_int"]/1000)
	stream["count"] +=1
	stream["count-10"] +=1
	if o["event_type"] =="http":
		to_kfk(o)
	#to_es(o)
	#to_kfk(o)
	#to_table(o)
	#to_pool("ckh",o)
	#push_stw("stw_10s",k,o)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("print10","%s==sum==%d"%(st,stream["count"]))
	printf("print10","%s==10===%d"%(st,stream["count-10"]))
	stream["count-10"] = 0
#end 

#窗口函数，使用FBI的原语

#窗口函数，使用FBI语句块 
def flow(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[csrtokafka.xlk]执行第[91]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI的原语

#窗口函数，使用FBI语句块 
def http(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[csrtokafka.xlk]执行第[96]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义批处理函数，使用FBI语句块, 可以在系统定时函数中调用

#使用push_arrays_to_df函数生成df,在语句块中使用

#如: push_arrays_to_df(table,"flow")

#自定义批处理函数，使用FBI语句块 
def save(k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[csrtokafka.xlk]执行第[104]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ss(d1,d2,d3):
	return d1+d2+d3
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
#end 

#udf

#end 
