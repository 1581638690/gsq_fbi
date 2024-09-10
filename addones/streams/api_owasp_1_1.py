#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp_1_1.xlk
#datetime: 2024-08-30T16:10:58.474114
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

#LastModifyDate:　2024-01-23T10:10:10    Author:   rzc

#LastModifyDate:　2024-01-06T21:12:27    Author:   superFBI

#LastModifyDate:　2024-01-06T16:15:52    Author:   superFBI

#LastModifyDate:　2024-01-05T10:54:29.420614    Author:   superFBI

#LastModifyDate:　2023-12-28T09:23:51.807691    Author:   superFBI

#LastModifyDate:　2023-12-27T15:19:04.324486    Author:   superFBI

#LastModifyDate:　2023-12-27T10:16:24.962013    Author:   superFBI

#LastModifyDate:　2023-12-26T14:54:07.417491    Author:   superFBI

#LastModifyDate:　2023-12-26T14:40:19.764035    Author:   superFBI

#LastModifyDate:　2023-12-26T14:38:34.525008    Author:   superFBI

#LastModifyDate:　2023-12-12T16:47:49.332904    Author:   superFBI

#xlink脚本

#file: api_owasp_1_1.xlk

#name: 

#描述： 

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with api_owasp_1_1

#停止

#a = @udf FBI.x_finder3_stop with api_owasp_1_1

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:api_owasp_1_1,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::api_owasp_1_1

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "OWASP_API19-1-1处理进程"
	stream["meta_desc"] = "进行参数可遍历操作"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"]= {"unix_udp":"/tmp/owp_1_1"}
	stream["source"] = {"shm_name":"httpub","count":8}
	#stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_785s"]={"times":785,"fun":"print785"}
	#stream["scw"]["scw_e1"] = {"count":10,"fun":"flow"}
	stream["stw"]["stw_flow"]={"times":20,"fun":"flow"}
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	owasp = load_ssdb_kv("qh_owasp")
	owasp_list=owasp["setting"]["API19-1"]["API19-1-1"]
	stream["token_rule"] = ""
	for i in owasp_list:
		stream["token_rule"]+=i.get("bianli")+"|"
	#stream["token_rule"]=stream["token_rule"].rstrip("|")
	try:
		stream["parm_iter"]=remove_file("/dev/shm/parm_iter.pkl","/data/xlink","parm_iter.pkl")
	except:
		stream["parm_iter"]={}
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	data_type=o.get("data_type")
	#if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
	total_info=o.get("total_info")
	k = iso_to_timestamp(o["timestamp"])
	#printf("total_info",total_info)
	message=[]
	#response_body=o.get("http_response_body","")
	#if total_info and "响应体" in total_info and is_json_string(response_body):
	if total_info:
		#printf("total_info",total_info)
		for pos,info in total_info.items():
			if info!={} and len(info)>=1:
				message.append(pos)
		#printf("message",message)
		status=o.get("http").get("status","")
		parameter=o.get("parameter","")
		if message and parameter != "" and status ==200:
			token_rule=stream["token_rule"].rstrip("|")
			#printf("token_rule",token_rule)
			url=o.get("url_c","")
			length=o.get("http").get('length',0)
			stream["parm_iter"],length,zj=parameter_iterable(url,stream["parm_iter"],length,parameter,token_rule)
			#printf("parm_iter",parm_iter)
			#printf("s1",s1)
			#stream["parm_iter"]=parm_iter
			printf("zj",zj)
			if zj:
			#存在数据则进行存储
				#end = {"参数可遍历": "", "类似参数": {},"证据样例":{}}
				end = {"参数可遍历": "", "证据样例":{}}
				for k, v in zj.items():
					v = list(set(v))
					if len(v) > 1:
						end["参数可遍历"] = end["参数可遍历"] + k + ","
						#end["类似参数"][k] = v
						#end["证据样例"][k]=list(set(zj[k]))
						end["证据样例"][k]=v
				if end["参数可遍历"]:
					end["参数可遍历"]=end["参数可遍历"].rstrip(",")
					#end["敏感信息"]=total_info
					end = ujson.dumps(end, ensure_ascii=False).replace("\\","")
					e=clone_event(o)
					e["length"]=length
					e["state"] = "待确认"
					e["type"] = "API19-1-1"
					e["more"]=end
					#to_table(e)
					#push_scw("scw_e1",e)
					push_stw("stw_flow",k,e)
					stream["count"]+=1
				
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	owasp = load_ssdb_kv("qh_owasp")
	owasp_list=owasp["setting"]["API19-1"]["API19-1-1"]
	stream["token_rule"] = ""
	for i in owasp_list:
		stream["token_rule"]+=i.get("bianli")+"|"
