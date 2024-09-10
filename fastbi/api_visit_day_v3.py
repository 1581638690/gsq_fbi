#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_visit_day
#datetime: 2024-08-30T16:10:53.460426
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
		add_the_error('[api_visit_day.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'xlink/api_visit_hx_day'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[21]原语 a = @udf ZFile.list_dir with xlink/api_visit_hx_da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.k', 'Action': 'lambda', 'lambda': 'filename', 'by': 'x:x[30:-4]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[24]原语 a.k = lambda filename by (x:x[30:-4]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a', 'Action': 'filter', 'filter': 'a', 'by': "k != '$k1' or k != '$k2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[25]原语 a = filter a by k != "$k1" or k != "$k2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.k1', 'Action': 'lambda', 'lambda': 'k', 'by': 'x:time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(x)))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[26]原语 a.k1 = lambda k by (x:time.strftime("%Y-%m-%d %H:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.k1', 'Action': 'lambda', 'lambda': 'k1', 'by': 'x:x[:-9]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[27]原语 a.k1 = lambda k1 by (x:x[:-9]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'a', 'Action': 'order', 'order': 'a', 'by': 'k', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[29]原语 a = order a by k with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'k1', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[30]原语 k1 = eval a by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'filename'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[31]原语 a = loc a by filename 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'day', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[34]原语 day = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'a', 'with': 'name=$1', 'run': '""\n##取出已处理的数据\nday_1 = load pq by @name\nday = union day,day_1\n##删除已经处理过的数据\nbb = @udf ZFile.rm_file with @name\n""'}
	try:
		ptree['lineno']=36
		ptree['funs']=block_foreach_36
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[36]原语 foreach a run "##取出已处理的数据day_1 = load pq by @named... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'day_1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[44]原语 drop day_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'day', 'Action': 'group', 'group': 'day', 'by': 'app,url,srcip,dstip,account', 'agg': 'visit_num:sum,visit_flow:sum,time:max'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[46]原语 day = group day by app,url,srcip,dstip,account agg... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'day', 'Action': '@udf', '@udf': 'day', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[47]原语 day = @udf day by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'day', 'as': "'visit_num_sum':'visit_num','visit_flow_sum':'visit_flow','time_max':'time'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[48]原语 rename day as ("visit_num_sum":"visit_num","visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'day', 'Action': 'order', 'order': 'day', 'by': 'visit_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[49]原语 day = order day by visit_num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'day', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[51]原语 num = eval day by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num > 400000', 'with': '""\nnum1 = @sdf sys_eval with (($num-400000)*-1)\nday1 = limit day by 400000\nday2 = limit day by $num1,\nday2 = add hh by 1\nday2 = group day2 by hh agg visit_num:sum,visit_flow:sum,time:max\nvisit_num = eval day2 by iloc[0,0]\nvisit_flow = eval day2 by iloc[0,1]\ntime = eval day2 by iloc[0,2]\nday = @udf day1 by udf0.df_append with (sum2,sum2,sum2,sum2,sum2,$visit_num,$visit_flow,$time)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=53
		ptree['funs']=block_if_53
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[53]原语 if $num > 400000 with "num1 = @sdf sys_eval with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'day', 'by': 'visit_num:int,visit_flow:int,time:datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[65]原语 alter day by visit_num:int,visit_flow:int,time:dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'day', 'to': 'ckh', 'by': 'ckh', 'with': 'api_visit_day'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[67]原语 store day to ckh by ckh with api_visit_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_visit_day.fbi]执行第[72]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],72

#主函数结束,开始块函数

def block_foreach_36(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'day_1', 'Action': 'load', 'load': 'pq', 'by': '@name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第36行foreach语句中]执行第[38]原语 day_1 = load pq by @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'day', 'Action': 'union', 'union': 'day,day_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第36行foreach语句中]执行第[39]原语 day = union day,day_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': '@name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第36行foreach语句中]执行第[41]原语 bb = @udf ZFile.rm_file with @name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_36

def block_if_53(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'num1', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '($num-400000)*-1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[54]原语 num1 = @sdf sys_eval with (($num-400000)*-1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'day1', 'Action': 'limit', 'limit': 'day', 'by': '400000'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[55]原语 day1 = limit day by 400000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'day2', 'Action': 'limit', 'limit': 'day', 'by': '$num1,'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[56]原语 day2 = limit day by $num1, 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'day2', 'Action': 'add', 'add': 'hh', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[57]原语 day2 = add hh by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'day2', 'Action': 'group', 'group': 'day2', 'by': 'hh', 'agg': 'visit_num:sum,visit_flow:sum,time:max'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[58]原语 day2 = group day2 by hh agg visit_num:sum,visit_fl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_num', 'Action': 'eval', 'eval': 'day2', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[59]原语 visit_num = eval day2 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_flow', 'Action': 'eval', 'eval': 'day2', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[60]原语 visit_flow = eval day2 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time', 'Action': 'eval', 'eval': 'day2', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[61]原语 time = eval day2 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'day', 'Action': '@udf', '@udf': 'day1', 'by': 'udf0.df_append', 'with': 'sum2,sum2,sum2,sum2,sum2,$visit_num,$visit_flow,$time'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第53行if语句中]执行第[62]原语 day = @udf day1 by udf0.df_append with (sum2,sum2,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_53

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



