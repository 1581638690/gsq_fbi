#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: dynamic_log_query
#datetime: 2024-08-30T16:10:53.263705
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
		add_the_error('[dynamic_log_query.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[15]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[16]原语 a = @udf a by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_name', 'Action': 'eval', 'eval': 'a', 'by': 'param0.values[0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[19]原语 app_name = eval a by param0.values[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'user_name', 'Action': 'eval', 'eval': 'a', 'by': 'param1.values[0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[21]原语 user_name = eval a by param1.values[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'action', 'Action': 'eval', 'eval': 'a', 'by': 'param2.values[0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[23]原语 action = eval a by param2.values[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'a', 'by': 'beginTime.values[0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[25]原语 time1 = eval a by beginTime.values[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'a', 'by': 'endTime.values[0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[26]原语 time2 = eval a by endTime.values[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'll', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'logList_all'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[30]原语 ll = load ssdb by ssdb0 with logList_all 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$app_name' != '' and '$app_name' != '全部'", 'with': '""\nll = filter ll by 应用名 == \'$app_name\'\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=32
		ptree['funs']=block_if_32
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[32]原语 if "$app_name" != "" and "$app_name" != "全部" with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$user_name' != '' and '$user_name' != '全部'", 'with': '""\nll = filter ll by 用户 == \'$user_name\'\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=36
		ptree['funs']=block_if_36
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[36]原语 if "$user_name" != "" and "$user_name" != "全部" wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$action' != '' and '$action' != '全部'", 'with': '""\nll = filter ll by 动作行为 == \'$action\'\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=40
		ptree['funs']=block_if_40
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[40]原语 if "$action" != "" and "$action" != "全部" with "ll ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$time1' != ''", 'with': '""\ntime1 = @sdf sys_lambda with ($time1,x:x.replace(\' \',\'T\'))\ntime1 = @sdf sys_lambda with ($time1,x:x + \':00\')\nll = filter ll by 时间 >= \'$time1\'\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=44
		ptree['funs']=block_if_44
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[44]原语 if "$time1" != "" with "time1 = @sdf sys_lambda wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$time2' != ''", 'with': '""\ntime2 = @sdf sys_lambda with ($time2,x:x.replace(\' \',\'T\'))\ntime2 = @sdf sys_lambda with ($time2,x:x + \':00\')\nll = filter ll by 时间 <= \'$time2\'\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=50
		ptree['funs']=block_if_50
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[50]原语 if "$time2" != "" with "time2 = @sdf sys_lambda wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'll.时间', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[56]原语 alter ll.时间 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'll.时间', 'Action': 'lambda', 'lambda': '时间', 'by': 'x:x[0:16]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[57]原语 ll.时间 = lambda 时间 by (x:x[0:16]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'll.时间', 'Action': 'lambda', 'lambda': '时间', 'by': "x:x.replace('T',' ')"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[58]原语 ll.时间 = lambda 时间 by (x:x.replace("T"," ")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'll', 'Action': 'order', 'order': 'll', 'by': '时间', 'with': 'desc limit 200'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[61]原语 ll = order ll by 时间 with desc limit 200 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '时间,用户,应用名,接口事件,动作行为,操作参数,width'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[64]原语 new = @udf udf0.new_df with (时间,用户,应用名,接口事件,动作行为,操... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new', 'Action': '@udf', '@udf': 'new', 'by': 'udf0.df_append', 'with': '170,100,180,220,150,460,td_width'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[65]原语 new = @udf new by udf0.df_append with (170,100,180... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'new', 'Action': 'loc', 'loc': 'new', 'by': 'width', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[66]原语 new = loc new by width to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'll', 'Action': 'union', 'union': 'new,ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[67]原语 ll = union new,ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'll', 'Action': 'loc', 'loc': 'll', 'by': '时间,用户,应用名,接口事件,动作行为,操作参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[68]原语 ll = loc ll by 时间,用户,应用名,接口事件,动作行为,操作参数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'll', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[71]原语 push ll as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[dynamic_log_query.fbi]执行第[74]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],74

#主函数结束,开始块函数

def block_if_32(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'll', 'Action': 'filter', 'filter': 'll', 'by': "应用名 == '$app_name'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第32行if语句中]执行第[33]原语 ll = filter ll by 应用名 == "$app_name" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_32

def block_if_36(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'll', 'Action': 'filter', 'filter': 'll', 'by': "用户 == '$user_name'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第36行if语句中]执行第[37]原语 ll = filter ll by 用户 == "$user_name" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_36

def block_if_40(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'll', 'Action': 'filter', 'filter': 'll', 'by': "动作行为 == '$action'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[41]原语 ll = filter ll by 动作行为 == "$action" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_40

def block_if_44(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'time1', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$time1,x:x.replace(' ','T')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第44行if语句中]执行第[45]原语 time1 = @sdf sys_lambda with ($time1,x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'time1', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$time1,x:x + ':00'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第44行if语句中]执行第[46]原语 time1 = @sdf sys_lambda with ($time1,x:x + ":00") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'll', 'Action': 'filter', 'filter': 'll', 'by': "时间 >= '$time1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第44行if语句中]执行第[47]原语 ll = filter ll by 时间 >= "$time1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_44

def block_if_50(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'time2', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$time2,x:x.replace(' ','T')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第50行if语句中]执行第[51]原语 time2 = @sdf sys_lambda with ($time2,x:x.replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'time2', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$time2,x:x + ':00'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第50行if语句中]执行第[52]原语 time2 = @sdf sys_lambda with ($time2,x:x + ":00") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'll', 'Action': 'filter', 'filter': 'll', 'by': "时间 <= '$time2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第50行if语句中]执行第[53]原语 ll = filter ll by 时间 <= "$time2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_50

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