#end 

#系统定时函数，st为时间戳 
def print785(st):
	
	with open("/data/xlink/parm_iter.pkl",'wb') as fp:
		parm_iter=copy.copy(stream["parm_iter"])
		pickle.dump(parm_iter,fp)
#end 

#克隆一个新事件,创建一个新的变量，并返回

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	e = {
		"api": o.get('url_c', ''),
		"app": o.get('app', ''),
		"method": o.get("http").get("http_method", ""),
		"dest_ip": o.get("dest_ip"),
		"dest_port": o.get("dest_port"),
		# "url": o.get("url", ""),
		"first_time": str(iso_to_datetime(o["timestamp"])),
		"last_time": str(iso_to_datetime(o["timestamp"]))
	}
	return e
#end 

#窗口函数，使用FBI语句块 
def flow (k,df):
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
		errors.append('[api_owasp_1_1.xlk]执行第[152]原语 API19 = distinct df by (a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'cc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,type,id,state states,length lengths from api19_risk where type = 'API19-1-1'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[154]原语 cc = load db by mysql1 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'API19', 'Action': 'join', 'join': 'API19,cc', 'by': '[api,type],[api,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[156]原语 API19 = join API19,cc by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[157]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[158]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API191', 'Action': 'filter', 'filter': 'API19', 'by': "states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[159]原语 API191 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API191', 'Action': 'loc', 'loc': 'API191', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[160]原语 API191 = loc API191 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API191', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[161]原语 @udf API191 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API192', 'Action': 'filter', 'filter': 'API19', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[162]原语 API192 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API193', 'Action': 'loc', 'loc': 'API192', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[163]原语 API193 = loc API192 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API193', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[165]原语 @udf API193 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API194', 'Action': 'loc', 'loc': 'API192', 'by': 'last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[166]原语 API194 = loc API192 by la... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API194', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[167]原语 @udf API194 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[168]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[169]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[170]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[171]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[172]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'cc'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[173]原语 drop cc... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[174]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[175]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义批处理函数，使用FBI语句块 
def save(k='1',df=pd.DataFrame()):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'API19', 'Action': 'distinct', 'distinct': 'API192', 'by': 'api,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[177]原语 API19 = distinct API192 b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'cc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,type,id,state states,length lengths from api19_risk where type = 'API19-1-1'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[179]原语 cc = load db by mysql1 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'API19', 'Action': 'join', 'join': 'API19,cc', 'by': '[api,type],[api,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[181]原语 API19 = join API19,cc by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[182]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'API19', 'Action': '@udf', '@udf': 'API19', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[183]原语 API19 = @udf API19 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API191', 'Action': 'filter', 'filter': 'API19', 'by': "states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[184]原语 API191 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API191', 'Action': 'loc', 'loc': 'API191', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[185]原语 API191 = loc API191 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API191', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[186]原语 @udf API191 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'API192', 'Action': 'filter', 'filter': 'API19', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[187]原语 API192 = filter API19 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API193', 'Action': 'loc', 'loc': 'API192', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[188]原语 API193 = loc API192 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API193', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[190]原语 @udf API193 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'API194', 'Action': 'loc', 'loc': 'API192', 'by': 'last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[191]原语 API194 = loc API192 by la... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'API194', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[192]原语 @udf API194 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API19'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[193]原语 drop API19... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API191'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[194]原语 drop API191... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API192'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[195]原语 drop API192... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API193'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[196]原语 drop API193... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'API194'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[197]原语 drop API194... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'cc'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[198]原语 drop cc... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_1_1.xlk]执行第[199]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
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
import base64
from API19_1_2 import *
#end 

#udf

#end 
