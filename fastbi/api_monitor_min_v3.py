#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_monitor_min
#datetime: 2024-08-30T16:10:54.610525
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
		add_the_error('[api_monitor_min.fbi]执行第[8]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'k', 'Action': '@sdf', '@sdf': 'sys_timestamp'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[10]原语 k = @sdf sys_timestamp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'xlink/api_monitor_min'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[15]原语 a = @udf ZFile.list_dir with xlink/api_monitor_min... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[18]原语 hour = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'a', 'with': 'name=$1', 'run': '""\n##取出数据\nmin_1 = load pkl by @name\nhour = union hour,min_1\n##删除已经处理过的数据\nb = @udf ZFile.rm_file with @name\n""'}
	try:
		ptree['lineno']=19
		ptree['funs']=block_foreach_19
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[19]原语 foreach a run "##取出数据min_1 = load pkl by @namehour... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'min_1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[27]原语 drop min_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hour.time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[29]原语 alter hour.time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.time1', 'Action': 'lambda', 'lambda': 'time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[30]原语 hour.time1 = lambda time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'hour.time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[31]原语 alter hour.time as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'hour', 'Action': 'group', 'group': 'hour', 'by': 'app,url,srcip,account,time1', 'agg': 'visit_num:sum,flow:sum,time:max'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[32]原语 hour = group hour by app,url,srcip,account,time1 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'hour', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[33]原语 hour = @udf hour by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'hour', 'as': "'visit_num_sum':'visit_num','flow_sum':'flow','time_max':'time'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[34]原语 rename hour as ("visit_num_sum":"visit_num","flow_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'hour', 'Action': 'order', 'order': 'hour', 'by': 'visit_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[35]原语 hour = order hour by visit_num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'tt', 'Action': 'group', 'group': 'hour', 'by': 'time1', 'agg': 'time1:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[36]原语 tt = group hour by time1 agg time1:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tt', 'Action': '@udf', '@udf': 'tt', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[37]原语 tt = @udf tt by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size > 0', 'with': 'tt1 = eval tt by iloc[0,0]'}
	try:
		ptree['lineno']=40
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[40]原语 if tt.index.size > 0 with tt1 = eval tt by iloc[0,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size > 0', 'with': "hour1 = filter hour by time1 == '$tt1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=41
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[41]原语 if tt.index.size > 0 with hour1 = filter hour by t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size > 0', 'with': 'hour1 = loc hour1 drop time1'}
	try:
		ptree['lineno']=42
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[42]原语 if tt.index.size > 0 with hour1 = loc hour1 drop t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size > 0', 'with': 'store hour1 to pkl by xlink/monitor/hour_$tt1/mon_hour_$k.pkl'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=43
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[43]原语 if tt.index.size > 0 with store hour1 to pkl by xl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '2 <= tt.index.size <= 3', 'with': 'tt2 = eval tt by iloc[1,0]'}
	try:
		ptree['lineno']=44
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[44]原语 if 2 <= tt.index.size <= 3 with tt2 = eval tt by i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '2 <= tt.index.size <= 3', 'with': "hour2 = filter hour by time1 == '$tt2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=45
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[45]原语 if 2 <= tt.index.size <= 3  with hour2 = filter ho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '2 <= tt.index.size <= 3', 'with': 'hour2 = loc hour2 drop time1'}
	try:
		ptree['lineno']=46
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[46]原语 if 2 <= tt.index.size <= 3 with hour2 = loc hour2 ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '2 <= tt.index.size <= 3', 'with': 'store hour2 to pkl by xlink/monitor/hour_$tt2/mon_hour_$k.pkl'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=47
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[47]原语 if 2 <= tt.index.size <= 3  with store hour2 to pk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size == 3', 'with': 'tt3 = eval tt by iloc[2,0]'}
	try:
		ptree['lineno']=48
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[48]原语 if tt.index.size == 3 with tt3 = eval tt by iloc[2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size == 3', 'with': "hour3 = filter hour by time1 == '$tt3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=49
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[49]原语 if tt.index.size == 3 with hour3 = filter hour by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size == 3', 'with': 'hour3 = loc hour3 drop time1'}
	try:
		ptree['lineno']=50
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[50]原语 if tt.index.size == 3 with hour3 = loc hour3 drop ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'tt.index.size == 3', 'with': 'store hour3 to pkl by xlink/monitor/hour_$tt3/mon_hour_$k.pkl'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=51
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[51]原语 if tt.index.size == 3 with store hour3 to pkl by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_monitor_min.fbi]执行第[55]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],55

#主函数结束,开始块函数

def block_foreach_19(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'min_1', 'Action': 'load', 'load': 'pkl', 'by': '@name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[21]原语 min_1 = load pkl by @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'hour', 'Action': 'union', 'union': 'hour,min_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[22]原语 hour = union hour,min_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': '@name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[24]原语 b = @udf ZFile.rm_file with @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_19

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



