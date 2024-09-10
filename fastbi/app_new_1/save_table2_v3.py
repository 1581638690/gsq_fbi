#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_new_1/save_table2
#datetime: 2024-08-30T16:10:56.545324
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
		add_the_error('[app_new_1/save_table2.fea]执行第[26]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[29]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'b', 'Action': 'loc', 'loc': 'a', 'by': 'name,sx,scope,app_status'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[31]原语 b = loc a by name,sx,scope,app_status 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'eval', 'eval': 'b', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[34]原语 ss = eval b by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'app,name,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[35]原语 a = loc a by app,name,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'id', 'by': 'a.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[36]原语 a = add id by a.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'apps', 'Action': 'loc', 'loc': 'a', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[37]原语 apps=loc a by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apps', 'Action': 'eval', 'eval': 'apps', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[39]原语 apps=eval apps by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,app,app_name from api19_risk where app="$apps"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[40]原语 api_risk=load db by mysql1 with  select id,app,app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_risk', 'Action': 'join', 'join': 'api_risk,a', 'by': 'app,app', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[41]原语 api_risk=join api_risk,a by app,app with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk', 'Action': 'loc', 'loc': 'api_risk', 'drop': 'id_y,app_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[43]原语 api_risk=loc api_risk drop id_y,app_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_risk', 'as': '{"name":"app_name"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[44]原语 rename api_risk as {"name":"app_name"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_risk', 'as': '{"id_x":"id"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[45]原语 rename api_risk as {"id_x":"id"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_risk', 'Action': '@udf', '@udf': 'api_risk', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[46]原语 api_risk=@udf api_risk by udf0.df_set_index with i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_risk', 'Action': '@udf', '@udf': 'api_risk', 'by': 'CRUD.save_table', 'with': '@link,api19_risk'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[47]原语 api_risk = @udf api_risk by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$ss == 1', 'with': '""\naaa = load db by mysql1 with select count(id) from data_api_new where api_status\naaa = eval aaa by iloc[0,0]\nb = @udf b by CRUD.save_table with (@link,@table)\n#返回结果\nstore b to ssdb by ssdb0 with @table:query:@FPS as 600\npush b as table\napp = loc a by app\napp1 = eval app by iloc[0,0]\nalter a.id as int\na = add app_status by ("1")\na = @udf a by udf0.df_set_index with id\n@udf a by CRUD.save_table with (@link,@table)\n# 合并应用处理合并\napp = load db by mysql1 with select app,id from data_app_new where app_merges=\'$app1\' and merge_state =1\napp = add app_status by ("1")\napp = @udf app by udf0.df_set_index with id\napp = @udf app by CRUD.save_table with (@link,@table)\n# 合并应用接口开启审计\napi = @udf RS.load_mysql_sql with (mysql1,select i.id,i.api_status,i.app from data_app_new p left join data_api_new i on p.app=i.app where p.app_merges=\'$app1\' and p.merge_state =1 )\napi = add api_status by ("1")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (@link,data_api_new)\n# 正常开启\napi = @udf RS.load_mysql_sql with (mysql1,select id,api_status from data_api_new where app=\'$app1\' )\napi = add api_status by ("1")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (@link,data_api_new)\n"', 'else': '"\napp = loc a by app\napp1 = eval app by iloc[0,0]\nalter a.id as int\na = add app_status by (\'0\')\na = @udf a by udf0.df_set_index with id\n@udf a by CRUD.save_table with (@link,@table)\n# 合并应用处理合并\napp = load db by mysql1 with select app,id from data_app_new where app_merges=\'$app1\' and merge_state =1\napp = add app_status by ("0")\napp = @udf app by udf0.df_set_index with id\napp = @udf app by CRUD.save_table with (@link,@table)\n# 关闭合并应用接口审计\napi = @udf RS.load_mysql_sql with (mysql1,select i.id,i.api_status,i.app from data_app_new p left join data_api_new i on p.app=i.app where p.app_merges=\'$app1\' and p.merge_state =1 )\napi = add api_status by ("0")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (@link,data_api_new)\n# 关闭接口审计\napi = @udf RS.load_mysql_sql with (mysql1,select id,api_status from data_api_new where app = \'$app1\' )\napi = add api_status by ("0")\napi = @udf api by udf0.df_set_index with id\nd = @udf api by CRUD.save_table with (@link,data_api_new)\n# 从应用管理删除\ndd = @udf RS.load_mysql_sql with (mysql1,select id from audit_statistics where name = \'$app1\' )\nid = eval dd by iloc[0,0]\n@udf dd by CRUD.delete_table with (mysql1,audit_statistics,$id)\nb = @udf b by CRUD.save_table with (@link,@table)\n#返回结果\nstore b to ssdb by ssdb0 with @table:query:@FPS as 600\npush b as table\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=49
		ptree['funs']=block_if_49
		ptree['funs2']=block_if_else_49
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[49]原语 if $ss == 1 with "aaa = load db by mysql1 with sel... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_new_1/save_table2.fea]执行第[109]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],109

#主函数结束,开始块函数

def block_if_49(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'aaa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(id) from data_api_new where api_status'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[50]原语 aaa = load db by mysql1 with select count(id) from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aaa', 'Action': 'eval', 'eval': 'aaa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[51]原语 aaa = eval aaa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[52]原语 b = @udf b by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'b', 'to': 'ssdb', 'by': 'ssdb0', 'with': '@table:query:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[54]原语 store b to ssdb by ssdb0 with @table:query:@FPS as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[55]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'a', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[56]原语 app = loc a by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app1', 'Action': 'eval', 'eval': 'app', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[57]原语 app1 = eval app by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[58]原语 alter a.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'app_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[59]原语 a = add app_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[60]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[61]原语 @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app,id from data_app_new where app_merges='$app1' and merge_state =1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[63]原语 app = load db by mysql1 with select app,id from da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[64]原语 app = add app_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[65]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[66]原语 app = @udf app by CRUD.save_table with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select i.id,i.api_status,i.app from data_app_new p left join data_api_new i on p.app=i.app where p.app_merges='$app1' and p.merge_state =1 "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[68]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[69]原语 api = add api_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[70]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': '@link,data_api_new'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[71]原语 d = @udf api by CRUD.save_table with (@link,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,api_status from data_api_new where app='$app1' "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[73]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"1"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[74]原语 api = add api_status by ("1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[75]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': '@link,data_api_new'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if语句中]执行第[76]原语 d = @udf api by CRUD.save_table with (@link,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_49

def block_if_else_49(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'a', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[49]原语 app = loc a by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app1', 'Action': 'eval', 'eval': 'app', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[50]原语 app1 = eval app by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[51]原语 alter a.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'app_status', 'by': "'0'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[52]原语 a = add app_status by ("0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[53]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[54]原语 @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app,id from data_app_new where app_merges='$app1' and merge_state =1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[56]原语 app = load db by mysql1 with select app,id from da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app_status', 'by': '"0"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[57]原语 app = add app_status by ("0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[58]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[59]原语 app = @udf app by CRUD.save_table with (@link,@tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select i.id,i.api_status,i.app from data_app_new p left join data_api_new i on p.app=i.app where p.app_merges='$app1' and p.merge_state =1 "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[61]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"0"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[62]原语 api = add api_status by ("0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[63]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': '@link,data_api_new'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[64]原语 d = @udf api by CRUD.save_table with (@link,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,api_status from data_api_new where app = '$app1' "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[66]原语 api = @udf RS.load_mysql_sql with (mysql1,select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'api_status', 'by': '"0"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[67]原语 api = add api_status by ("0") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[68]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': '@link,data_api_new'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[69]原语 d = @udf api by CRUD.save_table with (@link,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id from audit_statistics where name = '$app1' "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[71]原语 dd = @udf RS.load_mysql_sql with (mysql1,select id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'id', 'Action': 'eval', 'eval': 'dd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[72]原语 id = eval dd by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'dd', 'by': 'CRUD.delete_table', 'with': 'mysql1,audit_statistics,$id'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[73]原语 @udf dd by CRUD.delete_table with (mysql1,audit_st... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[74]原语 b = @udf b by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'b', 'to': 'ssdb', 'by': 'ssdb0', 'with': '@table:query:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[76]原语 store b to ssdb by ssdb0 with @table:query:@FPS as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[第49行if_else语句中]执行第[77]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_49

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



