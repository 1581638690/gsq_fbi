#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_app_1
#datetime: 2024-08-30T16:10:53.348302
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
		add_the_error('[qh_app_1.fbi]执行第[17]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_hx limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[20]原语 ccc = load ckh by ckh with select app from api_hx ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接 或者 无数据更新！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[qh_app_1.fbi]执行第[21]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[21]原语 assert find_df_have_data("ccc",ptree) as exit with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'app_hx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[24]原语 aa = load ssdb by ssdb0 with app_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[26]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_hx'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=27
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[27]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[29]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_hx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[31]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[32]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_hx'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[33]原语 store aa to ssdb by ssdb0 with app_hx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[36]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[qh_app_1.fbi]执行第[37]原语 month = @sdf format_now with ($month1,"%Y-%m-%dT00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[qh_app_1.fbi]执行第[38]原语 month1 = @sdf format_now with ($month1,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[39]原语 month2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[qh_app_1.fbi]执行第[40]原语 month2 = @sdf format_now with ($month2,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'time_date', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$month1,$month2,1D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[41]原语 time_date = @udf udf0.new_df_timerange with ($mont... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_date', 'Action': 'loc', 'loc': 'time_date', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[42]原语 time_date = loc time_date by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'time_date.end_time', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[43]原语 time_date.end_time = lambda end_time by (x:x[5:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_date', 'Action': 'loc', 'loc': 'time_date', 'by': 'end_time', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[44]原语 time_date = loc time_date by end_time to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[47]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[48]原语 day2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[qh_app_1.fbi]执行第[49]原语 day1 = @sdf format_now with ($day,"%Y-%m-%d %H:00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[qh_app_1.fbi]执行第[50]原语 day2 = @sdf format_now with ($day2,"%Y-%m-%d %H:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day1,$day2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[51]原语 j_hour = @udf udf0.new_df_timerange with ($day1,$d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.times', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[0:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[52]原语 j_hour.times = lambda end_time by (x:x[0:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'times'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[53]原语 j_hour = loc j_hour by times 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'applist', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,app_sum,merge_state from data_app_new where merge_state != 1 and app_type = 1 and portrait_status = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[56]原语 applist = load db by mysql1 with select app,app_su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist', 'Action': '@udf', '@udf': 'applist', 'by': 'udf0.df_fillna_cols', 'with': "app:'',app_sum:'',merge_state:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[57]原语 applist = @udf applist by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'applist', 'by': 'app:str,app_sum:str,merge_state:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[58]原语 alter applist by app:str,app_sum:str,merge_state:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'applist', 'Action': 'loc', 'loc': 'applist', 'by': 'app,app_sum,merge_state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[59]原语 applist = loc applist by app,app_sum,merge_state 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mon_ll', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,SUBSTRING(toString(time),6,5) as times,sum(visit_num) as time_count,sum(visit_flow) as llk from api_hx where time > '$month' group by app,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[62]原语 mon_ll = load ckh by ckh with select app,SUBSTRING... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'mon_ll', 'by': 'app:str,times:str,time_count:int,llk:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[63]原语 alter mon_ll by app:str,times:str,time_count:int,l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'mon_ll', 'Action': 'order', 'order': 'mon_ll', 'by': 'times', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[64]原语 mon_ll = order mon_ll by times with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mon_ll.llk', 'Action': 'lambda', 'lambda': 'llk', 'by': 'x:round(x/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[65]原语 mon_ll.llk = lambda llk by (x:round(x/1024,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_url', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,url,sum(visit_num) as url_num from api_hx where time >= '$time1' and time < '$time2' group by app,url"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[67]原语 visit_url = load ckh by ckh with select app,url,su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_url', 'by': 'app:str,url:str,url_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[68]原语 alter visit_url by app:str,url:str,url_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_dest', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,dstip,sum(visit_num) as dstip_num from api_hx where time >= '$time1' and time < '$time2' group by app,dstip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[69]原语 visit_dest = load ckh by ckh with select app,dstip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_dest', 'by': 'app:str,dstip:str,dstip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[70]原语 alter visit_dest by app:str,dstip:str,dstip_num:in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_src', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,srcip,sum(visit_num) as src_num from api_hx where time >= '$time1' and time < '$time2' group by app,srcip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[71]原语 visit_src = load ckh by ckh with select app,srcip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_src', 'by': 'app:str,srcip:str,src_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[72]原语 alter visit_src by app:str,srcip:str,src_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_account', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,account,sum(visit_num) as account_num from api_hx where time >= '$time1' and time < '$time2' and account != '' and account != '未知' group by app,account"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[73]原语 visit_account = load ckh by ckh with select app,ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_account', 'by': 'app:str,account:str,account_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[74]原语 alter visit_account by app:str,account:str,account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_data', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select a.app,a.api,a.dest_ip,a.dest_port,a.state,b.type1,a.last_time from api19_risk a left join api19_type b on a.type = b.type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[76]原语 app_data = load db by mysql1 with select a.app,a.a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_data', 'by': 'app:str,api:str,dest_ip:str,dest_port:int,state:str,type1:str,last_time:datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[77]原语 alter app_data by app:str,api:str,dest_ip:str,dest... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_data', 'Action': 'order', 'order': 'app_data', 'by': 'last_time', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[78]原语 app_data = order app_data by last_time with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,url,risk_level,first_time,api_type,risk_label,api_status from data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[80]原语 app_api = @udf RS.load_mysql_sql with (mysql1,sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_api', 'by': 'app:str,url:str,risk_level:int,first_time:datetime64,api_type:int,risk_label:str,api_state:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[81]原语 alter app_api by app:str,url:str,risk_level:int,fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select risk_label,risk_name as value from data_api_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[83]原语 sens = load db by mysql1 with select risk_label,ri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'risk_label:str,value:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[84]原语 alter sens by risk_label:str,value:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'risk_label', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[85]原语 sens = loc sens by risk_label to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_24', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,SUBSTRING(toString(time),1,13) as times,sum(visit_num) as count from api_hx where time > '$day1' group by app,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[87]原语 app_24 = load ckh by ckh with select app,SUBSTRING... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_24', 'by': 'app:str,times:str,count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[88]原语 alter app_24 by app:str,times:str,count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'applist', 'with': 'app = $1', 'run': '""\n\n#月访问趋势 192.168.1.201 ----------------------------------------------------------------------------------\nv1 = filter mon_ll by app == \'@app\'\n#v1 = filter mon_ll by app == \'www.gearsandgears.com\'\nv1 = loc v1 by times,time_count,llk\nv1 = loc v1 by times to index\nvs = join v1,time_date by index,index with right\nvs = @udf vs by udf0.df_fillna_cols with time_count:0,llk:0\nvs = loc vs by time_count,llk\nvs = add ss by 1\nss_mean = group vs by ss agg time_count:mean,llk:mean\nvs = loc vs drop ss\ntime_count_mean = eval ss_mean by iloc[0,0]\nif $time_count_mean > 10000 with vs.time_count = lambda time_count by (x:round(x/10000,2))\nif $time_count_mean > 10000 with rename vs by ("time_count":"访问数量(万)")\nif $time_count_mean <= 10000 with rename vs by ("time_count":"访问数量")\nllk_mean = eval ss_mean by iloc[0,1]\nif $llk_mean <= 1024 with rename vs by ("llk":"流量(B)")\nif 1024 < $llk_mean <= 1048576 with vs.llk = lambda llk by (x:round(x/1024,2))\nif 1024 < $llk_mean <= 1048576 with rename vs by ("llk":"流量(k)")\nif $llk_mean >1048576 with vs.llk = lambda llk by (x:round(x/1048576,2))\nif $llk_mean > 1048576 with rename vs by ("llk":"流量(M)")\nstore vs to ssdb with z:@app:timeh\n##近24小时平均访问次数 ----------------------------------------------------------------------------------\napp24 = filter app_24 by app == \'@app\'\n#app24 = filter app_24 by app == \'100.78.76.36\'\napp24 = join j_hour,app24 by times,times with left\napp24 = @udf app24 by udf0.df_fillna_cols with count:0\napp24.times = lambda times by (x:x[11:])\napp24.times = lambda times by (x:x+\'时\')\napp24 = loc app24 by times to index\napp24 = loc app24 by count\nrename app24 as (\'count\':\'每小时访问数量\')\nstore app24 to ssdb by ssdb0 with z:@app:time_24\n##清单IP ----------------------------------------------------------------------------------\nipls = filter visit_dest by app == \'@app\'\nipls_ll = load pq by dt_table/app_visit_dstip1_@app.pq\nipls = union ipls,ipls_ll\nipls = group ipls by app,dstip agg dstip_num:sum\nipls = @udf ipls by udf0.df_reset_index\nrename ipls as (\'dstip_num_sum\':\'dstip_num\')\n##动态表格\nvisit_dstip1 = loc ipls by app,dstip,dstip_num\nvisit_dstip1 = order visit_dstip1 by dstip_num with desc limit 1000\n#保存为pq文件\nstore visit_dstip1 to pq by dt_table/app_visit_dstip1_@app.pq\n## 清单\nipls = loc ipls by dstip,dstip_num\nipls = order ipls by dstip_num with desc limit 10\nrename ipls by ("dstip":"部署服务器IP",\'dstip_num\':\'访问数量\')\nstore ipls to ssdb with z:@app:ipls\n#访问账号清单 ----------------------------------------------------------------------------------\naccountls = filter visit_account by app == \'@app\'\naccountls_ll = load pq by dt_table/app_visit_account1_@app.pq\naccountls = union accountls,accountls_ll\naccountls = group accountls by app,account agg account_num:sum\naccountls = @udf accountls by udf0.df_reset_index\nrename accountls as (\'account_num_sum\':\'account_num\')\n##动态表格\nvisit_account1 = loc accountls by app,account,account_num\nvisit_account1 = order visit_account1 by account_num with desc limit 1000\n#保存为pq文件\nstore visit_account1 to pq by dt_table/app_visit_account1_@app.pq\n#重命名\nrename visit_account1 as ("app":"应用IP/域名","account":"访问账号","account_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,app_visit_account1_@app,-,-\n#保存Q\nstore visit_account1 to ssdb by ssdb0 with app_visit_account1_@app as Q\ndrop visit_account1\n##清单\naccountls = loc accountls by account,account_num\naccountls = order accountls by account_num with desc limit 10\nrename accountls by ("account":"访问账号",\'account_num\':\'访问数量\')\nstore accountls to ssdb with z:@app:accountls\n#终端访问清单 ----------------------------------------------------------------------------------\nsrcipls = filter visit_src by app == \'@app\'\nsrcipls_ll = load pq by dt_table/app_visit_src1_@app.pq\nsrcipls = union srcipls,srcipls_ll\nsrcipls = group srcipls by app,srcip agg src_num:sum\nsrcipls = @udf srcipls by udf0.df_reset_index\nrename srcipls as (\'src_num_sum\':\'src_num\')\n##动态表格\nvisit_src1 = loc srcipls by app,srcip,src_num\nvisit_src1 = order visit_src1 by src_num with desc limit 1000\n#保存为pq文件\nstore visit_src1 to pq by dt_table/app_visit_src1_@app.pq\n#重命名\nrename visit_src1 as ("app":"应用IP/域名","srcip":"终端访问","src_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,app_visit_src1_@app,-,-\n#保存Q\nstore visit_src1 to ssdb by ssdb0 with app_visit_src1_@app as Q\ndrop visit_src1\n##清单\nsrcipls = loc srcipls by srcip,src_num\nsrcipls = order srcipls by src_num with desc limit 10\nrename srcipls by ("srcip":"终端访问",\'src_num\':\'访问数量\')\nstore srcipls to ssdb with z:@app:srcipls\n#接口清单 \'192.168.10.50\' ----------------------------------------------------------------------------------\nurlls = filter visit_url by app == \'@app\'\nurlls_ll = load pq by dt_table/app_visit_url1_@app.pq\nurlls = union urlls,urlls_ll\nurlls = group urlls by app,url agg url_num:sum\nurlls = @udf urlls by udf0.df_reset_index\nrename urlls as (\'url_num_sum\':\'url_num\')\n##动态表格\nvisit_url1 = loc urlls by app,url,url_num\nvisit_url1 = order visit_url1 by url_num with desc limit 1000\n#保存为pq文件\nstore visit_url1 to pq by dt_table/app_visit_url1_@app.pq\n#重命名\nrename visit_url1 as ("app":"应用IP/域名","url":"接口","url_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,app_visit_url1_@app,-,-\n#保存Q\nstore visit_url1 to ssdb by ssdb0 with app_visit_url1_@app as Q\ndrop visit_url1\n##清单\nurlls = loc urlls by url,url_num\nurlls = order urlls by url_num with desc limit 10\nrename urlls by ("url":"接口",\'url_num\':\'访问数量\')\nstore urlls to ssdb with z:@app:urlls\n#原应用 ----------------------------------------------------------------------------------\nt = filter applist by app == \'@app\'\n#t = filter applist by app == \'100.78.76.36\'\nt = loc t by app,app_sum\nt.app_sum = lambda app_sum by (x:x.split(","))\nt = @udf t by udf0.df_l2cs with app_sum\nt = @udf t by udf0.df_reset_index\nt = loc t drop index,app,app_sum\nt = @udf t by udf0.df_T\nrename t as (0:\'原应用\')\nt = filter t by 原应用 != \'\'\nstore t to ssdb with z:@app:origin_app\n###弱点接口 ----------------------------------------------------------------------------------\napp = filter app_data by app == \'@app\'\n#app = filter app_data by app == \'100.78.76.36\'\napp = @udf app by udf0.df_reset_index\napp = loc app by app,api,dest_ip,dest_port,state,type1,last_time\n######################动态表格111111111111111111111111111动态表格111111111111111111111111111动态表格111111111111111111111111111动态表格111111111111111111111111111动态表格111111111111111111111111111\nrisk = loc app by index to _id\nrisk = loc risk by _id,app,api,dest_ip,dest_port,state,type1,last_time\nrisk = order risk by last_time with desc limit 1000\nalter risk.last_time as str\nrisk.last_time = str last_time by [0:19]\nrisk.last_time = str last_time by (replace(\'T\', \' \'))\n##保存为pq文件\nstore risk to pq by dt_table/app_19risk_@app.pq\n##重命名\nrename risk as ("app":"应用","api":"接口","dest_ip":"部署IP","dest_port":"部署端口","method":"请求类型","state":"弱点状态","type1":"弱点类型","last_time":"最新监测时间")\n##清空Q\nb = load ssdb by ssdb0 query qclear,app_19risk_@app,-,-\n#data,count\xa0=load ssdb by ssdb0 query qrange,app_19risk_205.174.165.68,0,30\n##保存Q\nstore risk to ssdb by ssdb0 with app_19risk_@app as Q\n##################动态表格111111111111111111111111111动态表格111111111111111111111111111动态表格111111111111111111111111111动态表格111111111111111111111111111动态表格111111111111111111111111111\napp = loc app by api,dest_ip,dest_port,state,type1,last_time\napp = order app by last_time with desc limit 500\nalter app.last_time as str\napp.last_time = str last_time by [0:19]\napp.last_time = str last_time by (replace(\'T\', \' \'))\napp = @udf app by VL.set_col_width with (360,130,110,110,200,200)\napp = @udf app by VL.set_col_color with (#000,#000,#000,#f00,#000,#000)\nrename app by ("api":"接口","dest_ip":"部署IP","dest_port":"部署端口","method":"请求类型","state":"弱点状态","type1":"弱点类型","last_time":"最新监测时间")\nstore app to ssdb with appriskall:@app\n\n##应用管理-> 画像 -> 风险-> 高风险接口、高、中、低风险 ----------------------------------------------------------------------------------\na = filter app_api by app== "@app"\n#a = filter app_api by app=="www.clipshack.com"\n#低风险数量---------------------------------\nt = filter a by risk_level == \'0\'\nt = group t by risk_level agg risk_level:count\na_num = eval t by index.size\nif $a_num == 0 with t = @udf t by udf0.df_append with (0)\nt = add aa by 1000\nstore t to ssdb with risk:@app:1\n#中风险数量\ns = filter a by risk_level == \'1\'\ns = group s by risk_level agg risk_level:count\na_num = eval s by index.size\nif $a_num == 0 with s = @udf s by udf0.df_append with (0)\ns = add aa by 1000\nstore s to ssdb with risk:@app:2\n#高风险数量\nz = filter a by risk_level == \'2\'\nz = group z by risk_level agg risk_level:count\na_num = eval z by index.size\nif $a_num == 0 with z = @udf z by udf0.df_append with (0)\nz = add aa by 1000\nstore z to ssdb with risk:@app:3\n#风险表格 ----------------------------------------------------------------------------------\na = filter a by risk_level == "2"\na.first_time = str first_time by [0:19]\na.first_time = str first_time by (replace(\'T\',\' \'))\nalter a.api_type as int\nalter a.api_type as str\ntype = load ssdb by ssdb0 with dd:API-api_type\na = @udf a,type by SP.tag2dict with api_type\na.api_status = str api_status by (replace(\'0\',\'未监控\'))\na.api_status = str api_status by (replace(\'1\',\'已监控\'))\na.risk_level = str risk_level by ( replace(\'0\',\'低风险\'))\na.risk_level = str risk_level by ( replace(\'1\',\'中风险\'))\na.risk_level = str risk_level by ( replace(\'2\',\'高风险\'))\na = @udf a,sens by SP.tag2dict with risk_label\n######################动态表格22222222222222222222222222222动态表格22222222222222222222222222222动态表格22222222222222222222222222222动态表格22222222222222222222222222222动态表格22222222222222222222222222222\na = @udf a by udf0.df_reset_index\na = loc a drop index\nrisk_g = loc a by index to _id\nrisk_g = loc risk_g by _id,app,url,risk_level,first_time,api_type,risk_label,api_status\nrisk_g = order risk_g by first_time with desc limit 1000\n##保存为pq文件\nstore risk_g to pq by dt_table/app_g_risk_@app.pq\n##重命名\nrename risk_g as ("app":"应用","url":"风险接口","risk_level":"风险等级","first_time":"首次发现时间","api_type":"接口类型","risk_label":"风险内容","api_status":"监控状态")\n##清空Q\nb = load ssdb by ssdb0 query qclear,app_g_risk_@app,-,-\n##保存Q\nstore risk_g to ssdb by ssdb0 with app_g_risk_@app as Q\n##################动态表格22222222222222222222222222222动态表格22222222222222222222222222222动态表格22222222222222222222222222222动态表格22222222222222222222222222222动态表格22222222222222222222222222222\na = order a by first_time with desc limit 500\na = loc a drop app\na = @udf a by VL.set_col_width with (550,100,200,100,300,100)\na = @udf a by VL.set_col_color with (#f00,#f00,#000,#000,#f00,#000)\nrename a by ("url":"风险接口","risk_level":"风险等级","first_time":"首次发现时间","api_type":"接口类型","risk_label":"风险内容","api_status":"监控状态")\nstore a to ssdb with z:@app:api\n\n""'}
	try:
		ptree['lineno']=90
		ptree['funs']=block_foreach_90
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[90]原语 foreach applist run "#月访问趋势 192.168.1.201  -------... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_app_1.fbi]执行第[324]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],324

#主函数结束,开始块函数

def block_foreach_90(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'v1', 'Action': 'filter', 'filter': 'mon_ll', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[93]原语 v1 = filter mon_ll by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'v1', 'Action': 'loc', 'loc': 'v1', 'by': 'times,time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[95]原语 v1 = loc v1 by times,time_count,llk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'v1', 'Action': 'loc', 'loc': 'v1', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[96]原语 v1 = loc v1 by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'vs', 'Action': 'join', 'join': 'v1,time_date', 'by': 'index,index', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[97]原语 vs = join v1,time_date by index,index with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'vs', 'Action': '@udf', '@udf': 'vs', 'by': 'udf0.df_fillna_cols', 'with': 'time_count:0,llk:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[98]原语 vs = @udf vs by udf0.df_fillna_cols with time_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'vs', 'Action': 'loc', 'loc': 'vs', 'by': 'time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[99]原语 vs = loc vs by time_count,llk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'vs', 'Action': 'add', 'add': 'ss', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[100]原语 vs = add ss by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ss_mean', 'Action': 'group', 'group': 'vs', 'by': 'ss', 'agg': 'time_count:mean,llk:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[101]原语 ss_mean = group vs by ss agg time_count:mean,llk:m... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'vs', 'Action': 'loc', 'loc': 'vs', 'drop': 'ss'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[102]原语 vs = loc vs drop ss 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time_count_mean', 'Action': 'eval', 'eval': 'ss_mean', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[103]原语 time_count_mean = eval ss_mean by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean > 10000', 'with': 'vs.time_count = lambda time_count by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=104
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[104]原语 if $time_count_mean > 10000 with vs.time_count = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean > 10000', 'with': 'rename vs by ("time_count":"访问数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=105
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[105]原语 if $time_count_mean > 10000 with rename vs by ("ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean <= 10000', 'with': 'rename vs by ("time_count":"访问数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=106
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[106]原语 if $time_count_mean <= 10000 with rename vs by ("t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'llk_mean', 'Action': 'eval', 'eval': 'ss_mean', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[107]原语 llk_mean = eval ss_mean by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean <= 1024', 'with': 'rename vs by ("llk":"流量(B)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=108
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[108]原语 if $llk_mean <= 1024 with rename vs by ("llk":"流量(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $llk_mean <= 1048576', 'with': 'vs.llk = lambda llk by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=109
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[109]原语 if 1024 < $llk_mean <= 1048576 with vs.llk = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $llk_mean <= 1048576', 'with': 'rename vs by ("llk":"流量(k)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=110
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[110]原语 if 1024 < $llk_mean <= 1048576 with rename vs by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean >1048576', 'with': 'vs.llk = lambda llk by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=111
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[111]原语 if $llk_mean >1048576 with vs.llk = lambda llk by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean > 1048576', 'with': 'rename vs by ("llk":"流量(M)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=112
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[112]原语 if $llk_mean > 1048576 with rename vs by ("llk":"流... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'vs', 'to': 'ssdb', 'with': 'z:@app:timeh'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[113]原语 store vs to ssdb with z:@app:timeh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app24', 'Action': 'filter', 'filter': 'app_24', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[115]原语 app24 = filter app_24 by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app24', 'Action': 'join', 'join': 'j_hour,app24', 'by': 'times,times', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[117]原语 app24 = join j_hour,app24 by times,times with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app24', 'Action': '@udf', '@udf': 'app24', 'by': 'udf0.df_fillna_cols', 'with': 'count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[118]原语 app24 = @udf app24 by udf0.df_fillna_cols with cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app24.times', 'Action': 'lambda', 'lambda': 'times', 'by': 'x:x[11:]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[119]原语 app24.times = lambda times by (x:x[11:]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app24.times', 'Action': 'lambda', 'lambda': 'times', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[120]原语 app24.times = lambda times by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app24', 'Action': 'loc', 'loc': 'app24', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[121]原语 app24 = loc app24 by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app24', 'Action': 'loc', 'loc': 'app24', 'by': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[122]原语 app24 = loc app24 by count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app24', 'as': "'count':'每小时访问数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[123]原语 rename app24 as ("count":"每小时访问数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app24', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'z:@app:time_24'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[124]原语 store app24 to ssdb by ssdb0 with z:@app:time_24 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ipls', 'Action': 'filter', 'filter': 'visit_dest', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[126]原语 ipls = filter visit_dest by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ipls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_visit_dstip1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[127]原语 ipls_ll = load pq by dt_table/app_visit_dstip1_@ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ipls', 'Action': 'union', 'union': 'ipls,ipls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[128]原语 ipls = union ipls,ipls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ipls', 'Action': 'group', 'group': 'ipls', 'by': 'app,dstip', 'agg': 'dstip_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[129]原语 ipls = group ipls by app,dstip agg dstip_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ipls', 'Action': '@udf', '@udf': 'ipls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[130]原语 ipls = @udf ipls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ipls', 'as': "'dstip_num_sum':'dstip_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[131]原语 rename ipls as ("dstip_num_sum":"dstip_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_dstip1', 'Action': 'loc', 'loc': 'ipls', 'by': 'app,dstip,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[133]原语 visit_dstip1 = loc ipls by app,dstip,dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_dstip1', 'Action': 'order', 'order': 'visit_dstip1', 'by': 'dstip_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[134]原语 visit_dstip1 = order visit_dstip1 by dstip_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_dstip1', 'to': 'pq', 'by': 'dt_table/app_visit_dstip1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[136]原语 store visit_dstip1 to pq by dt_table/app_visit_dst... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ipls', 'Action': 'loc', 'loc': 'ipls', 'by': 'dstip,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[138]原语 ipls = loc ipls by dstip,dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ipls', 'Action': 'order', 'order': 'ipls', 'by': 'dstip_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[139]原语 ipls = order ipls by dstip_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ipls', 'by': '"dstip":"部署服务器IP",\'dstip_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[140]原语 rename ipls by ("dstip":"部署服务器IP","dstip_num":"访问数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ipls', 'to': 'ssdb', 'with': 'z:@app:ipls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[141]原语 store ipls to ssdb with z:@app:ipls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'accountls', 'Action': 'filter', 'filter': 'visit_account', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[143]原语 accountls = filter visit_account by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'accountls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_visit_account1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[144]原语 accountls_ll = load pq by dt_table/app_visit_accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'accountls', 'Action': 'union', 'union': 'accountls,accountls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[145]原语 accountls = union accountls,accountls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'accountls', 'Action': 'group', 'group': 'accountls', 'by': 'app,account', 'agg': 'account_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[146]原语 accountls = group accountls by app,account agg acc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'accountls', 'Action': '@udf', '@udf': 'accountls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[147]原语 accountls = @udf accountls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'accountls', 'as': "'account_num_sum':'account_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[148]原语 rename accountls as ("account_num_sum":"account_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_account1', 'Action': 'loc', 'loc': 'accountls', 'by': 'app,account,account_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[150]原语 visit_account1 = loc accountls by app,account,acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_account1', 'Action': 'order', 'order': 'visit_account1', 'by': 'account_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[151]原语 visit_account1 = order visit_account1 by account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_account1', 'to': 'pq', 'by': 'dt_table/app_visit_account1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[153]原语 store visit_account1 to pq by dt_table/app_visit_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_account1', 'as': '"app":"应用IP/域名","account":"访问账号","account_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[155]原语 rename visit_account1 as ("app":"应用IP/域名","account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,app_visit_account1_@app,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[157]原语 b = load ssdb by ssdb0 query qclear,app_visit_acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_account1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_visit_account1_@app', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[159]原语 store visit_account1 to ssdb by ssdb0 with app_vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_account1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[160]原语 drop visit_account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'accountls', 'Action': 'loc', 'loc': 'accountls', 'by': 'account,account_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[162]原语 accountls = loc accountls by account,account_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'accountls', 'Action': 'order', 'order': 'accountls', 'by': 'account_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[163]原语 accountls = order accountls by account_num with de... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'accountls', 'by': '"account":"访问账号",\'account_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[164]原语 rename accountls by ("account":"访问账号","account_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'accountls', 'to': 'ssdb', 'with': 'z:@app:accountls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[165]原语 store accountls to ssdb with z:@app:accountls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'srcipls', 'Action': 'filter', 'filter': 'visit_src', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[167]原语 srcipls = filter visit_src by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcipls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_visit_src1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[168]原语 srcipls_ll = load pq by dt_table/app_visit_src1_@a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'srcipls', 'Action': 'union', 'union': 'srcipls,srcipls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[169]原语 srcipls = union srcipls,srcipls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'srcipls', 'Action': 'group', 'group': 'srcipls', 'by': 'app,srcip', 'agg': 'src_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[170]原语 srcipls = group srcipls by app,srcip agg src_num:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcipls', 'Action': '@udf', '@udf': 'srcipls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[171]原语 srcipls = @udf srcipls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'srcipls', 'as': "'src_num_sum':'src_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[172]原语 rename srcipls as ("src_num_sum":"src_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_src1', 'Action': 'loc', 'loc': 'srcipls', 'by': 'app,srcip,src_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[174]原语 visit_src1 = loc srcipls by app,srcip,src_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_src1', 'Action': 'order', 'order': 'visit_src1', 'by': 'src_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[175]原语 visit_src1 = order visit_src1 by src_num with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_src1', 'to': 'pq', 'by': 'dt_table/app_visit_src1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[177]原语 store visit_src1 to pq by dt_table/app_visit_src1_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_src1', 'as': '"app":"应用IP/域名","srcip":"终端访问","src_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[179]原语 rename visit_src1 as ("app":"应用IP/域名","srcip":"终端访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,app_visit_src1_@app,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[181]原语 b = load ssdb by ssdb0 query qclear,app_visit_src1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_src1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_visit_src1_@app', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[183]原语 store visit_src1 to ssdb by ssdb0 with app_visit_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_src1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[184]原语 drop visit_src1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcipls', 'Action': 'loc', 'loc': 'srcipls', 'by': 'srcip,src_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[186]原语 srcipls = loc srcipls by srcip,src_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'srcipls', 'Action': 'order', 'order': 'srcipls', 'by': 'src_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[187]原语 srcipls = order srcipls by src_num with desc limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'srcipls', 'by': '"srcip":"终端访问",\'src_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[188]原语 rename srcipls by ("srcip":"终端访问","src_num":"访问数量"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'srcipls', 'to': 'ssdb', 'with': 'z:@app:srcipls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[189]原语 store srcipls to ssdb with z:@app:srcipls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'urlls', 'Action': 'filter', 'filter': 'visit_url', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[191]原语 urlls = filter visit_url by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'urlls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/app_visit_url1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[192]原语 urlls_ll = load pq by dt_table/app_visit_url1_@app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'urlls', 'Action': 'union', 'union': 'urlls,urlls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[193]原语 urlls = union urlls,urlls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'urlls', 'Action': 'group', 'group': 'urlls', 'by': 'app,url', 'agg': 'url_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[194]原语 urlls = group urlls by app,url agg url_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'urlls', 'Action': '@udf', '@udf': 'urlls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[195]原语 urlls = @udf urlls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'urlls', 'as': "'url_num_sum':'url_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[196]原语 rename urlls as ("url_num_sum":"url_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_url1', 'Action': 'loc', 'loc': 'urlls', 'by': 'app,url,url_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[198]原语 visit_url1 = loc urlls by app,url,url_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_url1', 'Action': 'order', 'order': 'visit_url1', 'by': 'url_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[199]原语 visit_url1 = order visit_url1 by url_num with desc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_url1', 'to': 'pq', 'by': 'dt_table/app_visit_url1_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[201]原语 store visit_url1 to pq by dt_table/app_visit_url1_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_url1', 'as': '"app":"应用IP/域名","url":"接口","url_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[203]原语 rename visit_url1 as ("app":"应用IP/域名","url":"接口","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,app_visit_url1_@app,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[205]原语 b = load ssdb by ssdb0 query qclear,app_visit_url1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_url1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_visit_url1_@app', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[207]原语 store visit_url1 to ssdb by ssdb0 with app_visit_u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_url1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[208]原语 drop visit_url1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'urlls', 'Action': 'loc', 'loc': 'urlls', 'by': 'url,url_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[210]原语 urlls = loc urlls by url,url_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'urlls', 'Action': 'order', 'order': 'urlls', 'by': 'url_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[211]原语 urlls = order urlls by url_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'urlls', 'by': '"url":"接口",\'url_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[212]原语 rename urlls by ("url":"接口","url_num":"访问数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'urlls', 'to': 'ssdb', 'with': 'z:@app:urlls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[213]原语 store urlls to ssdb with z:@app:urlls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 't', 'Action': 'filter', 'filter': 'applist', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[215]原语 t = filter applist by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't', 'Action': 'loc', 'loc': 't', 'by': 'app,app_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[217]原语 t = loc t by app,app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 't.app_sum', 'Action': 'lambda', 'lambda': 'app_sum', 'by': 'x:x.split(",")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[218]原语 t.app_sum = lambda app_sum by (x:x.split(",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'udf0.df_l2cs', 'with': 'app_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[219]原语 t = @udf t by udf0.df_l2cs with app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[220]原语 t = @udf t by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't', 'Action': 'loc', 'loc': 't', 'drop': 'index,app,app_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[221]原语 t = loc t drop index,app,app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[222]原语 t = @udf t by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 't', 'as': "0:'原应用'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[223]原语 rename t as (0:"原应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 't', 'Action': 'filter', 'filter': 't', 'by': "原应用 != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[224]原语 t = filter t by 原应用 != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 't', 'to': 'ssdb', 'with': 'z:@app:origin_app'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[225]原语 store t to ssdb with z:@app:origin_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app', 'Action': 'filter', 'filter': 'app_data', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[227]原语 app = filter app_data by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[229]原语 app = @udf app by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'app,api,dest_ip,dest_port,state,type1,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[230]原语 app = loc app by app,api,dest_ip,dest_port,state,t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'app', 'by': 'index', 'to': '_id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[232]原语 risk = loc app by index to _id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': '_id,app,api,dest_ip,dest_port,state,type1,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[233]原语 risk = loc risk by _id,app,api,dest_ip,dest_port,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'risk', 'Action': 'order', 'order': 'risk', 'by': 'last_time', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[234]原语 risk = order risk by last_time with desc limit 100... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'risk.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[235]原语 alter risk.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'risk.last_time', 'Action': 'str', 'str': 'last_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[236]原语 risk.last_time = str last_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'risk.last_time', 'Action': 'str', 'str': 'last_time', 'by': "replace('T', ' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[237]原语 risk.last_time = str last_time by (replace("T", " ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'pq', 'by': 'dt_table/app_19risk_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[239]原语 store risk to pq by dt_table/app_19risk_@app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk', 'as': '"app":"应用","api":"接口","dest_ip":"部署IP","dest_port":"部署端口","method":"请求类型","state":"弱点状态","type1":"弱点类型","last_time":"最新监测时间"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[241]原语 rename risk as ("app":"应用","api":"接口","dest_ip":"部... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,app_19risk_@app,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[243]原语 b = load ssdb by ssdb0 query qclear,app_19risk_@ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_19risk_@app', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[246]原语 store risk to ssdb by ssdb0 with app_19risk_@app a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'api,dest_ip,dest_port,state,type1,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[248]原语 app = loc app by api,dest_ip,dest_port,state,type1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app', 'Action': 'order', 'order': 'app', 'by': 'last_time', 'with': 'desc limit 500'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[249]原语 app = order app by last_time with desc limit 500 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[250]原语 alter app.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'app.last_time', 'Action': 'str', 'str': 'last_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[251]原语 app.last_time = str last_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'app.last_time', 'Action': 'str', 'str': 'last_time', 'by': "replace('T', ' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[252]原语 app.last_time = str last_time by (replace("T", " "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'VL.set_col_width', 'with': '360,130,110,110,200,200'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[253]原语 app = @udf app by VL.set_col_width with (360,130,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'VL.set_col_color', 'with': '#000,#000,#000,#f00,#000,#000'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[254]原语 app = @udf app by VL.set_col_color with (#000,#000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app', 'by': '"api":"接口","dest_ip":"部署IP","dest_port":"部署端口","method":"请求类型","state":"弱点状态","type1":"弱点类型","last_time":"最新监测时间"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[255]原语 rename app by ("api":"接口","dest_ip":"部署IP","dest_p... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'with': 'appriskall:@app'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[256]原语 store app to ssdb with appriskall:@app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a', 'Action': 'filter', 'filter': 'app_api', 'by': 'app== "@app"'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[259]原语 a = filter app_api by app== "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 't', 'Action': 'filter', 'filter': 'a', 'by': "risk_level == '0'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[262]原语 t = filter a by risk_level == "0" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 't', 'Action': 'group', 'group': 't', 'by': 'risk_level', 'agg': 'risk_level:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[263]原语 t = group t by risk_level agg risk_level:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 't', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[264]原语 a_num = eval t by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 't = @udf t by udf0.df_append with (0)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=265
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[265]原语 if $a_num == 0 with t = @udf t by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'aa', 'by': '1000'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[266]原语 t = add aa by 1000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 't', 'to': 'ssdb', 'with': 'risk:@app:1'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[267]原语 store t to ssdb with risk:@app:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 's', 'Action': 'filter', 'filter': 'a', 'by': "risk_level == '1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[269]原语 s = filter a by risk_level == "1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 's', 'Action': 'group', 'group': 's', 'by': 'risk_level', 'agg': 'risk_level:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[270]原语 s = group s by risk_level agg risk_level:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 's', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[271]原语 a_num = eval s by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 's = @udf s by udf0.df_append with (0)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=272
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[272]原语 if $a_num == 0 with s = @udf s by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'aa', 'by': '1000'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[273]原语 s = add aa by 1000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'risk:@app:2'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[274]原语 store s to ssdb with risk:@app:2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'z', 'Action': 'filter', 'filter': 'a', 'by': "risk_level == '2'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[276]原语 z = filter a by risk_level == "2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'z', 'Action': 'group', 'group': 'z', 'by': 'risk_level', 'agg': 'risk_level:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[277]原语 z = group z by risk_level agg risk_level:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'z', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[278]原语 a_num = eval z by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'z = @udf z by udf0.df_append with (0)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=279
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[279]原语 if $a_num == 0 with z = @udf z by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'z', 'Action': 'add', 'add': 'aa', 'by': '1000'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[280]原语 z = add aa by 1000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'z', 'to': 'ssdb', 'with': 'risk:@app:3'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[281]原语 store z to ssdb with risk:@app:3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a', 'Action': 'filter', 'filter': 'a', 'by': 'risk_level == "2"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[283]原语 a = filter a by risk_level == "2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.first_time', 'Action': 'str', 'str': 'first_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[284]原语 a.first_time = str first_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.first_time', 'Action': 'str', 'str': 'first_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[285]原语 a.first_time = str first_time by (replace("T"," ")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.api_type', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[286]原语 alter a.api_type as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.api_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[287]原语 alter a.api_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[288]原语 type = load ssdb by ssdb0 with dd:API-api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a,type', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[289]原语 a = @udf a,type by SP.tag2dict with api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.api_status', 'Action': 'str', 'str': 'api_status', 'by': "replace('0','未监控')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[290]原语 a.api_status = str api_status by (replace("0","未监控... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.api_status', 'Action': 'str', 'str': 'api_status', 'by': "replace('1','已监控')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[291]原语 a.api_status = str api_status by (replace("1","已监控... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': " replace('0','低风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[292]原语 a.risk_level = str risk_level by ( replace("0","低风... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': " replace('1','中风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[293]原语 a.risk_level = str risk_level by ( replace("1","中风... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': " replace('2','高风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[294]原语 a.risk_level = str risk_level by ( replace("2","高风... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a,sens', 'by': 'SP.tag2dict', 'with': 'risk_label'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[295]原语 a = @udf a,sens by SP.tag2dict with risk_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[297]原语 a = @udf a by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[298]原语 a = loc a drop index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk_g', 'Action': 'loc', 'loc': 'a', 'by': 'index', 'to': '_id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[299]原语 risk_g = loc a by index to _id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk_g', 'Action': 'loc', 'loc': 'risk_g', 'by': '_id,app,url,risk_level,first_time,api_type,risk_label,api_status'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[300]原语 risk_g = loc risk_g by _id,app,url,risk_level,firs... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'risk_g', 'Action': 'order', 'order': 'risk_g', 'by': 'first_time', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[301]原语 risk_g = order risk_g by first_time with desc limi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk_g', 'to': 'pq', 'by': 'dt_table/app_g_risk_@app.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[303]原语 store risk_g to pq by dt_table/app_g_risk_@app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk_g', 'as': '"app":"应用","url":"风险接口","risk_level":"风险等级","first_time":"首次发现时间","api_type":"接口类型","risk_label":"风险内容","api_status":"监控状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[305]原语 rename risk_g as ("app":"应用","url":"风险接口","risk_le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,app_g_risk_@app,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[307]原语 b = load ssdb by ssdb0 query qclear,app_g_risk_@ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk_g', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_g_risk_@app', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[309]原语 store risk_g to ssdb by ssdb0 with app_g_risk_@app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'a', 'Action': 'order', 'order': 'a', 'by': 'first_time', 'with': 'desc limit 500'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[311]原语 a = order a by first_time with desc limit 500 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'drop': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[312]原语 a = loc a drop app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'VL.set_col_width', 'with': '550,100,200,100,300,100'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[313]原语 a = @udf a by VL.set_col_width with (550,100,200,1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'VL.set_col_color', 'with': '#f00,#f00,#000,#000,#f00,#000'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[314]原语 a = @udf a by VL.set_col_color with (#f00,#f00,#00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'a', 'by': '"url":"风险接口","risk_level":"风险等级","first_time":"首次发现时间","api_type":"接口类型","risk_label":"风险内容","api_status":"监控状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[315]原语 rename a by ("url":"风险接口","risk_level":"风险等级","fir... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'with': 'z:@app:api'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[316]原语 store a to ssdb with z:@app:api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_90

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



