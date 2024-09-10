#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: h_d_analsis.xlk
#datetime: 2024-08-30T16:10:58.289172
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

#LastModifyDate:　2023-11-03T18:26:55.742779    Author:   rzc

#LastModifyDate:　2023-11-03T18:25:14.818389    Author:   rzc

#LastModifyDate:　2023-11-03T17:52:25.981409    Author:   rzc

#LastModifyDate:　2023-11-03T17:43:00.916490    Author:   rzc

#LastModifyDate:　2023-11-03T17:42:35.744364    Author:   rzc

#LastModifyDate:　2023-11-03T17:04:39.621153    Author:   rzc

#LastModifyDate:　2023-11-03T16:51:06.345785    Author:   rzc

#LastModifyDate:　2023-11-03T16:21:08.200264    Author:   rzc

#LastModifyDate:　2023-11-03T16:11:59.445019    Author:   rzc

#LastModifyDate:　2023-11-03T15:40:57.811292    Author:   rzc

#LastModifyDate:　2023-11-03T15:39:19.405721    Author:   rzc

#LastModifyDate:　2023-11-03T15:30:34.025904    Author:   rzc

#LastModifyDate:　2023-11-03T15:29:51.139381    Author:   rzc

#LastModifyDate:　2023-11-03T14:29:51.545706    Author:   rzc

#LastModifyDate:　2023-11-03T14:10:13.040181    Author:   rzc

#LastModifyDate:　2023-11-03T14:07:01.419148    Author:   rzc

#LastModifyDate:　2023-11-03T14:05:53.913958    Author:   rzc

#LastModifyDate:　2023-11-03T13:52:02.343716    Author:   rzc

#LastModifyDate:　2023-11-03T11:48:13.157238    Author:   rzc

#LastModifyDate:　2023-11-03T11:44:28.076301    Author:   rzc

#LastModifyDate:　2023-11-03T11:42:26.373409    Author:   rzc

#LastModifyDate:　2023-11-03T11:26:15.275485    Author:   rzc

#LastModifyDate:　2023-11-03T11:07:21.686617    Author:   rzc

#LastModifyDate:　2023-11-03T11:03:33.278062    Author:   rzc

#LastModifyDate:　2023-11-03T11:02:37.094288    Author:   rzc

#LastModifyDate:　2023-11-03T09:47:29.296594    Author:   rzc

#LastModifyDate:　2023-11-03T09:43:46.442440    Author:   rzc

#LastModifyDate:　2023-11-02T17:57:13.290890    Author:   rzc

#LastModifyDate:　2023-11-02T17:08:31.660670    Author:   rzc

#LastModifyDate:　2023-11-02T16:03:47.867510    Author:   rzc

#LastModifyDate:　2023-11-02T15:00:56.737414    Author:   rzc

#LastModifyDate:　2023-11-01T19:01:13.547822    Author:   rzc

#LastModifyDate:　2023-11-01T18:05:49.636542    Author:   rzc

#LastModifyDate:　2023-11-01T15:42:47.722376    Author:   rzc

#LastModifyDate:　2023-11-01T14:33:12.380876    Author:   rzc

#LastModifyDate:　2023-11-01T14:27:29.826490    Author:   rzc

#LastModifyDate:　2023-11-01T14:27:16.090107    Author:   rzc

#LastModifyDate:　2023-11-01T14:11:23.945124    Author:   rzc

#LastModifyDate:　2023-11-01T11:33:07.619599    Author:   rzc

#LastModifyDate:　2023-11-01T10:27:37.832324    Author:   rzc

#LastModifyDate:　2023-11-01T10:27:34.411743    Author:   rzc

#LastModifyDate:　2023-10-31T18:53:35.229211    Author:   rzc

#LastModifyDate:　2023-10-31T16:58:16.211436    Author:   rzc

#LastModifyDate:　2023-10-31T14:29:21.177469    Author:   rzc

#LastModifyDate:　2023-10-31T10:28:26.131210    Author:   rzc

#LastModifyDate:　2023-10-31T10:19:54.877464    Author:   rzc

