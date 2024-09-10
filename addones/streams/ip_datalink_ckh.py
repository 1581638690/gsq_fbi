#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: ip_datalink_ckh.xlk
#datetime: 2024-08-30T16:10:57.758594
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

#LastModifyDate:　2024-01-08T09:41:07    Author:   superFBI

#LastModifyDate:　2023-12-27T14:01:15.037899    Author:   superFBI

#LastModifyDate:　2023-12-26T14:58:44.322750    Author:   superFBI

#LastModifyDate:　2023-12-26T14:49:06.865889    Author:   superFBI

#LastModifyDate:　2023-10-08T17:21:01.489244    Author:   superFBI

#LastModifyDate:　2023-09-27T15:31:38.357065    Author:   superFBI

#LastModifyDate:　2023-08-08T18:32:20.641697    Author:   pjb

#LastModifyDate:　2023-07-17T11:18:14.972947    Author:   pjb

#LastModifyDate:　2023-07-17T09:58:54.549666    Author:   pjb

#LastModifyDate:　2023-07-14T16:44:49.249827    Author:   pjb

#LastModifyDate:　2023-07-13T18:13:59.120421    Author:   pjb

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "终端链路进程"
	stream["meta_desc"] = "从api_visit主题中消费数据，存入ckh数据库表ip_datalink"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]= {"link":stream["link"],"topic":stream["topic"],"group":"ip_datalink","start-0":stream["reset"]}
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"] = {"unix_udp":"/tmp/ip"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_60s"]={"times":60,"fun":"print60"}
	stream["stw"]["ip_datalink"]={"times":10,"fun":"ip_datalink"}
	stream["stw"]["app_datalink"]={"times":10,"fun":"app_datalink"}
	stream["app2"] = load_set_pkl("/data/xlink/FF_app2.pkl")
	#app_datalink = = "/dev/shm/app_datalink.pkl"
	#temp_app_datalink = file_path + ".temp"
	stream["app_datalink"] = set()
	if os.path.exists("/data/xlink/app_datalink.pkl"):
		with open("/data/xlink/app_datalink.pkl",'rb')as fp:
			try:
				app_datalink=pickle.load(fp)
				stream["app_datalink"] = app_datalink
			except:
				stream["app_datalink"] = set()
	#ip_datalink = = "/dev/shm/ip_datalink.pkl"
	#temp_ip_datalink = file_path + ".temp"
	stream["ip_datalink"] = set()
	if os.path.exists("/data/xlink/ip_datalink.pkl"):
		with open("/data/xlink/ip_datalink.pkl",'rb')as fp:
			try:
				ip_datalink=pickle.load(fp)
				stream["ip_datalink"] = ip_datalink
			except:
				stream["ip_datalink"] = set()
	#stream["app_datalink"] = load_ssdb_hall("FF:app_datalink")
	#stream["ip_datalink"] = load_ssdb_hall("FF:ip_datalink")
	pool["agent_datalink"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	k = iso_to_timestamp(o.get("timestamp"))
	account = o.get("account")
	src_ip = o.get("src_ip")
	dest_ip = o.get("dest_ip")
	app = o.get("app")
	url = o.get("url_c")
	#httpjson = ujson.loads(o.get("httpjson"))
	request_headers = o.get("http").get("request_headers","")
	if src_ip in stream["app2"]:
		app_datalink = {}
		app_datalink["account"] = account
		app_datalink["src_ip"] = src_ip
		app_datalink["dest_ip"] = dest_ip
		app_datalink["app"] = app
		app_datalink["url"] = url
		app_link = str(account+src_ip+dest_ip+url)
		if app_link not in stream["app_datalink"]:
			push_stw("app_datalink",k,app_datalink)
			stream["app_datalink"].add(app_link)
			#to_ssdb_h("FF:app_datalink", app_link, True)
	
	realip, agent_ip = real_ip(request_headers,src_ip)
	#realip=o.get("realip")
	if "127.0.0.1" in agent_ip:
		agent_ip.remove("127.0.0.1")
	for i in range(len(agent_ip)):
		if i < len(agent_ip)-1:
			if agent_ip[i] == agent_ip[i+1]:
				agent_ip.remove(agent_ip[i])
	if realip != '':
		ip_datalink = {}
		ip_datalink["account"] = account
		ip_datalink["ip"] = realip
		ip_datalink["ip_link"] = str(agent_ip)
		ip_datalink["agent_ip"] = src_ip
		ip_datalink["app"] = app
		ip_datalink["url"] = url
		ip_link = str(agent_ip)
		if ip_link not in stream["ip_datalink"]:
			if len(agent_ip) ==1:
				agent_datalink = {}
				agent_datalink["A"] = realip
				agent_datalink["B"] = agent_ip[0]
				agent_datalink["C"] = "visit"
				agent_datalink["time"] = iso_to_datetime(o["timestamp"])
				to_pool("agent_datalink",agent_datalink)
				agent_datalink = {}
				agent_datalink["A"] = agent_ip[0]
				agent_datalink["B"] = o["url"]
				agent_datalink["C"] = "visit"
				agent_datalink["time"] = iso_to_datetime(o["timestamp"])
				to_pool("agent_datalink",agent_datalink)
				agent_datalink = {}
				agent_datalink["A"] = o["url"]
				agent_datalink["B"] = o["app"]
				agent_datalink["C"] = "belong"
				agent_datalink["time"] = iso_to_datetime(o["timestamp"])
				to_pool("agent_datalink",agent_datalink)
			if len(agent_ip) > 1:
				for i in range(len(agent_ip)-1):
					if i == 0:
						agent_datalink = {}
						agent_datalink["A"] = realip
						agent_datalink["B"] = agent_ip[0]
						agent_datalink["C"] = "visit"
						agent_datalink["time"] = iso_to_datetime(o["timestamp"])
						to_pool("agent_datalink",agent_datalink)
					agent_datalink = {}
					agent_datalink["A"] = agent_ip[i]
					agent_datalink["B"] = agent_ip[i+1]
					agent_datalink["C"] = "visit"
					agent_datalink["time"] = iso_to_datetime(o["timestamp"])
					to_pool("agent_datalink",agent_datalink)
				agent_datalink = {}
				agent_datalink["A"] = agent_ip[-1]
				agent_datalink["B"] = o["url"]
				agent_datalink["C"] = "visit"
				agent_datalink["time"] = iso_to_datetime(o["timestamp"])
				to_pool("agent_datalink",agent_datalink)
				agent_datalink = {}
				agent_datalink["A"] = o["url"]
				agent_datalink["B"] = o["app"]
				agent_datalink["C"] = "belong"
				agent_datalink["time"] = iso_to_datetime(o["timestamp"])
				to_pool("agent_datalink",agent_datalink)
			push_stw("ip_datalink",k,ip_datalink)
			#stream["ip_datalink"][ip_link] = True
			stream["ip_datalink"].add(ip_link)
			#to_ssdb_h("FF:ip_datalink", ip_link, True)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	store_ckh(pool["agent_datalink"],"agent_datalink")
	stream["app2"] = load_set_pkl("/data/xlink/FF_app2.pkl")
#end 

#系统定时函数，st为时间戳 
def print60(st):
	app_datalink = stream["app_datalink"].copy()
	ip_datalink = stream["ip_datalink"].copy()
	with open("/data/xlink/app_datalink.pkl", 'wb') as fp:
		fp.truncate()
		pickle.dump(app_datalink, fp)
	with open("/data/xlink/ip_datalink.pkl", 'wb') as fp:
		fp.truncate()
		pickle.dump(ip_datalink, fp)
#end 

#窗口函数，使用FBI语句块 
def ip_datalink(k,df):
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
		errors.append('[ip_datalink_ckh.xlk]执行第[170]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\nip_datalink = @udf df by udf0.df_fillna\nip_datalink = @udf ip_datalink by udf0.df_zero_index\n@udf ip_datalink by CRUD.save_table with (mysql1,ip_datalink)\ndrop ip_datalink\ndrop df\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=171
		if_fun(ptree)
	except Exception as e:
		errors.append('[ip_datalink_ckh.xlk]执行第[171]原语 if $size > 0 with "ip_dat... 出错,原因:'+e.__str__())

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
		errors.append('[ip_datalink_ckh.xlk]执行第[178]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def app_datalink(k,df):
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
		errors.append('[ip_datalink_ckh.xlk]执行第[180]原语 size = eval df by (index.... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '$size > 0', 'with': '""\napp_datalink = @udf df by udf0.df_fillna\napp_datalink = @udf app_datalink by udf0.df_zero_index\n@udf app_datalink by CRUD.save_table with (mysql1,app_datalink)\ndrop app_datalink\ndrop df\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=181
		if_fun(ptree)
	except Exception as e:
		errors.append('[ip_datalink_ckh.xlk]执行第[181]原语 if $size > 0 with "app_da... 出错,原因:'+e.__str__())

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
		errors.append('[ip_datalink_ckh.xlk]执行第[188]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import json
from stream_official_1119_sw import *
import pickle
import shutil
from mondic import *
#end 

#udf

#end 
