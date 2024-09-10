#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: http_datafilter.xlk
#datetime: 2024-08-30T16:10:58.521581
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

#LastModifyDate:　2024-01-15T15:35:36    Author:   rzc

#LastModifyDate:　2024-01-15T09:48:58    Author:   rzc

#LastModifyDate:　2024-01-11T13:51:00    Author:   rzc

#LastModifyDate:　2024-01-09T10:29:35    Author:   rzc

#LastModifyDate:　2024-01-06T15:52:03    Author:   superFBI

#LastModifyDate:　2024-01-06T15:40:42    Author:   superFBI

#LastModifyDate:　2024-01-06T14:02:32    Author:   superFBI

#LastModifyDate:　2023-12-28T09:50:17.712652    Author:   superFBI

#LastModifyDate:　2023-12-27T09:50:32.503616    Author:   superFBI

#LastModifyDate:　2023-12-20T11:28:16.258947    Author:   superFBI

#LastModifyDate:　2023-08-08T18:38:32.937856    Author:   pjb

#xlink脚本

#file: http_datafilter1.xlk

#name: 对http进行敏感数据识别

#描述： 除资源文件,CSS,JS,未知以外的进行敏感数据获取

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with http_datafilter1

#停止

#a = @udf FBI.x_finder3_stop with http_datafilter1

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:http_datafilter1,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::http_datafilter1

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "对http进行敏感数据识别"
	stream["meta_desc"] = "从senfilters主题中消费数据，进行敏感数据识别"
	#a = load_ssdb_kv("setting")
	#stream["link"] = a["kfk"]["visit"]["link"]
	#stream["topic"] = a["kfk"]["visit"]["topic"]
	#stream["reset"] = a["kfk"]["visit"]["reset"]
	#stream["source"]= {"link":"127.0.0.1:16379","topic":"http_datafilter1","redis":"list"}
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["redis_link"]+":6381","topic":"sen_count","redis":"list"}
	stream["source"]= {"unix_udp":"/tmp/sen_count"}
	#stream["redis"]={"host":"127.0.0.1","port":"16379"}
	#stream["kfk"]={"link":stream["link"],"topic":"api_send","key":""}
	stream["redis_pub_count"]=3
	#自定义的统计变量
	stream["count"] = 0
	try:
		stream["pre_cfg1"]=load_ssdb_kv("sensitive")["data"]
		stream["pre_cfg"]=[]
		for data in stream["pre_cfg1"]:
			if data["off"]==1:
				stream["pre_cfg"].append(data)
	except:
		stream["pre_cfg"]=load_ssdb_kv("sensitive")["data"]
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_15"]={"times":900,"fun":"send15"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	stream["st"]["st_1800s"]={"times":1800,"fun":"fpsearch"}
	al=load_ssdb_kv("alarm")["setting"]
	if "sensitive_data_alarm" in al:
		stream["sensitive_alarm_index"]=al.get("sensitive_data_alarm").get("names")
	else:
		stream["sensitive_alarm_index"]=[]
	
	stream["sensitive_alarm"] = load_ssdb_kv("dd:reqs_label")["data"]
	pool["sensitive_data_alarm"] = []
	pool["sensitive_data"] = []
	pool["sen_count"] = []
	pool["api_model"] = []
	b = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_senm" in b:
		stream["sends3"] = 1
	else:
		stream["sends3"] = 0
	if "api_model" in b:
		stream["sends4"] = 1
	else:
		stream["sends4"] = 0
	#stream["PreEvent"] = 4
	if "areas" not in stream:
		with open("/opt/openfbi/pylibs/areas.csv","r",encoding="utf-8") as fp:
			content=fp.readlines()
		areas_list=[i.strip() for i in content if len(i.strip())>1]
		stream["areas"]=areas_list
	#读取常见错误的名字信息
	if "wrong_name" not in stream:
		with open("/opt/openfbi/pylibs/wrong_name.csv","r",encoding="utf-8")as fp:
			name_con=fp.readlines()
		name_list=[i.strip() for i in name_con if len(i.strip())>1]
		stream["wrong_name"]=name_list
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	srcip_model = load_ssdb_kv("srcip_model_xlk")["data"]
	stream["srcip_model"] = []
	for item in srcip_model:
		stream["srcip_model"].append(item[0])
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	c = load_ssdb_kv("model_config")
	stream["fpcount"] = c["setting"]["model101"]["count"]
	stream["model101_on"] = c["setting"]["switch"]["model101"]
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
	m101 = c["setting"]["model101"]["whitelist"]
	for i in m101:
		for k in list(i.keys()):
			if not i[k]:
				del i[k]
	stream["model101_conf"] = m101
	stream["fpfirsttime"] = ""
	stream["fpmessage"] = {}
	stream["fps"] = {}
	stream["redis"]={"host":stream["redis_link"],"port":"6382"}
	#数据开关
	#stream["sen_off"] = load_ssdb_kv("protocol_data")["function"]["event"]["sensitive_data"]
