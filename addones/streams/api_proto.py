#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_proto.xlk
#datetime: 2024-08-30T16:10:58.336328
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

#LastModifyDate:　2024-04-07T17:15:16    Author:   pjb

#LastModifyDate:　2024-04-03T15:16:53    Author:   lch

#LastModifyDate:　2024-04-03T14:51:08    Author:   lch

#LastModifyDate:　2024-04-03T14:47:12    Author:   lch

#LastModifyDate:　2024-04-03T14:44:25    Author:   lch

#LastModifyDate:　2024-04-03T14:39:26    Author:   lch

#LastModifyDate:　2024-04-03T14:37:08    Author:   lch

#LastModifyDate:　2024-04-03T14:34:21    Author:   lch

#LastModifyDate:　2024-04-03T14:27:35    Author:   lch

#LastModifyDate:　2024-04-03T14:25:21    Author:   lch

#LastModifyDate:　2024-04-03T14:19:51    Author:   lch

#xlink脚本

#

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with test

#停止

#a = @udf FBI.x_finder3_stop with test

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log_2020-05-27,0,1000

#清除日志

#a = load ssdb by ssdb0 query qclear,X_log_2020-05-27,-,-

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::脚本名称,  如，printf::test 

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "协议数据存储数据库"
	stream["meta_desc"] = "在redis中取出proto主题中消费数据，存入ckh数据库表api_各协议"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["ckh_link"] = a["kfk"]["data"]["addr_c"]
	#stream["source"]={"link":stream["redis_link"]+":16379","topic":"proto","redis":"list"}
	stream["source"]={"unix_udp":"/tmp/proto"}
	stream["sends"] = load_ssdb_kv("qh_send")["sends"].split(',')
	#add by by gjw 增加文件的kafka队列和IP地域库
	
	#stream["kfk"]={"link":stream["link"],"topic":"fileinfo1","key":"","topics":["api_send"]}
	stream["ipdb"] = IPIPDatabase( '/opt/openfbi/workspace/ipdb.datx')
	#域内域外
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["wd"]=jk_tf(stream["json_wdgl"])
	##账号检索子项开关
	account1 = a["setting"]["account"]["account_key"]
	stream["account"] = []
	for account_key in account1:
		if account_key["off"]==1:
			stream["account"].append(account_key.get("name"))
	#stream["redis"]={"host":"127.0.0.1","port":"16379"}
	#chk的链接
	stream["CKH"] = CKH_Client(host=stream["ckh_link"],port=19000,user="default",password="client")
	#stream["m"] = {"count":0,"dns": 0, "smtp": 0,"imap":0, "pop3": 0, "ftp": 0, "tftp": 0, "fileinfo": 0, "alert": 0, "smb": 0, "abroad": 0}
	#stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_60s"]={"times":10,"fun":"send60"}
	#stream["st"]["dns"]={"times":10,"fun":"dns_store"}
	#stream["st"]["smtp"]={"times":10,"fun":"smtp_store"}
	#stream["st"]["imap"]={"times":10,"fun":"imap_store"}
	#stream["st"]["pop3"]={"times":10,"fun":"pop3_store"}
	#stream["st"]["ftp"]={"times":10,"fun":"ftp_store"}
	#stream["st"]["tftp"]={"times":10,"fun":"tftp_store"}
	stream["st"]["fileinfo"]={"times":10,"fun":"fileinfo_store"}
	#stream["st"]["alert"]={"times":10,"fun":"alert_store"}
	#stream["st"]["smb"]={"times":10,"fun":"smb_store"}
	#stream["st"]["abroad"]={"times":10,"fun":"abroad_store"}
	
	try:
		stream["fileinfo"]=remove_file("/dev/shm/FF_fileinfo.pkl","/data/xlink","FF_fileinfo.pkl")
	except:
		stream["fileinfo"]=set()
	try:
		stream["file_server"]=remove_file("/dev/shm/FF_file_server.pkl","/data/xlink","FF_file_server.pkl")
	except:
		stream["file_server"]=set()
	try:
		stream["file_user"]=remove_file("/dev/shm/FF_file_user.pkl","/data/xlink","FF_file_user.pkl")
	except:
		stream["file_user"]=set()
	#创建pool
	#pool["dns"] = []
	pool["smtp"] = []
	pool["imap"] = []
	pool["pop3"] = []
	pool["ftp"] = []
	pool["tftp"] = []
	pool["fileinfo"] = []
	pool["alert"] = []
	pool["smb"] = []
	pool["ssh"] = []
	pool["flow"] = []
	pool["telnet"] = []
	pool["abroad"] = []
	pool["tls"] = []
	pool["rdp"] = []
	pool["rfb"] = []
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#文件服务器、账号
	file_user = ''
	file_server = ''
	first_time = str(iso_to_datetime(o.get("timestamp")))
	last_time = str(iso_to_datetime(o.get("timestamp")))
	d_yuw = yn(o.get("dest_ip",""),stream["wd"])
	s_yuw = yn(o.get("src_ip",""),stream["wd"])
	file_yuw = 0
	active = 3
	file_share = 0
	if o["event_type"] == "fileinfo":
	
		a = clone_event(o)
		a["filename"] = o.get('fileinfo').get("filename", "")
		if o.get("http"):
			if o.get("http").get("status"):
				if str(o.get("http").get("status")).startswith("2"):
					###文件服务器
					cookie = ''
					for i in o.get("http").get("request_headers",""):
						if i.get("name") == "Cookie":
							cookie = i.get("value")
							break
					if cookie:
						file_user, file_type = search(stream["account"], cookie)
						file_user1 = file_user +":"+ o["event_type"]
					if o.get("http").get("http_method") == "GET":
						printf("GET",o)
					if o.get("http").get("http_method") == "POST":
						printf("POST",o)
					file_server = o.get("src_ip","") + ":" + str(o.get("src_port",0))
					dstip = o.get("src_ip","")
					protocol = o.get("app_proto","")
					if s_yuw:
						file_yuw = 1
					if s_yuw and not d_yuw:
						file_share = 1
					#Delete 注释 by pjb on 2024-03-11 11:16:35
