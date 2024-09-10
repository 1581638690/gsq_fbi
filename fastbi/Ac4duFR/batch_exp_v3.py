#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: Ac4duFR/batch_exp
#datetime: 2024-08-30T16:10:58.692381
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
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[14]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'v', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '@ids,replace("|",",")'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[16]原语 v = @sdf sys_str with (@ids,replace("|",",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ids1', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '@ids==""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[18]原语 ids1 = @sdf sys_eval with (@ids=="") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'cc', 'Action': 'if', 'if': '$ids1', 'with': '""\n#获取表单中的条件信息\ndatas = @udf udf0.new_df with id\na = load ssdb by ssdb0 with @data_key\n#保存\ndatas,c = @udf a by CRUD.query_table with (@link,@table)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=26
		ptree['funs']=block_if_26
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[26]原语 cc = if $ids1 with "#获取表单中的条件信息datas = @udf udf0.n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'a', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$ids1,"datas =@udf CRUD.load_mysql_sql with (@link,select * from @table where id in ($v))"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[33]原语 a = @sdf sys_unif_run with ($ids1,"datas =@udf CRU... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select type,type1 from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[36]原语 type = load db by mysql1 with select type,type1 fr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,type', 'by': 'type,type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[37]原语 datas = join datas,type by type,type with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'by': '_id,api,api_name,app,app_name,dest_ip,dest_port,method,length,first_time,last_time,state,type,type1,more'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[38]原语 datas = loc datas by _id,api,api_name,app,app_name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.more', 'Action': 'lambda', 'lambda': 'more', 'by': 'x: json.loads(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[40]原语 datas.more = lambda more by x: json.loads(x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.more', 'Action': 'lambda', 'lambda': 'more', 'by': 'x: x[-1] if isinstance(x,list) else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[41]原语 datas.more = lambda more by x: x[-1] if isinstance... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datas.more', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[42]原语 alter datas.more as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.more', 'Action': 'lambda', 'lambda': 'more', 'by': 'x:x[0:30000]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[43]原语 datas.more = lambda more by (x:x[0:30000]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': "'api':'接口','api_name':'接口名','app':'应用','app_name':'应用名','dest_ip':'部署IP','dest_port':'部署端口','method':'请求类型','length':'返回数据最大数据量','first_time':'首次发现时间','last_time':'最新监测时间','state':'弱点状态','type':'弱点 类型','type1':'弱点类型','more':'详情'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[44]原语 rename datas as ("api":"接口","api_name":"接口名","app"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datas', 'to': 'csv', 'by': '@file_name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[46]原语 store datas to csv by @file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[Ac4duFR/batch_exp.fbi]执行第[48]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],48

#主函数结束,开始块函数

def block_if_26(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第26行if语句中]执行第[28]原语 datas = @udf udf0.new_df with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第26行if语句中]执行第[29]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第26行if语句中]执行第[31]原语 datas,c = @udf a by CRUD.query_table with (@link,@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_26

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