#end 

#事件处理函数
def Events(o,topic=''):
	#存储监控信息
	#o["timestamp"]=iso_to_datetime(o["timestamp"])
	#o["timestamp"]=o["timestamp"]
	msg_total=o["msg_total"]
	sen_type_count =o["sen_type_count"]
	o["msg_total"]=ujson.dumps(o["msg_total"],ensure_ascii=False)
	o["sen_type_count"]=ujson.dumps(o["sen_type_count"],ensure_ascii=False)
	o["request_count"]=ujson.dumps(o["request_count"],ensure_ascii=False)
	o["response_count"]=ujson.dumps(o["response_count"],ensure_ascii=False)
	to_pool("sen_count",o)
	if stream["sends3"]:
		s = deepcopy(o)
		s["event_type"] = "sensitive_m"
		#to_kfk(s)
		s["timestamp"] = str(s["timestamp"])
		to_json_file("/data/syslog_file/eve",s)
	if stream["model101_on"]:
		stc = sen_type_count.get("响应体")
		if stc:
			nsrsbh = stc.get("纳税人识别号或社会统一信用代码")
			fpdm = stc.get("发票代码")
			nsrmc = stc.get("纳税人名称或公司名称")
			if nsrsbh and fpdm and nsrmc:
				srcip = o.get("src_ip")
				srcall = 1
				if srcip in stream["srcip_model"] or srcall:
					url = o.get("url")
					if stream["all_combo"] or url in stream["monitor_url"]:
						http_api = {}
						http_api["url"] = o.get("url")
						http_api["srcip"] = o.get("src_ip")
						http_api["srcport"] = o.get("srcport",0)
						http_api["dstip"] = o.get("dest_ip")
						http_api["dstport"] = o.get("dest_port",0)
						ps = 0
						for i in stream["model101_conf"]:
							a = 0
							for k in i:
								if http_api[k] == i[k]:
									a = a + 1
							if len(i) == a:
								ps = 1
								break
						if not stream["model101_conf"] or ps:
							min1 = []
							min1.append(nsrsbh)
							min1.append(fpdm)
							min1.append(nsrmc)
							min1 = min(min1)
							if min1 > stream["fpcount"]:
								if o.get("real_ip"):
									srcs = o.get("real_ip")
								else:
									srcs = o.get("src_ip")
								http_api["timestamp"] = o["timestamp"]
								http_api["url_a"] = o.get("url_a")
								http_api["account"] = o.get("account")
								http_api["real_ip"] = o.get("real_ip","")
								http_api["app"] = o.get("app")
								http_api["id"] = xlink_uuid(0)
								http_api["type"] = 101
								http_api["level"] = 2
								http_api["proof"] = o.get("id")
								http_api["desc"] = "终端通过接口获取发票信息"
								http_api["message"] = "终端“" + srcs + "”在接口" + http_api["url"] + "中获取了发票" + str(min1) + "张"
								proofs = {}
								proofs["判定标准"] = "发票信息获取行为:终端的接口访问行为，返回体中的内容至少同时包含纳税人识别号、发票代码和公司名称三种类型敏感信息的，定义为发票信息获取行为。取三种敏感类型中数量最少的作为发票数量，在设定时间周期内，获取超过设定阈值数量的发票时发出告警"
								proofs["接口"] = http_api["url"]
								proofs["终端"] = srcs
								proofs["单次获取阈值"] = stream["fpcount"]
								proofs["本次获取数量"] = min1
								proofs["纳税人识别号或社会统一信用代码"] = o.get("msg_total").get("响应体").get("纳税人识别号或社会统一信用代码")
								proofs["纳税人名称或公司名称"] = o.get("msg_total").get("响应体").get("纳税人名称或公司名称")
								proofs["发票代码"] = o.get("msg_total").get("响应体").get("发票代码")
								proofs["结果"] = "终端通过接口获取发票信息"
								proofs["证据"] = {}
								proofs["证据"]["时间"] = "HTTP协议ID"
								proofs["证据"][str(o.get("timestamp"))] = o.get("id")
								http_api["proofs"] = proofs
								to_pool("api_model",http_api)
								if stream["sends4"]:
									ssss = deepcopy(http_api)
									ssss["event_type"] = "model"
									#to_kfk(ssss)
									ssss["timestamp"] = str(ssss["timestamp"])
									to_json_file("/data/syslog_file/eve",ssss)
								if stream["fpfirsttime"] == "":
									stream["fpfirsttime"] = str(o.get("timestamp"))
								srcurl = srcs + "|" + http_api["url"]
								if srcurl in stream["fps"]:
									stream["fps"][srcurl] = stream["fps"][srcurl] + min1
								else:
									stream["fps"][srcurl] = min1
								sufp = deepcopy(http_api)
								del sufp["proofs"]
								stream["fpmessage"][srcurl] = sufp