#if o.get("http").get("http_method") == "POST":

#						printf("POST",o)

#						file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))

#						protocol = o.get("app_proto","")

#						if d_yuw:

#							file_yuw = 1

#						if d_yuw and not s_yuw:

#							file_share = 1

					###
			app = o.get("http").get("hostname")
			if app == '127.0.0.1' or not app:
				app = a["srcip"] + ":" + str(a["srcport"])
			else:
				app=app.split(",")[0].split(" ")[0]
			url = urllib.parse.unquote(o.get("http").get("url",""))
			if "?" in url :
				a["url"] = "http://" + app + url.split("?")[0]
				a["parameter"] = url.split("?")[-1]
			else:
				a["url"] = "http://" + app + url
				a["parameter"] = ""
		else:
			printf("other",o)
			a["parameter"] = ""
			a["url"] = ""
		if o.get("fileinfo"):
			a["sha256"] = o.get("fileinfo").get("sha256","")
			a["md5"] = o.get("fileinfo").get("md5","")
		else:
			a["sha256"] = ""
			a["md5"] = ""
		a["gaps"] = str(o.get('fileinfo').get("gaps", ""))
		if o.get('fileinfo').get("magic"):
			type = o.get('fileinfo').get("magic").split(",")[0]
			a["type"] = type
			a["magic"] = o.get('fileinfo').get("magic").split(type + ',')[-1]
		else:
			a["type"] = ''
			a["magic"] = ''
		a["magic"] = o.get('fileinfo').get("magic", "")
		a["size"] = o.get('fileinfo').get("size", 0)
		a["stored"] = str(o.get('fileinfo').get("stored", ""))
		a["file_path"] = str(o.get('fileinfo').get("file_path", ""))
		a["app_proto"] = o.get('app_proto')
		a["app_proto"] = a["app_proto"].replace("ftp-data","ftp")
		a["state"] = o.get('fileinfo').get("state", "")
		a["xff"] = ""
		if o.get('http'):
			if o.get('http').get('xff'):
				a["xff"] = o.get('http').get('xff').split(',')[0]
		to_pool("fileinfo",a)
		if a["type"]:
			sha256 = a["sha256"] + a["app_proto"] + a["filename"]
			if sha256 not in stream["fileinfo"]:
				stream["fileinfo"].add(sha256)
				file = {}
				file["first_time"] = str(a["timestamp"]) 
				file["last_time"] = str(a["timestamp"])
				file["md5"] = a["sha256"]
				file["filename"] = a["filename"]
				file["app_proto"] = a["app_proto"]
				file["type"] = a["type"]
				file["magic"] = a["magic"]
				file["dstip"] = a["dstip"]
				file["size"] = a["size"]
				to_unix_udp(file,"/tmp/obj_dbms")
		#to_kfk(o)
		if "api_fileinfo" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "fileinfo"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "ftp":
		###文件服务器
		if o.get('ftp').get("user",):
			file_user = o.get('ftp').get("user",)
			file_user1 = file_user +":"+ o["event_type"]
		file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
		dstip = o.get("dest_ip","")
		protocol = o["event_type"]
		if d_yuw:
			file_yuw = 1
		if d_yuw and not s_yuw:
			file_share = 1
		##
		a = clone_event(o)
		a["reply"] = str(o.get('ftp').get("reply", ""))
		a["command"] = o.get('ftp').get("command", "")
		files = o.get('ftp').get("command_data", "")
		try:
			decoded = files.encode('latin1').decode('gb2312')
		except:
			decoded = files
		a["command_data"] = decoded
		a["completion_code"] = str(o.get('ftp').get("completion_code", ""))
		a["user"] = o.get('ftp').get("user", "")
		a["reply_received"] = o.get('ftp').get("reply_received", "")
		#add by rzc 修改错误
		a["dynamic_port"] = str(o.get('ftp').get("dynamic_port"))
		if a["command"] == "STOR" or  a["command"] == "STOU" or a["command"] == "APPE" or a["command"] == "DELE" or a["command"] == "RETR":
			a["filename"] = a["command_data"]
		#add by rzc 将字段数量保持一致
		else:
			a["filename"]=""
		to_pool("ftp",a)
		if "api_ftp" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "ftp"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "pop3":
		###文件服务器
		#Delete 注释 by pjb on 2024-03-14 14:31:06
