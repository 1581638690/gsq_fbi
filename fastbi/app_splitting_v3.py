#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_splitting
#datetime: 2024-08-30T16:10:55.406249
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
		add_the_error('[app_splitting.fbi]执行第[22]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_splitting.fbi]执行第[23]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'app,app_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_splitting.fbi]执行第[24]原语 a = loc a by app,app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'a', 'with': 'app=$1,app_n=$2', 'run': '""\napp = eval a by (iloc[0,0])\napp = load db by mysql1 with select id,app,merge_state from data_app_new where app =\'@app\' and merge_state =2\nassert app by df.index.size >0 as break with 未合并应用不能拆分！\n# 接口更新\napi = load db by mysql1 with select id,app_merges app from data_api_new where app = \'@app\'\napi = add app_merges by (\'\')\napi = @udf api by udf0.df_set_index with id\n@udf api by CRUD.save_table with (mysql1,data_api_new)\n# 合并应用删除\nid = eval app by (iloc[0,0])\n@udf CRUD.delete_table with (mysql1,data_app_new,$id)\n# 拆出的应用状态改变 手动拆出来的不会自动合并\n#app_n = eval a by (iloc[0,1])\napps = @sdf sys_eval with (\'@app_n\'.split(\',\'))\napps = @sdf sys_eval with (str($apps)[1:-1])\napp_all = load db by mysql1 with select id,merge_state from data_app_new where app in ($apps) and merge_state =1\napp_all = add merge_state by 3\napp_all = add app_merges by ("")\napp_all = @udf app_all by udf0.df_set_index with id\n@udf app_all by CRUD.save_table with (mysql1,data_app_new)\n# 添加ssdb\napp = @udf RS.load_mysql_sql with (mysql1,select app,app_sum from data_app_new where merge_state = 2)\napp = @udf app by udf0.df_set_index with app\napp = add app by (app.index)\na=@udf SSDB.hclear with app_merge\nstore app to ssdb by ssdb0 with app_merge as H\n""'}
	try:
		ptree['lineno']=25
		ptree['funs']=block_foreach_25
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_splitting.fbi]执行第[25]原语 foreach a run "app = eval a by (iloc[0,0])app = lo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_splitting.fbi]执行第[53]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],53

#主函数结束,开始块函数

def block_foreach_25(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[26]原语 app = eval a by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,app,merge_state from data_app_new where app ='@app' and merge_state =2"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[27]原语 app = load db by mysql1 with select id,app,merge_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'app', 'by': 'df.index.size >0', 'as': 'break', 'with': '未合并应用不能拆分！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[第25行foreach语句中]执行第[28]原语 assert app by df.index.si... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[28]原语 assert app by df.index.size >0 as break with 未合并应用... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,app_merges app from data_api_new where app = '@app'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[30]原语 api = load db by mysql1 with select id,app_merges ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'app_merges', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[31]原语 api = add app_merges by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[32]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[33]原语 @udf api by CRUD.save_table with (mysql1,data_api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'id', 'Action': 'eval', 'eval': 'app', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[35]原语 id = eval app by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'CRUD.delete_table', 'with': 'mysql1,data_app_new,$id'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[36]原语 @udf CRUD.delete_table with (mysql1,data_app_new,$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'apps', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': "'@app_n'.split(',')"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[39]原语 apps = @sdf sys_eval with ("@app_n".split(",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'apps', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'str($apps)[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[40]原语 apps = @sdf sys_eval with (str($apps)[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_all', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,merge_state from data_app_new where app in ($apps) and merge_state =1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[41]原语 app_all = load db by mysql1 with select id,merge_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_all', 'Action': 'add', 'add': 'merge_state', 'by': '3'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[42]原语 app_all = add merge_state by 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_all', 'Action': 'add', 'add': 'app_merges', 'by': '""'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[43]原语 app_all = add app_merges by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_all', 'Action': '@udf', '@udf': 'app_all', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[44]原语 app_all = @udf app_all by udf0.df_set_index with i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'app_all', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[45]原语 @udf app_all by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,app_sum from data_app_new where merge_state = 2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[47]原语 app = @udf RS.load_mysql_sql with (mysql1,select a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[48]原语 app = @udf app by udf0.df_set_index with app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app', 'by': 'app.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[49]原语 app = add app by (app.index) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'app_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[50]原语 a=@udf SSDB.hclear with app_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_merge', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第25行foreach语句中]执行第[51]原语 store app to ssdb by ssdb0 with app_merge as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_25

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