#LastModifyDate:　2023-10-31T10:15:50.928996    Author:   rzc

#LastModifyDate:　2023-10-31T10:14:02.337747    Author:   rzc

#LastModifyDate:　2023-10-31T10:13:37.745687    Author:   rzc

#LastModifyDate:　2023-10-31T09:53:03.319700    Author:   rzc

#LastModifyDate:　2023-10-30T19:00:10.522783    Author:   rzc

#LastModifyDate:　2023-10-30T18:55:55.680474    Author:   rzc

#LastModifyDate:　2023-10-30T18:54:49.074021    Author:   rzc

#LastModifyDate:　2023-10-30T18:52:46.074540    Author:   rzc

#LastModifyDate:　2023-10-30T18:48:22.992598    Author:   rzc

#LastModifyDate:　2023-10-30T18:45:17.051482    Author:   rzc

#LastModifyDate:　2023-10-30T18:42:18.006121    Author:   rzc

#LastModifyDate:　2023-10-30T18:41:44.024166    Author:   rzc

#LastModifyDate:　2023-10-30T18:38:53.402737    Author:   rzc

#LastModifyDate:　2023-10-30T18:37:42.569303    Author:   rzc

#LastModifyDate:　2023-10-30T18:37:38.760697    Author:   rzc

#LastModifyDate:　2023-10-30T18:33:03.701860    Author:   rzc

#LastModifyDate:　2023-10-30T18:31:45.742683    Author:   rzc

#LastModifyDate:　2023-10-30T18:25:00.848304    Author:   rzc

#LastModifyDate:　2023-10-30T18:21:01.989456    Author:   rzc

#LastModifyDate:　2023-10-30T18:01:24.469313    Author:   rzc

#LastModifyDate:　2023-10-30T16:57:18.380148    Author:   rzc

#LastModifyDate:　2023-10-30T16:56:46.855915    Author:   rzc

#LastModifyDate:　2023-10-30T16:46:23.007951    Author:   rzc

#LastModifyDate:　2023-10-30T16:42:14.481912    Author:   rzc

#LastModifyDate:　2023-10-30T16:02:16.996541    Author:   rzc

#LastModifyDate:　2023-10-30T11:32:17.834318    Author:   superFBI

#LastModifyDate:　2023-10-30T09:49:53.359094    Author:   superFBI

#LastModifyDate:　2023-10-27T16:14:10.960220    Author:   superFBI

#LastModifyDate:　2023-10-27T10:27:25.689871    Author:   superFBI

#LastModifyDate:　2023-10-26T16:18:43.817034    Author:   rzc

#LastModifyDate:　2023-10-26T16:00:52.858548    Author:   rzc

#LastModifyDate:　2023-10-26T11:32:20.137278    Author:   rzc

#LastModifyDate:　2023-10-26T11:29:17.672120    Author:   rzc

#LastModifyDate:　2023-10-26T11:28:07.027152    Author:   rzc

#LastModifyDate:　2023-10-26T11:27:34.038773    Author:   rzc

#LastModifyDate:　2023-10-26T11:09:51.453257    Author:   superFBI

#LastModifyDate:　2023-10-26T11:04:45.395688    Author:   superFBI

#LastModifyDate:　2023-10-26T10:54:02.665708    Author:   superFBI

#LastModifyDate:　2023-10-26T10:49:20.272541    Author:   superFBI

#LastModifyDate:　2023-10-26T10:45:56.894104    Author:   superFBI

#LastModifyDate:　2023-10-26T10:45:38.428776    Author:   superFBI

#LastModifyDate:　2023-10-26T09:43:23.324417    Author:   superFBI

#LastModifyDate:　2023-10-26T09:40:58.479449    Author:   superFBI

#LastModifyDate:　2023-10-25T17:39:05.153546    Author:   superFBI

#LastModifyDate:　2023-10-25T16:11:27.351157    Author:   superFBI

#LastModifyDate:　2023-10-24T17:45:08.743596    Author:   superFBI

#LastModifyDate:　2023-10-24T17:41:51.041486    Author:   superFBI

#LastModifyDate:　2023-10-24T17:33:23.897522    Author:   superFBI

