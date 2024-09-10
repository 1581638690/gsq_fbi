#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: test_udp.xlk
#datetime: 2024-08-30T16:10:58.536045
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

#LastModifyDate:　2023-12-28T12:17:18.879470    Author:   superFBI

#LastModifyDate:　2023-12-28T11:54:39.562341    Author:   superFBI

#LastModifyDate:　2023-12-28T11:46:53.226596    Author:   superFBI

#LastModifyDate:　2023-12-28T11:46:31.272040    Author:   superFBI

#xlink脚本

#file: test_udp.xlk

#name: 测试网络ＵＤＰ的数据源

#描述： 测试网络ＵＤＰ的数据源

#创建时间: 2023-12-28T11:44:54.495920

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with test_udp

#停止

#a = @udf FBI.x_finder3_stop with test_udp

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:test_udp,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::test_udp

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "测试网络ＵＤＰ的数据源"
	stream["meta_desc"] = "测试网络ＵＤＰ的数据源"
	stream["source"]= {"unix_udp":"0.0.0.0","port":10000}
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	#chk的链接
	#stream["CKH"] = CKH_Client(host="192.168.1.192",port=19999,user="default",password="client")
	#chk创建表
	#stream["CKH"].execute("CREATE TABLE test2 (x Int32) ENGINE = MergeTree() order by x")
	#创建pool
	#pool["ckh"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	o2 = ujson.loads(o)
	to_udp_json(o2,("192.168.124.20",10000))
	return o2
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
	stream["count-10"] = 0
	push_arrays_to_df(table,"flow")
	#store_ckh(pools["ckh"],"flow")
	save()
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
	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df', 'by': 'dest_ip', 'agg': 'count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[70]原语 df2 = group df by dest_ip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_sum'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[71]原语 df3 = @udf df by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'DF:agg=>@k'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[72]原语 store df2 to ssdb by ssdb... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'DF:sum=>@k'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[73]原语 store df3 to ssdb by ssdb... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'flow', 'by': 'CRUD.save_table', 'with': 'msyql,df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[74]原语 @udf flow by CRUD.save_ta... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'assert', 'assert': 'df', 'by': 'df.index.size >0', 'as': 'xlink', 'to': '调度成功[df.index.size]', 'with': '调度失败!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[75]原语 assert df by df.index.siz... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[76]原语 drop df... 出错,原因:'+e.__str__())

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
	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df', 'by': 'dest_ip', 'agg': 'count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[80]原语 df2 = group df by dest_ip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_sum'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[81]原语 df3 = @udf df by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'DF:agg=>@k'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[82]原语 store df2 to ssdb by ssdb... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'df3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'DF:sum=>@k'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[83]原语 store df3 to ssdb by ssdb... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 't2', 'Action': '@sdf', '@sdf': 'format_timestamp', 'with': '@k,"%Y-%m-%dT%H:%M:%S"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[84]原语 t2 = @sdf format_timestam... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'assert', 'assert': 'True', 'as': 'xlink', 'to': '调度成功[$t2]', 'with': '调度失败!'}
	ptree['to'] = deal_sdf(workspace,ptree['to'])
	try:
		ret,err = assert_fun(ptree,errors,True)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[86]原语 assert True as xlink to 调... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[87]原语 drop df... 出错,原因:'+e.__str__())

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
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'flow'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[94]原语 drop flow... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[test_udp.xlk]执行第[95]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ss(d1,d2,d3):
	return d1+d2+d3
#end 

#克隆一个新事件,创建一个新的变量，并返回

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	e={}
	e["timestamp"]= o["timestamp"]
	e["src_ip"]= o["src_ip"]
	e["dest_ip"]= o["dest_ip"]
	e["dest_port"]= o["dest_port"]
	return e
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
