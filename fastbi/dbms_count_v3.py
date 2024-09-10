#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: dbms_count
#datetime: 2024-08-30T16:10:55.504038
#copyright: OpenFBI

import sys 
sys.path.append("./")
sys.path.append("/opt/openfbi/fbi-bin")
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/pylibs")
import threading
import time
from avenger.fglobals import *
from avenger.fbiobject import *
from avenger.fbiprocesser import *
from avenger.fbicluster import run_cluster


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
#end 




#begin

#主入口
def fbi_main(ptree):
	import resource
	resource.setrlimit(resource.RLIMIT_NOFILE,(10000,10000))
	t = threading.current_thread()
	if t.ident not in global_tasks:
		init_task(t,"")
	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]
	
	workspace = ptree["work_space"]
	
	
	ptree={'runtime': runtime, 'Action': 'use', 'use': '@FID'}
	ptree['use'] = replace_ps(ptree['use'],runtime)
	try:
		use_fun(ptree)
		workspace=ptree['work_space']
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[25]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_time', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dest_ip, ':', cast(dest_port as String)) AS dbms_obj,max(timestamp) AS last_time FROM dbms group by dbms_obj"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[29]原语 dbms_time = load ckh by ckh with SELECT CONCAT(des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms_time.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[30]原语 alter dbms_time.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[31]原语 dbms_obj = load db by mysql1 with select id,dbms_o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'dbms_time,dbms_obj', 'by': 'dbms_obj,dbms_obj'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[32]原语 last_time_data = join dbms_time,dbms_obj by dbms_o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[33]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[34]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select dest_ip,dest_port,user,max(timestamp) as timestamp from dbms where user !='' group by dest_ip,dest_port,user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[37]原语 dbms = load ckh by ckh with select dest_ip,dest_po... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[38]原语 alter dbms.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms', 'Action': 'add', 'add': 'dbms_obj', 'by': 'dbms["dest_ip"] + ":" + dbms["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[39]原语 dbms = add dbms_obj by dbms["dest_ip"] + ":" + dbm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'user,dbms_obj,timestamp'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[40]原语 dbms = loc dbms by user,dbms_obj,timestamp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_user', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,user,id from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[41]原语 dbms_user = load db by mysql1 with select dbms_obj... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'dbms_user,dbms', 'by': '[dbms_obj,user],[dbms_obj,user]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[42]原语 dbms = join dbms_user,dbms by [dbms_obj,user],[dbm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[43]原语 dbms = @udf dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'dbms', 'Action': 'order', 'order': 'dbms', 'by': 'timestamp', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[44]原语 dbms = order dbms by timestamp with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dbms', 'Action': 'distinct', 'distinct': 'dbms', 'by': 'dbms_obj,user'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[45]原语 dbms = distinct dbms by dbms_obj,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'dbms', 'Action': 'order', 'order': 'dbms', 'by': 'id', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[46]原语 dbms = order dbms by id with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dbms', 'as': '"timestamp":"last_time"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[47]原语 rename dbms as ("timestamp":"last_time") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[48]原语 alter dbms.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[49]原语 dbms = loc dbms by id,last_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[50]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[51]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'show create table dbms'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[52]原语 dbms = load ckh by ckh with show create table dbms... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct CONCAT(dest_ip, ':', cast(dest_port as String)) AS dbms_obj,src_ip src from dbms where src_ip != '127.0.0.1'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[55]原语 dbms = load ckh by ckh with select distinct CONCAT... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'dbms', 'Action': 'group', 'group': 'dbms', 'by': 'dbms_obj', 'agg': 'src:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[56]原语 dbms = group dbms by dbms_obj agg src:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[57]原语 dbms = @udf dbms by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,id from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[58]原语 a = load db by mysql1 with select dbms_obj,id from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'a,dbms', 'by': 'dbms_obj,dbms_obj', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[59]原语 dbms = join a,dbms by dbms_obj,dbms_obj with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[60]原语 dbms = @udf dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,src_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[61]原语 dbms = loc dbms by id,src_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[62]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[63]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select dbms_obj,user from dbms_user where user !=''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[65]原语 dbms = load db by mysql1 with select dbms_obj,user... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'dbms', 'Action': 'group', 'group': 'dbms', 'by': 'dbms_obj', 'agg': 'user:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[66]原语 dbms = group dbms by dbms_obj agg user:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[67]原语 dbms = @udf dbms by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,id from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[68]原语 a = load db by mysql1 with select dbms_obj,id from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'a,dbms', 'by': 'dbms_obj,dbms_obj', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[69]原语 dbms = join a,dbms by dbms_obj,dbms_obj with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[70]原语 dbms = @udf dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,user_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[71]原语 dbms = loc dbms by id,user_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[72]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[73]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select dest_ip,dest_port,count() count from dbms group by dest_ip,dest_port'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[75]原语 dbms = load ckh by ckh with select dest_ip,dest_po... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[76]原语 alter dbms.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms', 'Action': 'add', 'add': 'dbms_obj', 'by': 'dbms["dest_ip"] + ":" + dbms["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[77]原语 dbms = add dbms_obj by dbms["dest_ip"] + ":" + dbm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'dbms_obj,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[78]原语 dbms = loc dbms by dbms_obj,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,id from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[79]原语 a = load db by mysql1 with select dbms_obj,id from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'a,dbms', 'by': 'dbms_obj,dbms_obj', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[80]原语 dbms = join a,dbms by dbms_obj,dbms_obj with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[81]原语 dbms = @udf dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.count', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[82]原语 alter dbms.count as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[83]原语 dbms = loc dbms by id,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[84]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[85]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select dest_ip,dest_port,user,count() count from dbms where user !='' group by dest_ip,dest_port,user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[87]原语 dbms = load ckh by ckh with select dest_ip,dest_po... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[88]原语 alter dbms.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms', 'Action': 'add', 'add': 'dbms_obj', 'by': 'dbms["dest_ip"] + ":" + dbms["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[89]原语 dbms = add dbms_obj by dbms["dest_ip"] + ":" + dbm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'dbms_obj,user,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[90]原语 dbms = loc dbms by dbms_obj,user,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,user,id from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[91]原语 a = load db by mysql1 with select dbms_obj,user,id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'a,dbms', 'by': '[dbms_obj,user],[dbms_obj,user]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[92]原语 dbms = join a,dbms by [dbms_obj,user],[dbms_obj,us... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[93]原语 dbms = @udf dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.count', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[94]原语 alter dbms.count as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[95]原语 dbms = loc dbms by id,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[96]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[97]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select sql dbms_sql,count() count from dbms where cmd =='query' group by sql"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[99]原语 dbms = load ckh by ckh with select sql dbms_sql,co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_sql,id from dbms_sql'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[100]原语 a = load db by mysql1 with select dbms_sql,id from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'a,dbms', 'by': 'dbms_sql,dbms_sql', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[101]原语 dbms = join a,dbms by dbms_sql,dbms_sql with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[102]原语 dbms = @udf dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.count', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[103]原语 alter dbms.count as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[104]原语 dbms = loc dbms by id,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[105]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_sql'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[106]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct dest_ip,dest_port,req,resp,db_type from dbms where cmd = 'version'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[108]原语 dbms = load ckh by ckh with select distinct dest_i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_row_lambda', 'with': 'x: x["req"] if x["req"] != \'\' else x["resp"]'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[109]原语 dbms = @udf dbms by udf0.df_row_lambda with x: x["... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbms.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[110]原语 alter dbms.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms', 'Action': 'add', 'add': 'dbms_obj', 'by': 'dbms["dest_ip"] + ":" + dbms["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[111]原语 dbms = add dbms_obj by dbms["dest_ip"] + ":" + dbm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'dbms_obj,lambda1,db_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[112]原语 dbms = loc dbms by dbms_obj,lambda1,db_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dbms', 'as': '"lambda1":"version"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[113]原语 rename dbms as ("lambda1":"version") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select dbms_obj,id from dbms_obj where version =''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[114]原语 a = load db by mysql1 with select dbms_obj,id from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms', 'Action': 'join', 'join': 'a,dbms', 'by': 'dbms_obj,dbms_obj', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[115]原语 dbms = join a,dbms by dbms_obj,dbms_obj with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[116]原语 dbms = @udf dbms by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbms', 'Action': 'filter', 'filter': 'dbms', 'by': "db_type !=''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[117]原语 dbms = filter dbms by db_type !="" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id,version,db_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[118]原语 dbms = loc dbms by id,version,db_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[119]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[120]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_dbms.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[123]原语 sens = load pq by sensitive/sens_dbms.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[124]原语 alter sens.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'dest_ip', 'by': 'sens["dest_ip"] +\':\'+ sens["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[125]原语 sens = add dest_ip by sens["dest_ip"] +":"+ sens["... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens', 'by': "total_type == 'Sql语句'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[127]原语 sens1 = filter sens by total_type == "Sql语句" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens1', 'by': 'dest_ip,user,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[128]原语 sens1 = loc sens1 by dest_ip,user,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens1', 'Action': 'distinct', 'distinct': 'sens1', 'by': 'dest_ip,user,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[129]原语 sens1 = distinct sens1 by dest_ip,user,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('身份证','0')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[130]原语 sens1.key = str key by (replace("身份证","0")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('手机号','1')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[131]原语 sens1.key = str key by (replace("手机号","1")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('邮箱','2')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[132]原语 sens1.key = str key by (replace("邮箱","2")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('地址','3')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[133]原语 sens1.key = str key by (replace("地址","3")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('婚姻状况','4')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[134]原语 sens1.key = str key by (replace("婚姻状况","4")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('宗教信仰','5')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[135]原语 sens1.key = str key by (replace("宗教信仰","5")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('发票代码','6')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[136]原语 sens1.key = str key by (replace("发票代码","6")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人识别号或社会统一信用代码','7')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[137]原语 sens1.key = str key by (replace("纳税人识别号或社会统一信用代码",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人名称或公司名称','8')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[138]原语 sens1.key = str key by (replace("纳税人名称或公司名称","8"))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('银行卡号','9')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[139]原语 sens1.key = str key by (replace("银行卡号","9")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('收入','10')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[140]原语 sens1.key = str key by (replace("收入","10")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('姓名','11')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[141]原语 sens1.key = str key by (replace("姓名","11")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens1', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[143]原语 sens1 = filter sens1 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens1', 'Action': 'add', 'add': 'key', 'by': "sens1.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[145]原语 sens1 = add key by (sens1.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens2', 'Action': 'group', 'group': 'sens1', 'by': 'dest_ip,user', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[146]原语 sens2 = group sens1 by dest_ip,user agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens2.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[147]原语 sens2.key_sum = lambda key_sum by x:x.split(",")[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens2.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[148]原语 alter sens2.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens2.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[149]原语 sens2.key_sum = lambda key_sum by x:x.replace(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[150]原语 sens2 = @udf sens2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens2', 'as': '"key_sum":"req_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[151]原语 rename sens2 as ("key_sum":"req_label") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_user', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj,user from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[152]原语 dbms_user = load db by mysql1 with select id,dbms_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens2', 'Action': 'join', 'join': 'dbms_user,sens2', 'by': '[dbms_obj,user],[dest_ip,user]'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[153]原语 sens2 = join dbms_user,sens2 by [dbms_obj,user],[d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens2', 'Action': 'loc', 'loc': 'sens2', 'by': 'id,req_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[154]原语 sens2 = loc sens2 by id,req_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[155]原语 sens2 = @udf sens2 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[156]原语 sens2 = @udf sens2 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[159]原语 dbms = load db by mysql1 with select id,dbms_obj f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens1', 'Action': 'group', 'group': 'sens1', 'by': 'dest_ip', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[160]原语 sens1 = group sens1 by dest_ip agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[161]原语 sens1.key_sum = lambda key_sum by x:x.split(",")[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens1.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[162]原语 alter sens1.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[163]原语 sens1.key_sum = lambda key_sum by x:x.replace(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[164]原语 sens1 = @udf sens1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens1', 'as': '"key_sum":"req_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[165]原语 rename sens1 as ("key_sum":"req_label") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens1', 'Action': 'join', 'join': 'dbms,sens1', 'by': 'dbms_obj,dest_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[167]原语 sens1 = join dbms,sens1 by dbms_obj,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens1', 'by': 'id,req_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[168]原语 sens1 = loc sens1 by id,req_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[169]原语 sens1 = @udf sens1 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[170]原语 sens1 = @udf sens1 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens3', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_dbms.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[174]原语 sens3 = load load pq by sensitive/sens_dbms.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens3.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[175]原语 alter sens3.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens3', 'Action': 'add', 'add': 'dest_ip', 'by': 'sens3["dest_ip"] +\':\'+ sens3["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[176]原语 sens3 = add dest_ip by sens3["dest_ip"] +":"+ sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens4', 'Action': 'filter', 'filter': 'sens3', 'by': "total_type == 'Sql语句'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[178]原语 sens4 = filter sens3 by total_type == "Sql语句" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens4', 'Action': 'loc', 'loc': 'sens4', 'by': 'dest_ip,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[179]原语 sens4 = loc sens4 by dest_ip,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens4', 'Action': 'distinct', 'distinct': 'sens4', 'by': 'dest_ip,key,num'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[180]原语 sens4 = distinct sens4 by dest_ip,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens4', 'Action': 'filter', 'filter': 'sens4', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[182]原语 sens4 = filter sens4 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens4', 'Action': 'group', 'group': 'sens4', 'by': 'dest_ip,key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[183]原语 sens4 = group sens4 by dest_ip,key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens4', 'Action': '@udf', '@udf': 'sens4', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[184]原语 sens4 = @udf sens4 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens4.num_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[185]原语 alter sens4.num_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens4', 'Action': 'add', 'add': 'key_count', 'by': 'sens4["key"]+"("+sens4["num_sum"]+")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[186]原语 sens4 = add key_count by (sens4["key"]+"("+sens4["... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens4', 'Action': 'add', 'add': 'key_count1', 'by': "sens4.key_count+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[187]原语 sens4 = add key_count1 by (sens4.key_count+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens4', 'Action': 'loc', 'loc': 'sens4', 'by': 'dest_ip,key_count1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[188]原语 sens4 = loc sens4 by dest_ip,key_count1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens5', 'Action': 'group', 'group': 'sens4', 'by': 'dest_ip', 'agg': 'key_count1:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[189]原语 sens5 = group sens4 by dest_ip agg key_count1:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens5', 'Action': '@udf', '@udf': 'sens5', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[190]原语 sens5 = @udf sens5 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[191]原语 dbms_obj = load db by mysql1 with select id,dbms_o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens5', 'Action': 'join', 'join': 'dbms_obj,sens5', 'by': 'dbms_obj,dest_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[192]原语 sens5 = join dbms_obj,sens5 by dbms_obj,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens5', 'Action': 'loc', 'loc': 'sens5', 'by': 'id,key_count1_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[193]原语 sens5 = loc sens5 by id,key_count1_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens5', 'as': '"key_count1_sum":"req_label_count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[194]原语 rename sens5 as ("key_count1_sum":"req_label_count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens5', 'Action': '@udf', '@udf': 'sens5', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[195]原语 sens5 = @udf sens5 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens5.req_label_count', 'Action': 'lambda', 'lambda': 'req_label_count', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[196]原语 sens5.req_label_count = lambda  req_label_count by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens5', 'Action': '@udf', '@udf': 'sens5', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[197]原语 sens5 = @udf sens5 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens_0', 'Action': 'filter', 'filter': 'sens', 'by': "total_type == 'Sql语句'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[199]原语 sens_0 = filter sens by total_type == "Sql语句" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens_0', 'Action': 'loc', 'loc': 'sens_0', 'by': 'dest_ip,user,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[200]原语 sens_0 = loc sens_0 by dest_ip,user,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens_0', 'Action': 'distinct', 'distinct': 'sens_0', 'by': 'dest_ip,user,key,num'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[201]原语 sens_0 = distinct sens_0 by dest_ip,user,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens_0', 'Action': 'filter', 'filter': 'sens_0', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[203]原语 sens_0 = filter sens_0 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_0.num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[204]原语 alter sens_0.num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens_1', 'Action': 'group', 'group': 'sens_0', 'by': 'dest_ip,user,key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[206]原语 sens_1 = group sens_0 by dest_ip,user,key agg num:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens_1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[207]原语 sens_1 = @udf sens_1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_1.num_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[208]原语 alter sens_1.num_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_1', 'Action': 'add', 'add': 'key', 'by': "sens_1.key+'('+sens_1.num_sum+')'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[209]原语 sens_1 = add key by (sens_1.key+"("+sens_1.num_sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_1.num_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[210]原语 alter sens_1.num_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_1', 'Action': 'add', 'add': 'key', 'by': "sens_1.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[211]原语 sens_1 = add key by (sens_1.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens_1', 'Action': 'group', 'group': 'sens_1', 'by': 'dest_ip,user', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[212]原语 sens_1 = group sens_1 by dest_ip,user agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens_1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[213]原语 sens_1.key_sum = lambda key_sum by (x:x[0:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens_1', 'as': '"key_sum":"req_label_count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[214]原语 rename sens_1 as ("key_sum":"req_label_count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_user', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj,user from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[215]原语 dbms_user = load db by mysql1 with select id,dbms_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens_1', 'Action': 'join', 'join': 'dbms_user,sens_1', 'by': '[dbms_obj,user],[dest_ip,user]'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[216]原语 sens_1 = join dbms_user,sens_1 by [dbms_obj,user],... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens_1', 'Action': 'loc', 'loc': 'sens_1', 'by': 'id,req_label_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[217]原语 sens_1 = loc sens_1 by id,req_label_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens_1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[218]原语 sens_1 = @udf sens_1 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens_1', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[219]原语 sens_1 = @udf sens_1 by CRUD.save_table with (mysq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens', 'by': "total_type == 'Msg值'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[224]原语 sens1 = filter sens by total_type == "Msg值" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens1', 'by': 'dest_ip,user,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[225]原语 sens1 = loc sens1 by dest_ip,user,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens1', 'Action': 'distinct', 'distinct': 'sens1', 'by': 'dest_ip,user,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[226]原语 sens1 = distinct sens1 by dest_ip,user,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('身份证','0')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[227]原语 sens1.key = str key by (replace("身份证","0")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('手机号','1')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[228]原语 sens1.key = str key by (replace("手机号","1")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('邮箱','2')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[229]原语 sens1.key = str key by (replace("邮箱","2")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('地址','3')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[230]原语 sens1.key = str key by (replace("地址","3")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('婚姻状况','4')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[231]原语 sens1.key = str key by (replace("婚姻状况","4")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('宗教信仰','5')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[232]原语 sens1.key = str key by (replace("宗教信仰","5")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('发票代码','6')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[233]原语 sens1.key = str key by (replace("发票代码","6")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人识别号或社会统一信用代码','7')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[234]原语 sens1.key = str key by (replace("纳税人识别号或社会统一信用代码",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人名称或公司名称','8')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[235]原语 sens1.key = str key by (replace("纳税人名称或公司名称","8"))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('银行卡号','9')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[236]原语 sens1.key = str key by (replace("银行卡号","9")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('收入','10')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[237]原语 sens1.key = str key by (replace("收入","10")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens1.key', 'Action': 'str', 'str': 'key', 'by': "replace('姓名','11')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[238]原语 sens1.key = str key by (replace("姓名","11")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens1', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[240]原语 sens1 = filter sens1 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens1', 'Action': 'add', 'add': 'key', 'by': "sens1.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[242]原语 sens1 = add key by (sens1.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens2', 'Action': 'group', 'group': 'sens1', 'by': 'dest_ip,user', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[243]原语 sens2 = group sens1 by dest_ip,user agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens2.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[244]原语 sens2.key_sum = lambda key_sum by x:x.split(",")[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens2.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[245]原语 alter sens2.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens2.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[246]原语 sens2.key_sum = lambda key_sum by x:x.replace(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[247]原语 sens2 = @udf sens2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens2', 'as': '"key_sum":"res_llabel"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[248]原语 rename sens2 as ("key_sum":"res_llabel") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_user', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj,user from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[249]原语 dbms_user = load db by mysql1 with select id,dbms_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens2', 'Action': 'join', 'join': 'dbms_user,sens2', 'by': '[dbms_obj,user],[dest_ip,user]'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[250]原语 sens2 = join dbms_user,sens2 by [dbms_obj,user],[d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens2', 'Action': 'loc', 'loc': 'sens2', 'by': 'id,res_llabel'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[251]原语 sens2 = loc sens2 by id,res_llabel 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[252]原语 sens2 = @udf sens2 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens2', 'Action': '@udf', '@udf': 'sens2', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[253]原语 sens2 = @udf sens2 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens1', 'Action': 'group', 'group': 'sens1', 'by': 'dest_ip', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[256]原语 sens1 = group sens1 by dest_ip agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[257]原语 sens1.key_sum = lambda key_sum by x:x.split(",")[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens1.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[258]原语 alter sens1.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[259]原语 sens1.key_sum = lambda key_sum by x:x.replace(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[260]原语 sens1 = @udf sens1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens1', 'as': '"key_sum":"res_llabel"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[262]原语 rename sens1 as ("key_sum":"res_llabel") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[263]原语 dbms = load db by mysql1 with select id,dbms_obj f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens1', 'Action': 'join', 'join': 'dbms,sens1', 'by': 'dbms_obj,dest_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[264]原语 sens1 = join dbms,sens1 by dbms_obj,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens1', 'by': 'id,res_llabel'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[265]原语 sens1 = loc sens1 by id,res_llabel 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[266]原语 sens1 = @udf sens1 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[267]原语 sens1 = @udf sens1 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens3', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_dbms.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[271]原语 sens3 = load pq by sensitive/sens_dbms.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens3.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[272]原语 alter sens3.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens3', 'Action': 'add', 'add': 'dest_ip', 'by': 'sens3["dest_ip"] +\':\'+ sens3["dest_port"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[273]原语 sens3 = add dest_ip by sens3["dest_ip"] +":"+ sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens4', 'Action': 'filter', 'filter': 'sens3', 'by': "total_type == 'Msg值'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[274]原语 sens4 = filter sens3 by total_type == "Msg值" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens4', 'Action': 'loc', 'loc': 'sens4', 'by': 'dest_ip,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[275]原语 sens4 = loc sens4 by dest_ip,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens4', 'Action': 'distinct', 'distinct': 'sens4', 'by': 'dest_ip,key,num'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[276]原语 sens4 = distinct sens4 by dest_ip,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens4', 'Action': 'filter', 'filter': 'sens4', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[278]原语 sens4 = filter sens4 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens4', 'Action': 'group', 'group': 'sens4', 'by': 'dest_ip,key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[279]原语 sens4 = group sens4 by dest_ip,key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens4', 'Action': '@udf', '@udf': 'sens4', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[280]原语 sens4 = @udf sens4 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens4.num_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[281]原语 alter sens4.num_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens4', 'Action': 'add', 'add': 'key_count', 'by': 'sens4["key"]+"("+sens4["num_sum"]+")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[282]原语 sens4 = add key_count by (sens4["key"]+"("+sens4["... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens4', 'Action': 'add', 'add': 'key_count1', 'by': "sens4.key_count+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[283]原语 sens4 = add key_count1 by (sens4.key_count+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens4', 'Action': 'loc', 'loc': 'sens4', 'by': 'dest_ip,key_count1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[284]原语 sens4 = loc sens4 by dest_ip,key_count1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens5', 'Action': 'group', 'group': 'sens4', 'by': 'dest_ip', 'agg': 'key_count1:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[285]原语 sens5 = group sens4 by dest_ip agg key_count1:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens5', 'Action': '@udf', '@udf': 'sens5', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[286]原语 sens5 = @udf sens5 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[287]原语 dbms_obj = load db by mysql1 with select id,dbms_o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens5', 'Action': 'join', 'join': 'dbms_obj,sens5', 'by': 'dbms_obj,dest_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[288]原语 sens5 = join dbms_obj,sens5 by dbms_obj,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens5', 'Action': 'loc', 'loc': 'sens5', 'by': 'id,key_count1_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[289]原语 sens5 = loc sens5 by id,key_count1_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens5', 'as': '"key_count1_sum":"res_llabel_count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[290]原语 rename sens5 as ("key_count1_sum":"res_llabel_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens5', 'Action': '@udf', '@udf': 'sens5', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[291]原语 sens5 = @udf sens5 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens5.res_llabel_count', 'Action': 'lambda', 'lambda': 'res_llabel_count', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[292]原语 sens5.res_llabel_count = lambda  res_llabel_count ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens5', 'Action': '@udf', '@udf': 'sens5', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[293]原语 sens5 = @udf sens5 by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens_0', 'Action': 'filter', 'filter': 'sens', 'by': "total_type == 'Msg值'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[295]原语 sens_0 = filter sens by total_type == "Msg值" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens_0', 'Action': 'loc', 'loc': 'sens_0', 'by': 'dest_ip,user,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[296]原语 sens_0 = loc sens_0 by dest_ip,user,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sens_0', 'Action': 'distinct', 'distinct': 'sens_0', 'by': 'dest_ip,user,key,num'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[297]原语 sens_0 = distinct sens_0 by dest_ip,user,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens_0', 'Action': 'filter', 'filter': 'sens_0', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[299]原语 sens_0 = filter sens_0 by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_0.num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[300]原语 alter sens_0.num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens_1', 'Action': 'group', 'group': 'sens_0', 'by': 'dest_ip,user,key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[302]原语 sens_1 = group sens_0 by dest_ip,user,key agg num:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens_1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[303]原语 sens_1 = @udf sens_1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_1.num_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[304]原语 alter sens_1.num_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_1', 'Action': 'add', 'add': 'key', 'by': "sens_1.key+'('+sens_1.num_sum+')'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[305]原语 sens_1 = add key by (sens_1.key+"("+sens_1.num_sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_1.num_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[306]原语 alter sens_1.num_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_1', 'Action': 'add', 'add': 'key', 'by': "sens_1.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[307]原语 sens_1 = add key by (sens_1.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens_1', 'Action': 'group', 'group': 'sens_1', 'by': 'dest_ip,user', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[308]原语 sens_1 = group sens_1 by dest_ip,user agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens_1.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[309]原语 sens_1.key_sum = lambda key_sum by (x:x[0:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens_1', 'as': '"key_sum":"res_llabel_count"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[310]原语 rename sens_1 as ("key_sum":"res_llabel_count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_user', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dbms_obj,user from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[311]原语 dbms_user = load db by mysql1 with select id,dbms_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens_1', 'Action': 'join', 'join': 'dbms_user,sens_1', 'by': '[dbms_obj,user],[dest_ip,user]'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[312]原语 sens_1 = join dbms_user,sens_1 by [dbms_obj,user],... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens_1', 'Action': 'loc', 'loc': 'sens_1', 'by': 'id,res_llabel_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[313]原语 sens_1 = loc sens_1 by id,res_llabel_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens_1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[314]原语 sens_1 = @udf sens_1 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens_1', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[315]原语 sens_1 = @udf sens_1 by CRUD.save_table with (mysq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_level', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[320]原语 sen_level = load ssdb by ssdb0 with sensitive as j... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_level', 'Action': '@udf', '@udf': 'sen_level', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[321]原语 sen_level = @udf sen_level by FBI.json2df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_level.data', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[322]原语 alter sen_level.data as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sen_level.sensitive_label', 'Action': 'str', 'str': 'data', 'by': 'findall("level\': \'(.*?)\'")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[323]原语 sen_level.sensitive_label = str data by (findall("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sen_level.key', 'Action': 'str', 'str': 'data', 'by': 'findall("rekey\': \'(.*?)\',")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[324]原语 sen_level.key = str data by (findall("rekey": "(.*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_level', 'Action': '@udf', '@udf': 'sen_level', 'by': 'udf0.df_drop_col', 'with': 'data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[325]原语 sen_level = @udf sen_level by udf0.df_drop_col wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_level.key', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[326]原语 alter sen_level.key as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_level.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[327]原语 alter sen_level.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_level.key', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x[2:-2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[328]原语 sen_level.key = lambda key by (x:x[2:-2]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_level.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x[2:-2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[329]原语 sen_level.sensitive_label = lambda sensitive_label... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_dbms', 'Action': 'loc', 'loc': 'sens', 'by': 'dest_ip,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[331]原语 sen_dbms = loc sens by dest_ip,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_dbms', 'Action': 'join', 'join': 'sen_dbms,sen_level', 'by': 'key,key', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[332]原语 sen_dbms = join sen_dbms,sen_level by key,key with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[333]原语 sen_dbms = @udf sen_dbms by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_dbms', 'Action': 'filter', 'filter': 'sen_dbms', 'by': 'sensitive_label != ""'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[334]原语 sen_dbms = filter sen_dbms by sensitive_label != "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_drop_col', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[335]原语 sen_dbms = @udf sen_dbms by udf0.df_drop_col with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sen_dbms', 'Action': 'distinct', 'distinct': 'sen_dbms', 'by': 'dest_ip,sensitive_label'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[336]原语 sen_dbms = distinct sen_dbms by dest_ip,sensitive_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_dbms.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[337]原语 alter sen_dbms.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x + \',\' if x != "" else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[338]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_dbms', 'Action': 'group', 'group': 'sen_dbms', 'by': 'dest_ip', 'agg': 'sensitive_label:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[339]原语 sen_dbms = group sen_dbms by dest_ip agg sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[340]原语 sen_dbms = @udf sen_dbms by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_dbms', 'as': '"sensitive_label_sum":"sensitive_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[341]原语 rename sen_dbms as ("sensitive_label_sum":"sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'3' if '3' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[342]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'2' if '2' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[343]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'1' if '1' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[344]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,id from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[345]原语 dbms_obj = load db by mysql1 with select dbms_obj,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms_obj', 'Action': 'join', 'join': 'dbms_obj,sen_dbms', 'by': 'dbms_obj,dest_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[346]原语 dbms_obj = join dbms_obj,sen_dbms by dbms_obj,dest... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms_obj', 'Action': '@udf', '@udf': 'dbms_obj', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[347]原语 dbms_obj = @udf dbms_obj by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms_obj', 'Action': 'loc', 'loc': 'dbms_obj', 'by': 'sensitive_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[348]原语 dbms_obj = loc dbms_obj by sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms_obj', 'Action': '@udf', '@udf': 'dbms_obj', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[349]原语 dbms_obj = @udf dbms_obj by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_dbms', 'Action': 'loc', 'loc': 'sens', 'by': 'dest_ip,user,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[351]原语 sen_dbms = loc sens by dest_ip,user,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_dbms', 'Action': 'join', 'join': 'sen_dbms,sen_level', 'by': 'key,key', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[352]原语 sen_dbms = join sen_dbms,sen_level by key,key with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[353]原语 sen_dbms = @udf sen_dbms by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_dbms', 'Action': 'filter', 'filter': 'sen_dbms', 'by': 'sensitive_label != ""'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[354]原语 sen_dbms = filter sen_dbms by sensitive_label != "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_drop_col', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[355]原语 sen_dbms = @udf sen_dbms by udf0.df_drop_col with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sen_dbms', 'Action': 'distinct', 'distinct': 'sen_dbms', 'by': 'dest_ip,user,sensitive_label'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[356]原语 sen_dbms = distinct sen_dbms by dest_ip,user,sensi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_dbms.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[357]原语 alter sen_dbms.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x + \',\' if x != "" else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[358]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_dbms', 'Action': 'group', 'group': 'sen_dbms', 'by': 'dest_ip,user', 'agg': 'sensitive_label:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[359]原语 sen_dbms = group sen_dbms by dest_ip,user agg sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[360]原语 sen_dbms = @udf sen_dbms by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_dbms', 'as': '"sensitive_label_sum":"sensitive_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[361]原语 rename sen_dbms as ("sensitive_label_sum":"sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'3' if '3' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[362]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'2' if '2' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[363]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_dbms.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'1' if '1' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[364]原语 sen_dbms.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dbms_obj,user,id from dbms_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[365]原语 dbms_obj = load db by mysql1 with select dbms_obj,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbms_obj', 'Action': 'join', 'join': 'dbms_obj,sen_dbms', 'by': '[dbms_obj,user],[dest_ip,user]'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[366]原语 dbms_obj = join dbms_obj,sen_dbms by [dbms_obj,use... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms_obj', 'Action': '@udf', '@udf': 'dbms_obj', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[367]原语 dbms_obj = @udf dbms_obj by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms_obj', 'Action': 'loc', 'loc': 'dbms_obj', 'by': 'sensitive_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[368]原语 dbms_obj = loc dbms_obj by sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms_obj', 'Action': '@udf', '@udf': 'dbms_obj', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[369]原语 dbms_obj = @udf dbms_obj by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct sha256 md5,rekey key from datafilter'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[371]原语 file = load ckh by ckh with select distinct sha256... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'fileinfo', 'Action': 'distinct', 'distinct': 'file', 'by': 'md5,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[372]原语 fileinfo = distinct file by md5,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('身份证','0')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[373]原语 fileinfo.key = str key by (replace("身份证","0")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('手机号','1')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[374]原语 fileinfo.key = str key by (replace("手机号","1")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('邮箱','2')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[375]原语 fileinfo.key = str key by (replace("邮箱","2")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('地址','3')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[376]原语 fileinfo.key = str key by (replace("地址","3")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('婚姻状况','4')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[377]原语 fileinfo.key = str key by (replace("婚姻状况","4")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('宗教信仰','5')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[378]原语 fileinfo.key = str key by (replace("宗教信仰","5")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('发票代码','6')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[379]原语 fileinfo.key = str key by (replace("发票代码","6")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人识别号或社会统一信用代码','7')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[380]原语 fileinfo.key = str key by (replace("纳税人识别号或社会统一信用代... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('纳税人名称或公司名称','8')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[381]原语 fileinfo.key = str key by (replace("纳税人名称或公司名称","8... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('银行卡号','9')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[382]原语 fileinfo.key = str key by (replace("银行卡号","9")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('收入','10')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[383]原语 fileinfo.key = str key by (replace("收入","10")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'fileinfo.key', 'Action': 'str', 'str': 'key', 'by': "replace('姓名','11')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[384]原语 fileinfo.key = str key by (replace("姓名","11")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'fileinfo', 'Action': 'filter', 'filter': 'fileinfo', 'by': 'key !="发票号码"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[386]原语 fileinfo = filter fileinfo by key !="发票号码" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'key', 'by': "fileinfo.key+','"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[388]原语 fileinfo = add key by (fileinfo.key+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'fileinfo', 'Action': 'group', 'group': 'fileinfo', 'by': 'md5', 'agg': 'key:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[389]原语 fileinfo = group fileinfo by md5 agg key:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'fileinfo.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.split(",")[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[390]原语 fileinfo.key_sum = lambda key_sum by x:x.split(","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'fileinfo.key_sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[391]原语 alter fileinfo.key_sum as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'fileinfo.key_sum', 'Action': 'lambda', 'lambda': 'key_sum', 'by': 'x:x.replace("\'",\'"\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[392]原语 fileinfo.key_sum = lambda key_sum by x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'fileinfo', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[393]原语 fileinfo = @udf fileinfo by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fileinfo', 'as': '"key_sum":"sen_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[394]原语 rename fileinfo as ("key_sum":"sen_label") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_obj', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select md5,id from fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[395]原语 file_obj = load db by mysql1 with select md5,id fr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'file_obj', 'Action': 'join', 'join': 'file_obj,fileinfo', 'by': 'md5,md5'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[396]原语 file_obj = join file_obj,fileinfo by md5,md5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_obj', 'Action': 'loc', 'loc': 'file_obj', 'by': 'id,sen_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[397]原语 file_obj = loc file_obj by id,sen_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_obj', 'Action': '@udf', '@udf': 'file_obj', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[398]原语 file_obj = @udf file_obj by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_obj', 'Action': '@udf', '@udf': 'file_obj', 'by': 'CRUD.save_table', 'with': 'mysql1,fileinfo'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[399]原语 file_obj = @udf file_obj by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'file_level', 'Action': 'distinct', 'distinct': 'file', 'by': 'md5,key'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[401]原语 file_level = distinct file by md5,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_file', 'Action': 'join', 'join': 'file_level,sen_level', 'by': 'key,key', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[402]原语 sen_file = join file_level,sen_level by key,key wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_file', 'Action': '@udf', '@udf': 'sen_file', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[403]原语 sen_file = @udf sen_file by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_file', 'Action': 'filter', 'filter': 'sen_file', 'by': 'sensitive_label != ""'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[404]原语 sen_file = filter sen_file by sensitive_label != "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_file', 'Action': '@udf', '@udf': 'sen_file', 'by': 'udf0.df_drop_col', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[405]原语 sen_file = @udf sen_file by udf0.df_drop_col with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'sen_file', 'Action': 'distinct', 'distinct': 'sen_file', 'by': 'md5,sensitive_label'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[406]原语 sen_file = distinct sen_file by md5,sensitive_labe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_file.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[407]原语 alter sen_file.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_file.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:x + \',\' if x != "" else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[408]原语 sen_file.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_file', 'Action': 'group', 'group': 'sen_file', 'by': 'md5', 'agg': 'sensitive_label:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[409]原语 sen_file = group sen_file by md5 agg sensitive_lab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_file', 'Action': '@udf', '@udf': 'sen_file', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[410]原语 sen_file = @udf sen_file by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_file', 'as': '"sensitive_label_sum":"sensitive_label"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[411]原语 rename sen_file as ("sensitive_label_sum":"sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_file.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'3' if '3' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[412]原语 sen_file.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_file.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'2' if '2' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[413]原语 sen_file.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_file.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': "x:'1' if '1' in x else x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[414]原语 sen_file.sensitive_label = lambda sensitive_label ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select md5,id from fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[415]原语 fileinfo = load db by mysql1 with select md5,id fr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'fileinfo', 'Action': 'join', 'join': 'fileinfo,sen_file', 'by': 'md5,md5'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[416]原语 fileinfo = join fileinfo,sen_file by md5,md5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'fileinfo', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[417]原语 fileinfo = @udf fileinfo by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'fileinfo', 'Action': 'loc', 'loc': 'fileinfo', 'by': 'sensitive_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[418]原语 fileinfo = loc fileinfo by sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'fileinfo', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'CRUD.save_table', 'with': 'mysql1,fileinfo'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[419]原语 fileinfo = @udf fileinfo by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[dbms_count.fbi]执行第[421]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],424

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