#end 

#系统定时函数，st为时间戳 
def print10(st):
	#printf("总数",stream["count"])
	store_ckh(pool["sen_count"],"sen_http_count")
	store_ckh(pool["api_model"],"api_model")
	
#end 

#系统定时函数，st为时间戳 
def send60(st):
	#stream["sen_off"] = load_ssdb_kv("protocol_data")["function"]["event"]["sensitive_data"]
	try:
		stream["pre_cfg1"]=load_ssdb_kv("sensitive")["data"]
		stream["pre_cfg"]=[]
		for data in stream["pre_cfg1"]:
			if data["off"]==1:
				stream["pre_cfg"].append(data)
	except:
		stream["pre_cfg"]=load_ssdb_kv("sensitive")["data"]
	al=load_ssdb_kv("alarm")["setting"]
	if "sensitive_data_alarm" in al:
		stream["sensitive_alarm_index"]=al.get("sensitive_data_alarm").get("names")
	else:
		stream["sensitive_alarm_index"]=[]
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_senm" in a:
		stream["sends3"] = 1
	else:
		stream["sends3"] = 0
	if "api_model" in a:
		stream["sends4"] = 1
	else:
		stream["sends4"] = 0
	c = load_ssdb_kv("model_config")
	stream["fpcount"] = c["setting"]["model101"]["count"]
	stream["model101_on"] = c["setting"]["switch"]["model101"]
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
	m101 = c["setting"]["model1"]["whitelist"]
	for i in m101:
		for k in list(i.keys()):
			if not i[k]:
				del i[k]
	stream["model101_conf"] = m101
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	b = []
	for item in s:
		b.append(item[0])
	stream["monitor_url"] = b
	srcip_model = load_ssdb_kv("srcip_model_xlk")["data"]
	src = []
	for item in srcip_model:
		src.append(item[0])
	stream["srcip_model"] = src
#end 

#系统定时函数，st为时间戳 
def send15(st):
	if "areas" not in stream:
		with open("/opt/openfbi/pylibs/areas.csv","r",encoding="utf-8") as fp:
			content=fp.readlines()
		areas_list=[i.strip() for i in content if len(i.strip())>1]
		stream["areas"]=areas_list
	#读取常见错误的名字信息
	if "wrong_name" not in stream:
		with open("/opt/openfbi/pylibs/wrong_name.csv","r",encoding="utf-8")as fp:
			name_con=fp.readlines()
		name_list=[i.strip() for i in name_con if len(i.strip())>1]
		stream["wrong_name"]=name_list
#end 