#LastModifyDate:　2023-10-24T17:30:12.784194    Author:   superFBI

#LastModifyDate:　2023-10-24T17:22:06.594252    Author:   superFBI

#LastModifyDate:　2023-10-24T17:09:41.157514    Author:   superFBI

#LastModifyDate:　2023-10-24T15:12:45.818311    Author:   superFBI

#LastModifyDate:　2023-10-24T15:08:07.866358    Author:   superFBI

#LastModifyDate:　2023-10-24T14:32:52.162604    Author:   superFBI

#LastModifyDate:　2023-10-24T10:56:18.378382    Author:   superFBI

#LastModifyDate:　2023-10-24T10:48:22.096193    Author:   superFBI

#LastModifyDate:　2023-10-24T10:47:14.657601    Author:   superFBI

#LastModifyDate:　2023-10-24T10:45:09.627532    Author:   superFBI

#LastModifyDate:　2023-10-24T10:21:34.195567    Author:   superFBI

#LastModifyDate:　2023-10-24T10:18:06.019077    Author:   superFBI

#LastModifyDate:　2023-10-24T10:14:12.238344    Author:   superFBI

#LastModifyDate:　2023-10-24T10:10:33.007715    Author:   superFBI

#LastModifyDate:　2023-10-24T10:04:30.936239    Author:   superFBI

#LastModifyDate:　2023-10-24T10:03:05.269543    Author:   superFBI

#LastModifyDate:　2023-10-23T18:52:30.310979    Author:   superFBI

#LastModifyDate:　2023-10-23T17:47:17.127176    Author:   superFBI

#LastModifyDate:　2023-10-23T17:36:21.828467    Author:   superFBI

#LastModifyDate:　2023-10-23T17:33:35.831691    Author:   superFBI

#LastModifyDate:　2023-10-23T17:32:58.352859    Author:   superFBI

#LastModifyDate:　2023-10-23T17:28:29.748070    Author:   superFBI

#LastModifyDate:　2023-10-23T17:28:09.645081    Author:   superFBI

#LastModifyDate:　2023-10-23T17:26:13.748699    Author:   superFBI

#LastModifyDate:　2023-10-23T17:21:24.867213    Author:   superFBI

#LastModifyDate:　2023-10-23T14:19:06.470813    Author:   superFBI

#LastModifyDate:　2023-10-23T11:17:19.576493    Author:   superFBI

#LastModifyDate:　2023-10-23T10:29:45.530226    Author:   superFBI

#xlink脚本

#file: h_d_analysis.xlk

#name: http与dbms数据进行分析

#描述： 对数据进行分析关联

#查看流计算服务

#a = @udf FBI.x_finder3_list

#启动

#a = @udf FBI.x_finder3_start with h_d_analysis

#停止

#a = @udf FBI.x_finder3_stop with h_d_analysis

#查询错误日志

#a = load ssdb by ssdb0 query qrange,X_log:h_d_analysis,0,1000

#查看xlink内部信息, 每５秒更新

#在对象查看器里输入　printf::h_d_analysis

#断点调试

#debug_on(1)

