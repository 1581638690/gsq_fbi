#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_new_1/batch_exp
#datetime: 2024-08-30T16:10:56.532988
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
		add_the_error('[app_new_1/batch_exp.fbi]执行第[23]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[app_new_1/batch_exp.fbi]执行第[25]原语 v = @sdf sys_str with (@ids,replace("|",",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[app_new_1/batch_exp.fbi]执行第[27]原语 ids1 = @sdf sys_eval with (@ids=="") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'cc', 'Action': 'if', 'if': '$ids1', 'with': '""\n#获取表单中的条件信息\ndatas = @udf udf0.new_df with id\na = load ssdb by ssdb0 with @data_key\n#保存\ndatas,c = @udf a by CRUD.query_table with (@link,@table,app_type = 1)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=35
		ptree['funs']=block_if_35
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[35]原语 cc = if $ids1 with "#获取表单中的条件信息datas = @udf udf0.n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[app_new_1/batch_exp.fbi]执行第[42]原语 a = @sdf sys_unif_run with ($ids1,"datas =@udf CRU... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'gmt_create,gmt_modified,creator,owner,res_label,req_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[44]原语 datas = loc datas drop (gmt_create,gmt_modified,cr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"高敏感" if x ==\'3\' else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[45]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"中敏感" if x ==\'2\' else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[46]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"低敏感" if x ==\'1\' else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[47]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:"非敏感" if x ==\'0\' else x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[48]原语 datas.sensitive_label = lambda sensitive_label by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.app_status', 'Action': 'lambda', 'lambda': 'app_status', 'by': 'x:"已审计" if x ==\'1\' else "未审计"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[49]原语 datas.app_status = lambda app_status by x:"已审计" if... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.app_type', 'Action': 'lambda', 'lambda': 'app_type', 'by': 'x:"内部应用" if x ==1 else "外部应用"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[50]原语 datas.app_type = lambda app_type by x:"内部应用" if x ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sx', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:app_sx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[52]原语 sx = load ssdb by ssdb0 with dd:app_sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sx', 'Action': 'add', 'add': 'id', 'by': 'sx.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[53]原语 sx  = add id by sx.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sx', 'as': '"sysname":"关联应用"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[54]原语 rename sx as ("sysname":"关联应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,sx', 'by': 'sx,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[55]原语 datas = join datas,sx by sx,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id,sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[56]原语 datas = loc datas drop id,sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[57]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'active', 'Action': 'add', 'add': 'id', 'by': 'active.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[58]原语 active  = add id by active.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'active', 'as': '"value":"活跃状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[59]原语 rename active as ("value":"活跃状态") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'datas', 'Action': 'alter', 'alter': 'datas.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[60]原语 datas = alter datas.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,active', 'by': 'active,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[61]原语 datas = join datas,active by active,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'id_x,id_y,active,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[62]原语 datas = loc datas drop id_x,id_y,active,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"app":"应用IP/域名","app_title":"标题","name":"应用名称","first_time":"首次发现时间","server":"服务器信息","visits_num":"访问数量","visits_flow":"访问流量","monitor_flow":"审计访问数量","api_num":"接口数量","imp_api_num":"审计接口数量","srcip_num":"访问IP数量","account_num":"访问账号数量","sensitive_label":"敏感标签","dstip_num":"部署数量","dstip":"目的IP","dstport":"目的端口","sj_num":"审计访问数量","last_time":"最后修改时间","app_status":"审计状态","scope":"应用标签","app_type":"应用类型","app_sum":"子应用","app_merges":"合并应用名","merge_state":"合并状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[64]原语 rename datas as ("app":"应用IP/域名","app_title":"标题",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datas', 'to': 'csv', 'by': '@file_name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[66]原语 store datas to csv by @file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_new_1/batch_exp.fbi]执行第[68]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],68

#主函数结束,开始块函数

def block_if_35(ptree):

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
		add_the_error('[第35行if语句中]执行第[37]原语 datas = @udf udf0.new_df with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第35行if语句中]执行第[38]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas,c', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.query_table', 'with': '@link,@table,app_type = 1'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第35行if语句中]执行第[40]原语 datas,c = @udf a by CRUD.query_table with (@link,@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_35

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



