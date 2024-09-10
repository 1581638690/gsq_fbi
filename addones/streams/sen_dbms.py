#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: sen_dbms.xlk
#datetime: 2024-08-30T16:10:58.458751
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

#LastModifyDate:　2024-03-05T10:32:44    Author:   pjb

#LastModifyDate:　2024-03-04T18:04:09    Author:   pjb

#LastModifyDate:　2024-03-04T15:34:33    Author:   pjb

#LastModifyDate:　2024-02-02T15:22:05    Author:   pjb

#LastModifyDate:　2024-01-25T15:22:40    Author:   pjb

#LastModifyDate:　2023-11-24T17:26:28.604707    Author:   pjb

#LastModifyDate:　2023-11-20T11:10:33.022680    Author:   pjb

#LastModifyDate:　2023-11-10T17:26:23.439077    Author:   pjb

#LastModifyDate:　2023-11-10T11:37:33.603109    Author:   superFBI

#LastModifyDate:　2023-11-10T09:51:45.233021    Author:   superFBI

#LastModifyDate:　2023-11-09T16:11:44.146946    Author:   superFBI

#xlink脚本

#4主体信息

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "dbms敏感数据，sql指纹"
	stream["meta_desc"] = "从redis中消费数据，存入mariadb数据库dbms_obj表和ckh的dbms_sendata"
	#stream["max_xlink"]=8
	a = load_ssdb_kv("setting")
	stream["source"]= {"unix_udp":"/tmp/sen_dbms"}
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#域内域外
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["wd"]=jk_tf(stream["json_wdgl"])
	#stream["source"]={"link":stream["redis_link"]+":6380","topic":"sen_dbms","redis":"list"}
	stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
	#stream["redis"] = {"host":"127.0.0.1","port":"6380"}
	stream["st"]["st_10s"] = {"times":30,"fun":"print10"}
	try:
		stream["dbms"]=remove_file("/dev/shm/FF_dbms.pkl","/data/xlink","FF_dbms.pkl")
	except:
		stream["dbms"]=set()
	try:
		stream["dbms_user"]=remove_file("/dev/shm/FF_dbms_user.pkl","/data/xlink","FF_dbms_user.pkl")
	except:
		stream["dbms_user"]=set()
	try:
		stream["dbms_sql"]=remove_file("/dev/shm/FF_dbms_sql.pkl","/data/xlink","FF_dbms_sql.pkl")
	except:
		stream["dbms_sql"]=set()
	pool["dbms_sendata"] = []
	
	#敏感数据正则配置
	try:
		sensitive1=load_ssdb_kv("sensitive")["data"]
		stream["sensitive"]=[]
		for data in sensitive1:
			if data["off"]==1:
				stream["sensitive"].append(data)
	except:
		stream["sensitive"]=load_ssdb_kv("sensitive")["data"]
#end 

# 	flow1 = filter flow1 by (sql !="SET AUTOCOMMIT = ?" and sql !="SET NAMES utf8mb4" and sql !="SELECT VERSION()" and sql !="SELECT DATABASE()" and sql !="SELECT @@transaction_isolation" and sql != "SELECT @@sql_mode" and sql !="SELECT @@lower_case_table_names" and sql !="ROLLBACK" and sql !="COMMIT" and sql!="SET autocommit=?" and sql !="SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?" and sql != "SELECT @@session.transaction_read_only")

#事件处理函数

