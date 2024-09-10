#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: dbms_obj.xlk
#datetime: 2024-08-30T16:10:58.327253
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

#LastModifyDate:　2024-03-05T10:46:37    Author:   pjb

#LastModifyDate:　2024-03-05T10:41:54    Author:   pjb

#LastModifyDate:　2024-03-04T17:59:25    Author:   pjb

#LastModifyDate:　2024-03-04T17:45:37    Author:   pjb

#LastModifyDate:　2024-02-02T14:28:41    Author:   pjb

#LastModifyDate:　2024-02-01T18:49:34    Author:   pjb

#LastModifyDate:　2024-02-01T18:38:47    Author:   pjb

#LastModifyDate:　2024-02-01T18:29:38    Author:   pjb

#LastModifyDate:　2024-01-25T15:22:27    Author:   pjb

#LastModifyDate:　2023-11-24T11:44:29.530429    Author:   pjb

#LastModifyDate:　2023-11-15T14:15:47.766223    Author:   pjb

#xlink脚本

#4主体信息

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "数据库对象管理"
	stream["meta_desc"] = "从redis中消费数据，存入mariadb数据库dbms_obj表"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["source"]= {"unix_udp":"/tmp/obj_dbms"}
	#stream["source"]={"link":stream["redis_link"]+":6380","topic":"dbms_obj","redis":"list","topics":["dbms_user","dbms_sql","fileinfo"]}
	stream["scw"]["scw_obj"] = {"count":5,"fun":"flow1"}
	stream["scw"]["scw_user"] = {"count":1,"fun":"flow2"}
	stream["scw"]["scw_sql"] = {"count":10,"fun":"flow3"}
	stream["scw"]["scw_fileinfo"] = {"count":10,"fun":"flow4"}
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	if o.get("version") or o.get("version")=="":
		printf("scw_obj",o)
		o["active"] = "3"
		o["sensitive_label"] = "0"
		push_scw("scw_obj",o)
	if o.get("user") and not o.get("dbms_sql"):
		printf("scw_user",o)
		o["active"] = "3"
		o["sensitive_label"] = "0"
		push_scw("scw_user",o)
	if o.get("dbms_sql"):
		printf("scw_sql",o)
		push_scw("scw_sql",o)
	if o.get("filename"):
		printf("scw_fileinfo",o)
		push_scw("scw_fileinfo",o)
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
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'dbms_obj', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[56]原语 dbms_obj = @udf df by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'dbms_obj', 'Action': '@udf', '@udf': 'dbms_obj', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[57]原语 dbms_obj = @udf dbms_obj ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'dbms_obj', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[59]原语 @udf dbms_obj by CRUD.sav... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'dbms_obj'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[60]原语 drop dbms_obj... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[61]原语 drop df... 出错,原因:'+e.__str__())

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
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'dbms_user', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[63]原语 dbms_user = @udf df by ud... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'dbms_user', 'Action': '@udf', '@udf': 'dbms_user', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[64]原语 dbms_user = @udf dbms_use... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'dbms_user', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[65]原语 @udf dbms_user by CRUD.sa... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'dbms_user'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[66]原语 drop dbms_user... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[67]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow3(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'dbms_sql', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[69]原语 dbms_sql = @udf df by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'dbms_sql', 'Action': '@udf', '@udf': 'dbms_sql', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[70]原语 dbms_sql = @udf dbms_sql ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'dbms_sql', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_sql'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[71]原语 @udf dbms_sql by CRUD.sav... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'dbms_sql'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[72]原语 drop dbms_sql... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[73]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow4(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'fileinfo', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[75]原语 fileinfo = @udf df by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'fileinfo', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[76]原语 fileinfo = @udf fileinfo ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'fileinfo', 'by': 'CRUD.save_table', 'with': 'mysql1,fileinfo'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[77]原语 @udf fileinfo by CRUD.sav... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'fileinfo'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[78]原语 drop fileinfo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[dbms_obj.xlk]执行第[79]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义批处理函数，使用FBI语句块, 可以在系统定时函数中调用

#使用push_arrays_to_df函数生成df,在语句块中使用

#如: push_arrays_to_df(table,"flow")

#需要额外引入的包

#需要引入的包 
import sys
import gc
#end 

#udf

#end 
