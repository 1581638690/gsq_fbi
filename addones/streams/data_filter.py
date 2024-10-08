#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: data_filter.xlk
#datetime: 2024-08-30T16:10:57.789144
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

#LastModifyDate:　2024-01-16T18:42:04    Author:   rzc

#LastModifyDate:　2024-01-16T14:25:36    Author:   rzc

#LastModifyDate:　2024-01-09T10:31:15    Author:   rzc

#LastModifyDate:　2024-01-09T10:28:18    Author:   rzc

#LastModifyDate:　2024-01-06T16:29:45    Author:   superFBI

#LastModifyDate:　2024-01-06T15:50:53    Author:   superFBI

#LastModifyDate:　2024-01-06T15:41:29    Author:   superFBI

#LastModifyDate:　2024-01-06T14:01:09    Author:   superFBI

#LastModifyDate:　2024-01-05T11:23:13.582402    Author:   superFBI

#LastModifyDate:　2023-12-27T14:05:22.020685    Author:   superFBI

#LastModifyDate:　2023-08-31T16:36:02.048075    Author:   pjb

#xlink脚本

#file: data_filter.xlk

#name: 敏感数据过滤和提取

#描述： 所有协议的敏感数据识别和提取

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with data_filter

#停止

#a = @udf FBI.x_finder3_stop with data_filter

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:data_filter,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::data_filter

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "文件信息敏感识别"
	stream["meta_desc"] = "从redis中取出fileinfo队列消费文件信息，进行敏感数据识别和提取和敏感信息告警"
	stream["max_xlink"]=5
	#a=load_ssdb_kv("setting")
	#stream["link"] = a["kfk"]["origin"]["link"]
	#stream["reset"] = a["kfk"]["origin"]["reset"]
	#stream["source"]= {"link":stream["link"],"topic":"fileinfo1","group":"filter","start-0":True}
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]={"link":stream["redis_link"]+":16379","topic":"fileinfo_proto","redis":"list"}
	stream["source"]={"unix_udp":"/tmp/fileinfo_proto"}
	#stream["redis"]={"host":"127.0.0.1","port":"6381"}
	#敏感数据配置
	al=load_ssdb_kv("alarm")["setting"]
	if "datafilter_alarm"  in al:
		stream["datafilter_alarm_index"]=al.get("datafilter_alarm").get("names")
	else:
		stream["datafilter_alarm_index"] = []
	stream["datafilter_alarm"]=load_ssdb_kv("dd:reqs_label")["data"]
	file_data=load_ssdb_kv("writelist")["file_sen"]
	for data in file_data:
		stream["file_type"]=set(data["file_type"].split("/"))
		#敏感数据正则配置
	try:
		sensitive1=load_ssdb_kv("sensitive")["data"]
		stream["sensitive"]=[]
		for data in sensitive1:
			if data["off"]==1:
				if data["rekey"]=="姓名" or data["rekey"]=="地址":
					if name_switch!="0":
						data["name"]=re.compile(data["name"])
						stream["sensitive"].append(data)
				else:
					data["name"]=re.compile(data["name"])
					stream["sensitive"].append(data)
	except:
		stream["sensitive"]=load_ssdb_kv("sensitive")["data"]
	stream["st"]["st_10s"]={"times":5,"fun":"print10"}
	stream["count"] = 0
	stream["count-10"] = 0
	stream["alarm_count"] = 0
	#chk的链接
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	#chk创建表
	#stream["CKH"].execute("CREATE TABLE test2 (x Int32) ENGINE = MergeTree() order by x")
	#创建pool
	pool["ckh"] = []
	pool["datafilter_alarm"] = []
	pool["file_count"]=[]
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_sensfile" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	if "api_sensfilet" in a:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
	if "api_sensfilem" in a:
		stream["sends3"] = 1
	else:
		stream["sends3"] = 0
	
	#白名单
	stream["whitelist"]={}
	with open("/opt/openfbi/pylibs/wrong_name.csv","r",encoding="utf-8")as fp:
		name_con=fp.readlines()
	name_list=[i.strip() for i in name_con if len(i.strip())>1]
	stream["wrong_name"]=name_list
	write_list=load_ssdb_kv("writelist")["write_list"]
	if "name_list" in write_list:
		name_list=write_list.get("name_list").get("name")
		for name in name_list:
			stream["wrong_name"].append(name["data"])
	stream["whitelist"]["姓名"]=stream["wrong_name"]
	stream["wrong_moblie"]=[]
	if "moblie_list" in write_list:
		moblie_list=write_list.get("moblie_list").get("moblie")
		for moblie in moblie_list:
			stream["wrong_moblie"].append(moblie["data"])
	stream["whitelist"]["手机号"]=stream["wrong_moblie"]
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	src_port=o["src_port"]
	if "areas" not in stream:
		with open("/opt/openfbi/pylibs/areas.csv","r",encoding="utf-8") as fp:
			content=fp.readlines()
		areas_list=[i.strip() for i in content if len(i.strip())>1]
		stream["areas"]=areas_list
	if o["event_type"] == "fileinfo":
		files = "/data/" + o["fileinfo"]["file_path"]
		t_path = "/dev/shm/znsm/"
		
		if not os.path.exists(t_path):
			os.mkdir(t_path)
		#判断文件大小
		max_size=4*1024*1024*1024
		if os.path.exists(files):
			file_size=getDocSize(files)
			#判断size是否为空
			if file_size is not None:
				if file_size < max_size:
					#存放敏感信息
					sen_info = {}
					#存放文件信息
					yuanfile_path = {}
					filename=o.get("fileinfo").get("filename")
					magic = o.get('fileinfo').get("magic", "")
					total_info = guess_file(files,t_path,yuanfile_path,stream["file_type"],magic)
					#debug_on(1)
					#return total_info
					file_info={}
					#取出total_info唯一值
					for key,value in total_info.items():
						all_key=""
						#调用函数，返回file_info
						all_key,file_info=filename_group(value,all_key,file_info)
					stream["count"]+=1
					#debug_on(1)
					#return file_info
					#获取到带文件路径file_info数据
					for key,content in file_info.items():
						#key:表示文件路径
						# content:文件读取内容
						# 对获取的所有压缩文件数据进行处理
						if content=="加密zip":
							sen_info[key]="加密zip"
						else:
							#用正则匹配所有的敏感信息数据
							info= {re_match["rekey"]: regex.findall(re_match["name"], content) for re_match in stream["sensitive"]}
							sen_info[key]=info
					name=files.split("/")[-1]
					
					for file_detail,info in sen_info.items():
						
						if name == file_detail:
							file_pos=""
						else:
							file_pos=file_detail
						#判断是否为加密的zip文件
						if info =="加密zip":
							e = clone_event(o)
							e["uuid"] = xlink_uuid(0)
							e["data_match"]="加密ZIP"
							e["file_pos"] = file_detail
							to_pool("ckh", e)
							if stream["sends2"]:
								ss = deepcopy(e)
								ss["event_type"] = "sensfile_trace"
								#to_kfk(ss)
								ss["timestamp"] = str(ss["timestamp"])
								to_json_file("/data/syslog_file/eve",ss)
							stream["count-10"] += 1
						else:
							info_count=0
							for i in info.values():
								info_count+=len(i)
							#如果字典中存在敏感信息
							if info_count>0:
								#监控
								c=clone_event(o)
								c["uuid"]=xlink_uuid(0)
								al=clone_event(o)
								#告警
								al["uuid"]=xlink_uuid(0)
								#printf("al",al)
								ainfo={}
								msg={}
								type_info={}
								for key, value in info.items():
									msg_list=[]
									a_list=[]
									value_count=0
									if key in stream["whitelist"]:
										worng_name=stream["whitelist"].get(key)
										value_list=list(set(value_list)-set(worng_name))
										if not value_list:
											continue
									value_list=list(set(value))
									# info:{"手机号":[],"姓名":[]}
									if value_list != []:
										for val in value_list:
											#if val not in err_name:
											val=val.strip(",")
											if key=="银行卡号" or key=="纳税人识别号或社会统一信用代码" or key =="身份证":
												an=check_y_n(key,val)
												if an:
													e,value_count,a_list,msg_list=msg_match(value_count,a_list,key,o,val,file_pos,msg_list,stream["datafilter_alarm_index"],stream["datafilter_alarm"])
													to_pool("ckh", e)
													stream["count-10"] += 1
											else:
												e,value_count,a_list,msg_list=msg_match(value_count,a_list,key,o,val,file_pos,msg_list,stream["datafilter_alarm_index"],stream["datafilter_alarm"])
												to_pool("ckh", e)
												stream["count-10"] += 1
										ainfo[key]=a_list
										if value_count:
											#监控
											type_info[key]=value_count
											#汇总信息
											msg[key]=msg_list
								printf("ainfo",ainfo)
								#告警
								al["rekey"]="此文件包含了"+json.dumps(type_info,ensure_ascii=False)
								#debug_on(1)
								printf("rekey",al["rekey"])
								t_v=""
								for k,v in ainfo.items():
									if v:
										t_v += k + ":"+",".join(v)+"\n"
								printf("t_v",t_v)
								#debug_on(1)
								#return t_v
								if t_v:
									al["data_match"]=t_v
									to_pool("datafilter_alarm",al)
									stream["alarm_count"]+=1
									if stream["sends"]:
										s = deepcopy(al)
										s["event_type"] = "sensfile"
										#to_kfk(s)
										s["timestamp"] = str(s["timestamp"])
										to_json_file("/data/syslog_file/eve",s)
								#监控
								if type_info:
									c["msg_total"]=msg
									c["sen_type_count"]=type_info
									to_pool("file_count",c)
									if stream["sends3"]:
										sss = deepcopy(c)
										sss["event_type"] = "sensfile_m"
										#to_kfk(sss)
										sss["timestamp"] = str(sss["timestamp"])
										to_json_file("/data/syslog_file/eve",sss)
									
