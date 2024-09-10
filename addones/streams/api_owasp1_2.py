#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp1_2.xlk
#datetime: 2024-08-30T16:10:58.507572
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

#LastModifyDate:　2024-01-23T10:21:57    Author:   rzc

#LastModifyDate:　2024-01-08T09:18:20    Author:   superFBI

#LastModifyDate:　2024-01-05T09:59:48.144098    Author:   superFBI

#LastModifyDate:　2023-12-28T09:22:04.612867    Author:   superFBI

#LastModifyDate:　2023-12-27T15:18:17.436986    Author:   superFBI

#LastModifyDate:　2023-12-27T10:14:53.545171    Author:   superFBI

#LastModifyDate:　2023-12-26T14:39:10.050521    Author:   superFBI

#LastModifyDate:　2023-11-27T14:55:13.739967    Author:   pjb

#LastModifyDate:　2023-10-08T17:31:35.349726    Author:   superFBI

#LastModifyDate:　2023-10-08T16:24:59.297979    Author:   superFBI

#LastModifyDate:　2023-09-25T18:09:23.605943    Author:   superFBI

#xlink脚本

#file: api_owasp1.xlk

#name: OWASP_API19-1处理进程

#描述： 从api_visit主题中消费数据

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with api_owasp1

#停止

#a = @udf FBI.x_finder3_stop with api_owasp1

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:api_owasp1,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::api_owasp1

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "OWASP_API19-1-2处理进程"
	stream["meta_desc"] = "从api_visit主题中消费数据"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/owp_1_2"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["stw"]["stw_flow"]={"times":20,"fun":"flow"}
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	try:
		stream["object_guess"]=remove_file("/dev/shm/object_guess.pkl","/data/xlink","object_guess.pkl")
		#pickle.load(fp)
	except:
		stream["object_guess"]={}
#end 

#事件处理函数
def Events(o,topic=''):
	data_type=o.get("data_type")
	#if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
	total_info=o.get("total_info")
	response_body=o.get("http_response_body","")
	k = iso_to_timestamp(o["timestamp"])
	if total_info:
		http=o.get("http")
		purl=http.get("url")
		app=o.get("app")
		if "?" in purl:
			uri=purl.split("?")[0]
		else:
			uri=purl
		url=o.get("url")
		url_c=o.get("url_c")
		length=http.get("length")
		#返回总字典，类似接口内容，对象可猜测接口数
		url_dic,object_str,similar_url,lengths,url_c=guess_object(url,uri,url_c,stream["object_guess"],app,length)
		printf("similar_url",similar_url)
		stream["object_guess"]=url_dic
		if similar_url:
			#end={"对象可猜测":object_str,"类似接口内容":similar_url,"敏感信息":total_info}
			end={"对象可猜测":object_str,"类似接口内容":similar_url}
			e=clone_event(o)
			e["more"]=json.dumps(end,ensure_ascii=False).encode("utf-8")
			e["api"]=url_c
			e["state"]="待确认"
			e["type"]="API19-1-2"
			e["length"]=lengths
			#to_table(e)
			#push_scw("scw_e",e)
			push_stw("stw_flow",k,e)
			stream["count"]+=1
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
#end 

#系统定时函数，st为时间戳 
def print120(st):
	
	with open("/data/xlink/object_guess.pkl",'wb') as fp:
		object_guess=copy.copy(stream["object_guess"])
		pickle.dump(object_guess,fp)
#end 

#窗口函数，使用FBI语句块 
def flow(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'API19', 'Action': 'distinct', 'distinct': 'df', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[102]原语 API19 = distinct df by (a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'cc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,app,type,id,state states,length lengths from api19_risk where type = 'API19-1-2'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[105]原语 cc = load db by mysql1 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'API19', 'Action': 'join', 'join': 'API19,cc', 'by': '[api,app,type],[api,app,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[108]原语 API19 = join API19,cc by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[109]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[110]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API191', 'Action': 'filter', 'filter': 'API19', 'by': "index == 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[111]原语 API191 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API191', 'Action': 'loc', 'loc': 'API191', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[112]原语 API191 = loc API191 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API191', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[113]原语 @udf API191 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API192', 'Action': 'filter', 'filter': 'API19', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[114]原语 API192 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API193', 'Action': 'loc', 'loc': 'API192', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[115]原语 API193 = loc API192 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API193', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[116]原语 @udf API193 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API194', 'Action': 'loc', 'loc': 'API192', 'by': 'last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[117]原语 API194 = loc API192 by la... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API194', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[118]原语 @udf API194 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'cc'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[119]原语 drop cc... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[120]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[121]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[122]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[123]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[124]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[125]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp1_2.xlk]执行第[126]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#克隆一个新事件,创建一个新的变量，并返回

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	e={}
	e["api"]=o.get('url','')
	e["app"]=o.get('app','')
	e["method"]=o.get("http").get("http_method","")
	#e["url_c"]=o.get("url","")
	e["dest_ip"]=o.get("dest_ip")
	e["dest_port"]=o.get("dest_port")
	e["length"]=o.get("http").get('length',0)
	e["first_time"]= str(iso_to_datetime(o["timestamp"]))
	e["last_time"] = str(iso_to_datetime(o["timestamp"]))
	return e
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def is_json_string(s):
	try:
		json.loads(s)
		return True
	except ValueError:
		return False
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc

import regex as re
import difflib
#from API1912 import contrast
from API19_1_2 import *
from mondic import *
#end 

#udf

#end 
