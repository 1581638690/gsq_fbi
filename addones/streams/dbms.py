#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: dbms.xlk
#datetime: 2024-08-30T16:10:58.272242
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

#LastModifyDate:　2024-04-24T15:20:57    Author:   pjb

#LastModifyDate:　2024-04-24T14:42:33    Author:   pjb

#LastModifyDate:　2024-04-24T11:32:00    Author:   pjb

#LastModifyDate:　2024-04-23T13:57:39    Author:   pjb

#LastModifyDate:　2024-04-22T17:58:45    Author:   pjb

#LastModifyDate:　2024-04-22T17:55:22    Author:   pjb

#LastModifyDate:　2024-04-07T17:10:17    Author:   pjb

#LastModifyDate:　2024-03-27T11:53:43    Author:   pjb

#LastModifyDate:　2024-03-26T10:52:44    Author:   pjb

#LastModifyDate:　2024-03-16T10:57:30    Author:   pjb

#LastModifyDate:　2024-03-15T19:04:20    Author:   pjb

#FBI脚本文件

#文件名: xlinktest.xlk

#作者: admin

#xlink脚本

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "dbms协议处理"
	stream["meta_desc"] = "从redis中取出dbms数据"
	stream["max_xlink"]=2
	#kfk = load_ssdb_kv("json_Link_configuration")
	#stream["source"] = {"link":kfk["link"]["kafka"]["ip"]+':'+kfk["link"]["kafka"]["port"],"topic":"zichan","group":"aaaaa2","start-0":False}
	#stream["es"]={"link":"http://192.168.1.185:59200","_index":"zichan4","_id":""}
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["source"]= {"unix_udp":"/tmp/yuan_dbms"}
	#stream["source"]={"link":stream["redis_link"]+":16379","topic":"yuan_dbms","redis":"list","topics":["http"]}
	stream["st"]["st_3s"] = {"times":1,"fun":"print3"}
	
	#去重列表
	stream["dbms"] = load_ssdb_hall("FF:dbms")
	stream["dbms_user"] = load_ssdb_hall("FF:dbms_user")
	#chk的链接
	stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
	stream["redis"] = {"host":"127.0.0.1","port":"6380"}
	#chk创建表
	#stream["CKH"].execute("CREATE TABLE test2 (x Int32) ENGINE = MergeTree() order by x")
	#创建pool
	pool["ckh"] = []
	pool["http"] = []
	pool["db"]=[]
	pool["http_dbms"]=[]
	
#end 

#事件处理

#事件处理函数
def Events(o,topic=''):
	#k = lambda_iso_to_timestamp(o["timestamp"])
	#dbms协议
	dbms = o.get("dbms")
	if dbms.get("db_type") == "kingbase" and dbms.get("req"):
		printf(dbms.get("db_type", ""),o)
	sql = dbms.get("req","")
	a = {
		"proto": o.get("proto", ""),
		"src_ip": o.get("src_ip", ""),
		"src_port": o.get("src_port", 0),
		"dest_ip": o.get("dest_ip", ""),
		"dest_port": o.get("dest_port", 0),
		"timestamp": iso_to_datetime(o["timestamp"]),
		"cmd": dbms.get("cmd", ""),
		"db_type": dbms.get("db_type", ""),
		"req": dbms.get("req", ""),
		"user": dbms.get("user", ""),
		"db": dbms.get("db", ""),
		"resp": dbms.get("resp", ""),
		"msg_type": "",
		"col_list": ""
	}
	msg = dbms.get("msg","")
	if msg:
		try:
			msg = json.loads(msg)
		except:
			pass
	if isinstance(msg,dict):
		a["msg_type"] = msg.get("msg_type","")
		a["col_list"] = str(msg.get("columns",""))
	else:
		a["msg_type"] = ""
		a["col_list"] = ""
	a["msg"] = dbms.get("msg","")
	a["id"] = xlink_uuid(0)
	a["flow_id"] = str(o.get("flow_id",0))
	a["context"] = dbms.get("resp","")
	a["md"] = md(a["req"])
	if sql:
		ret = sql_a1_md5(sql)
		#if ret.get("type") in ["DML","DDL","CMD"] and ret.get("key") not in ["COMMIT","ROLLBACK"]:
		ret = sql_a1_md5(sql)
		a["sql"] = ret.get("sql")
		a["md5"] = ret.get("md5")
		a["table_list"] = str(ret.get("table_list"))
		a["type"] = ret.get("type")
		a["key"] = ret.get("key")
		a["len"] = ret.get("len")
		a["len"] = str(a["len"])
		to_pool("ckh",a)
		to_unix_udp(a,"/tmp/sen_dbms")
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print3(st):
	store_ckh(pool["http"],"http_dbms")
	store_ckh(pool["ckh"],"dbms")
	store_ckh(pool["http_dbms"],"http_dbms")
	#push_arrays_to_df(pool["ckh"],"flow")
	#pool["ckh"] = []
	#save()
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

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def md(x):
	md = lambda x:'查询' if x.strip().lower().startswith('select') else ('删除' if x.strip().lower().startswith('delete') or x.strip().lower().startswith('drop') else ('新增' if x.strip().lower().startswith('create') or x.strip().lower().startswith('insert') else ('修改' if x.strip().lower().startswith('alter') or x.strip().lower().startswith('update') else '')))
	return md(x)
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def is_subselect(parsed):
	#是否子查询
	if not parsed.is_group:
		return False
	else:
		return True
	#Delete 注释 by pjb on 2024-03-15 18:45:06
