#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: zts_sj2
#datetime: 2024-08-30T16:10:54.224850
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
		add_the_error('[zts_sj2.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj01', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,SELECT app,count(id) audit_old from data_api_new where api_status=1 and merge_state != 1 group by app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[18]原语 zts_sj01 = @udf RS.load_mysql_sql with (mysql1,SEL... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'qqq', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,app_merges from data_app_new where app_status=1 and merge_state != 2'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[19]原语 qqq = load db by mysql1 with select app,app_merges... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj01', 'Action': 'join', 'join': 'zts_sj01,qqq', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[20]原语 zts_sj01 = join zts_sj01,qqq by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'qq', 'Action': '@udf', '@udf': 'zts_sj01', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[21]原语 qq = @udf zts_sj01 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'qq1', 'Action': 'filter', 'filter': 'qq', 'by': "app_merges == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[22]原语 qq1 = filter qq by app_merges == "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'qq2', 'Action': 'filter', 'filter': 'qq', 'by': "app_merges != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[23]原语 qq2 = filter qq by app_merges != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'qq2.app', 'Action': 'lambda', 'lambda': 'app_merges', 'by': "x: x if x !='' else ''"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[24]原语 qq2.app = lambda app_merges by x: x if x !=""  els... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'zts_sj01', 'Action': 'union', 'union': 'qq1,qq2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[25]原语 zts_sj01 = union qq1,qq2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_sj01', 'Action': 'loc', 'loc': 'zts_sj01', 'by': 'app,audit_old'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[26]原语 zts_sj01 = loc zts_sj01 by app,audit_old 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'zts_sj01', 'Action': 'group', 'group': 'zts_sj01', 'by': 'app', 'agg': 'audit_old:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[27]原语 zts_sj01 = group zts_sj01 by app agg audit_old:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj01', 'Action': '@udf', '@udf': 'zts_sj01', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[28]原语 zts_sj01 = @udf zts_sj01 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_sj01', 'by': '"audit_old_sum":"audit_old"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[29]原语 rename zts_sj01 by ("audit_old_sum":"audit_old") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj02', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,SELECT app,count(id) audit_sum from data_api_new where merge_state != 1 group by app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[31]原语 zts_sj02 = @udf RS.load_mysql_sql with (mysql1,SEL... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj02', 'Action': 'join', 'join': 'zts_sj02,qqq', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[32]原语 zts_sj02 = join zts_sj02,qqq by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'qq', 'Action': '@udf', '@udf': 'zts_sj02', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[33]原语 qq = @udf zts_sj02 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'qq1', 'Action': 'filter', 'filter': 'qq', 'by': "app_merges == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[34]原语 qq1 = filter qq by app_merges == "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'qq2', 'Action': 'filter', 'filter': 'qq', 'by': "app_merges != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[35]原语 qq2 = filter qq by app_merges != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'qq2.app', 'Action': 'lambda', 'lambda': 'app_merges', 'by': "x: x if x !='' else ''"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[36]原语 qq2.app = lambda app_merges by x: x if x !=""  els... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'zts_sj02', 'Action': 'union', 'union': 'qq1,qq2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[37]原语 zts_sj02 = union qq1,qq2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_sj02', 'Action': 'loc', 'loc': 'zts_sj02', 'by': 'app,audit_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[38]原语 zts_sj02 = loc zts_sj02 by app,audit_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'zts_sj02', 'Action': 'group', 'group': 'zts_sj02', 'by': 'app', 'agg': 'audit_sum:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[39]原语 zts_sj02 = group zts_sj02 by app agg audit_sum:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj02', 'Action': '@udf', '@udf': 'zts_sj02', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[40]原语 zts_sj02 = @udf zts_sj02 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_sj02', 'by': '"audit_sum_sum":"audit_sum"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[41]原语 rename zts_sj02 by ("audit_sum_sum":"audit_sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj', 'Action': 'join', 'join': 'zts_sj01,zts_sj02', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[43]原语 zts_sj = join zts_sj01,zts_sj02 by app,app with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_sj03', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT app,count() audit_data from api_monitor group by app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[44]原语 zts_sj03 =load ckh by ckh with SELECT app,count() ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj', 'Action': 'join', 'join': 'zts_sj,zts_sj03', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[45]原语 zts_sj = join zts_sj,zts_sj03 by app,app with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zts_sj04', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT distinct app,api_type from api_monitor group by app,api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[46]原语 zts_sj04 = load ckh by ckh with SELECT distinct ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'zts_sj04', 'Action': 'group', 'group': 'zts_sj04', 'by': 'app', 'agg': 'api_type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[47]原语 zts_sj04 = group zts_sj04 by app agg api_type:coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj04', 'Action': '@udf', '@udf': 'zts_sj04', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[48]原语 zts_sj04 = @udf zts_sj04 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj', 'Action': 'join', 'join': 'zts_sj,zts_sj04', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[49]原语 zts_sj = join zts_sj,zts_sj04 by app,app with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj', 'Action': '@udf', '@udf': 'zts_sj', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[50]原语 zts_sj = @udf zts_sj by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj05', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,SELECT distinct app,name app_name from data_app_new where name != ''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[51]原语 zts_sj05 = @udf RS.load_mysql_sql with (mysql1,SEL... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'zts_sj', 'Action': 'join', 'join': 'zts_sj,zts_sj05', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[52]原语 zts_sj = join zts_sj,zts_sj05 by app,app with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'zts_sj', 'Action': '@udf', '@udf': 'zts_sj', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[53]原语 zts_sj = @udf zts_sj by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts_sj', 'as': "'app':'name','audit_sum':'xsjjk','audit_old':'ysjjk','audit_data':'sjfw','api_type_count':'sjlx'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[54]原语 rename zts_sj as ("app":"name","audit_sum":"xsjjk"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select id,name from audit_statistics '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[57]原语 dd = @udf RS.load_mysql_sql with (mysql1,select id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'b5', 'Action': 'join', 'join': 'zts_sj,dd', 'by': 'name,name', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[58]原语 b5 = join zts_sj,dd by name,name with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b5', 'Action': '@udf', '@udf': 'b5', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[59]原语 b5 = @udf b5 by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b5', 'Action': '@udf', '@udf': 'b5', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[60]原语 b5 = @udf b5 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'b5', 'by': 'CRUD.save_table', 'with': 'mysql1,audit_statistics'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[61]原语 @udf b5 by CRUD.save_table with (mysql1,audit_stat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app from data_app_new where app_status=1 and merge_state = 2'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[82]原语 a = load db by mysql1 with select app from data_ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'a', 'with': 'app=$1', 'run': '""\n# 正常开启\napi = @udf RS.load_mysql_sql with (mysql1,select id,api_status from data_api_new where app=\'@app\' and api_status=0 )\napi = add api_status by ("1")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (mysql1,data_api_new)\n""'}
	try:
		ptree['lineno']=83
		ptree['funs']=block_foreach_83
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[83]原语 foreach a run "# 正常开启api = @udf RS.load_mysql_sql ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app from data_app_new where app_status=1 and merge_state != 2'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[90]原语 a = load db by mysql1 with select app from data_ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'a', 'with': 'app=$1', 'run': '""\n# 正常开启\napi = @udf RS.load_mysql_sql with (mysql1,select id,api_status from data_api_new where app=\'@app\' and api_status=0 )\napi = add api_status by ("1")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (mysql1,data_api_new)\n""'}
	try:
		ptree['lineno']=91
		ptree['funs']=block_foreach_91
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[91]原语 foreach a run "# 正常开启api = @udf RS.load_mysql_sql ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[zts_sj2.fbi]执行第[100]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],100

#主函数结束,开始块函数

def block_foreach_83(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,api_status from data_api_new where app='@app' and api_status=0 "}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第83行foreach语句中]执行第[85]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第83行foreach语句中]执行第[86]原语 api = add api_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第83行foreach语句中]执行第[87]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第83行foreach语句中]执行第[88]原语 d = @udf api by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_83

def block_foreach_91(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,api_status from data_api_new where app='@app' and api_status=0 "}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行foreach语句中]执行第[93]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第91行foreach语句中]执行第[94]原语 api = add api_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行foreach语句中]执行第[95]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第91行foreach语句中]执行第[96]原语 d = @udf api by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_91

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



