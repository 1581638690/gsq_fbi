#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_2syslog.xlk
#datetime: 2024-08-30T16:10:58.308934
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

#LastModifyDate:　2023-07-27T11:10:43.745131    Author:   superFBI

#LastModifyDate:　2023-07-20T14:29:49.139502    Author:   qh

#LastModifyDate:　2023-02-28T14:45:08.837100    Author:   qh

#LastModifyDate:　2023-01-13T10:34:36.998786    Author:   pjb

#LastModifyDate:　2023-01-13T09:55:27.927277    Author:   qh

#LastModifyDate:　2023-01-12T17:04:29.301476    Author:   superFBI

#LastModifyDate:　2023-01-12T16:59:42.545132    Author:   qh

#LastModifyDate:　2023-01-12T16:24:07.322546    Author:   qh

#LastModifyDate:　2023-01-12T16:13:39.866780    Author:   qh

#LastModifyDate:　2022-12-02T17:28:11.092184    Author:   qh

#LastModifyDate:　2022-12-01T15:14:14.415574    Author:   qh

#LastModifyDate:　2022-11-22T15:06:02.452436    Author:   qh

#LastModifyDate:　2022-11-22T10:53:53.972407    Author:   gjw

#LastModifyDate:　2022-11-21T18:36:02.028768    Author:   hs

#LastModifyDate:　2022-11-21T18:32:02.390639    Author:   hs

#LastModifyDate:　2022-11-21T17:33:11.700364    Author:   qh

#LastModifyDate:　2022-11-01T15:04:17.097777    Author:   qh

#LastModifyDate:　2022-10-29T14:20:41.705838    Author:   qh

#LastModifyDate:　2022-10-29T11:20:09.840900    Author:   admin

#LastModifyDate:　2022-10-28T22:46:00.870173    Author:   admin

#LastModifyDate:　2022-10-28T19:37:23.476961    Author:   admin

#LastModifyDate:　2022-10-28T18:22:25.421061    Author:   admin

#LastModifyDate:　2022-10-28T11:59:33.703941    Author:   admin

#只发http协议

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	#stream["source"]= {"link":"127.0.0.1:9092","topic":"api_send","group":"send0112","start-0":False}
	stream["source"] = {"files":"/data/syslog_file/eve_*"}
	stream["SDK"] = load_ssdb_kv("qh_send")["SDK"]
	stream["cert"] = load_ssdb_kv("cert:TorF")["data"][0][0]
	stream["st"]["st_10s"]={"times":5,"fun":"print10"}
	stream["st"]["st_60s"]={"times":60,"fun":"sdk"}
	stream["count"] = 0
	stream["count-10"] = 0
	stream["m"]={"http":0}
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	s = 1
	if stream["SDK"] == "1":
		while s:
			if stream["cert"]:
				s = 0
			else:
				cert_again()
				time.sleep(60)
	a = {}
	#for k,v in o.items():
	#	o[k] = str(v)
	a["data"] = json.dumps(o)
	to_table(a)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	#printf("print10","sum==%d==%d==%d"%(m["http"],m["flow"],m["alert"] ))
	push_arrays_to_df(table,"logs")
	save()
#end 

#系统定时函数，st为时间戳 
def sdk(st):
	stream["SDK"] = load_ssdb_kv("qh_send")["SDK"]
	stream["cert"] = load_ssdb_kv("cert:TorF")["data"][0][0]
#end 

#自定义批处理函数，使用FBI语句块, 可以在系统定时函数中调用

#使用push_arrays_to_df函数生成df,在语句块中使用

#如: push_arrays_to_df(table,"flow")

#自定义批处理函数，使用FBI语句块 
def cert_again (k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'run', 'run': 'qh_sdk.fbi'}
	try:
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run qh_sdk.fbi')
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[75]原语 run qh_sdk.fbi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[76]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义批处理函数，使用FBI语句块 
def save (k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'zz', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_send as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[80]原语 zz = load ssdb by ssdb0 w... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'proto', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_proto"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[81]原语 proto = jaas zz by zz["sy... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'ip', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_ip"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[82]原语 ip = jaas zz by zz["syslo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'port', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_port"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[83]原语 port = jaas zz by zz["sys... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'enc', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["syslog_enc"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[84]原语 enc = jaas zz by zz["sysl... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'SDK', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[85]原语 SDK = jaas zz by zz["SDK"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'SDK_enc', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_enc"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[86]原语 SDK_enc = jaas zz by zz["... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'ip_or_id', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["SDK_ip_or_id"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[87]原语 ip_or_id = jaas zz by zz[... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'ip', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$ip,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[88]原语 ip = @sdf sys_str with ($... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'enc', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$enc,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[89]原语 enc= @sdf sys_str with ($... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'SDK', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$SDK,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[90]原语 SDK= @sdf sys_str with ($... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'ip_or_id', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$ip_or_id,[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[91]原语 ip_or_id= @sdf sys_str wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[92]原语 df1 = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'a', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[93]原语 df1 = add a by 1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': 'utf-8'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[94]原语 df1 = @udf df1 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'charset', 'Action': 'eval', 'eval': 'df1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[95]原语 charset = eval df1 by ilo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$proto == "UDP"', 'with': '""\ndf2 = @udf logs by net2.send_udp_syslog with $ip,$port,$enc,$charset,$SDK,$ip_or_id,$SDK_enc\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=96
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[96]原语 if $proto == "UDP" with "... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$proto == "TCP"', 'with': '""\ndf2 = @udf logs by net2.send_tcp_syslog with $ip,$port,$enc,$charset,$SDK,$ip_or_id,$SDK_enc\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=99
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[99]原语 if $proto == "TCP" with "... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'logs'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[102]原语 drop logs... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_2syslog.xlk]执行第[103]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
#import time
#end 

#udf

#end 
