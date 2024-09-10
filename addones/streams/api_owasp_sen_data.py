#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp_sen_data.xlk
#datetime: 2024-08-30T16:10:58.377496
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

#LastModifyDate:　2024-01-09T11:37:20    Author:   qh

#LastModifyDate:　2024-01-09T10:25:43    Author:   rzc

#LastModifyDate:　2024-01-08T09:34:20    Author:   superFBI

#LastModifyDate:　2024-01-06T16:20:05    Author:   superFBI

#LastModifyDate:　2024-01-06T15:43:17    Author:   superFBI

#LastModifyDate:　2024-01-06T13:58:03    Author:   superFBI

#LastModifyDate:　2024-01-05T11:09:39.315295    Author:   superFBI

#LastModifyDate:　2023-12-28T09:24:55.743731    Author:   superFBI

#LastModifyDate:　2023-12-27T15:19:25.760687    Author:   superFBI

#LastModifyDate:　2023-12-27T10:17:14.271774    Author:   superFBI

#LastModifyDate:　2023-12-20T11:26:46.133609    Author:   superFBI

#xlink脚本

#file: api_owasp_sen_data.xlk

#name: 

#描述： 

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "OWASP_数据流动敏感数据"
	stream["meta_desc"] = "处理弱点和数据流动中有关敏感数据的数据和api19-3，api19-7-5，api19-8"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["link"] = a["kfk"]["origin"]["link"]
	stream["topic"] = a["kfk"]["origin"]["topic"]
	stream["reset"] = a["kfk"]["origin"]["reset"]
	#stream["source"]= {"link":"127.0.0.1:16379","topic":"api_visit","redis":"pubsub"}
	#stream["source"]= {"link":stream["link"],"topic":stream["topic"],"group":"API19SEN","start-0":stream["reset"]}
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/owp_sen_data"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["redis"]={"host":stream["redis_link"],"port":"6382"}
	#kfk
	#stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
	stream["ipdb"] = IPIPDatabase( '/opt/openfbi/workspace/ipdb.datx')
	#自定义的统计变量
	stream["count"] = 0
	stream["count_10"] = 0
	s = load_ssdb_kv("qh_owasp")
	stream["API19_3"] = s["setting"]["API19-3"]
	stream["API19_8"] = s["setting"]["API19-8"]
	#自定义的统计变量
	b = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_sen" in b:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	if "api_sent" in b:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
	if "api_senm" in b:
		stream["sends3"] = 1
	else:
		stream["sends3"] = 0
	set_param("l",stream["link"])
	if "api_model" in b:
		set_param("m","1")
	else:
		set_param("m","0")
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["stw"]["stw_flow"]={"times":10,"fun":"flow"}
	stream["stw"]["stw_flow2"]={"times":90,"fun":"flow2"}
	stream["stw"]["stw_flow3"]={"times":100,"fun":"flow3"}
	#stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	c = load_ssdb_kv("model_config")
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#hp = ujson.loads(o["httpjson"])
	#http = hp.get("http")
	#debug_on(1)
	#return o
	data_type=o.get("data_type")
	if data_type == "XML" or data_type == "数据文件" or data_type == "JSON" or data_type == "动态脚本":
		app = o.get("app")
		api = o.get("url_c")
		http=o.get("http")
		k = iso_to_timestamp(o["timestamp"])
		timestamp = iso_to_datetime(o["timestamp"])
		parameter = o.get("parameter")
		srcip=o.get("src_ip")
		#Delete 注释 by rzc on 2023-04-26 17:32:50
		if http:
			request_headers = http.get('request_headers', '')
		else:
			request_headers=""
		request_body=o.get("http_request_body","")
		response_body=o.get("http_response_body","")
		ID=o.get("id")
		api_8 = api19_8(str(timestamp),parameter,request_headers,request_body,stream["API19_8"], stream["API19_3"])
		total_info=o.get("total_info")
		datas,lk,length,msg=sen_data(srcip,str(timestamp),total_info,request_body,response_body,ID)
		if api_8:
			for data in api_8:
				e = clone_event(o)
				e["app"] = app
				e["api"] = api
				e["type"] = data["type"]
				e["more"] = ujson.dumps(data["more"])
				push_stw("stw_flow",k,e)
				#to_redis("owasp_data",o)
		# 敏感数据访问数据波动过大
		if length >0:
			e = clone_event(o)
			e["app"] =  app
			e["api"] =  api
			e["type"] = "API19-3-4"
			e["num"] = length
			e["time"] = str(timestamp)
			push_stw("stw_flow2",k,e)
			if o.get("url_c") in stream["monitor_url"] or stream["all_combo"]:
				#下面模型用
				e['srcip'] = srcip
				e['srcport'] = o.get('src_port')
				e['url_a'] = o.get('url')
				e['account'] = o.get('account')
				e['real_ip'] = o.get('realip')
				e["id"] = xlink_uuid(1)
				e['proof'] = o.get('id')
				push_stw("stw_flow3",k,e)
			#to_redis("owasp_data",o)
		# 则判断是否是内网访问
		ip_is = ip_lookup(srcip)
		if ip_is and datas:
			#printf("message",message)
			e = clone_event(o)
			e["app"] =  app
			e["api"] =  api
			e["type"] = "API19-7-5"
			e["more"] = ujson.dumps(datas,ensure_ascii=False)
			push_stw("stw_flow",k,e)
			#to_redis("owasp_data",o)
		#数据量过大
		if stream["API19_3"]["API19-3-1"] <= length and datas:
			e = clone_event(o)
			e["app"] =  app
			e["api"] =  api
			e["type"] = "API19-3-1"
			e["more"] =  ujson.dumps(datas,ensure_ascii=False)
			push_stw("stw_flow",k,e)
			#to_redis("owasp_data",o)
		#数据类型过多
		if stream["API19_3"]["API19-3-2"] <= lk and datas:
			e = clone_event(o)
			e["app"] =  app
			e["api"] =  api
			e["type"] = "API19-3-2"
			datas.pop('敏感数据', None)
			e["more"] = ujson.dumps(datas,ensure_ascii=False)
			push_stw("stw_flow",k,e)
			#to_redis("owasp_data",o)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	c = load_ssdb_kv("model_config")
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	s = load_ssdb_kv("qh_owasp")
	stream["API19_3"] = s["setting"]["API19-3"]
	stream["API19_8"] = s["setting"]["API19-8"]
	b = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_sen" in b:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	if "api_sent" in b:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
	if "api_senm" in b:
		stream["sends3"] = 1
	else:
		stream["sends3"] = 0
	set_param("l",stream["link"])
	if "api_model" in b:
		set_param("m","1")
	else:
		set_param("m","0")
	#push_arrays_to_df(table,"flow")
	#store_ckh(pools["ckh"],"flow")
	#save()
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
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_owasp as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[199]原语 a = load ssdb by ssdb0 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["setting"]["API19-3"]["API19-3-4"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[200]原语 b = jaas a by a["setting"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'flow2', 'Action': 'group', 'group': 'df', 'by': 'api', 'agg': 'num:median'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[201]原语 flow2 = group df by api a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'flow2', 'Action': '@udf', '@udf': 'flow2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[202]原语 flow2 = @udf flow2 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'flow2', 'Action': 'join', 'join': 'df,flow2', 'by': 'api,api'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[203]原语 flow2 = join df,flow2 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'flow2', 'Action': 'add', 'add': 'num_mad', 'by': 'abs(flow2["num"]-flow2["num_median"])/flow2["num_median"]'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[204]原语 flow2 = add num_mad by ab... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'flow2', 'Action': 'loc', 'loc': 'flow2', 'by': 'api,num_mad'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[205]原语 flow2 = loc flow2 by api,... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'flow2', 'Action': 'filter', 'filter': 'flow2', 'by': 'num_mad > $b'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[209]原语 flow2 = filter flow2 by n... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'flow2', 'Action': 'join', 'join': 'flow2,df', 'by': 'api,api'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[210]原语 flow2 = join flow2,df by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'flow2', 'Action': 'distinct', 'distinct': 'flow2', 'by': 'api'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[211]原语 flow2 = distinct flow2 by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'flow2.num_mad', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[212]原语 alter flow2.num_mad as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'flow2', 'Action': 'add', 'add': 'more', 'with': '\'{"敏感数据平均极差过大":"超过限制","波动平均极差为":"\' + flow2["num_mad"] + \'", "访问时间":"\' + flow2["time"] + \'"}\''}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[213]原语 flow2 = add more with ("{... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'flow2', 'Action': 'loc', 'loc': 'flow2', 'drop': 'num,time,num_mad,url_a,account,real_ip,id,srcport,srcip,uid'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[214]原语 flow2 = loc flow2 drop nu... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'flow2', 'Action': '@udf', '@udf': 'flow2', 'by': 'udf0.df_set', 'with': "state='待确认'"}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[215]原语 flow2 = @udf flow2 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select api,type,id,state states,length lengths from api19_risk where type = 'API19-3-4'"}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[216]原语 a = load db by mysql1 wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'flow2', 'Action': 'join', 'join': 'flow2,a', 'by': '[api,type],[api,type]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[217]原语 flow2 = join flow2,a by [... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'flow2', 'Action': '@udf', '@udf': 'flow2', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[218]原语 flow2 = @udf flow2 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'flow2', 'Action': '@udf', '@udf': 'flow2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[219]原语 flow2 = @udf flow2 by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'flow21', 'Action': 'filter', 'filter': 'flow2', 'by': "index == 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[220]原语 flow21 = filter flow2 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'flow21', 'Action': 'loc', 'loc': 'flow21', 'drop': 'states,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[221]原语 flow21 = loc flow21 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'flow21', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[222]原语 @udf flow21 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'flow22', 'Action': 'filter', 'filter': 'flow2', 'by': "index != 0 and states !='忽略'"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[223]原语 flow22 = filter flow2 by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.length', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[224]原语 alter API192.length as in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'API192.lengths', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[225]原语 alter API192.lengths as i... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'flow22', 'Action': '@udf', '@udf': 'flow22', 'by': 'udf0.df_row_lambda', 'with': 'x: x["length"] if x["length"] > x["lengths"] else x["lengths"]'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[226]原语 flow22 = @udf flow22 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'flow22', 'Action': 'loc', 'loc': 'flow22', 'drop': 'first_time,state,states,length,lengths'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[227]原语 flow22 = loc flow22 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= rename', 'Ta': 'flow22', 'Action': 'rename', 'rename': 'flow22', 'as': "'lambda1':'length'"}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[228]原语 flow22= rename flow22 as ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': '@udf', '@udf': 'flow22', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_risk,more'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[230]原语 @udf flow22 by CRUD.save_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[233]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'flow2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[234]原语 drop flow2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'flow21'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[235]原语 drop flow21... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'flow22'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[236]原语 drop flow22... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[237]原语 drop df... 出错,原因:'+e.__str__())

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
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'src_model', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'srcip_model_xlk'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[239]原语 src_model = load ssdb by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'model_config', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'model_config as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[240]原语 model_config = load ssdb ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'on', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["switch"]["model3"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[241]原语 on = jaas model_config by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"$on" == "true"', 'with': '""\nmodel3 = loc df drop (first_time,state,method,length,type,last_time,num_mad,more)\nrename model3 as ("time":"timestamp","dest_ip":"dstip","dest_port":"dstport","api":"url")\nmodel3 = join src_model,model3 by srcip,srcip\n"', 'else': '"\nmodel3 = @udf udf0.new_df\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=242
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[242]原语 if "$on" == "true" with "... 出错,原因:'+e.__str__())

#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'monitor_url', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'monitor_url_xlk'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[249]原语 monitor_url = load ssdb b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'model3', 'Action': 'join', 'join': 'monitor_url,model3', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[250]原语 model3 = join monitor_url... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'wl', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model3"]["whitelist"]'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[251]原语 wl = jaas model_config by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wl', 'Action': '@udf', '@udf': 'wl', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[252]原语 wl = @udf wl by FBI.json2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wl', 'Action': '@udf', '@udf': 'wl', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[253]原语 wl = @udf wl by udf0.df_r... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wls', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[254]原语 wls = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'wl', 'with': 'idx=$1', 'run': '""\nwl1 = filter wl by (index == @idx)\nwl1 = @udf wl1 by model.dropem\nwl1 = loc wl1 drop index\nwl2 = @udf wl1,model3 by model.join2\nwls = union (wls,wl2)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[255]原语 foreach wl run "wl1 = fil... 出错,原因:'+e.__str__())

#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': 'wls.index.size == 0', 'with': '""\nwls = limit model3 by 500000\n""'}
	try:
		ptree['lineno']=262
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[262]原语 if wls.index.size == 0 wi... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'wls', 'Action': 'distinct', 'distinct': 'wls', 'by': 'id'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[265]原语 wls = distinct wls by id... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'sens_mean', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sens_mean'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[266]原语 sens_mean = load ssdb by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model3"]["mean"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[267]原语 b = jaas model_config by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'sens_mean', 'Action': 'add', 'add': 'mean', 'with': 'sens_mean["mean"]*$b'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[268]原语 sens_mean = add mean with... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'model3', 'Action': 'join', 'join': 'wls,sens_mean', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[269]原语 model3 = join wls,sens_me... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'model3', 'Action': '@udf', '@udf': 'model3', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[270]原语 model3 = @udf model3 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'model3', 'Action': 'filter', 'filter': 'model3', 'by': 'num > mean'}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[271]原语 model3 = filter model3 by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'model3.num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[272]原语 alter model3.num as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'model3.mean', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[273]原语 alter model3.mean as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'model3', 'Action': 'add', 'add': 'message', 'with': '\'终端“\' + model3["srcip"] + \'访问接口\' + model3["url"] + \'返回数据波动超过限制，波动值：\' + model3["num"] + \'，月平均值：\' + model3["mean"]'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[274]原语 model3 = add message with... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'b', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$b,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[275]原语 b = @sdf sys_str with ($b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[277]原语 proofs = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'model3', 'Action': 'loc', 'loc': 'model3', 'by': 'srcip,url,num,mean,dstip,dstport,app,url,timestamp,srcport,url_a,account,real_ip,id,proof,mean,message'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[278]原语 model3 = loc model3 by (s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'model3', 'with': 'url=$2,srcip=$1,num=$3,mean=$4', 'run': '""\nf = filter model3 by (srcip == "@srcip" and url == "@url")\nc = loc f by timestamp,proof\nrename c as ("proof":"suid")\nd = @udf c by model.proof3 with @srcip,@url,@num,@mean,$b\nproofs = union (proofs,d)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[279]原语 foreach model3 run "f = f... 出错,原因:'+e.__str__())

#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'model3', 'Action': 'loc', 'loc': 'model3', 'drop': 'mean,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[286]原语 model3 = loc model3 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'proofs', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[287]原语 proofs = @udf proofs by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proofs', 'Action': 'loc', 'loc': 'proofs', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[288]原语 proofs = loc proofs drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'model3', 'Action': '@udf', '@udf': 'model3', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[289]原语 model3 = @udf model3 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'model3', 'Action': '@udf', '@udf': 'model3', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[290]原语 model3 = @udf model3 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'model3', 'Action': 'loc', 'loc': 'model3', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[291]原语 model3 = loc model3 drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'model3', 'Action': 'join', 'join': 'model3,proofs', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[292]原语 model3 = join model3,proo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'model3.timestamp', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[293]原语 alter model3.timestamp as... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'model3', 'Action': 'add', 'add': 'type', 'with': '3'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[294]原语 model3 = add type with (3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'model3', 'Action': 'add', 'add': 'level', 'with': '2'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[295]原语 model3 = add level with (... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'model3', 'Action': 'add', 'add': 'desc', 'with': '"超出限定值视为波动过大，此访问行为判定为有风险"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[296]原语 model3 = add desc with ("... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'model3', 'to': 'ckh', 'by': 'ckh', 'with': 'api_model'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[297]原语 store model3 to ckh by ck... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"@mm" == "1"', 'with': '""\ndefine kfka as "@l"\nk = @udf KFK.df_link with kfka\nalter model3.timestamp as str\nmodel3 = add event_type by ("model")\na = @udf model3 by KFK.fast_store with kfka,api_send\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=299
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[299]原语 if "@mm" == "1" with "def... 出错,原因:'+e.__str__())

#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'model3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[306]原语 drop model3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'model33'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[307]原语 drop model33... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'proofs'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[308]原语 drop proofs... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'wl'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[309]原语 drop wl... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'wl1'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[310]原语 drop wl1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'wl2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[311]原语 drop wl2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'wls'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[312]原语 drop wls... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'sens_mean'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[313]原语 drop sens_mean... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'src_model'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[314]原语 drop src_model... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'b'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[315]原语 drop b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'a'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[316]原语 drop a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'monitor_url'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[317]原语 drop monitor_url... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[318]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[319]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
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
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'size', 'Action': 'eval', 'eval': 'df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[321]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\n# 去重\n#df.more=str more by replace("\\\\","")\nAPI19 = distinct df by (api,type)\nAPI19 = @udf API19 by udf0.df_set with (state=\'待确认\')\na = load db by mysql1 with select api,type,id,state states,length lengths from api19_risk where type = \'API19-3-1\' or type = \'API19-3-2\' or type = \'API19-3-3\' or type = \'API19-7-5\' or type like \'API19-8%%\'\nAPI19 = join API19,a by [api,type],[api,type] with left\n#获取只对id将nan值 存为0\n\nAPI19 = @udf API19 by udf0.df_fillna with 0\n#API19.id=lambda id by x:0 if not x else x\nAPI19 = @udf API19 by udf0.df_set_index with id\nAPI191 = filter API19 by index == 0 and states !=\'忽略\'\nAPI191 = loc API191 drop states,lengths\n###\n@udf API191 by CRUD.save_table with (mysql1,api19_risk)\nAPI192 = filter API19 by index != 0 and states !=\'忽略\'\nalter API192.length as int\nalter API192.lengths as int\nAPI192 = @udf API192 by udf0.df_row_lambda with x: x["length"] if x["length"] > x["lengths"] else x["lengths"]\nAPI193 = loc API192 drop first_time,state,states,length,lengths\nAPI193= rename API193 as (\'lambda1\':\'length\')\n#API192.request_body=lambda request_body by x:x if x!=0 else \'{}\'\n#API192.response_body=lambda response_body by x:x if x!=0 else \'{}\'\n# 保存\n@udf API193 by CRUD.save_table with (mysql1,api19_risk,more)\nAPI194 = loc API192 by last_time\n@udf API194 by CRUD.save_table with (mysql1,api19_risk)\ndrop df\ndrop API19\ndrop API191\ndrop API192\ndrop API193\ndrop API194\ndrop a\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=322
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[322]原语 if $size > 0 with "# 去重#d... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp_sen_data.xlk]执行第[358]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def sen_data(srcip,time,total_info,request_body,response_body,ID):
	datas = {}
	infos = {}
	keys = {}
	message=[]
	#判断是响应体大于还是请求体大于
	for pos,info in total_info.items():
		if len(info)>=3:
			message.append(pos)
			for key,value in info.items():
				if value:
				#if value and value not in err_name:
					if infos.get(key):
						infos[key].extend(value)
					else:
						infos[key] = value
					if keys.get(key):
						keys[key] += len(value)
					else:
						keys[key] = len(value)
	msg={}
	for i in message:
		if i=="请求体":
			msg["请求体"]=request_body
		elif i=="响应体":
			msg["响应体"]=response_body
	#Delete 注释 by superFBI on 2023-05-10 14:44:34
#if msg:

#		msg=ujson.dumps(msg,ensure_ascii=False).replace("\\","")

#	else:

		#msg=""
	if keys and infos:
		#datas["原始ID"]=ID
		datas["源端IP"] = srcip
		datas["访问时间"] = time
		datas["敏感数据类型及数量"] = keys
		datas["敏感数据"] = infos
		datas["证据样例"]=msg
		
	lk = 0
	li = 0
	for a in keys.values():
		li += a
	for a in infos.values():
		lk += 1
	return datas,lk,li,msg
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	e = {
		"first_time": str(iso_to_datetime(o["timestamp"])),
		"last_time": str(iso_to_datetime(o["timestamp"])),
		"dest_ip": o.get("dest_ip"),
		"dest_port": o.get("dest_port"),
		"method": o.get("http").get("http_method", ""),
		"state": "待确认",
		"length": o.get("http").get('length', 0)
	}
	return e
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ip_lookup(ip):
	try:
		ip_is = False
		result = stream["ipdb"].lookup(ip).split('	')[0]
		if result not in ["局域网","本地链路","共享地址","本机地址","保留地址"]:
			ip_is = True
	except:
		ip_is = False
	return ip_is
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import base64
from stream_official_1119_sw import *
from un_file import *
from copy import deepcopy
from pyipip import IPIPDatabase
#end 

#udf

#end 
