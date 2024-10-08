#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_sj/app_all_sj_t1
#datetime: 2024-08-30T16:10:57.071025
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
		add_the_error('[app_sj/app_all_sj_t1.fbi]执行第[10]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_sj/app_all_sj_t1.fbi]执行第[13]原语 app = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_sj/app_all_sj_t1.fbi]执行第[14]原语 app = loc app by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'app', 'with': 'app=$1', 'run': '""\n\n##修改审计状态（data_app_new）\na = load db by mysql1 with select id,app from data_app_new where app = \'@app\'\nalter a.id as int\na = add app_status by ("1")\na = @udf a by udf0.df_set_index with id\nb = @udf a by CRUD.save_table with (@link,@table)\n\n# 合并应用处理合并\napp = load db by mysql1 with select app,id from data_app_new where app_merges=\'@app\' and merge_state =1\napp = add app_status by ("1")\napp = @udf app by udf0.df_set_index with id\napp = @udf app by CRUD.save_table with (@link,@table)\n\n# 合并应用接口开启审计\napi = @udf RS.load_mysql_sql with (mysql1,select i.id,i.api_status,i.app from data_app_new p left join data_api_new i on p.app=i.app where p.app_merges=\'@app\' and p.merge_state =1 )\napi = add api_status by ("1")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (@link,data_api_new)\n\n# 正常开启\napi = @udf RS.load_mysql_sql with (mysql1,select id,api_status from data_api_new where app=\'@app\' )\napi = add api_status by ("1")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (@link,data_api_new)\n\n""'}
	try:
		ptree['lineno']=16
		ptree['funs']=block_foreach_16
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_sj/app_all_sj_t1.fbi]执行第[16]原语 foreach app run "##修改审计状态（data_app_new）a = load db... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[app_sj/app_all_sj_t1.fbi]执行第[46]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_sj/app_all_sj_t1.fbi]执行第[48]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],48

#主函数结束,开始块函数

def block_foreach_16(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,app from data_app_new where app = '@app'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[19]原语 a = load db by mysql1 with select id,app from data... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[20]原语 alter a.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'app_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[21]原语 a = add app_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[22]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[23]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app,id from data_app_new where app_merges='@app' and merge_state =1"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[26]原语 app = load db by mysql1 with select app,id from da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[27]原语 app = add app_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[28]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[29]原语 app = @udf app by CRUD.save_table with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select i.id,i.api_status,i.app from data_app_new p left join data_api_new i on p.app=i.app where p.app_merges='@app' and p.merge_state =1 "}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[32]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[33]原语 api = add api_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[34]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': '@link,data_api_new'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[35]原语 d = @udf api by CRUD.save_table with (@link,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,api_status from data_api_new where app='@app' "}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[38]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[39]原语 api = add api_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[40]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': '@link,data_api_new'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第16行foreach语句中]执行第[41]原语 d = @udf api by CRUD.save_table with (@link,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_16

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



