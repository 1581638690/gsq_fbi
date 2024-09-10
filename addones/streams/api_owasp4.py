#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp4.xlk
#datetime: 2024-08-30T16:10:58.542003
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

#LastModifyDate:　2024-01-09T15:16:38    Author:   superFBI

#LastModifyDate:　2024-01-09T11:19:51    Author:   qh

#LastModifyDate:　2024-01-09T10:41:42    Author:   qh

#LastModifyDate:　2024-01-08T09:31:51    Author:   superFBI

#LastModifyDate:　2024-01-06T16:09:50    Author:   superFBI

#LastModifyDate:　2024-01-05T10:09:57.986035    Author:   superFBI

#LastModifyDate:　2023-12-28T09:23:02.507824    Author:   superFBI

#LastModifyDate:　2023-12-27T15:18:39.131456    Author:   superFBI

#LastModifyDate:　2023-12-27T10:15:41.745213    Author:   superFBI

#LastModifyDate:　2023-12-26T09:51:25.709554    Author:   superFBI

#LastModifyDate:　2023-11-27T14:55:33.666555    Author:   pjb

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	
	# 消费kfk 
	stream["meta_name"] = "OWASP4处理进程"
	stream["meta_desc"] = "从api_visit主题中消费数据，分析单个接口访问频率过高,单个IP访问频率过高存入数据库api_risk表"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["link"] = a["kfk"]["origin"]["link"]
	stream["topic"] = a["kfk"]["origin"]["topic"]
	stream["reset"] = a["kfk"]["origin"]["reset"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/owp_4"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["stw"]["stw_flow"]={"times":60,"fun":"flow, flow1"}
	stream["max_mem"] = 6
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	set_param("ss",stream["link"])
	if "api_model" in a:
		set_param("m","1")
	else:
		set_param("m","0")
#end 

#事件处理函数
def Events(o,topic=''):
	data_type=o.get("data_type")
	if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
		k = iso_to_timestamp(o["timestamp"])
		temp = {
			'srcip': o.get('src_ip'),
			'dest_ip': o.get('dest_ip'),
			'dest_port': int(o.get('dest_port')),
			'first_time': iso_to_datetime(o.get('timestamp')),
			'last_time': iso_to_datetime(o.get('timestamp')),
			'app': o.get('app'),
			'api': o.get('url'),	'method': o.get("http").get('http_method'),
			'length': o.get("http").get('length', 0),
			'age': o.get("http").get('age'),
			'state': "待确认"
			}
		push_stw("stw_flow",k,temp)
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
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_owasp as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[55]原语 a = load ssdb by ssdb0 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["setting"]["API19-4"]["API19-4-1"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[56]原语 b = jaas a by a["setting"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df', 'by': 'api', 'agg': 'api:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[58]原语 df2 = group df by api agg... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[59]原语 df2 = @udf df2 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df2', 'Action': 'filter', 'filter': 'df2', 'by': 'api_count > $b'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[60]原语 df2 = filter df2 by api_c... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df,df2', 'by': 'api,api'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[61]原语 df3 = join df,df2 by api,... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df3', 'Action': 'distinct', 'distinct': 'df3', 'by': 'api'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[62]原语 df3 = distinct df3 by api... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.api_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[63]原语 alter df3.api_count as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'more', 'with': '\'{"单个接口访问频率过高":"\' + df3["api_count"] + \'", "时间范围":"60s"}\''}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[64]原语 df3 = add more with ("{"单... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'type', 'with': '"API19-4-1"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[65]原语 df3 = add type with ("API... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'drop': 'api_count,age,srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[66]原语 df3 = loc df3 drop (api_c... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'af', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[67]原语 af = @udf af by udf0.df_f... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[68]原语 af = @udf df3 by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.first_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[69]原语 alter af.first_time as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[70]原语 alter af.last_time as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'API19', 'Action': 'distinct', 'distinct': 'af', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[71]原语 API19 = distinct af by (a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set', 'with': "state='待确认'"}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[73]原语 API19=@udf API19 by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,type,id,state states,length lengths from api19_risk where type like 'API19-4%%'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[75]原语 a = load db by mysql1 wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'API19', 'Action': 'join', 'join': 'API19,a', 'by': '[api,type],[api,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[76]原语 API19 = join API19,a by [... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[77]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[78]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API191', 'Action': 'filter', 'filter': 'API19', 'by': "index == 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[79]原语 API191 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API191', 'Action': 'loc', 'loc': 'API191', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[80]原语 API191 = loc API191 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API191', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk,more'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[81]原语 @udf API191 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API192', 'Action': 'filter', 'filter': 'API19', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[82]原语 API192 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.length', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[83]原语 alter API192.length as in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.lengths', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[84]原语 alter API192.lengths as i... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API192', 'Action': '@udf', '@udf': 'API192', 'by': 'udf0.df_row_lambda', 'with': 'x: x["length"] if x["length"] > x["lengths"] else x["lengths"]'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[85]原语 API192 = @udf API192 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API192', 'Action': 'loc', 'loc': 'API192', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[86]原语 API192 = loc API192 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= rename', 'Ta': 'API192', 'Action': 'rename', 'rename': 'API192', 'as': "'lambda1':'length'"}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[87]原语 API192= rename API192 as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API192', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk,more,5'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[89]原语 @udf API192 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[90]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[91]原语 drop df2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[92]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'af'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[93]原语 drop af... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[94]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[95]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[96]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'a'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[97]原语 drop a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[98]原语 drop df... 出错,原因:'+e.__str__())

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
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_owasp as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[101]原语 a = load ssdb by ssdb0 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["setting"]["API19-4"]["API19-4-2"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[102]原语 b = jaas a by a["setting"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df', 'by': 'srcip', 'agg': 'srcip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[103]原语 df2 = group df by srcip a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[104]原语 df2 = @udf df2 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df2', 'Action': 'filter', 'filter': 'df2', 'by': 'srcip_count > $b'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[105]原语 df2 = filter df2 by srcip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df,df2', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[106]原语 df3 = join df,df2 by srci... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df3', 'Action': 'distinct', 'distinct': 'df3', 'by': 'srcip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[107]原语 df3 = distinct df3 by src... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.srcip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[108]原语 alter df3.srcip_count as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'more', 'with': '\'{"单个IP访问频率过高":"\' + df3["srcip_count"] + \'", "时间范围":"60s","访问IP":"\' + df3["srcip"] +\'"}\''}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[109]原语 df3 = add more with ("{"单... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'type', 'with': '"API19-4-2"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[110]原语 df3 = add type with ("API... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'drop': 'srcip_count,srcip,age'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[111]原语 df3 = loc df3 drop (srcip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'af', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[112]原语 af = @udf af by udf0.df_f... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[113]原语 af = @udf df3 by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.first_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[114]原语 alter af.first_time as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[115]原语 alter af.last_time as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'API19', 'Action': 'distinct', 'distinct': 'af', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[116]原语 API19 = distinct af by (a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set', 'with': "state='待确认'"}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[118]原语 API19=@udf API19 by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,type,id,state states,length lengths from api19_risk where type like 'API19-4%%'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[120]原语 a = load db by mysql1 wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'API19', 'Action': 'join', 'join': 'API19,a', 'by': '[api,type],[api,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[121]原语 API19 = join API19,a by [... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[122]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[123]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API191', 'Action': 'filter', 'filter': 'API19', 'by': "index == 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[124]原语 API191 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API191', 'Action': 'loc', 'loc': 'API191', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[125]原语 API191 = loc API191 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API191', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[126]原语 @udf API191 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API192', 'Action': 'filter', 'filter': 'API19', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[127]原语 API192 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.length', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[128]原语 alter API192.length as in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.lengths', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[129]原语 alter API192.lengths as i... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API192', 'Action': '@udf', '@udf': 'API192', 'by': 'udf0.df_row_lambda', 'with': 'x: x["length"] if x["length"] > x["lengths"] else x["lengths"]'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[130]原语 API192 = @udf API192 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API193', 'Action': 'loc', 'loc': 'API192', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[131]原语 API193 = loc API192 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= rename', 'Ta': 'API193', 'Action': 'rename', 'rename': 'API193', 'as': "'lambda1':'length'"}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[132]原语 API193= rename API193 as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API193', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk,more,5'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[134]原语 @udf API193 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API194', 'Action': 'loc', 'loc': 'API192', 'by': 'last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[135]原语 API194 = loc API192 by la... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API194', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[136]原语 @udf API194 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[137]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[138]原语 drop df2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[139]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'af'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[140]原语 drop af... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[141]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[142]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[143]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[144]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[145]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'a'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[146]原语 drop a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[147]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI的原语

#窗口函数，使用FBI语句块 
def flow2(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_owasp as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[154]原语 a = load ssdb by ssdb0 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["setting"]["API19-4"]["API19-4-3"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[155]原语 b = jaas a by a["setting"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df.age', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[156]原语 alter df.age as int... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df', 'by': 'srcip,api', 'agg': 'age:median'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[157]原语 df2 = group df by srcip,a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[158]原语 df2 = @udf df2 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df2', 'Action': 'join', 'join': 'df,df2', 'by': '[srcip,api],[srcip,api]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[159]原语 df2 = join df,df2 by [src... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df2', 'Action': 'add', 'add': 'age_mad', 'by': 'abs(df2["age"]-df2["age_median"])/df2["age_median"]'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[160]原语 df2 = add age_mad by abs(... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df2', 'Action': 'loc', 'loc': 'df2', 'by': 'srcip,api,age_mad'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[161]原语 df2 = loc df2 by srcip,ap... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df2', 'Action': 'filter', 'filter': 'df2', 'by': 'age_mad > $b'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[162]原语 df2 = filter df2 by age_m... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df', 'Action': 'distinct', 'distinct': 'df', 'by': 'srcip,api'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[163]原语 df = distinct df by (srci... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df2,df', 'by': '[srcip,api],[srcip,api]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[164]原语 df3 = join df2,df by [src... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.age_mad', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[165]原语 alter df3.age_mad as int... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.age_mad', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[166]原语 alter df3.age_mad as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.first_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[167]原语 alter df3.first_time as s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'more', 'with': '\'{"响应时间波动过大":"超过限制", "波动平均极差为":"\' + df3["age_mad"] + \'ms","访问时间":"\' + df3["first_time"] + \'"}\''}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[168]原语 df3 = add more with ("{"响... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'type', 'with': '"API19-4-3"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[169]原语 df3 = add type with ("API... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'drop': 'age_mad,age,srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[170]原语 df3 = loc df3 drop (age_m... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'af', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[171]原语 af = @udf af by udf0.df_f... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[172]原语 af = @udf df3 by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.first_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[173]原语 alter af.first_time as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[174]原语 alter af.last_time as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'API19', 'Action': 'distinct', 'distinct': 'af', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[175]原语 API19 = distinct af by (a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set', 'with': "state='待确认'"}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[176]原语 API19=@udf API19 by udf0.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,type,id,state states,length lengths from api19_risk where type like 'API19-4%%'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[177]原语 a = load db by mysql1 wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'API19', 'Action': 'join', 'join': 'API19,a', 'by': '[api,type],[api,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[178]原语 API19 = join API19,a by [... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[179]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[180]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API191', 'Action': 'filter', 'filter': 'API19', 'by': "index == 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[181]原语 API191 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API191', 'Action': 'loc', 'loc': 'API191', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[182]原语 API191 = loc API191 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API191', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[183]原语 @udf API191 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API192', 'Action': 'filter', 'filter': 'API19', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[184]原语 API192 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.length', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[185]原语 alter API192.length as in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.lengths', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[186]原语 alter API192.lengths as i... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API192', 'Action': '@udf', '@udf': 'API192', 'by': 'udf0.df_row_lambda', 'with': 'x: x["length"] if x["length"] > x["lengths"] else x["lengths"]'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[187]原语 API192 = @udf API192 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API193', 'Action': 'loc', 'loc': 'API192', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[188]原语 API193 = loc API192 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= rename', 'Ta': 'API193', 'Action': 'rename', 'rename': 'API193', 'as': "'lambda1':'length'"}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[189]原语 API193= rename API193 as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API193', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk,more,5'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[191]原语 @udf API193 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API194', 'Action': 'loc', 'loc': 'API192', 'by': 'last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[192]原语 API194 = loc API192 by la... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API194', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[193]原语 @udf API194 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[194]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[195]原语 drop df2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[196]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'af'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[197]原语 drop af... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[198]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[199]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[200]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[201]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[202]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'a'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[203]原语 drop a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4.xlk]执行第[204]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#udf

#end 
