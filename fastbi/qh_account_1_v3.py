#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_account_1
#datetime: 2024-08-30T16:10:55.749808
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
		add_the_error('[qh_account_1.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_hx limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[18]原语 ccc = load ckh by ckh with select app from api_hx ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接 或者 无数据更新！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[qh_account_1.fbi]执行第[19]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[19]原语 assert find_df_have_data("ccc",ptree) as exit with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'account_hx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[22]原语 aa = load ssdb by ssdb0 with account_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[24]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_hx'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=25
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[25]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[27]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_hx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[29]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[30]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_hx'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[31]原语 store aa to ssdb by ssdb0 with account_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[35]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month1,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[36]原语 month = @sdf format_now with ($month1,"%Y-%m-%dT00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month1,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[37]原语 month1 = @sdf format_now with ($month1,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[38]原语 month2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$month2,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[39]原语 month2 = @sdf format_now with ($month2,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'time_date', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$month1,$month2,1D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[40]原语 time_date = @udf udf0.new_df_timerange with ($mont... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_date', 'Action': 'loc', 'loc': 'time_date', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[41]原语 time_date = loc time_date by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'time_date.end_time', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[42]原语 time_date.end_time = lambda end_time by (x:x[5:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_date', 'Action': 'loc', 'loc': 'time_date', 'by': 'end_time', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[43]原语 time_date = loc time_date by end_time to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1w'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[46]原语 day = @sdf sys_now with -1w 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[47]原语 week = @sdf format_now with ($day,"%Y-%m-%dT00:00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-6d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[48]原语 day1 = @sdf sys_now with -6d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day1,"%Y-%m-%d 00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[49]原语 week1 = @sdf format_now with ($day1,"%Y-%m-%d 00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[50]原语 day2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'week2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day2,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[51]原语 week2 = @sdf format_now with ($day2,"%Y-%m-%d %H:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'time_d', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$week1,$week2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[52]原语 time_d = @udf udf0.new_df_timerange with ($week1,$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'time_d.times', 'Action': 'lambda', 'lambda': 'start_time', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[53]原语 time_d.times = lambda start_time by (x:x[5:10]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'time_d.time2', 'Action': 'lambda', 'lambda': 'start_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[54]原语 time_d.time2 = lambda start_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_d', 'Action': 'loc', 'loc': 'time_d', 'by': 'times,time2'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[55]原语 time_d = loc time_d by times,time2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[58]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[59]原语 day2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[60]原语 day1 = @sdf format_now with ($day,"%Y-%m-%d %H:00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day2,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[61]原语 day2 = @sdf format_now with ($day2,"%Y-%m-%d %H:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day1,$day2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[62]原语 j_hour = @udf udf0.new_df_timerange with ($day1,$d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.times', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[0:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[63]原语 j_hour.times = lambda end_time by (x:x[0:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'times'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[64]原语 j_hour = loc j_hour by times 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'accountlist1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select account from data_account_new where portrait_status = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[67]原语 accountlist1 = load db by mysql1 with select accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'accountlist1', 'by': 'account:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[68]原语 alter accountlist1 by account:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mon_ll', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,SUBSTRING(toString(time),6,5) as times,sum(visit_num) as time_count,sum(visit_flow) as llk from api_hx where time > '$month' and account != '' and account != '未知' group by account,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[70]原语 mon_ll = load ckh by ckh with select account,SUBST... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'mon_ll', 'by': 'account:str,times:str,time_count:int,llk:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[71]原语 alter mon_ll by account:str,times:str,time_count:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mon_ll.llk', 'Action': 'lambda', 'lambda': 'llk', 'by': 'x:round(x/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[72]原语 mon_ll.llk = lambda llk by (x:round(x/1024,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_url', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,url,sum(visit_num) as url_num,sum(visit_flow) as flow from api_hx where time >= '$time1' and time < '$time2' and account != '' and account != '未知' group by account,url"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[74]原语 visit_url = load ckh by ckh with select account,ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_url', 'by': 'account:str,url:str,url_num:int,flow:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[75]原语 alter visit_url by account:str,url:str,url_num:int... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_dstip', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,dstip,sum(visit_num) as dstip_num from api_hx where time >= '$time1' and time < '$time2' and account != '' and account != '未知' group by account,dstip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[76]原语 visit_dstip = load ckh by ckh with select account,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_dstip', 'by': 'account:str,dstip:str,dstip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[77]原语 alter visit_dstip by account:str,dstip:str,dstip_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_app', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,app,sum(visit_num) as app_num from api_hx where time >= '$time1' and time < '$time2' and account != '' and account != '未知' group by account,app"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[78]原语 visit_app = load ckh by ckh with select account,ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_app', 'by': 'account:str,app:str,app_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[79]原语 alter visit_app by account:str,app:str,app_num:int... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_srcip', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,srcip,sum(visit_num) as srcip_num from api_hx where time >= '$time1' and time < '$time2' and account != '' and account != '未知' group by account,srcip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[80]原语 visit_srcip = load ckh by ckh with select account,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_srcip', 'by': 'account:str,srcip:str,srcip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[81]原语 alter visit_srcip by account:str,srcip:str,srcip_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_api_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct url,api_type from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[82]原语 data_api_new = load db by mysql1 with select disti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api_new', 'Action': '@udf', '@udf': 'data_api_new', 'by': 'udf0.df_fillna_cols', 'with': "url:'',api_type:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[83]原语 data_api_new = @udf data_api_new by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_api_new', 'by': 'url:str,api_type:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[84]原语 alter data_api_new by url:str,api_type:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_api_new', 'by': 'api_type:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[85]原语 alter data_api_new by api_type:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[86]原语 api_type = load ssdb with dd:API-api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_type', 'Action': '@udf', '@udf': 'data_api_new,api_type', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[87]原语 api_type = @udf data_api_new,api_type by SP.tag2di... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_type.api_type', 'Action': 'lambda', 'lambda': 'api_type', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[88]原语 api_type.api_type = lambda api_type by (x:x+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_type', 'Action': 'group', 'group': 'api_type', 'by': 'url', 'agg': 'api_type:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[89]原语 api_type = group api_type by url agg api_type:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_type', 'Action': 'loc', 'loc': 'api_type', 'by': 'index', 'to': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[90]原语 api_type = loc api_type by index to url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_type.api_type', 'Action': 'lambda', 'lambda': 'api_type_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[91]原语 api_type.api_type = lambda api_type_sum by (x:x[:-... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'visit_url', 'Action': 'join', 'join': 'visit_url,api_type', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[92]原语 visit_url = join visit_url,api_type by url,url wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_url', 'as': "'api_type':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[93]原语 rename visit_url as ("api_type":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_url', 'Action': 'loc', 'loc': 'visit_url', 'by': 'account,url,url_num,flow,value'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[94]原语 visit_url = loc visit_url by account,url,url_num,f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_url', 'Action': '@udf', '@udf': 'visit_url', 'by': 'udf0.df_fillna_cols', 'with': "account:'',url:'',url_num:0,flow:0,value:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[95]原语 visit_url = @udf visit_url by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_api_new'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[96]原语 drop data_api_new 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'api_type'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[97]原语 drop api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'week_ll', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,SUBSTRING(toString(time),6,8) as times,sum(visit_num) as time_count from api_hx where time >'$week' and account != '' and account != '未知' group by account,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[99]原语 week_ll = load ckh by ckh with select account,SUBS... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'week_ll', 'by': 'account:str,times:str,time_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[100]原语 alter week_ll by account:str,times:str,time_count:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_24', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account,SUBSTRING(toString(time),1,13) as times,sum(visit_num) as count from api_hx where time > '$day1' and account != '' and account != '未知' group by account,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[102]原语 account_24 = load ckh by ckh with select account,S... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'account_24', 'by': 'account:str,times:str,count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[103]原语 alter account_24 by account:str,times:str,count:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'accountlist1', 'with': 'account=$1', 'run': '""\n#24小时平均访问次数--------------------------------------------------------------------------------\naccount24 = filter account_24 by account == \'@account\'\n#account24 = filter account_24 by account == \'0\'\naccount24 = join j_hour,account24 by times,times with left\naccount24 = @udf account24 by udf0.df_fillna_cols with count:0\naccount24.times = lambda times by (x:x[11:])\naccount24.times = lambda times by (x:x+\'时\')\naccount24 = loc account24 by times to index\naccount24 = loc account24 by count\nrename account24 as (\'count\':\'每小时访问次数\')\nstore account24 to ssdb by ssdb0 with z:@account:time_24\n##月流量趋势-----------------------------------------------------------------------------\nv1 = filter mon_ll by account == \'@account\'\nv1 = loc v1 by times to index\nss = join v1,time_date by index,index with right\nss = loc ss by (time_count,llk)\nss = @udf ss by udf0.df_fillna_cols with time_count:0,llk:0\nss_mean = loc ss by time_count,llk\nss_mean = add ss by 1\nss_mean = group ss_mean by ss agg time_count:mean,llk:mean\ntime_count_mean = eval ss_mean by iloc[0,0]\nif $time_count_mean > 10000 with ss.time_count = lambda time_count by (x:round(x/10000,2))\nif $time_count_mean > 10000 with rename ss by ("time_count":"访问数量(万)")\nif $time_count_mean <= 10000 with rename ss by ("time_count":"访问数量")\nllk_mean = eval ss_mean by iloc[0,1]\nif $llk_mean <= 1024 with ss.llk = lambda llk by (x:x)\nif 1024 < $llk_mean <= 1048576 with ss.llk = lambda llk by (x:round(x/1024,2))\nif $llk_mean > 1048576 with ss.llk = lambda llk by (x:round(x/1048576,2))\nif $llk_mean <= 1024 with rename ss by ("llk":"流量(B)")\nif 1024 < $llk_mean <= 1048576 with rename ss by ("llk":"流量(k)")\nif $llk_mean > 1048576 with rename ss by ("llk":"流量(M)")\nstore ss to ssdb with acc:@account:timeh\n#应用IP清单 admin -------------------------------------------------------------------------------\nipls = filter visit_dstip by account == \'@account\'\nipls_ll = load pq by dt_table/account_visit_dstip1_@account.pq\nipls = union ipls,ipls_ll\nipls = group ipls by account,dstip agg dstip_num:sum\nipls = @udf ipls by udf0.df_reset_index\nrename ipls as (\'dstip_num_sum\':\'dstip_num\')\nipls1 = distinct ipls by dstip with first\n## 动态表格\nvisit_dstip1 = loc ipls1 by account,dstip,dstip_num\nvisit_dstip1 = order visit_dstip1 by dstip_num with desc limit 1000\n#保存为pq文件\nstore visit_dstip1 to pq by dt_table/account_visit_dstip1_@account.pq\n#重命名\nrename visit_dstip1 as ("account":"账号","dstip":"目的IP","dstip_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,account_visit_dstip1_@account,-,-\n#保存Q\nstore visit_dstip1 to ssdb by ssdb0 with account_visit_dstip1_@account as Q\ndrop visit_dstip1\nipls = loc ipls by dstip,dstip_num\nipls = order ipls by dstip_num with desc limit 10\nrename ipls by ("dstip":"访问应用IP",\'dstip_num\':\'访问数量\')\nstore ipls to ssdb with acc:@account:ipls\n#终端IP清单 -------------------------------------------------------------------------------\nsrcipls = filter visit_srcip by account == \'@account\'\nsrcipls_ll = load pq by dt_table/account_visit_srcip1_@account.pq\nsrcipls = union srcipls,srcipls_ll\nsrcipls = group srcipls by account,srcip agg srcip_num:sum\nsrcipls = @udf srcipls by udf0.df_reset_index\nrename srcipls as (\'srcip_num_sum\':\'srcip_num\')\nsrcipls1 = distinct srcipls by srcip with first\n##数量\nsrcip_count = @udf srcipls1 by udf0.df_count\nsrcip_count = add index by ("终端使用数量")\nsrcip_count = loc srcip_count by index to index\nstore srcip_count to ssdb with acc:@account:srcip_count\n## 动态表格\nvisit_srcip1 = loc srcipls by account,srcip,srcip_num\nvisit_srcip1 = order visit_srcip1 by srcip_num with desc limit 1000\n#保存为pq文件\nstore visit_srcip1 to pq by dt_table/account_visit_srcip1_@account.pq\n#重命名\nrename visit_srcip1 as ("account":"账号","srcip":"源IP","srcip_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,account_visit_srcip1_@account,-,-\n#保存Q\nstore visit_srcip1 to ssdb by ssdb0 with account_visit_srcip1_@account as Q\ndrop visit_srcip1\nsrcipls = loc srcipls by srcip,srcip_num\nsrcipls = order srcipls by srcip_num with desc limit 10\nrename srcipls by ("srcip":"终端IP",\'srcip_num\':\'访问数量\')\nstore srcipls to ssdb with acc:@account:srcipls\n#访问应用清单 -------------------------------------------------------------------------------\nappls = filter visit_app by account == \'@account\'\nappls_ll = load pq by dt_table/account_visit_app1_@account.pq\nappls = union appls,appls_ll\nappls = group appls by account,app agg app_num:sum\nappls = @udf appls by udf0.df_reset_index\nrename appls as (\'app_num_sum\':\'app_num\')\nappls1 = distinct appls by app with first\n###数量\nappls_count = @udf appls1 by udf0.df_count\nappls_count = add index by ("访问应用数量")\nappls_count = loc appls_count by index to index\nstore appls_count to ssdb with acc:@account:appls_count\n## 动态表格\nvisit_app1 = loc appls by account,app,app_num\nvisit_app1 = order visit_app1 by app_num with desc limit 1000\n#保存为pq文件\nstore visit_app1 to pq by dt_table/account_visit_app1_@account.pq\n#重命名\nrename visit_app1 as ("account":"账号","app":"应用IP/域名","app_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,account_visit_app1_@account,-,-\n#保存Q\nstore visit_app1 to ssdb by ssdb0 with account_visit_app1_@account as Q\ndrop visit_app1\nappls = loc appls by app,app_num\nappls = order appls by app_num with desc limit 10\nrename appls by ("app":"访问应用",\'app_num\':\'访问数量\')\nstore appls to ssdb with acc:@account:appls\n#访问接口清单--------------------------------------------------------------------------------\nurlls = filter visit_url by account == \'@account\'\nurlls_ll = load pq by dt_table/account_visit_url1_@account.pq\nurlls = union urlls,urlls_ll\nurlls = group urlls by account,url,value agg url_num:sum,flow:sum\nurlls = @udf urlls by udf0.df_reset_index\nrename urlls as (\'url_num_sum\':\'url_num\',\'flow_sum\':\'flow\')\n#urlls = filter visit_url by account == \'Stuartcraw\'\n## 动态表格\nurlls.flow = lambda flow by (x:round(x/1024,2))\nvisit_url1 = loc urlls by account,url,url_num,flow,value\nvisit_url1 = order visit_url1 by url_num with desc limit 1000\n#保存为pq文件\nstore visit_url1 to pq by dt_table/account_visit_url1_@account.pq\n#重命名\nrename visit_url1 as ("account":"账号","url":"访问接口","url_num":"访问次数","flow":"访问流量(k)","value":"接口类型")\n#清空Q\nb = load ssdb by ssdb0 query qclear,account_visit_url1_@account,-,-\n#保存Q\nstore visit_url1 to ssdb by ssdb0 with account_visit_url1_@account as Q\ndrop visit_url1\nurlls = loc urlls by url,url_num,flow,value\nurlls = order urlls by url_num with desc limit 10\nurlls = @udf urlls by udf0.df_fillna_cols with url:\'\',url_num:0,flow:0,value:\'\'\nalter urlls by flow:str\nrename urlls by ("url":"访问接口","url_num":"访问次数","flow":"访问流量(k)","value":"接口类型")\nurlls = @udf urlls by VL.set_col_width with (850,180,180,190)\nurlls = @udf urlls by VL.set_col_color with (#000,#000,#000,#000)\nstore urlls to ssdb with acc:@account:urlls\n#周热力图 admin --------------------------------------------------------------------------------------------------\nv2 = filter week_ll by account == \'@account\'\n#v2 = filter week_ll by account == \'68640161\'\nv2 = loc v2 by times,time_count\nv2 = add time2 by v2["times"]\nv2.time2 = str time2 by (slice(6,8))\nv2.times = str times by (slice(0,5))\nvv = join v2,time_d by [times,time2],[times,time2] with outer\nvv = @udf vv by udf0.df_fillna_cols with time_count:0\nvv = group vv by (times,time2) agg time_count:sum\nvv = @udf vv by udf0.df_unstack with time_count_sum\nvv = @udf vv by udf0.df_fillna with 0\nvv = @udf vv by udf0.df_sort_index\nstore vv to ssdb with accountweek:@account\n\n""'}
	try:
		ptree['lineno']=105
		ptree['funs']=block_foreach_105
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[105]原语 foreach accountlist1 run "#24小时平均访问次数-------------... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_account_1.fbi]执行第[266]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],266

#主函数结束,开始块函数

def block_foreach_105(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'account24', 'Action': 'filter', 'filter': 'account_24', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[107]原语 account24 = filter account_24 by account == "@acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account24', 'Action': 'join', 'join': 'j_hour,account24', 'by': 'times,times', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[109]原语 account24 = join j_hour,account24 by times,times w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account24', 'Action': '@udf', '@udf': 'account24', 'by': 'udf0.df_fillna_cols', 'with': 'count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[110]原语 account24 = @udf account24 by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'account24.times', 'Action': 'lambda', 'lambda': 'times', 'by': 'x:x[11:]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[111]原语 account24.times = lambda times by (x:x[11:]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'account24.times', 'Action': 'lambda', 'lambda': 'times', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[112]原语 account24.times = lambda times by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account24', 'Action': 'loc', 'loc': 'account24', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[113]原语 account24 = loc account24 by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account24', 'Action': 'loc', 'loc': 'account24', 'by': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[114]原语 account24 = loc account24 by count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account24', 'as': "'count':'每小时访问次数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[115]原语 rename account24 as ("count":"每小时访问次数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account24', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'z:@account:time_24'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[116]原语 store account24 to ssdb by ssdb0 with z:@account:t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'v1', 'Action': 'filter', 'filter': 'mon_ll', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[118]原语 v1 = filter mon_ll by account == "@account" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'v1', 'Action': 'loc', 'loc': 'v1', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[119]原语 v1 = loc v1 by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ss', 'Action': 'join', 'join': 'v1,time_date', 'by': 'index,index', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[120]原语 ss = join v1,time_date by index,index with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss', 'Action': 'loc', 'loc': 'ss', 'by': 'time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[121]原语 ss = loc ss by (time_count,llk) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_fillna_cols', 'with': 'time_count:0,llk:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[122]原语 ss = @udf ss by udf0.df_fillna_cols with time_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss_mean', 'Action': 'loc', 'loc': 'ss', 'by': 'time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[123]原语 ss_mean = loc ss by time_count,llk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss_mean', 'Action': 'add', 'add': 'ss', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[124]原语 ss_mean = add ss by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ss_mean', 'Action': 'group', 'group': 'ss_mean', 'by': 'ss', 'agg': 'time_count:mean,llk:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[125]原语 ss_mean = group ss_mean by ss agg time_count:mean,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time_count_mean', 'Action': 'eval', 'eval': 'ss_mean', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[126]原语 time_count_mean = eval ss_mean by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean > 10000', 'with': 'ss.time_count = lambda time_count by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=127
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[127]原语 if $time_count_mean > 10000 with ss.time_count = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean > 10000', 'with': 'rename ss by ("time_count":"访问数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=128
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[128]原语 if $time_count_mean > 10000 with rename ss by ("ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean <= 10000', 'with': 'rename ss by ("time_count":"访问数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=129
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[129]原语 if $time_count_mean <= 10000 with rename ss by ("t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'llk_mean', 'Action': 'eval', 'eval': 'ss_mean', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[130]原语 llk_mean = eval ss_mean by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean <= 1024', 'with': 'ss.llk = lambda llk by (x:x)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=131
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[131]原语 if $llk_mean <= 1024 with ss.llk = lambda llk by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $llk_mean <= 1048576', 'with': 'ss.llk = lambda llk by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=132
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[132]原语 if 1024 < $llk_mean <= 1048576 with ss.llk = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean > 1048576', 'with': 'ss.llk = lambda llk by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=133
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[133]原语 if $llk_mean > 1048576 with ss.llk = lambda llk by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean <= 1024', 'with': 'rename ss by ("llk":"流量(B)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=134
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[134]原语 if $llk_mean <= 1024 with rename ss by ("llk":"流量(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $llk_mean <= 1048576', 'with': 'rename ss by ("llk":"流量(k)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=135
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[135]原语 if 1024 < $llk_mean <= 1048576 with rename ss by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean > 1048576', 'with': 'rename ss by ("llk":"流量(M)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=136
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[136]原语 if $llk_mean > 1048576 with rename ss by ("llk":"流... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ss', 'to': 'ssdb', 'with': 'acc:@account:timeh'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[137]原语 store ss to ssdb with acc:@account:timeh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ipls', 'Action': 'filter', 'filter': 'visit_dstip', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[139]原语 ipls = filter visit_dstip by account == "@account"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ipls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/account_visit_dstip1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[140]原语 ipls_ll = load pq by dt_table/account_visit_dstip1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ipls', 'Action': 'union', 'union': 'ipls,ipls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[141]原语 ipls = union ipls,ipls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ipls', 'Action': 'group', 'group': 'ipls', 'by': 'account,dstip', 'agg': 'dstip_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[142]原语 ipls = group ipls by account,dstip agg dstip_num:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ipls', 'Action': '@udf', '@udf': 'ipls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[143]原语 ipls = @udf ipls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ipls', 'as': "'dstip_num_sum':'dstip_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[144]原语 rename ipls as ("dstip_num_sum":"dstip_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ipls1', 'Action': 'distinct', 'distinct': 'ipls', 'by': 'dstip', 'with': 'first'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[145]原语 ipls1 = distinct ipls by dstip with first 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_dstip1', 'Action': 'loc', 'loc': 'ipls1', 'by': 'account,dstip,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[147]原语 visit_dstip1 = loc ipls1 by account,dstip,dstip_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_dstip1', 'Action': 'order', 'order': 'visit_dstip1', 'by': 'dstip_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[148]原语 visit_dstip1 = order visit_dstip1 by dstip_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_dstip1', 'to': 'pq', 'by': 'dt_table/account_visit_dstip1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[150]原语 store visit_dstip1 to pq by dt_table/account_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_dstip1', 'as': '"account":"账号","dstip":"目的IP","dstip_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[152]原语 rename visit_dstip1 as ("account":"账号","dstip":"目的... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,account_visit_dstip1_@account,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[154]原语 b = load ssdb by ssdb0 query qclear,account_visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_dstip1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_visit_dstip1_@account', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[156]原语 store visit_dstip1 to ssdb by ssdb0 with account_v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_dstip1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[157]原语 drop visit_dstip1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ipls', 'Action': 'loc', 'loc': 'ipls', 'by': 'dstip,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[158]原语 ipls = loc ipls by dstip,dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ipls', 'Action': 'order', 'order': 'ipls', 'by': 'dstip_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[159]原语 ipls = order ipls by dstip_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ipls', 'by': '"dstip":"访问应用IP",\'dstip_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[160]原语 rename ipls by ("dstip":"访问应用IP","dstip_num":"访问数量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ipls', 'to': 'ssdb', 'with': 'acc:@account:ipls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[161]原语 store ipls to ssdb with acc:@account:ipls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'srcipls', 'Action': 'filter', 'filter': 'visit_srcip', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[163]原语 srcipls = filter visit_srcip by account == "@accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcipls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/account_visit_srcip1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[164]原语 srcipls_ll = load pq by dt_table/account_visit_src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'srcipls', 'Action': 'union', 'union': 'srcipls,srcipls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[165]原语 srcipls = union srcipls,srcipls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'srcipls', 'Action': 'group', 'group': 'srcipls', 'by': 'account,srcip', 'agg': 'srcip_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[166]原语 srcipls = group srcipls by account,srcip agg srcip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcipls', 'Action': '@udf', '@udf': 'srcipls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[167]原语 srcipls = @udf srcipls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'srcipls', 'as': "'srcip_num_sum':'srcip_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[168]原语 rename srcipls as ("srcip_num_sum":"srcip_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'srcipls1', 'Action': 'distinct', 'distinct': 'srcipls', 'by': 'srcip', 'with': 'first'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[169]原语 srcipls1 = distinct srcipls by srcip with first 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcip_count', 'Action': '@udf', '@udf': 'srcipls1', 'by': 'udf0.df_count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[171]原语 srcip_count = @udf srcipls1 by udf0.df_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'srcip_count', 'Action': 'add', 'add': 'index', 'by': '"终端使用数量"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[172]原语 srcip_count = add index by ("终端使用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcip_count', 'Action': 'loc', 'loc': 'srcip_count', 'by': 'index', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[173]原语 srcip_count = loc srcip_count by index to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'srcip_count', 'to': 'ssdb', 'with': 'acc:@account:srcip_count'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[174]原语 store srcip_count to ssdb with acc:@account:srcip_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_srcip1', 'Action': 'loc', 'loc': 'srcipls', 'by': 'account,srcip,srcip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[176]原语 visit_srcip1 = loc srcipls by account,srcip,srcip_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_srcip1', 'Action': 'order', 'order': 'visit_srcip1', 'by': 'srcip_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[177]原语 visit_srcip1 = order visit_srcip1 by srcip_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_srcip1', 'to': 'pq', 'by': 'dt_table/account_visit_srcip1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[179]原语 store visit_srcip1 to pq by dt_table/account_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_srcip1', 'as': '"account":"账号","srcip":"源IP","srcip_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[181]原语 rename visit_srcip1 as ("account":"账号","srcip":"源I... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,account_visit_srcip1_@account,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[183]原语 b = load ssdb by ssdb0 query qclear,account_visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_srcip1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_visit_srcip1_@account', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[185]原语 store visit_srcip1 to ssdb by ssdb0 with account_v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_srcip1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[186]原语 drop visit_srcip1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcipls', 'Action': 'loc', 'loc': 'srcipls', 'by': 'srcip,srcip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[187]原语 srcipls = loc srcipls by srcip,srcip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'srcipls', 'Action': 'order', 'order': 'srcipls', 'by': 'srcip_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[188]原语 srcipls = order srcipls by srcip_num with desc lim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'srcipls', 'by': '"srcip":"终端IP",\'srcip_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[189]原语 rename srcipls by ("srcip":"终端IP","srcip_num":"访问数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'srcipls', 'to': 'ssdb', 'with': 'acc:@account:srcipls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[190]原语 store srcipls to ssdb with acc:@account:srcipls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'appls', 'Action': 'filter', 'filter': 'visit_app', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[192]原语 appls = filter visit_app by account == "@account" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'appls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/account_visit_app1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[193]原语 appls_ll = load pq by dt_table/account_visit_app1_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'appls', 'Action': 'union', 'union': 'appls,appls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[194]原语 appls = union appls,appls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'appls', 'Action': 'group', 'group': 'appls', 'by': 'account,app', 'agg': 'app_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[195]原语 appls = group appls by account,app agg app_num:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'appls', 'Action': '@udf', '@udf': 'appls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[196]原语 appls = @udf appls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'appls', 'as': "'app_num_sum':'app_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[197]原语 rename appls as ("app_num_sum":"app_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'appls1', 'Action': 'distinct', 'distinct': 'appls', 'by': 'app', 'with': 'first'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[198]原语 appls1 = distinct appls by app with first 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'appls_count', 'Action': '@udf', '@udf': 'appls1', 'by': 'udf0.df_count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[200]原语 appls_count = @udf appls1 by udf0.df_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'appls_count', 'Action': 'add', 'add': 'index', 'by': '"访问应用数量"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[201]原语 appls_count = add index by ("访问应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'appls_count', 'Action': 'loc', 'loc': 'appls_count', 'by': 'index', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[202]原语 appls_count = loc appls_count by index to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'appls_count', 'to': 'ssdb', 'with': 'acc:@account:appls_count'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[203]原语 store appls_count to ssdb with acc:@account:appls_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_app1', 'Action': 'loc', 'loc': 'appls', 'by': 'account,app,app_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[205]原语 visit_app1 = loc appls by account,app,app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_app1', 'Action': 'order', 'order': 'visit_app1', 'by': 'app_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[206]原语 visit_app1 = order visit_app1 by app_num with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_app1', 'to': 'pq', 'by': 'dt_table/account_visit_app1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[208]原语 store visit_app1 to pq by dt_table/account_visit_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_app1', 'as': '"account":"账号","app":"应用IP/域名","app_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[210]原语 rename visit_app1 as ("account":"账号","app":"应用IP/域... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,account_visit_app1_@account,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[212]原语 b = load ssdb by ssdb0 query qclear,account_visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_app1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_visit_app1_@account', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[214]原语 store visit_app1 to ssdb by ssdb0 with account_vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_app1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[215]原语 drop visit_app1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'appls', 'Action': 'loc', 'loc': 'appls', 'by': 'app,app_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[216]原语 appls = loc appls by app,app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'appls', 'Action': 'order', 'order': 'appls', 'by': 'app_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[217]原语 appls = order appls by app_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'appls', 'by': '"app":"访问应用",\'app_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[218]原语 rename appls by ("app":"访问应用","app_num":"访问数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'appls', 'to': 'ssdb', 'with': 'acc:@account:appls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[219]原语 store appls to ssdb with acc:@account:appls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'urlls', 'Action': 'filter', 'filter': 'visit_url', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[221]原语 urlls = filter visit_url by account == "@account" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'urlls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/account_visit_url1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[222]原语 urlls_ll = load pq by dt_table/account_visit_url1_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'urlls', 'Action': 'union', 'union': 'urlls,urlls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[223]原语 urlls = union urlls,urlls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'urlls', 'Action': 'group', 'group': 'urlls', 'by': 'account,url,value', 'agg': 'url_num:sum,flow:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[224]原语 urlls = group urlls by account,url,value agg url_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urlls', 'Action': '@udf', '@udf': 'urlls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[225]原语 urlls = @udf urlls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'urlls', 'as': "'url_num_sum':'url_num','flow_sum':'flow'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[226]原语 rename urlls as ("url_num_sum":"url_num","flow_sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'urlls.flow', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[229]原语 urlls.flow = lambda flow by (x:round(x/1024,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_url1', 'Action': 'loc', 'loc': 'urlls', 'by': 'account,url,url_num,flow,value'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[230]原语 visit_url1 = loc urlls by account,url,url_num,flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_url1', 'Action': 'order', 'order': 'visit_url1', 'by': 'url_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[231]原语 visit_url1 = order visit_url1 by url_num with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_url1', 'to': 'pq', 'by': 'dt_table/account_visit_url1_@account.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[233]原语 store visit_url1 to pq by dt_table/account_visit_u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_url1', 'as': '"account":"账号","url":"访问接口","url_num":"访问次数","flow":"访问流量(k)","value":"接口类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[235]原语 rename visit_url1 as ("account":"账号","url":"访问接口",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,account_visit_url1_@account,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[237]原语 b = load ssdb by ssdb0 query qclear,account_visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_url1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_visit_url1_@account', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[239]原语 store visit_url1 to ssdb by ssdb0 with account_vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_url1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[240]原语 drop visit_url1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'urlls', 'Action': 'loc', 'loc': 'urlls', 'by': 'url,url_num,flow,value'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[241]原语 urlls = loc urlls by url,url_num,flow,value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'urlls', 'Action': 'order', 'order': 'urlls', 'by': 'url_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[242]原语 urlls = order urlls by url_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urlls', 'Action': '@udf', '@udf': 'urlls', 'by': 'udf0.df_fillna_cols', 'with': "url:'',url_num:0,flow:0,value:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[243]原语 urlls = @udf urlls by udf0.df_fillna_cols with url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'urlls', 'by': 'flow:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[244]原语 alter urlls by flow:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'urlls', 'by': '"url":"访问接口","url_num":"访问次数","flow":"访问流量(k)","value":"接口类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[245]原语 rename urlls by ("url":"访问接口","url_num":"访问次数","fl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urlls', 'Action': '@udf', '@udf': 'urlls', 'by': 'VL.set_col_width', 'with': '850,180,180,190'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[246]原语 urlls = @udf urlls by VL.set_col_width with (850,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urlls', 'Action': '@udf', '@udf': 'urlls', 'by': 'VL.set_col_color', 'with': '#000,#000,#000,#000'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[247]原语 urlls = @udf urlls by VL.set_col_color with (#000,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'urlls', 'to': 'ssdb', 'with': 'acc:@account:urlls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[248]原语 store urlls to ssdb with acc:@account:urlls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'v2', 'Action': 'filter', 'filter': 'week_ll', 'by': "account == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[250]原语 v2 = filter week_ll by account == "@account" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'v2', 'Action': 'loc', 'loc': 'v2', 'by': 'times,time_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[252]原语 v2 = loc v2 by times,time_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'v2', 'Action': 'add', 'add': 'time2', 'by': 'v2["times"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[253]原语 v2 = add time2 by v2["times"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'v2.time2', 'Action': 'str', 'str': 'time2', 'by': 'slice(6,8)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[254]原语 v2.time2 = str time2 by (slice(6,8)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'v2.times', 'Action': 'str', 'str': 'times', 'by': 'slice(0,5)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[255]原语 v2.times = str times by (slice(0,5)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'vv', 'Action': 'join', 'join': 'v2,time_d', 'by': '[times,time2],[times,time2]', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[256]原语 vv = join v2,time_d by [times,time2],[times,time2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'vv', 'Action': '@udf', '@udf': 'vv', 'by': 'udf0.df_fillna_cols', 'with': 'time_count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[257]原语 vv = @udf vv by udf0.df_fillna_cols with time_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'vv', 'Action': 'group', 'group': 'vv', 'by': 'times,time2', 'agg': 'time_count:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[258]原语 vv = group vv by (times,time2) agg time_count:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'vv', 'Action': '@udf', '@udf': 'vv', 'by': 'udf0.df_unstack', 'with': 'time_count_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[259]原语 vv = @udf vv by udf0.df_unstack with time_count_su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'vv', 'Action': '@udf', '@udf': 'vv', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[260]原语 vv = @udf vv by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'vv', 'Action': '@udf', '@udf': 'vv', 'by': 'udf0.df_sort_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[261]原语 vv = @udf vv by udf0.df_sort_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'vv', 'to': 'ssdb', 'with': 'accountweek:@account'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第105行foreach语句中]执行第[262]原语 store vv to ssdb with accountweek:@account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_105

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