#					# 清除文件夹内数据

					del_file(t_path)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	
	al=load_ssdb_kv("alarm")["setting"]
	if "datafilter_alarm"  in al:
		stream["datafilter_alarm_index"]=al.get("datafilter_alarm").get("names")
	else:
		stream["datafilter_alarm_index"] = []
	printf("sum","匹配到正确的文件数：%d===存入总数:%d"%(stream["count"],stream["count-10"]))
	printf("print10","敏感告警总数====>>%d"%stream["alarm_count"])
	stream["datafilter_alarm"]=load_ssdb_kv("dd:reqs_label")["data"]
	store_ckh(pool["ckh"],"datafilter")
	store_ckh(pool["file_count"],"filter_count")
	store_ckh(pool["datafilter_alarm"],"datafilter_alarm")
#end 

#系统定时函数，st为时间戳 
def send60(st):
	#敏感数据文件配置
	file_data=load_ssdb_kv("writelist")["file_sen"]
	for data in file_data:
		stream["file_type"]=set(data["file_type"].split("/"))
	#敏感数据正则配置
	try:
		sensitive1=load_ssdb_kv("sensitive")["data"]
		stream["sensitive"]=[]
		for data in sensitive1:
			if data["off"]==1:
				if data["rekey"]=="姓名" or data["rekey"]=="地址":
					if name_switch!="0":
						data["name"]=re.compile(data["name"])
						stream["sensitive"].append(data)
				else:
					data["name"]=re.compile(data["name"])
					stream["sensitive"].append(data)
	except:
		stream["sensitive"]=load_ssdb_kv("sensitive")["data"]
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_sensfile" in a:
		stream["sends"] = 1
	else:
		stream["sends"] = 0
	if "api_sensfilet" in a:
		stream["sends2"] = 1
	else:
		stream["sends2"] = 0
	if "api_sensfilem" in a:
		stream["sends3"] = 1
	else:
		stream["sends3"] = 0
	#白名单
	stream["whitelist"]={}
	with open("/opt/openfbi/pylibs/wrong_name.csv","r",encoding="utf-8")as fp:
		name_con=fp.readlines()
	name_list=[i.strip() for i in name_con if len(i.strip())>1]
	stream["wrong_name"]=name_list
	write_list=load_ssdb_kv("writelist")["write_list"]
	if "name_list" in write_list:
		name_list=write_list.get("name_list").get("name")
		for name in name_list:
			stream["wrong_name"].append(name["data"])
	stream["whitelist"]["姓名"]=stream["wrong_name"]
	stream["wrong_moblie"]=[]
	if "moblie_list" in write_list:
		moblie_list=write_list.get("moblie_list").get("moblie")
		for moblie in moblie_list:
			stream["wrong_moblie"].append(moblie["data"])
	stream["whitelist"]["手机号"]=stream["wrong_moblie"]