#if o.get("dest_port",0) == 110:

#			if o.get('pop3').get("From"):

#				file_user = o.get('pop3').get("From")

#				file_user1 = file_user +":"+ o["event_type"]

#			file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))

#			dstip = o.get("dest_ip","")

#			protocol = o["event_type"]

#			if d_yuw:

#				file_yuw = 1

#			if d_yuw and not s_yuw:

#				file_share = 1

#		if o.get("src_port",0) == 110:

#			if o.get('pop3').get("To"):

#				file_user = o.get('pop3').get("To")

#				file_user1 = file_user +":"+ o["event_type"]

#			file_server = o.get("src_ip","") + ":" + str(o.get("src_port",0))

#			dstip = o.get("src_ip","")

#			protocol = o["event_type"]

#			if s_yuw:

#				file_yuw = 1

#			if s_yuw and not d_yuw:

#				file_share = 1

		###
		a = clone_event(o)
		a["cmd"] = o.get('pop3').get("cmd", "")
		a["mod"] = o.get('pop3').get("主题", "")
		a["greeting"] = o.get('pop3').get("greeting", "")
		a["From"] = o.get('pop3').get("From", "")
		a["To"] = o.get('pop3').get("To", "")
		try:
			a["content"] = o.get('pop3').get("response", [{}])[0].get("content", "")
		except:
			a["content"] = ""
		to_pool("pop3",a)
		if "api_pop3" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "pop3"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "tftp":
		###文件服务器
		#Delete 注释 by pjb on 2024-03-14 14:31:22
		file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
		dstip = o.get("dest_ip","")
		protocol = o["event_type"]
		if d_yuw:
			file_yuw = 1
		if d_yuw and not s_yuw:
			file_share = 1
		###
		a = clone_event(o)
		files = o.get('tftp').get("file", "")
		try:
			decoded = files.encode('latin1').decode('gb2312')
		except:
			decoded = files
		a["file"] = decoded
		a["mode"] = o.get('tftp').get("mode", "")
		a["packet"] = o.get('tftp').get("cmd", "")
		a["status"] = "true"
		to_pool("tftp",a)
		if "api_tftp" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "tftp"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "smtp":
		###文件服务器
		#Delete 注释 by pjb on 2024-03-14 14:31:37