#for item in parsed.tokens:

#		if item.ttype is Keyword.DML and item.value.upper() == 'SELECT':

#			return True

	return False
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def extract_from_part(parsed):
	#提取from,into,TABLE,update 等之后模块
	from_seen = False
	for item in parsed.tokens:
		if is_subselect(item):
			for x in extract_from_part(item):
				yield x
		if from_seen:
			if item.ttype is Keyword:
				from_seen = False
				continue
			else:
				yield item
		elif item.ttype is Keyword and item.value.upper() in ['FROM','INTO','TABLE','EXISTS']:
			from_seen = True
		elif item.ttype is Keyword.DML and item.value.upper() == 'UPDATE':
			from_seen = True
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def extract_join_part(parsed):
	#提取join之后模块
	ALL_JOIN_TYPE = ('LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN', 'LEFT OUTER JOIN', 'FULL OUTER JOIN', 'JOIN')
	flag = False
	for item in parsed.tokens:
		if flag:
			if item.ttype is Keyword:
				flag = False
				continue
			else:
				yield item
		if item.ttype is Keyword and item.value.upper() in ALL_JOIN_TYPE:
			flag = True
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def extract_table_identifiers(token_stream):
	#提取表名
	for item in token_stream:
		#print(item,type(item),dir(item))
		if isinstance(item, IdentifierList):
			for identifier in item.get_identifiers():
				if "get_real_name" in dir(identifier):
					yield identifier.get_real_name()
		elif isinstance(item, Identifier):
			if item.get_real_name():
				yield item.get_real_name()
			else:
				yield item.value
		elif isinstance(item, Function):
			yield item.get_name()
		elif item.ttype is Keyword:
			yield item.value
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def extract_tables(parsed):
	#提取sql中的表名（select语句）
	if isinstance(parsed,str):
		parsed = sqlparse.parse(parsed)
	from_stream = extract_from_part(parsed[0])
	join_stream = extract_join_part(parsed[0])
	return list(set(list(extract_table_identifiers(from_stream)) + list(extract_table_identifiers(join_stream))))
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def sql_a1_md5(sql):
	sql = sql.strip()
	ret={}
	parsed = sqlparse.parse(sql)
	stmt = parsed[0]
	if stmt.tokens[0].ttype==Keyword.DML:
		ret["type"] = "DML"
	elif stmt.tokens[0].ttype==Keyword.DDL:
		ret["type"] = "DDL"
	elif stmt.tokens[0].ttype==Token.Keyword:
		ret["type"] = "CMD"
	else:
		ret["type"] = "UNK"
	#第一个关键字
	ret["key"] =  stmt.tokens[0].value.upper()
	#平面长度
	a = [i for i in stmt.flatten()]
	ret["len"] = len(a)
	mds=[]
	sql_keys=["SET","WHERE","VALUES"]
	key_switch = False
	for token in a:
		if token.ttype not in [tokens.String.Single,tokens.String.Symbol,tokens.Number.Integer,tokens.Number.Float,tokens.Number.Hexadecimal]:
			if token.value.upper() in sql_keys: #开始提取关键字
				key_switch = True
			mds.append(token.value)
		else:
			if key_switch:
				mds.append("?")
			else:
				mds.append(token.value)
	ret["sql"] = "".join(mds)
	ret["md5"] = hashlib.md5(ret["sql"].encode("utf8")).hexdigest()
	ret["table_list"] = ",".join(extract_tables(sql))
	return ret
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return "%d-%7f-%3f" % (x,time.time(), random.random())
#end 

#需要引入的包 
import sqlparse
from sqlparse import tokens
from sqlparse.tokens import Keyword, Name, Token
from sqlparse.sql import Identifier, IdentifierList, Where, Comparison, Function
import hashlib
#end 

#udf

#end 