#end 

#克隆一个新事件,创建一个新的变量，并返回

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	http=o.get("http")
	if o["app_proto"]=="ftp-data":
		app_proto="ftp"
	else:
		app_proto=o["app_proto"]
	e = {
		"timestamp": iso_to_datetime(o["timestamp"]),
		"filename": o["fileinfo"]["filename"],
		"flow_id": o["flow_id"],
		"src_ip": o["src_ip"],
		"dest_ip": o["dest_ip"],
		"dest_port": o["dest_port"],
		"src_port": o["src_port"],
		"app_proto": app_proto,
		"url": http.get("url"),
		"size": o["fileinfo"]["size"],
		"file_path": o["fileinfo"]["file_path"]
	}
	return e
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def msg_match(value_count,a_list,key,o,val,file_pos,msg_list,datafilter_alarm_index,datafilter_alarm):
	value_count+=1
	e = clone_event(o)
	e["uuid"] = xlink_uuid(0)
	e["rekey"] = key
	e["data_match"] = val
	e["file_pos"] = file_pos
	msg_list.append(val)
	if datafilter_alarm_index:
		for i in datafilter_alarm_index:
			index = int(i["name"]) #取出 index值来取出下拉框的值
			value=i.get("value","")
			if key == datafilter_alarm[index][0]:#如果key相同 判断值是否相等
				if value == val:
					a_list.append(val)
	return e,value_count,a_list,msg_list
#end 

#对银行卡号和纳税人识别号进行检测

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def check_y_n(key,val):
	if key=="银行卡号":
		an=luhn(val)
		return an
	if key=="纳税人识别号或社会统一信用代码":
		an=check_social(val)
		return an 
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
import sys
import gc
#import re
import os
import uuid
import random
import regex
from copy import deepcopy
from un_file import *
#udf

#end 