#事件处理函数
def Events(o,topic=''):
#对象管理

	dbms_obj = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
	db_type = o.get("db_type","")
	if db_type and dbms_obj not in stream["dbms"]:
		stream["dbms"].add(dbms_obj)
		yuw = yn(o.get("dest_ip"),stream["wd"])
		yun = yn(o.get("src_ip"),stream["wd"])
		a = {}
		if yuw:
			a["dbms_yuw"] = 1
		else:
			a["dbms_yuw"] = 0
		if yuw and not yun:
			a["dbms_share"] = 1
		else:
			a["dbms_share"] = 0
		a["dbms_obj"] = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
		a["dstip"] = o.get("dest_ip","")
		a["dstport"] = o.get("dest_port",0)
		a["first_time"] = str(o["timestamp"])
		a["last_time"] = str(o["timestamp"])
		a["db_type"] = o.get("db_type","")
		a["count"] = 1
		if o.get("cmd") == "version":
			if o.get("req"):
				a["version"] = o.get("req","")
			else:
				a["version"] = o.get("resp","")
		else:
			a["version"] = ""
		#to_redis("obj_dbms",a)
		to_unix_udp(a,"/tmp/obj_dbms")
	user = o.get("user","")
	if user and db_type:
		users = user + ":" + dbms_obj
		if users not in stream["dbms_user"]:
			stream["dbms_user"].add(users)
			a = {}
			a["user"] = user
			a["db_type"] = o.get("db_type","")
			a["dbms_obj"] = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
			a["first_time"] = str(o["timestamp"])
			a["last_time"] = str(o["timestamp"])
			a["count"] = 1
			to_unix_udp(a,"/tmp/obj_dbms")
	if o.get("cmd") == "query":
		sql = o.get("sql","")
		if sql and o.get("type","") in ["DQL","DML","DDL","TCL","dCL"]:
			dbms_obj = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
			if sql not in stream["dbms_sql"]:
				stream["dbms_sql"].add(sql)
				a = {}
				a["dbms_obj"] = dbms_obj
				a["dbms_sql"] = sql
				a["md5"] = o.get("md5","")
				a["first_time"] = str(o.get("timestamp",""))
				a["db_type"] = o.get("db_type","")
				a["db"] = o.get("db","")
				a["user"] = o.get("user","")
				a["table_list"] = str(o.get("table_list",""))
				a["col_list"] = str(o.get("col_list",""))
				a["count"] = 1
				to_unix_udp(a,"/tmp/obj_dbms")
	#敏感识别
	total_info={}
	total_count={}
	total_info,total_count=sen_con_deta(o["msg"],o["req"])
	if total_info:
		req_count = total_count.get("Sql语句",'')
		res_count = total_count.get("Msg值",'')
		total_info = json.dumps(total_info ,ensure_ascii=False)
		total_count = json.dumps(total_count ,ensure_ascii=False)
		o["total_info"]=total_info
		o["total_count"]=total_count
		o["req_count"] = json.dumps(req_count ,ensure_ascii=False)
		o["res_count"] = json.dumps(res_count ,ensure_ascii=False)
		to_pool("dbms_sendata",o)
		
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	store_ckh(pool["dbms_sendata"],"dbms_sendata")
	dbms=copy.copy(stream["dbms"])
	dump_pkl("/data/xlink/FF_dbms.pkl",dbms)
	dbms_user=copy.copy(stream["dbms_user"])
	dump_pkl("/data/xlink/FF_dbms_user.pkl",dbms_user)
	dbms_sql=copy.copy(stream["dbms_sql"])
	dump_pkl("/data/xlink/FF_dbms_sql.pkl",dbms_sql)
	#域内域外
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["wd"]=jk_tf(stream["json_wdgl"])
	#敏感数据正则配置
	try:
		sensitive1=load_ssdb_kv("sensitive")["data"]
		stream["sensitive"]=[]
		for data in sensitive1:
			if data["off"]==1:
				stream["sensitive"].append(data)
	except:
		stream["sensitive"]=load_ssdb_kv("sensitive")["data"]
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def sen_con_deta(message,sql_data):
	total_info={}
	total_count={}
	if message != "":
		sen_data= filter_data(stream["sensitive"],message)
		if sen_data != {}:
			total_info["Msg值"] = {k: list(set(v)) for k, v in sen_data.items()}
			total_count["Msg值"]= {k: len(list(set(v))) for k, v in sen_data.items()}
	if sql_data != "":
		sen_data= filter_data(stream["sensitive"],sql_data)
		if sen_data != {}:
			total_info["Sql语句"] = {k: list(set(v)) for k, v in sen_data.items()}
			total_count["Sql语句"]= {k: len(list(set(v))) for k, v in sen_data.items()}
	return total_info,total_count
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def filter_data(data, message):
	da = {}
	for re_match in data:
		# an = []
		an = re.findall(re_match["name"], message)
		# an.extend(an1)
		##{“响应体”:{"姓名":[]}}
		if an:
			#Delete 注释 by superFBI on 2023-10-17 16:09:21
#if re_match["rekey"] in whitelist:

#				worng_name = whitelist.get(re_match["rekey"])

#				an = list(set(an) - set(worng_name))

#				if not an:

#					continue

			da[re_match["rekey"]] = an
	return da
#end 

#自定义批处理函数，使用FBI语句块, 可以在系统定时函数中调用

#使用push_arrays_to_df函数生成df,在语句块中使用

#如: push_arrays_to_df(table,"flow")

#需要额外引入的包

#需要引入的包 
import sys
import gc
from mondic import *
import pickle
from jk_ip import *
#end 

#udf

#end 
