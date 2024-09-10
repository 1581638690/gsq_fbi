#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sen_label_tree
#datetime: 2024-08-30T16:10:56.190804
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
		add_the_error('[sen_label_tree.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[14]原语 sen = load pq by sensitive/sens_data.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen', 'as': '"key":"sen_key"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[15]原语 rename sen as ("key":"sen_key") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_api', 'Action': 'group', 'group': 'sen', 'by': 'url,sen_key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[17]原语 sen_api = group sen by url,sen_key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[18]原语 sen_api = @udf sen_api by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select url,count() count from sen_http_count group by url'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[19]原语 count = load ckh by ckh with select url,count() co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_api', 'Action': 'join', 'join': 'sen_api,count', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[20]原语 sen_api = join sen_api,count by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_api', 'Action': 'add', 'add': 'type', 'by': "'流动'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[21]原语 sen_api = add type by ("流动") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[22]原语 sen_api = @udf sen_api by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_api', 'as': '"num_sum":"num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[23]原语 rename sen_api as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[24]原语 sen_api = @udf sen_api by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_api_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[25]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'sen_api', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_api_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[26]原语 @udf sen_api by CRUD.save_table with (mysql1,sen_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_api', 'Action': 'group', 'group': 'sen', 'by': 'app,sen_key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[28]原语 sen_api = group sen by app,sen_key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[29]原语 sen_api = @udf sen_api by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app,count() count from sen_http_count group by app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[30]原语 count = load ckh by ckh with select app,count() co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_api', 'Action': 'join', 'join': 'sen_api,count', 'by': 'app,app'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[31]原语 sen_api = join sen_api,count by app,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_api', 'Action': 'add', 'add': 'type', 'by': "'流动'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[32]原语 sen_api = add type by ("流动") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[33]原语 sen_api = @udf sen_api by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_api', 'as': '"num_sum":"num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[34]原语 rename sen_api as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[35]原语 sen_api = @udf sen_api by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_app_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[36]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'sen_api', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_app_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[37]原语 @udf sen_api by CRUD.save_table with (mysql1,sen_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_api', 'Action': 'group', 'group': 'sen', 'by': 'account,sen_key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[39]原语 sen_api = group sen by account,sen_key agg num:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[40]原语 sen_api = @udf sen_api by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_api', 'Action': 'filter', 'filter': 'sen_api', 'by': "account !=''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[41]原语 sen_api = filter sen_api by account !="" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,count() count from sen_http_count where account !='' group by account"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[42]原语 count = load ckh by ckh with select account,count(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_api', 'Action': 'join', 'join': 'sen_api,count', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[43]原语 sen_api = join sen_api,count by account,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_api', 'Action': 'add', 'add': 'type', 'by': "'使用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[44]原语 sen_api = add type by ("使用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[45]原语 sen_api = @udf sen_api by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_api', 'as': '"num_sum":"num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[46]原语 rename sen_api as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[47]原语 sen_api = @udf sen_api by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_acc_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[48]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'sen_api', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_acc_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[49]原语 @udf sen_api by CRUD.save_table with (mysql1,sen_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_api', 'Action': 'group', 'group': 'sen', 'by': 'src_ip,sen_key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[51]原语 sen_api = group sen by src_ip,sen_key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[52]原语 sen_api = @udf sen_api by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select src_ip,count() count from sen_http_count group by src_ip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[53]原语 count = load ckh by ckh with select src_ip,count()... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_api', 'Action': 'join', 'join': 'sen_api,count', 'by': 'src_ip,src_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[54]原语 sen_api = join sen_api,count by src_ip,src_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_api', 'Action': 'add', 'add': 'type', 'by': "'使用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[55]原语 sen_api = add type by ("使用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[56]原语 sen_api = @udf sen_api by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_api', 'as': '"num_sum":"num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[57]原语 rename sen_api as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_api', 'Action': '@udf', '@udf': 'sen_api', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[58]原语 sen_api = @udf sen_api by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_src_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[59]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'sen_api', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_src_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[60]原语 @udf sen_api by CRUD.save_table with (mysql1,sen_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_dbms.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[61]原语 sen = load pq by sensitive/sens_dbms.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen.dest_port', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[62]原语 alter sen.dest_port as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen', 'Action': 'add', 'add': 'dest_ip', 'by': 'sen.dest_ip +":"+ sen.dest_port'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[63]原语 sen = add dest_ip by sen.dest_ip +":"+ sen.dest_po... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen', 'as': '"key":"sen_key"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[64]原语 rename sen as ("key":"sen_key") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_dbms', 'Action': 'group', 'group': 'sen', 'by': 'dest_ip,sen_key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[66]原语 sen_dbms = group sen by dest_ip,sen_key agg num:su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[67]原语 sen_dbms = @udf sen_dbms by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select CONCAT(dest_ip, ':', cast(dest_port as String)) AS dest_ip,count() count from dbms_sendata group by dest_ip"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[68]原语 count = load ckh by ckh with select CONCAT(dest_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_dbms', 'Action': 'join', 'join': 'sen_dbms,count', 'by': 'dest_ip,dest_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[69]原语 sen_dbms = join sen_dbms,count by dest_ip,dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_dbms', 'Action': 'add', 'add': 'type', 'by': "'存储'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[70]原语 sen_dbms = add type by ("存储") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[71]原语 sen_dbms = @udf sen_dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_dbms', 'as': '"num_sum":"num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[72]原语 rename sen_dbms as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[73]原语 sen_dbms = @udf sen_dbms by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_dbms_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[74]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_dbms_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[75]原语 @udf sen_dbms by CRUD.save_table with (mysql1,sen_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_dbms', 'Action': 'group', 'group': 'sen', 'by': 'user,sen_key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[77]原语 sen_dbms = group sen by user,sen_key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[78]原语 sen_dbms = @udf sen_dbms by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_dbms', 'Action': 'filter', 'filter': 'sen_dbms', 'by': "user !=''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[79]原语 sen_dbms = filter sen_dbms by user !="" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select user,count() count from dbms_sendata where user !='' group by user"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[80]原语 count = load ckh by ckh with select user,count() c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_dbms', 'Action': 'join', 'join': 'sen_dbms,count', 'by': 'user,user'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[81]原语 sen_dbms = join sen_dbms,count by user,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_dbms', 'Action': 'add', 'add': 'type', 'by': "'使用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[82]原语 sen_dbms = add type by ("使用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[83]原语 sen_dbms = @udf sen_dbms by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_dbms', 'as': '"num_sum":"num"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[84]原语 rename sen_dbms as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_dbms', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[85]原语 sen_dbms = @udf sen_dbms by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_dbuser_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[86]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'sen_dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_dbuser_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[87]原语 a = @udf sen_dbms by CRUD.save_table with (mysql1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_file', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select sha256 md5,rekey sen_key,filename,count() num from datafilter group by md5,sen_key,filename'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[90]原语 sen_file = load ckh by ckh with select sha256 md5,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_file', 'Action': '@udf', '@udf': 'sen_file', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[91]原语 sen_file = @udf sen_file by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sen_file', 'Action': 'add', 'add': 'type', 'by': "'存储'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[92]原语 sen_file = add type by ("存储") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_file_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[93]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'sen_file', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_file_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[94]原语 a = @udf sen_file by CRUD.save_table with (mysql1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_file', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select sha256 md5,filename,count() count from filter_count group by md5,filename'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[96]原语 sen_file = load ckh by ckh with select sha256 md5,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select md5,filename,id from sen_file_tree'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[97]原语 a = load db by mysql1 with select md5,filename,id ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_file', 'Action': 'join', 'join': 'sen_file,a', 'by': '[md5,filename],[md5,filename]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[98]原语 sen_file = join sen_file,a by [md5,filename],[md5,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_file', 'Action': '@udf', '@udf': 'sen_file', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[99]原语 sen_file = @udf sen_file by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_file', 'Action': '@udf', '@udf': 'sen_file', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[100]原语 sen_file = @udf sen_file by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_file', 'Action': 'loc', 'loc': 'sen_file', 'by': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[101]原语 sen_file = loc sen_file by count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'sen_file', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_file_tree'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[104]原语 @udf sen_file by CRUD.save_table with (mysql1,sen_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) o_count,sum(count) f_count,sum(num) m_count,sen_key from sen_app_tree group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[107]原语 app = load db by mysql1 with select count(id) o_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'obj', 'by': '"应用"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[108]原语 app = add obj by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) o_count,sum(count) f_count,sum(num) m_count,sen_key from sen_api_tree group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[109]原语 api = load db by mysql1 with select count(id) o_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'obj', 'by': '"接口"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[110]原语 api = add obj by ("接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'acc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) o_count,sum(count) f_count,sum(num) m_count,sen_key from sen_acc_tree group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[111]原语 acc = load db by mysql1 with select count(id) o_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'acc', 'Action': 'add', 'add': 'obj', 'by': '"应用账号"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[112]原语 acc = add obj by ("应用账号") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) o_count,sum(count) f_count,sum(num) m_count,sen_key from sen_src_tree group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[113]原语 src = load db by mysql1 with select count(id) o_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'src', 'Action': 'add', 'add': 'obj', 'by': '"终端"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[114]原语 src = add obj by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) o_count,sum(count) f_count,sum(num) m_count,sen_key from sen_dbms_tree group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[115]原语 dbms = load db by mysql1 with select count(id) o_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms', 'Action': 'add', 'add': 'obj', 'by': '"数据库对象"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[116]原语 dbms = add obj by ("数据库对象") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbuser', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) o_count,sum(count) f_count,sum(num) m_count,sen_key from sen_dbuser_tree group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[117]原语 dbuser = load db by mysql1 with select count(id) o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbuser', 'Action': 'add', 'add': 'obj', 'by': '"数据库账号"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[118]原语 dbuser = add obj by ("数据库账号") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'aa', 'Action': 'union', 'union': 'app,api,acc,src,dbms,dbuser'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[119]原语 aa = union app,api,acc,src,dbms,dbuser 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[120]原语 aa = @udf aa by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[121]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'aa', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[122]原语 a = @udf aa by CRUD.save_table with (mysql1,sen_ob... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sen_key,sum(o_count) o_count,sum(f_count) f_count, sum(m_count) m_count from sen_obj group by sen_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[126]原语 a = load db by mysql1 with select sen_key,sum(o_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_class', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[127]原语 sen_class = load ssdb by ssdb0 with dd:reqs_label1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_class', 'as': '"data":"sen_key","class":"obj"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[128]原语 rename sen_class as ("data":"sen_key","class":"obj... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a', 'Action': 'join', 'join': 'a,sen_class', 'by': 'sen_key,sen_key'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[129]原语 a = join a,sen_class by sen_key,sen_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[130]原语 a = @udf a by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_class'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[131]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_class'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[132]原语 a = @udf a by CRUD.save_table with (mysql1,sen_cla... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select '流动' type,sen_key,count(id) o_count,sum(count) f_count,sum(num) m_count,'应用' name from sen_app_tree group by type,sen_key"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[136]原语 app = load db by mysql1 with select "流动" type,sen_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select '流动' type,sen_key,count(id) o_count,sum(count) f_count,sum(num) m_count,'接口' name from sen_api_tree group by type,sen_key"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[137]原语 api = load db by mysql1 with select "流动" type,sen_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'acc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select '使用' type,sen_key,count(id) o_count,sum(count) f_count,sum(num) m_count,'应用账号' name from sen_acc_tree group by type,sen_key"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[138]原语 acc = load db by mysql1 with select "使用" type,sen_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select '使用' type,sen_key,count(id) o_count,sum(count) f_count,sum(num) m_count,'终端' name from sen_src_tree group by type,sen_key"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[139]原语 src = load db by mysql1 with select "使用" type,sen_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select '存储' type,sen_key,count(id) o_count,sum(count) f_count,sum(num) m_count,'数据库' name from sen_dbms_tree group by type,sen_key"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[140]原语 dbms = load db by mysql1 with select "存储" type,sen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbuser', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select '使用' type,sen_key,count(id) o_count,sum(count) f_count,sum(num) m_count,'数据库账号' name from sen_dbuser_tree group by type,sen_key"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[141]原语 dbuser = load db by mysql1 with select "使用" type,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'aa', 'Action': 'union', 'union': 'app,api,acc,src,dbms,dbuser'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[142]原语 aa = union app,api,acc,src,dbms,dbuser 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[143]原语 aa = @udf aa by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql1,truncate table sen_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[144]原语 @udf RS.exec_mysql_sql with (mysql1,truncate table... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'aa', 'by': 'CRUD.save_table', 'with': 'mysql1,sen_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[145]原语 a = @udf aa by CRUD.save_table with (mysql1,sen_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[sen_label_tree.fbi]执行第[148]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],148

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