#系统定时函数，st为时间戳 
def fpsearch(st):
	if stream["fpfirsttime"]:
		c = load_ssdb_kv("model_config")
		fptime = c["setting"]["model101"]["times"]
		fpft = int(stream["fpfirsttime"][11:13])
		t1 = int(time.strftime("%H"))
		t2 = fpft + fptime
		if t2 > 24:
			t2 = t2 - 24
		if t1 > t2:
			fpc = c["setting"]["model101"]["timec"]
			for k in stream["fps"]:
				if stream["fps"][k] > fpc:
					s = stream["fpmessage"][k]
					if s.get("real_ip"):
						srcs = s.get("real_ip")
					else:
						srcs = s.get("srcip")
					s["id"] = xlink_uuid(0)
					s["proof"] = ""
					s["desc"] = "终端通过接口段时间获取发票信息"
					s["message"] = "终端“" + srcs + "”在接口" + s["url"] + "中" + str(fptime) + "小时内获取了发票" + str(stream["fps"][k]) + "张"
					proofs = {}
					proofs["判定标准"] = "发票信息获取行为:终端的接口访问行为，返回体中的内容至少同时包含纳税人识别号、发票代码和公司名称三种类型敏感信息的，定义为发票信息获取行为。取三种敏感类型中数量最少的作为发票数量，在设定时间周期内，获取超过设定阈值数量的发票时发出告警"
					proofs["接口"] = s["url"]
					proofs["终端"] = srcs
					proofs["时间段（小时）"] = fptime
					proofs["段时间获取阈值"] = fpc
					proofs["段时间获取数量"] = stream["fps"][k]
					proofs["结果"] = "终端通过接口段时间获取发票信息"
					s["proofs"] = proofs
					to_pool("api_model",s)
					if stream["sends4"]:
						ssss = deepcopy(s)
						ssss["event_type"] = "model"
						#to_kfk(ssss)
						ssss["timestamp"] = str(ssss["timestamp"])
						to_json_file("/data/syslog_file/eve",ssss)
			stream["fpfirsttime"] = ""
			stream["fpmessage"] = {}
			stream["fps"] = {}
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	c={}
	c["timestamp"]= iso_to_datetime(o["timestamp"])
	c["flow_id"]=o.get("flow_id")
	c["src_ip"]= o.get("src_ip")
	c["dest_ip"]= o.get("dest_ip")
	c["dest_port"]=o.get("dest_port")
	if o.get("http").get("http_method"):
		c["http_method"]=o["http"]["http_method"]
	else:
		c["http_method"]=''
	return c
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def filter_data(cfg,data):
	da={}
	for re_match in cfg:
		an=re.findall(re_match["name"],data)
		if an:
			da[re_match["rekey"]]=an
	#n_d=identify_per_adr_name(data)
	#da["姓名"]=n_d[0]
	#da["地址"]=n_d[1]
	return da
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def sen_data(total_info):
	c={}
	err_name=stream["wrong_name"]
	
	#datas弱点汇总字典，info弱点铭感数据，key弱点敏感类型，lk li弱点敏感信息数量，ds告警敏感信息汇总，http_sen告警敏感信息
	ds = []
	pos_info={}#监控
	msg_info={}#信息汇总
	#对敏感信息进行存储
	for pos,info in total_info.items():
		#响应体：{},
		info_count=0
		type_info={}
		msg={}
		for key,value in info.items():
			value_count=0
			detail_msg=[]
			val_list=list(set(value))
			for val in val_list:
				val=val.strip(",")
				if len(val)>1 and val not in err_name:
					if key=="银行卡号" or key=="身份证":
						an=check_y_n(key,val)
						if an:
							value_count+=1
							http_sen = {}
							http_sen["sens"] = pos
							http_sen["message"] = val
							http_sen["key"] = key
									#将敏感信息添加到汇总信息中
							detail_msg.append(val)
								#添加原始消息
							ds.append(http_sen)
					elif key=="手机号":
						if "00000000" not in val:
							value_count+=1
							http_sen = {}
							http_sen["sens"] = pos
							http_sen["message"] = val
							http_sen["key"] = key
							#将敏感信息添加到汇总信息中
							detail_msg.append(val)
							#添加原始消息
							ds.append(http_sen)
					else:
						value_count+=1
						http_sen = {}
						http_sen["sens"] = pos
						http_sen["message"] = val
						http_sen["key"] = key
						#将敏感信息添加到汇总信息中
						detail_msg.append(val)
						#添加原始消息
						ds.append(http_sen)
			if value_count !=0:
				type_info[key]=value_count
				msg[key]=detail_msg
		if type_info !={}:
			pos_info[pos]=type_info
		if msg!={}:
			msg_info[pos]=msg
	c["msg_total"]=msg_info
	c["sen_type_count"]=pos_info
	return ds,c
#end 

#base64字符串的解码,处理被截断的情况

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def base64_decode(x):
	try:
		a =  base64.b64decode(x).decode("utf-8")
	except Exception as e:
		a=""
	return a
#end 

#对银行卡号和纳税人识别号进行检测

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def check_y_n(key,val):
	if key=="银行卡号":
		an=luhn(val)
		return an
	#Delete 注释 by superFBI on 2023-05-17 10:00:32
#if key=="纳税人识别号或社会统一信用代码":

#		an=check_social(val)

#		return an 

	if key=="身份证":
		an=id_validators(val)
		return an
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#需要额外引入的包

#需要引入的包 
from un_file import *
import ujson
import sys
import gc
import base64
import regex as re
import orjson
import uuid
from copy import deepcopy
from pyipip import IPIPDatabase
#end 

#udf

#end 