#if o.get('email').get("from"):

#			file_user = html.unescape(o.get('email').get("from"))

#			file_user1 = file_user +":"+ o["event_type"]

#		file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))

#		dstip = o.get("dest_ip","")

#		protocol = o["event_type"]

#		if d_yuw:

#			file_yuw = 1

#		if d_yuw and not s_yuw:

#			file_share = 1

		###
		a = clone_event(o)
		a["cmd"] = o.get('smtp').get("cmd", "")
		a["mod"] = o.get('smtp').get("主题", "")
		a["From"] = html.unescape(o.get('email').get("from", ""))
		a["To"] = html.unescape(o.get('email').get("to", ""))
		a["status"] = o.get('email').get("status", "")
		a["subject"] = o.get('email').get("subject", "")
		a["helo"] = o.get('smtp').get("helo", "")
		to_pool("smtp",a)
		if "api_smtp" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "smtp"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "alert":
		a = clone_event(o)
		a["action"] = o.get('alert').get("action", "")
		a["signature"] = o.get('alert').get("signature", "")
		a["category"] = o.get('alert').get("category", "")
		a["severity"] = str(o.get('alert').get("severity", ""))
		a["filename"] = ""
		a["proto"] = o.get('proto')
		a["app_proto"] = o.get('app_proto')
		to_pool("alert",a)
		if "api_alert" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "alert"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "imap":
		###文件服务器
		#Delete 注释 by pjb on 2024-03-14 14:31:49
#file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))

#		dstip = o.get("dest_ip","")

#		protocol = o["event_type"]

#		if d_yuw:

#			file_yuw = 1

#		if d_yuw and not s_yuw:

#			file_share = 1

		###
		a = clone_event(o)
		a["cmd"] = o.get('imap').get("cmd", "")
		a["mod"] = o.get('imap').get("主题", "")
		a["From"] = html.unescape(o.get('imap').get("From", ""))
		a["To"] = html.unescape(o.get('imap').get("To", ""))
		try:
			a["content"] = o.get('imap').get("response", [{}])[0].get("content", "")
		except:
			a["content"] = ""
		to_pool("imap",a)
		if "api_imap" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "imap"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "smb":
		###文件服务器
		if o.get('smb').get("dialect", "") != 'unknown':
			if o.get('smb').get('ntlmssp', {}).get("user", ""):
				file_user = o.get('smb').get('ntlmssp', {}).get("user", "")
				file_user1 = file_user +":"+ o["event_type"]
			file_server = o.get("dest_ip","") + ":" + str(o.get("dest_port",0))
			dstip = o.get("dest_ip","")
			protocol = o["event_type"]
			if d_yuw:
				file_yuw = 1
			if d_yuw and not s_yuw:
				file_share = 1
		###
		a = clone_event(o)
		a["dialect"] = o.get('smb').get("dialect", "")
		a["command"] = o.get('smb').get("command", "")
		a["status"] = o.get('smb').get("status", "")
		a["share"] = o.get('smb').get("share", "")
		a["share_type"] = o.get('smb').get("share_type", "")
		a["server_guid"] = o.get('smb').get("server_guid", "")
		a["ntlmssp_host"] = o.get('smb').get('ntlmssp', {}).get("host", "")
		a["ntlmssp_user"] = o.get('smb').get('ntlmssp', {}).get("user", "")
		a["ntlmssp_domain"] = o.get('smb').get('ntlmssp', {}).get("domain", "")
		a["filename"] = o.get('smb').get("filename", "")
		a["size"] = o.get('smb').get("size", 0)
		to_pool("smb",a)
		if "api_smb" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "smb"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	if file_server:
		if file_server not in stream["file_server"]:
			stream["file_server"].add(file_server)
			file_s = {
				"file_server": file_server,
				"protocol": protocol,
				"file_yuw": file_yuw,
				"file_share": file_share,
				"first_time": first_time,
				"last_time": last_time,
				"active": active,
				"dstip": dstip
			}
			to_unix_udp(file_s,"/tmp/obj_dbms")
	if file_user:
		if file_user1 not in stream["file_user"]:
			stream["file_user"].add(file_user1)
			file_u = {
				"file_user": file_user,
				"protocol": protocol,
				"first_time": first_time,
				"last_time": last_time,
				"active": active
			}
			to_unix_udp(file_u,"/tmp/obj_dbms")
	elif o["event_type"] == "flow":
		a = clone_event(o)
		a["pkts_toserver"] = o.get('flow').get("pkts_toserver",0)
		a["pkts_toclient"] = o.get('flow').get("pkts_toclient", 0)
		a["bytes_toserver"] = o.get('flow').get("pkts_toserver", 0)
		a["bytes_toclient"] = o.get('flow').get("pkts_toserver", 0)
		a["flow_start"] = iso_to_datetime(str(o.get('flow').get("start", "")))
		a["flow_end"] = iso_to_datetime(str(o.get('flow').get("end", "")))
		a["proto"] = o.get('proto',"")
		a["age"] = o.get('flow').get("age",0)
		a["app_proto"] = o.get('app_proto',"")
		to_pool("flow",a)
		if "flow2" in stream["sends"]:
			s = deepcopy(a)
			s["event_type"] = "flow"
			#to_kfk2("api_send",s)
			#to_redis("api_send",s)
			s["timestamp"] = str(s["timestamp"])
			to_json_file("/data/syslog_file/eve",s)
	elif o["event_type"] == "ssh":
		a = {
		"id":xlink_uuid(0),
		"src_ip":o["src_ip"],
		"dest_ip":o["dest_ip"],
		"src_port":o["src_port"],
		"dest_port":o["dest_port"],
		"ssh_start":o.get('ssh').get("start",""),
		"timestamp":iso_to_datetime(str(o["timestamp"])),
		"proto":o["proto"],
		"tx_id":o["tx_id"],
		"client_proto_version":o["ssh"]["client"]["proto_version"] if "client" in o["ssh"] else "",
		"client_software_version":o["ssh"]["client"]["software_version"] if "client" in o["ssh"] else "",
		"server_proto_version":o["ssh"]["server"]["proto_version"] if "server" in o["ssh"]  else "",
		"server_software_version":o["ssh"]["server"]["software_version"] if "server" in o["ssh"]  else "",
		}
		to_pool("ssh",a)
	elif o["event_type"] == "telnet":