#初始化

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	stream["meta_name"] = "http与dbms数据进行分析"
	stream["meta_desc"] = "对数据进行分析关联"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["source"]={"link":stream["redis_link"]+":6380","topic":"h_d_data","redis":"list"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	stream["st"]["st_30s"]={"times":30,"fun":"print30"}
	#自定义的统计变量
	stream["count"] = 0
	stream["count-10"] = 0
	#创建文件作为存储数据容器
	stream["h_d"]=load_pkl("/data/xlink/h_d.pkl")
	stream["merge_hd"]=load_pkl("/data/xlink/merge_hd.pkl")
	stream["db_data"]=load_pkl("/data/xlink/db_data.pkl")
	pool["ckh"] = []
	stream["CKH"] = CKH_Client(host="127.0.0.1",port=19000,user="default",password="client")
#end 

#事件处理函数

#事件处理函数
def Events(o,topic=''):
	#开始进行判断 首先判断其ip地址问题，在进行时间上的判断
	pro_type=o.get("pro_type","")
	
	if pro_type=="http":
		age=o.get("age")
		id=o.get("id")
		#pro_type=o.get("pro_type")
		#printf("pro",pro_type)
		srcip=o.get("srcip")
		dstip=o.get("dstip")
		urld=o.get("urld")
		request_body=o.get("request_body")
		app=o.get("app","")
		srcport=o.get("srcport")
		dstport=o.get("dstport")
		times_obj=o.get("time")
		api_type=o.get("api_type")
		#获取起始时间
		start_times_obj=iso_to_datetime(o["start"])
		#判断数据库容器中是否包含数据
		if stream["db_data"]:
			#判断时间
			for db_times,value in stream["db_data"].items():
				db_sql=value[0]
				db_srcip=value[1]
				db_dstip=value[2]
				d_h_con=(db_srcip == srcip and db_dstip==dstip) or db_srcip==dstip
				if (db_times >= start_times_obj and db_times <= times_obj) and d_h_con:
					#符合条件直接存储好吧
					db_data=clone_event(value)
					db_data["id"]=id
					db_data["h_req_body"]=request_body
					db_data["timestamp"]=times_obj
					db_data["h_srcip"]=srcip
					db_data["h_dstip"]=dstip
					db_data["h_srcport"]=srcport
					db_data["h_dstport"]=dstport
					db_data["h_app"]=app
					db_data["h_url"]=urld
					#对数据进行添加
					if id not in stream["merge_hd"]:
						stream["merge_hd"][id]=[]
						stream["merge_hd"][id].append(urld)
						stream["merge_hd"][id].append(db_sql)
					else:
						if db_sql not in stream["merge_hd"][id] and len(stream["merge_hd"][id])<=20:
							stream["merge_hd"][id].append(db_sql)
					to_pool("ckh",db_data)
					stream["count"]+=1
			#只要db时间小于http起始时间的,如果http起始时间大于db时间,那将毫无意义
			
			stream["db_data"]={db_times:value for db_times,value in stream["db_data"].items() if start_times_obj<db_times}
		#判断时间段键值是否存在字典中
		if id not in stream["h_d"]:
			stream["h_d"][id]=[]
			stream["h_d"][id].append(start_times_obj)
			stream["h_d"][id].append(times_obj)
			stream["h_d"][id].append(urld)
			stream["h_d"][id].append(request_body)
			stream["h_d"][id].append(app)
			stream["h_d"][id].append(srcip)
			stream["h_d"][id].append(dstip)
			stream["h_d"][id].append(srcport)
			stream["h_d"][id].append(dstport)
			stream["h_d"][id].append(int(api_type))
		stream["h_d"]={id:value for id,value in stream["h_d"].items() if start_times_obj>value[1]}
		#printf("h_d",stream["h_d"])
	else:
		#printf("types","这是mysql")
		timestamp=o.get("timestamp")
		if timestamp:
			id=o.get("id")
			pro_type=o.get("db_type")
			#printf("pro",pro_type)
			srcip=o.get("src_ip")
			dstip=o.get("dest_ip")
			sqls=o.get("sql")
			col_list=o.get("col_list")
			db=o.get("db","")
			srcport=o.get("src_port")
			dstport=o.get("dest_port")
			#times_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
			times_obj=timestamp
			md5=o.get("md5")
			user=o.get("user")
			#将db数据存储起来（db比http速度快情况下，将时间作为主键） 存储数据库信息
			if times_obj not in stream["db_data"]:
				if sqls!="ROLLBACK" and sqls!="COMMIT" and sqls!="":
					stream["db_data"][times_obj]=[]
					db_id=stream["db_data"][times_obj]
					db_id.append(sqls)
					db_id.append(srcip)
					db_id.append(dstip)
					db_id.append(col_list)
					db_id.append(db)
					db_id.append(srcport)
					db_id.append(dstport)
					db_id.append(md5)
					db_id.append(user)
					db_id.append(pro_type)
			#判断http容器中是否存在数据
			if stream["h_d"]:
				for h_id,value in stream["h_d"].items():
					#用于存储id，url与mysql的分组数据
					h_srcip=value[5] 
					h_dstip=value[6]
					#针对mysql与http的IP相同的情况进行
					ip_t_f=(h_srcip == srcip and h_dstip == dstip) or (h_dstip == srcip)
					if (times_obj >= value[0] and times_obj <= value[1]) and ip_t_f:
						url_d=value[2]
						#存储数据信息，以http_id作为键值
						#存储数据信息，以http_id作为键值
						if h_id not in stream["merge_hd"]:
							stream["merge_hd"][h_id]=[]
							stream["merge_hd"][h_id].append(url_d)
							stream["merge_hd"][h_id].append(sqls)
						else:
							if sqls not in stream["merge_hd"][h_id] and len(stream["merge_hd"][h_id])<=20 and sqls!="COMMIT" and sqls!="ROLLBACK" and sqls!="":
								stream["merge_hd"][h_id].append(sqls)
						data=clone_event(o)
						data["id"]=h_id
						data["timestamp"]=times_obj
						data["pro_type"]=pro_type
						datas=h_clone_event(value,data)
						datas["h_url"]=url_d
						to_pool("ckh",datas)
						stream["count"]+=1
#end 

#系统定时函数

#系统定时函数，st为时间戳 
def print10(st):
	store_ckh(pool["ckh"],"hd_analysis")
	printf("总数","%s==sum==%d"%(st,stream["count"]))
	printf("10秒统计数","%s==10===%d"%(st,stream["count-10"]))
	stream["count-10"] = 0
	
#end 

#系统定时函数，st为时间戳 
def print30(st):
	my_dict_copy=stream["h_d"].copy()
	temp_dic(my_dict_copy,"/data/xlink/h_d.pkl")
	#dump_pkl("/data/xlink/h_d.pkl",my_dict_copy)
	merge_hd_copy=stream["merge_hd"].copy()
	#temp_dic(merge_hd_copy,"/data/xlink/merge_hd.pkl")
	dump_pkl("/data/xlink/merge_hd.pkl",merge_hd_copy)
	db_data=stream["db_data"].copy()
	#dump_pkl("/data/xlink/db_data.pkl",db_data)
	temp_dic(db_data,"/data/xlink/db_data.pkl")
	file="/data/xlink/merge_hd.pkl"
	counts=1000
	res=d_l_pkl(file,counts)
	if res:
		#删除当前文件，重新进行文件存储
		try:
			os.remove(file)
			stream["merge_hd"]=load_pkl(file)
		except:
			pass
			
#end 

#克隆一个新事件,创建一个新的变量，并返回

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def clone_event(o):
	if isinstance(o,dict):
		data={}
		data["sqls"]=o.get("sqls")
		data["d_srcip"]=o.get("src_ip")
		data["d_dstip"]=o.get("dest_ip")
		data["d_req"]=o.get("col_list")
		data["d_app"]=o.get("db","")
		
		data["d_srcport"]=o.get("src_port")
		data["d_dstport"]=o.get("dest_port")
		data["user"]=o.get("user")
		data["md5"]=o.get("md5")
		return data
	elif isinstance(o,list):
		data={}
		data["sqls"]=o[0]
		data["d_srcip"]=o[1]
		data["d_dstip"]=o[2]
		data["d_req"]=o[3]
		data["d_app"]=o[4]
		data["d_srcport"]=o[5]
		data["d_dstport"]=o[6]
		data["md5"]=o[7]
		data["user"]=o[8]
		data["pro_type"]=o[9]
		return data
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def h_clone_event(value,data):
	h_srcip=value[5]
	h_dstip=value[6]
	req_body=value[3]
	h_app=value[4]
	h_srcport=value[7]
	h_dstport=value[8]
	api_type=value[9]
	data["h_req_body"]=req_body
	
	data["h_srcip"]=h_srcip
	data["h_dstip"]=h_dstip
	data["h_srcport"]=h_srcport
	data["h_dstport"]=h_dstport
	data["h_app"]=h_app
	data["api_type"]=api_type
	return data
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
from datetime import timedelta,datetime
from mondic import *
#end 

#udf

#end 
