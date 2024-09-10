#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: file_count
#datetime: 2024-08-30T16:10:55.838496
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
		add_the_error('[file_count.fbi]执行第[6]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_http', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(srcip, ':', cast(srcport as String)) AS file_server,max(timestamp) AS last_time FROM api_fileinfo where app_proto == 'http' group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[8]原语 file_http = load ckh by ckh with SELECT CONCAT(src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'file_http.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[9]原语 alter file_http.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'http'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[10]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_http', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[11]原语 last_time_data = join file_server,file_http by fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[12]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[13]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dstip, ':', cast(dstport as String)) AS file_server,max(timestamp) AS last_time FROM api_ftp group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[15]原语 file_ftp = load ckh by ckh with SELECT CONCAT(dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'file_ftp.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[16]原语 alter file_ftp.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'ftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[17]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[18]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[19]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[20]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dstip, ':', cast(dstport as String)) AS file_server,max(timestamp) AS last_time FROM api_tftp group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[38]原语 file_ftp = load ckh by ckh with SELECT CONCAT(dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'file_ftp.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[39]原语 alter file_ftp.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'tftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[40]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[41]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[42]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[43]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dstip, ':', cast(dstport as String)) AS file_server,max(timestamp) AS last_time FROM api_smb where dialect !='unknown' group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[61]原语 file_ftp = load ckh by ckh with SELECT CONCAT(dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'file_ftp.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[62]原语 alter file_ftp.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'smb'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[63]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[64]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[65]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[66]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_http', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(srcip, ':', cast(srcport as String)) AS file_server,count() AS visits_num FROM api_fileinfo where app_proto == 'http' group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[68]原语 file_http = load ckh by ckh with SELECT CONCAT(src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'http'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[69]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_http', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[70]原语 last_time_data = join file_server,file_http by fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[71]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[72]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dstip, ':', cast(dstport as String)) AS file_server,count() AS visits_num FROM api_ftp group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[74]原语 file_ftp = load ckh by ckh with SELECT CONCAT(dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'ftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[75]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[76]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[77]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[78]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dstip, ':', cast(dstport as String)) AS file_server,count() AS visits_num FROM api_tftp group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[95]原语 file_ftp = load ckh by ckh with SELECT CONCAT(dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'tftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[96]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[97]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[98]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[99]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT CONCAT(dstip, ':', cast(dstport as String)) AS file_server,count() AS visits_num FROM api_smb where dialect !='unknown' group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[117]原语 file_ftp = load ckh by ckh with SELECT CONCAT(dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_server from data_file_server where protocol = 'smb'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[118]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[119]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[120]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[121]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,left(first_time,10) first_time,left(last_time,10) last_time,curdate() now,active from data_file_server where last_time != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[124]原语 a = load db by mysql1 with select id,left(first_ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.first_time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[125]原语 alter a.first_time as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.last_time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[126]原语 alter a.last_time as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.now', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[127]原语 alter a.now as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:0 if x[2] == x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[128]原语 a1 = @udf a by udf0.df_row_lambda with x:0 if x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a1', 'Action': 'rename', 'rename': 'a1', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[129]原语 a1 = rename a1 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a1', 'Action': 'filter', 'filter': 'a1', 'by': 'active1 == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[130]原语 a1 = filter a1 by active1 == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if x[4] == x[5] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[131]原语 a1 = @udf a1 by udf0.df_row_lambda with x:"t" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a1', 'Action': 'filter', 'filter': 'a1', 'by': "lambda1 == 'f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[132]原语 a1 = filter a1 by lambda1 == "f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'a1', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[133]原语 a1 = loc a1 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a1', 'Action': 'rename', 'rename': 'a1', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[134]原语 a1 = rename a1 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:1 if x[2] != x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[135]原语 a2 = @udf a by udf0.df_row_lambda with x:1 if x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a2', 'Action': 'rename', 'rename': 'a2', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[136]原语 a2 = rename a2 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a2', 'Action': 'filter', 'filter': 'a2', 'by': 'active1 == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[137]原语 a2 = filter a2 by active1 == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a2', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if x[4] == x[5] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[138]原语 a2 = @udf a2 by udf0.df_row_lambda with x:"t" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a2', 'Action': 'filter', 'filter': 'a2', 'by': "lambda1 == 'f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[139]原语 a2 = filter a2 by lambda1 == "f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a2', 'Action': 'loc', 'loc': 'a2', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[140]原语 a2 = loc a2 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a2', 'Action': 'rename', 'rename': 'a2', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[141]原语 a2 = rename a2 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a3', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:3 if x[1] == x[2] == x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[142]原语 a3 = @udf a by udf0.df_row_lambda with x:3 if x[1]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a3', 'Action': 'rename', 'rename': 'a3', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[143]原语 a3 = rename a3 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a3', 'Action': 'filter', 'filter': 'a3', 'by': 'active1 == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[144]原语 a3 = filter a3 by active1 == 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a3', 'Action': 'loc', 'loc': 'a3', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[145]原语 a3 = loc a3 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a3', 'Action': 'rename', 'rename': 'a3', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[146]原语 a3 = rename a3 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'a', 'Action': 'union', 'union': 'a1,a2,a3'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[147]原语 a = union a1,a2,a3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[148]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[149]原语 @udf a by CRUD.save_table with (mysql1,data_file_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,left(first_time,10) first_time,left(last_time,10) last_time,curdate() now,active from data_file_user where last_time != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[152]原语 a = load db by mysql1 with select id,left(first_ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.first_time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[153]原语 alter a.first_time as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.last_time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[154]原语 alter a.last_time as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.now', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[155]原语 alter a.now as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:0 if x[2] == x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[156]原语 a1 = @udf a by udf0.df_row_lambda with x:0 if x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a1', 'Action': 'rename', 'rename': 'a1', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[157]原语 a1 = rename a1 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a1', 'Action': 'filter', 'filter': 'a1', 'by': 'active1 == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[158]原语 a1 = filter a1 by active1 == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'a1', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if x[4] == x[5] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[159]原语 a1 = @udf a1 by udf0.df_row_lambda with x:"t" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a1', 'Action': 'filter', 'filter': 'a1', 'by': "lambda1 == 'f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[160]原语 a1 = filter a1 by lambda1 == "f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'a1', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[161]原语 a1 = loc a1 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a1', 'Action': 'rename', 'rename': 'a1', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[162]原语 a1 = rename a1 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:1 if x[2] != x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[163]原语 a2 = @udf a by udf0.df_row_lambda with x:1 if x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a2', 'Action': 'rename', 'rename': 'a2', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[164]原语 a2 = rename a2 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a2', 'Action': 'filter', 'filter': 'a2', 'by': 'active1 == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[165]原语 a2 = filter a2 by active1 == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'a2', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if x[4] == x[5] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[166]原语 a2 = @udf a2 by udf0.df_row_lambda with x:"t" if x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a2', 'Action': 'filter', 'filter': 'a2', 'by': "lambda1 == 'f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[167]原语 a2 = filter a2 by lambda1 == "f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a2', 'Action': 'loc', 'loc': 'a2', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[168]原语 a2 = loc a2 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a2', 'Action': 'rename', 'rename': 'a2', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[169]原语 a2 = rename a2 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a3', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_row_lambda', 'with': "x:3 if x[1] == x[2] == x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[170]原语 a3 = @udf a by udf0.df_row_lambda with x:3 if x[1]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a3', 'Action': 'rename', 'rename': 'a3', 'as': "'lambda1':'active1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[171]原语 a3 = rename a3 as ("lambda1":"active1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a3', 'Action': 'filter', 'filter': 'a3', 'by': 'active1 == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[172]原语 a3 = filter a3 by active1 == 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a3', 'Action': 'loc', 'loc': 'a3', 'by': 'id,active1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[173]原语 a3 = loc a3 by id,active1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'a3', 'Action': 'rename', 'rename': 'a3', 'as': "'active1':'active'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[174]原语 a3 = rename a3 as ("active1":"active") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'a', 'Action': 'union', 'union': 'a1,a2,a3'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[175]原语 a = union a1,a2,a3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[176]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[177]原语 @udf a by CRUD.save_table with (mysql1,data_file_u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT user AS file_user,max(timestamp) AS last_time FROM api_ftp where file_user !='' group by file_user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[179]原语 file_ftp = load ckh by ckh with SELECT user AS fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'file_ftp.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[180]原语 alter file_ftp.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_user from data_file_user where protocol = 'ftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[181]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_user,file_user'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[182]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[183]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[184]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT user AS file_user,count() AS visits_num FROM api_ftp where file_user !='' group by file_user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[185]原语 file_ftp = load ckh by ckh with SELECT user AS fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_user from data_file_user where protocol = 'ftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[186]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_user,file_user'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[187]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[188]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[189]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT ntlmssp_user AS file_user,max(timestamp) AS last_time FROM api_smb where file_user !='' group by file_user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[191]原语 file_ftp = load ckh by ckh with SELECT ntlmssp_use... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'file_ftp.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[192]原语 alter file_ftp.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_user from data_file_user where protocol = 'smb'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[193]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_user,file_user'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[194]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[195]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[196]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT ntlmssp_user AS file_user,count() AS visits_num FROM api_smb where file_user !='' group by file_user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[197]原语 file_ftp = load ckh by ckh with SELECT ntlmssp_use... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,file_user from data_file_user where protocol = 'smb'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[198]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'last_time_data', 'Action': 'join', 'join': 'file_server,file_ftp', 'by': 'file_user,file_user'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[199]原语 last_time_data = join file_server,file_ftp by file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[200]原语 last_time_data = @udf last_time_data by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'last_time_data', 'Action': '@udf', '@udf': 'last_time_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[201]原语 last_time_data = @udf last_time_data by CRUD.save_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select CONCAT(dstip, ':', cast(dstport as String)) AS file_server,sum(size) visits_flow from api_fileinfo where size !=0 and app_proto ='http' group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[203]原语 a = load ckh by ckh with select CONCAT(dstip, ":",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,file_server from data_file_server'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[204]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'file_server', 'Action': 'join', 'join': 'file_server,a', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[205]原语 file_server = join file_server,a by file_server,fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[206]原语 file_server = loc file_server by id,visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[207]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[208]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select CONCAT(srcip, ':', cast(srcport as String)) AS file_server,sum(size) visits_flow from api_fileinfo where size !=0 and app_proto ='http' group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[209]原语 a = load ckh by ckh with select CONCAT(srcip, ":",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,file_server from data_file_server'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[210]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'file_server', 'Action': 'join', 'join': 'file_server,a', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[211]原语 file_server = join file_server,a by file_server,fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[212]原语 file_server = loc file_server by id,visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[213]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[214]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select CONCAT(dstip, ':', cast(dstport as String)) AS file_server,sum(size) visits_flow from api_smb where size !=0 group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[216]原语 a = load ckh by ckh with select CONCAT(dstip, ":",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,file_server from data_file_server'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[217]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'file_server', 'Action': 'join', 'join': 'file_server,a', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[218]原语 file_server = join file_server,a by file_server,fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[219]原语 file_server = loc file_server by id,visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[220]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[221]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select CONCAT(srcip, ':', cast(srcport as String)) AS file_server,sum(size) visits_flow from api_smb where size !=0 group by file_server"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[222]原语 a = load ckh by ckh with select CONCAT(srcip, ":",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,file_server from data_file_server'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[223]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'file_server', 'Action': 'join', 'join': 'file_server,a', 'by': 'file_server,file_server'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[224]原语 file_server = join file_server,a by file_server,fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[225]原语 file_server = loc file_server by id,visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[226]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[227]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select ntlmssp_user file_user,sum(size) visits_flow from api_smb where size !=0 and ntlmssp_user !='' group by file_user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[229]原语 a = load ckh by ckh with select ntlmssp_user file_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,file_user from data_file_user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[230]原语 file_server = load db by mysql1 with select id,fil... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'file_server', 'Action': 'join', 'join': 'file_server,a', 'by': 'file_user,file_user'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[231]原语 file_server = join file_server,a by file_user,file... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[232]原语 file_server = loc file_server by id,visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[233]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[234]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[file_count.fbi]执行第[237]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],237

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