#Delete 注释 by rzc on 2022-12-07 15:47:31

#		stream["count-10"] += 1

#		a = {"src_ip":o["src_ip"],"src_port":o["src_port"],"dest_ip":o["dest_ip"],"dest_port":o["dest_port"],"event_type":o["event_type"],\

#			"flow_start":iso_to_datetime(o["timestamp"]),"fuse":str({"telnet_user":o["telnet"]["user"],"telnet_cmd":o["telnet"]["cmd"]})

#		}

#		to_pool("ckh",a)

		b = {
		"id":xlink_uuid(0),
		"src_ip":o["src_ip"],
		"src_port":o["src_port"],
		"dest_ip":o["dest_ip"],
		"dest_port":o["dest_port"],
		"timestamp":iso_to_datetime(str(o["timestamp"])),
		"telnet_user":o["telnet"]["user"],
		"telnet_cmd":o["telnet"]["cmd"],
		}
		to_pool("telnet",b)
	elif o["event_type"] == "tls":
		a = {
		"id":xlink_uuid(0),
		"flow_id":o.get("flow_id",0),
		"src_ip":o.get("src_ip",""),
		"dest_ip":o.get("dest_ip",""),
		"src_port":o.get("src_port",0),
		"dest_port":o.get("dest_port",0),
		"pcap_cnt":o.get("pacat,cnt",0),
		"timestamp":iso_to_datetime(str(o["timestamp"])),
		"proto":o.get("proto",""),
		}
		a["tls_sni"] = o.get('tls').get("sni","")
		a["tls_version"] = o.get('tls').get("version","")
		a["tls"]=ujson.dumps(o.get("tls",{}),ensure_ascii=False)
		to_pool("tls",a)
	elif o["event_type"] == "rdp":
			a = {
			"id" :xlink_uuid(0),
			"flow_id":o.get("flow_id",0),
			"src_ip":o.get("src_ip",""),
			"dest_ip":o.get("dest_ip",""),
			"src_port":o.get("src_port",0),
			"dest_port":o.get("dest_port",0),
			"timestamp":iso_to_datetime(str(o["timestamp"])),
			"proto":o.get("proto",""),
			"event_type":o.get("event_type","")
			}
			
			a["tx_id"] = o.get ("rdp").get("tx_id",0)
			a["event_type_rdp"] = o.get ("rdp").get("event_type","")
			a["cookie"] = o.get("rdp").get("cookie","")
			a["rdp"] = ujson.dumps(o.get("rdp"))
			to_pool("rdp",a)
	elif o["event_type"] == "rfb":
			a = {
			"id" :xlink_uuid(0),
			"flow_id":o.get("flow_id",0),
			"src_ip":o.get("src_ip",""),
			"dest_ip":o.get("dest_ip",""),
			"src_port":o.get("src_port",0),
			"dest_port":o.get("dest_port",0),
			"timestamp":iso_to_datetime(str(o["timestamp"])),
			"proto":o.get("proto",""),
			"event_type":o.get("event_type","")
			}
			a["rfb"] = ujson.dumps(o.get("rfb",""))
			a["server_protocol_version"] = str(ujson.dumps(o.get("rfb").get("server_protocol_version","")))
			a["client_protocol_version"] = str(ujson.dumps(o.get("rfb").get("client_protocol_version","")))
			a["authentication"] = ujson.dumps(o.get("authentication",""))
			to_pool("rfb",a)
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def send60(st):
	fileinfo=copy.copy(stream["fileinfo"])
	dump_pkl("/data/xlink/FF_fileinfo.pkl",fileinfo)
	file_server=copy.copy(stream["file_server"])
	dump_pkl("/data/xlink/FF_file_server.pkl",file_server)
	file_user=copy.copy(stream["file_user"])
	dump_pkl("/data/xlink/FF_file_user.pkl",file_user)
	stream["sends"] = load_ssdb_kv("qh_send")["sends"].split(',')
	#域内域外
	stream["json_wdgl"] = load_ssdb_kv("json_wdgl")
	stream["wd"]=jk_tf(stream["json_wdgl"])
	##账号检索子项开关
	a = load_ssdb_kv("setting")
	account1 = a["setting"]["account"]["account_key"]
	stream["account"] = []
	for account_key in account1:
		if account_key["off"]==1:
			stream["account"].append(account_key.get("name"))
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	a = {
		"id": xlink_uuid(0),
		"timestamp": iso_to_datetime(o.get("timestamp")),
		"srcip": o.get('src_ip',""),
		"srcport": o.get('src_port',0),
		"dstip": o.get('dest_ip',""),
		"dstport": o.get('dest_port',0),
		"flow_id": str(o.get("flow_id", ""))
	}
	return a
#end 

#系统定时函数，st为时间戳 
def fileinfo_store(st):
	store_ckh(pool["fileinfo"],"api_fileinfo")
	store_ckh(pool["abroad"],"api_abroad")
	store_ckh(pool["tftp"],"api_tftp")
	store_ckh(pool["ftp"],"api_ftp")
	store_ckh(pool["pop3"],"api_pop3")
	store_ckh(pool["alert"],"api_alert")
	store_ckh(pool["smb"],"api_smb")
	store_ckh(pool["imap"],"api_imap")
	store_ckh(pool["smtp"],"api_smtp")
	store_ckh(pool["ssh"],"event_ssh")
	store_ckh(pool["telnet"],"event_telnet")
	store_ckh(pool["flow"],"flow2")
	store_ckh(pool["tls"],"api_tls")
	store_ckh(pool["rdp"],"api_rdp")
	store_ckh(pool["rfb"],"api_rfb")
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def ip_lookup(ip):
	try:
		ip_is = False
		result = stream["ipdb"].lookup(ip).split('	')[0]
		if result not in ["中国","局域网","本地链路","共享地址","本机地址","保留地址"]:
			ip_is = True
	except Exception as e:
		ip_is = False
		result = ''
	return ip_is,result
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#需要额外引入的包

#需要引入的包 
import sys
import gc
import uuid
import html
from copy import deepcopy
import json
from pyipip import IPIPDatabase
import urllib
from urllib import parse
from mondic import *
import pickle
from jk_ip import *
from stream_official_1119_sw import *
#end 

#udf

#end 
