#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_api_1
#datetime: 2024-08-30T16:10:53.408141
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
		add_the_error('[qh_api_1.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_hx limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[19]原语 ccc = load ckh by ckh with select app from api_hx ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接 或者 无数据更新！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[qh_api_1.fbi]执行第[20]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[20]原语 assert find_df_have_data("ccc",ptree) as exit with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'api_hx1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[23]原语 aa = load ssdb by ssdb0 with api_hx1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[25]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_hx'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=26
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[26]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[28]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_hx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[30]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[31]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_hx1'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[32]原语 store aa to ssdb by ssdb0 with api_hx1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[35]原语 month1 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[qh_api_1.fbi]执行第[36]原语 month = @sdf format_now with ($month1,"%Y-%m-%dT00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[qh_api_1.fbi]执行第[37]原语 month1 = @sdf format_now with ($month1,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'month2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[38]原语 month2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[qh_api_1.fbi]执行第[39]原语 month2 = @sdf format_now with ($month2,"%Y-%m-%d")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'time_date', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$month1,$month2,1D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[40]原语 time_date = @udf udf0.new_df_timerange with ($mont... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_date', 'Action': 'loc', 'loc': 'time_date', 'by': 'end_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[41]原语 time_date = loc time_date by end_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'time_date.end_time', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[42]原语 time_date.end_time = lambda end_time by (x:x[5:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'time_date', 'Action': 'loc', 'loc': 'time_date', 'by': 'end_time', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[43]原语 time_date = loc time_date by end_time to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[46]原语 day = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[47]原语 day2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[qh_api_1.fbi]执行第[48]原语 day1 = @sdf format_now with ($day,"%Y-%m-%d %H:00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[qh_api_1.fbi]执行第[49]原语 day2 = @sdf format_now with ($day2,"%Y-%m-%d %H:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$day1,$day2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[50]原语 j_hour = @udf udf0.new_df_timerange with ($day1,$d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.times', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[0:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[51]原语 j_hour.times = lambda end_time by (x:x[0:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'times'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[52]原语 j_hour = loc j_hour by times 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apilist1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url,risk_level,risk_label_value,auto_merge from data_api_new where merge_state != 1 and portrait_status = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[56]原语 apilist1 = load db by mysql1 with select id,url,ri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'apilist1', 'Action': '@udf', '@udf': 'apilist1', 'by': 'udf0.df_fillna_cols', 'with': "risk_level:0,risk_label_value:'',auto_merge:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[57]原语 apilist1 = @udf apilist1 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'apilist1', 'by': 'url:str,risk_level:int,risk_label_value:str,auto_merge:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[58]原语 alter apilist1 by url:str,risk_level:int,risk_labe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'apilist1', 'Action': 'loc', 'loc': 'apilist1', 'by': 'id,url,risk_level,risk_label_value,auto_merge'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[59]原语 apilist1 = loc apilist1 by id,url,risk_level,risk_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mon_ll', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,SUBSTRING(toString(time),6,5) as times,sum(visit_num) as time_count,sum(visit_flow) as llk from api_hx where time > '$month' group by url,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[62]原语 mon_ll = load ckh by ckh with select url,SUBSTRING... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'mon_ll', 'by': 'url:str,times:str,time_count:int,llk:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[63]原语 alter mon_ll by url:str,times:str,time_count:int,l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mon_ll.llk', 'Action': 'lambda', 'lambda': 'llk', 'by': 'x:round(x/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[64]原语 mon_ll.llk = lambda llk by (x:round(x/1024,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'mon_ll', 'Action': 'order', 'order': 'mon_ll', 'by': 'times', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[65]原语 mon_ll = order mon_ll by times with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_url', 'Action': 'loc', 'loc': 'apilist1', 'by': 'url,auto_merge'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[67]原语 visit_url = loc apilist1 by url,auto_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'visit_url', 'Action': '@udf', '@udf': 'visit_url', 'by': 'udf0.df_fillna_cols', 'with': "auto_merge:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[68]原语 visit_url = @udf visit_url by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'aa', 'Action': 'filter', 'filter': 'visit_url', 'by': "auto_merge != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[69]原语 aa = filter visit_url by auto_merge != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_dstip', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,dstip,sum(visit_num) as dstip_num from api_hx where time >= '$time1' and time < '$time2' group by url,dstip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[70]原语 visit_dstip = load ckh by ckh with select url,dsti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_dstip', 'by': 'url:str,dstip:str,dstip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[71]原语 alter visit_dstip by url:str,dstip:str,dstip_num:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_srcip', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,srcip,sum(visit_num) as srcip_num from api_hx where time >= '$time1' and time < '$time2' group by url,srcip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[72]原语 visit_srcip = load ckh by ckh with select url,srci... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_srcip', 'by': 'url:str,srcip:str,srcip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[73]原语 alter visit_srcip by url:str,srcip:str,srcip_num:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit_account', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,account,sum(visit_num) as account_num from api_hx where time >= '$time1' and time < '$time2'and account != '' and account != '未知' group by url,account"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[74]原语 visit_account = load ckh by ckh with select url,ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit_account', 'by': 'url:str,account:str,account_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[75]原语 alter visit_account by url:str,account:str,account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts_apilist1', 'Action': 'loc', 'loc': 'apilist1', 'by': 'id,url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[77]原语 zts_apilist1 = loc apilist1 by id,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive_data', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[79]原语 sensitive_data = load pq by sensitive/sens_data.pq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive_data', 'by': 'app:str,url:str,src_ip:str,account:str,key:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[80]原语 alter sensitive_data by app:str,url:str,src_ip:str... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sensitive_data', 'Action': 'join', 'join': 'zts_apilist1,sensitive_data', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[81]原语 sensitive_data = join zts_apilist1,sensitive_data ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sensitive_data', 'Action': '@udf', '@udf': 'sensitive_data', 'by': 'udf0.df_fillna_cols', 'with': "app:'',src_ip:'',account:'',type:'',key:'',num:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[82]原语 sensitive_data = @udf sensitive_data by udf0.df_fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_24', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url,SUBSTRING(toString(time),1,13) as times,sum(visit_num) as count from api_hx where time > '$day1' group by url,times"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[84]原语 api_24 = load ckh by ckh with select url,SUBSTRING... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_24', 'by': 'url:str,times:str,count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[85]原语 alter api_24 by url:str,times:str,count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'apilist1', 'with': 'url=$2,id=$1', 'run': '""\n\n###24小时平均访问次数 -----------------------------------------------------------------------------\napi24 = filter api_24 by (url == """@url""")\n#api24 = filter api_24 by (url == \'http://www.mattheaton.com/\')\napi24 = join j_hour,api24 by times,times with left\napi24 = @udf api24 by udf0.df_fillna_cols with times:\'\',count:0\napi24.times = lambda times by (x:x[11:])\napi24.times = lambda times by (x:x+\'时\')\napi24 = loc api24 by times to index\napi24 = loc api24 by count\nrename api24 as (\'count\':\'每小时访问数量\')\nstore api24 to ssdb by ssdb0 with z:@id:time_24\n#########API风险---- -----------------------------------------------------------------------------\nt = filter apilist1 by (url == """@url""")\n#t = filter apilist1 by url == "http://www.ujiaoshou.com/xtjc/{dst}"\ni = loc t by (risk_level,risk_label_value)\ni.risk_level = str risk_level by ( replace(\'0\',\'低风险\'))\ni.risk_level = str risk_level by ( replace(\'1\',\'中风险\'))\ni.risk_level = str risk_level by ( replace(\'2\',\'高风险\'))\ni = @udf i by VL.set_col_width with (100,350)\ni = @udf i by VL.set_col_color with (#f00,#f00)\nrename i as ("risk_level":"风险等级","risk_label_value":"风险内容")\nstore i to ssdb with z:@id:risklll\ndrop i\n#月访问数量和流量 http://192.168.1.196:9999/run_blockp -----------------------------------------------------------------------------\nv1 = filter mon_ll by (url == """@url""")\nv1 = filter mon_ll by (url == \'http://www.mattheaton.com/\')\nv1 = loc v1 by times,time_count,llk\nv1 = loc v1 by times to index\nss = join v1,time_date by index,index with right\nss = loc ss by (time_count,llk)\nss = @udf ss by udf0.df_fillna_cols with time_count:0,llk:0\nss_mean = loc ss by time_count,llk\nss_mean = add ss by 1\nss_mean = group ss_mean by ss agg time_count:mean,llk:mean\ntime_count_mean = eval ss_mean by iloc[0,0]\nif $time_count_mean > 10000 with ss.time_count = lambda time_count by (x:round(x/10000,2))\nif $time_count_mean > 10000 with rename ss by ("time_count":"访问数量(万)")\nif $time_count_mean <= 10000 with rename ss by ("time_count":"访问数量")\nllk_mean = eval ss_mean by iloc[0,1]\nif $llk_mean > 1024 with ss.llk = lambda llk by (x:round(x/1024,2))\nif $llk_mean > 1024 with rename ss by ("llk":"流量(M)")\nif $llk_mean <= 1024 with rename ss by ("llk":"流量(k)")\nstore ss to ssdb with z:@id:timeh\n#IP清单 -----------------------------------------------------------------------------\nipls = filter visit_dstip by (url == """@url""")\nipls_ll = load pq by dt_table/api_visit_dstip1_@id.pq\nipls = union ipls,ipls_ll\nipls = group ipls by url,dstip agg dstip_num:sum\nipls = @udf ipls by udf0.df_reset_index\nrename ipls as (\'dstip_num_sum\':\'dstip_num\')\n## 动态表格\nvisit_dstip1 = loc ipls by url,dstip,dstip_num\nvisit_dstip1 = order visit_dstip1 by dstip_num with desc limit 1000\n#保存为pq文件\nstore visit_dstip1 to pq by dt_table/api_visit_dstip1_@id.pq\n##清单\nipls = loc ipls by dstip,dstip_num\nipls = order ipls by dstip_num with desc limit 10\nrename ipls by ("dstip":"部署服务器IP",\'dstip_num\':\'访问数量\')\nstore ipls to ssdb with z:@id:ipls\n#访问账号清单 -----------------------------------------------------------------------------\naccountls = filter visit_account by (url == """@url""")\naccountls_ll = load pq by dt_table/api_visit_account1_@id.pq\naccountls = union accountls,accountls_ll\naccountls = group accountls by url,account agg account_num:sum\naccountls = @udf accountls by udf0.df_reset_index\nrename accountls as (\'account_num_sum\':\'account_num\')\n##动态表格\nvisit_account1 = loc accountls by url,account,account_num\nvisit_account1 = order visit_account1 by account_num with desc limit 1000\n#保存为pq文件\nstore visit_account1 to pq by dt_table/api_visit_account1_@id.pq\n#重命名\nrename visit_account1 as ("url":"接口","account":"账号","account_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,api_visit_account1_@id,-,-\n#保存Q\nstore visit_account1 to ssdb by ssdb0 with api_visit_account1_@id as Q\ndrop visit_account1\n##清单\naccountls = loc accountls by account,account_num\naccountls = order accountls by account_num with desc limit 10\nrename accountls by ("account":"访问账号",\'account_num\':\'访问数量\')\nstore accountls to ssdb with z:@id:accountls\n#访问终端清单 -----------------------------------------------------------------------------\nsrcipls = filter visit_srcip by (url == """@url""")\nsrcipls_ll = load pq by dt_table/api_visit_srcip1_@id.pq\nsrcipls = union srcipls,srcipls_ll\nsrcipls = group srcipls by url,srcip agg srcip_num:sum\nsrcipls = @udf srcipls by udf0.df_reset_index\nrename srcipls as (\'srcip_num_sum\':\'srcip_num\')\n##动态表格\nvisit_srcip1 = loc srcipls by url,srcip,srcip_num\nvisit_srcip1 = order visit_srcip1 by srcip_num with desc limit 1000\n#保存为pq文件\nstore visit_srcip1 to pq by dt_table/api_visit_srcip1_@id.pq\n#重命名\nrename visit_srcip1 as ("url":"接口","srcip":"访问终端","srcip_num":"访问数量")\n#清空Q\nb = load ssdb by ssdb0 query qclear,api_visit_srcip1_@id,-,-\n#保存Q\nstore visit_srcip1 to ssdb by ssdb0 with api_visit_srcip1_@id as Q\ndrop visit_srcip1\n## 清单\nsrcipls = loc srcipls by srcip,srcip_num\nsrcipls = order srcipls by srcip_num with desc limit 10\nrename srcipls by ("srcip":"访问终端",\'srcip_num\':\'访问数量\')\nstore srcipls to ssdb with z:@id:srcipls\n#原接口 -----------------------------------------------------------------------------\nurl_a = filter visit_url by (url == """@url""")\n#url_a = filter visit_url by (url == """http://100.78.26.82/ebus/00000000000_nw_dzfpfwpt/SJCS_FPJF_ZJ_MRJK""")\nurl_a.auto_merge = lambda auto_merge by (x:x[1:-1])\nurl_a.auto_merge = lambda auto_merge by (x:x.split(", "))\nurl_a = @udf url_a by udf0.df_l2cs with auto_merge\nurl_a = @udf url_a by udf0.df_reset_index\nurl_a = loc url_a by drop url,index,auto_merge\nurl_a = @udf url_a by udf0.df_T\nrename url_a as (0:\'url\')\nurl_a.url = lambda url by (x:x[1:-1])\nrename url_a by ("url":"原接口")\nurl_a = filter url_a by 原接口 != \'\'\nstore url_a to ssdb with z:@id:url_a\n##敏感信息 -----------------------------------------------------------------------------\nzts = filter sensitive_data by (url == """@url""")\n#zts = filter sensitive_data by (url == """http://100.78.76.36/ebus/00000000000_nw_dzfpfwpt/yp/{p1}/v1/{p2}""")\nzts = filter zts by app != \'\'\nzts1 = loc zts by app,src_ip,account,type,key\nzts1 = order zts1 by key with desc limit 500\nzts1 = filter zts1 by key != \'\'\nrename zts1 by (\'key\':\'敏感类型\',\'type\':\'标签\',\'app\':\'应用\',\'src_ip\':\'终端\',\'account\':\'账号\')\nstore zts1 to ssdb by ssdb0 with zts:@id:sens\n######################敏感信息1111111111111111111111111111敏感信息1111111111111111111111111111敏感信息1111111111111111111111111111敏感信息1111111111111111111111111111\nzts2 = loc zts by id,url,app,src_ip,account,type,key\nrename zts2 as (\'id\':\'_id\')\nzts2 = filter zts2 by key != \'\'\nzts2 = order zts2 by _id with desc limit 1000\n##保存为pq文件\nstore zts2 to pq by dt_table/api_zts_@id.pq\n##重命名\nrename zts2 as (\'url\':\'接口\',\'key\':\'敏感类型\',\'type\':\'标签\',\'app\':\'应用\',\'src_ip\':\'终端\',\'account\':\'账号\')\n##清空Q\nb = load ssdb by ssdb0 query qclear,api_zts_@id,-,-\n##保存Q\nstore zts2 to ssdb by ssdb0 with api_zts_@id as Q\ndrop zts2\n######################敏感信息1111111111111111111111111111敏感信息1111111111111111111111111111敏感信息1111111111111111111111111111敏感信息1111111111111111111111111111\n""'}
	try:
		ptree['lineno']=89
		ptree['funs']=block_foreach_89
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[89]原语 foreach apilist1 run "###24小时平均访问次数   ------------... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_api_1.fbi]执行第[240]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],240

#主函数结束,开始块函数

def block_foreach_89(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api24', 'Action': 'filter', 'filter': 'api_24', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[92]原语 api24 = filter api_24 by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api24', 'Action': 'join', 'join': 'j_hour,api24', 'by': 'times,times', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[94]原语 api24 = join j_hour,api24 by times,times with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api24', 'Action': '@udf', '@udf': 'api24', 'by': 'udf0.df_fillna_cols', 'with': "times:'',count:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[95]原语 api24 = @udf api24 by udf0.df_fillna_cols with tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api24.times', 'Action': 'lambda', 'lambda': 'times', 'by': 'x:x[11:]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[96]原语 api24.times = lambda times by (x:x[11:]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api24.times', 'Action': 'lambda', 'lambda': 'times', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[97]原语 api24.times = lambda times by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api24', 'Action': 'loc', 'loc': 'api24', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[98]原语 api24 = loc api24 by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api24', 'Action': 'loc', 'loc': 'api24', 'by': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[99]原语 api24 = loc api24 by count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api24', 'as': "'count':'每小时访问数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[100]原语 rename api24 as ("count":"每小时访问数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api24', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'z:@id:time_24'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[101]原语 store api24 to ssdb by ssdb0 with z:@id:time_24 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 't', 'Action': 'filter', 'filter': 'apilist1', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[103]原语 t = filter apilist1 by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'i', 'Action': 'loc', 'loc': 't', 'by': 'risk_level,risk_label_value'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[105]原语 i = loc t by (risk_level,risk_label_value) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'i.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': " replace('0','低风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[106]原语 i.risk_level = str risk_level by ( replace("0","低风... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'i.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': " replace('1','中风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[107]原语 i.risk_level = str risk_level by ( replace("1","中风... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'i.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': " replace('2','高风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[108]原语 i.risk_level = str risk_level by ( replace("2","高风... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'i', 'Action': '@udf', '@udf': 'i', 'by': 'VL.set_col_width', 'with': '100,350'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[109]原语 i = @udf i by VL.set_col_width with (100,350) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'i', 'Action': '@udf', '@udf': 'i', 'by': 'VL.set_col_color', 'with': '#f00,#f00'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[110]原语 i = @udf i by VL.set_col_color with (#f00,#f00) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'i', 'as': '"risk_level":"风险等级","risk_label_value":"风险内容"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[111]原语 rename i as ("risk_level":"风险等级","risk_label_value... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'i', 'to': 'ssdb', 'with': 'z:@id:risklll'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[112]原语 store i to ssdb with z:@id:risklll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'i'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[113]原语 drop i 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'v1', 'Action': 'filter', 'filter': 'mon_ll', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[115]原语 v1 = filter mon_ll by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'v1', 'Action': 'filter', 'filter': 'mon_ll', 'by': "url == 'http://www.mattheaton.com/'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[116]原语 v1 = filter mon_ll by (url == "http://www.mattheat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'v1', 'Action': 'loc', 'loc': 'v1', 'by': 'times,time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[117]原语 v1 = loc v1 by times,time_count,llk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'v1', 'Action': 'loc', 'loc': 'v1', 'by': 'times', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[118]原语 v1 = loc v1 by times to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ss', 'Action': 'join', 'join': 'v1,time_date', 'by': 'index,index', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[119]原语 ss = join v1,time_date by index,index with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss', 'Action': 'loc', 'loc': 'ss', 'by': 'time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[120]原语 ss = loc ss by (time_count,llk) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_fillna_cols', 'with': 'time_count:0,llk:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[121]原语 ss = @udf ss by udf0.df_fillna_cols with time_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss_mean', 'Action': 'loc', 'loc': 'ss', 'by': 'time_count,llk'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[122]原语 ss_mean = loc ss by time_count,llk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss_mean', 'Action': 'add', 'add': 'ss', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[123]原语 ss_mean = add ss by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ss_mean', 'Action': 'group', 'group': 'ss_mean', 'by': 'ss', 'agg': 'time_count:mean,llk:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[124]原语 ss_mean = group ss_mean by ss agg time_count:mean,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time_count_mean', 'Action': 'eval', 'eval': 'ss_mean', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[125]原语 time_count_mean = eval ss_mean by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean > 10000', 'with': 'ss.time_count = lambda time_count by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=126
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[126]原语 if $time_count_mean > 10000 with ss.time_count = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean > 10000', 'with': 'rename ss by ("time_count":"访问数量(万)")'}
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
		add_the_error('[第89行foreach语句中]执行第[127]原语 if $time_count_mean > 10000 with rename ss by ("ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$time_count_mean <= 10000', 'with': 'rename ss by ("time_count":"访问数量")'}
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
		add_the_error('[第89行foreach语句中]执行第[128]原语 if $time_count_mean <= 10000 with rename ss by ("t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'llk_mean', 'Action': 'eval', 'eval': 'ss_mean', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[129]原语 llk_mean = eval ss_mean by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean > 1024', 'with': 'ss.llk = lambda llk by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=130
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[130]原语 if $llk_mean > 1024 with ss.llk = lambda llk by (x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean > 1024', 'with': 'rename ss by ("llk":"流量(M)")'}
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
		add_the_error('[第89行foreach语句中]执行第[131]原语 if $llk_mean > 1024 with rename ss by ("llk":"流量(M... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$llk_mean <= 1024', 'with': 'rename ss by ("llk":"流量(k)")'}
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
		add_the_error('[第89行foreach语句中]执行第[132]原语 if $llk_mean <= 1024 with rename ss by ("llk":"流量(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ss', 'to': 'ssdb', 'with': 'z:@id:timeh'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[133]原语 store ss to ssdb with z:@id:timeh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ipls', 'Action': 'filter', 'filter': 'visit_dstip', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[135]原语 ipls = filter visit_dstip by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ipls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/api_visit_dstip1_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[136]原语 ipls_ll = load pq by dt_table/api_visit_dstip1_@id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ipls', 'Action': 'union', 'union': 'ipls,ipls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[137]原语 ipls = union ipls,ipls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ipls', 'Action': 'group', 'group': 'ipls', 'by': 'url,dstip', 'agg': 'dstip_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[138]原语 ipls = group ipls by url,dstip agg dstip_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ipls', 'Action': '@udf', '@udf': 'ipls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[139]原语 ipls = @udf ipls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ipls', 'as': "'dstip_num_sum':'dstip_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[140]原语 rename ipls as ("dstip_num_sum":"dstip_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_dstip1', 'Action': 'loc', 'loc': 'ipls', 'by': 'url,dstip,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[142]原语 visit_dstip1 = loc ipls by url,dstip,dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_dstip1', 'Action': 'order', 'order': 'visit_dstip1', 'by': 'dstip_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[143]原语 visit_dstip1 = order visit_dstip1 by dstip_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_dstip1', 'to': 'pq', 'by': 'dt_table/api_visit_dstip1_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[145]原语 store visit_dstip1 to pq by dt_table/api_visit_dst... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ipls', 'Action': 'loc', 'loc': 'ipls', 'by': 'dstip,dstip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[147]原语 ipls = loc ipls by dstip,dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ipls', 'Action': 'order', 'order': 'ipls', 'by': 'dstip_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[148]原语 ipls = order ipls by dstip_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ipls', 'by': '"dstip":"部署服务器IP",\'dstip_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[149]原语 rename ipls by ("dstip":"部署服务器IP","dstip_num":"访问数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ipls', 'to': 'ssdb', 'with': 'z:@id:ipls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[150]原语 store ipls to ssdb with z:@id:ipls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'accountls', 'Action': 'filter', 'filter': 'visit_account', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[152]原语 accountls = filter visit_account by (url == "@url"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'accountls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/api_visit_account1_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[153]原语 accountls_ll = load pq by dt_table/api_visit_accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'accountls', 'Action': 'union', 'union': 'accountls,accountls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[154]原语 accountls = union accountls,accountls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'accountls', 'Action': 'group', 'group': 'accountls', 'by': 'url,account', 'agg': 'account_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[155]原语 accountls = group accountls by url,account agg acc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'accountls', 'Action': '@udf', '@udf': 'accountls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[156]原语 accountls = @udf accountls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'accountls', 'as': "'account_num_sum':'account_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[157]原语 rename accountls as ("account_num_sum":"account_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_account1', 'Action': 'loc', 'loc': 'accountls', 'by': 'url,account,account_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[159]原语 visit_account1 = loc accountls by url,account,acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_account1', 'Action': 'order', 'order': 'visit_account1', 'by': 'account_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[160]原语 visit_account1 = order visit_account1 by account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_account1', 'to': 'pq', 'by': 'dt_table/api_visit_account1_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[162]原语 store visit_account1 to pq by dt_table/api_visit_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_account1', 'as': '"url":"接口","account":"账号","account_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[164]原语 rename visit_account1 as ("url":"接口","account":"账号... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,api_visit_account1_@id,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[166]原语 b = load ssdb by ssdb0 query qclear,api_visit_acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_account1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_visit_account1_@id', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[168]原语 store visit_account1 to ssdb by ssdb0 with api_vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_account1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[169]原语 drop visit_account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'accountls', 'Action': 'loc', 'loc': 'accountls', 'by': 'account,account_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[171]原语 accountls = loc accountls by account,account_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'accountls', 'Action': 'order', 'order': 'accountls', 'by': 'account_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[172]原语 accountls = order accountls by account_num with de... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'accountls', 'by': '"account":"访问账号",\'account_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[173]原语 rename accountls by ("account":"访问账号","account_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'accountls', 'to': 'ssdb', 'with': 'z:@id:accountls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[174]原语 store accountls to ssdb with z:@id:accountls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'srcipls', 'Action': 'filter', 'filter': 'visit_srcip', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[176]原语 srcipls = filter visit_srcip by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcipls_ll', 'Action': 'load', 'load': 'pq', 'by': 'dt_table/api_visit_srcip1_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[177]原语 srcipls_ll = load pq by dt_table/api_visit_srcip1_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'srcipls', 'Action': 'union', 'union': 'srcipls,srcipls_ll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[178]原语 srcipls = union srcipls,srcipls_ll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'srcipls', 'Action': 'group', 'group': 'srcipls', 'by': 'url,srcip', 'agg': 'srcip_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[179]原语 srcipls = group srcipls by url,srcip agg srcip_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcipls', 'Action': '@udf', '@udf': 'srcipls', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[180]原语 srcipls = @udf srcipls by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'srcipls', 'as': "'srcip_num_sum':'srcip_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[181]原语 rename srcipls as ("srcip_num_sum":"srcip_num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_srcip1', 'Action': 'loc', 'loc': 'srcipls', 'by': 'url,srcip,srcip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[183]原语 visit_srcip1 = loc srcipls by url,srcip,srcip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_srcip1', 'Action': 'order', 'order': 'visit_srcip1', 'by': 'srcip_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[184]原语 visit_srcip1 = order visit_srcip1 by srcip_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_srcip1', 'to': 'pq', 'by': 'dt_table/api_visit_srcip1_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[186]原语 store visit_srcip1 to pq by dt_table/api_visit_src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_srcip1', 'as': '"url":"接口","srcip":"访问终端","srcip_num":"访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[188]原语 rename visit_srcip1 as ("url":"接口","srcip":"访问终端",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,api_visit_srcip1_@id,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[190]原语 b = load ssdb by ssdb0 query qclear,api_visit_srci... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_srcip1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_visit_srcip1_@id', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[192]原语 store visit_srcip1 to ssdb by ssdb0 with api_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'visit_srcip1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[193]原语 drop visit_srcip1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcipls', 'Action': 'loc', 'loc': 'srcipls', 'by': 'srcip,srcip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[195]原语 srcipls = loc srcipls by srcip,srcip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'srcipls', 'Action': 'order', 'order': 'srcipls', 'by': 'srcip_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[196]原语 srcipls = order srcipls by srcip_num with desc lim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'srcipls', 'by': '"srcip":"访问终端",\'srcip_num\':\'访问数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[197]原语 rename srcipls by ("srcip":"访问终端","srcip_num":"访问数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'srcipls', 'to': 'ssdb', 'with': 'z:@id:srcipls'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[198]原语 store srcipls to ssdb with z:@id:srcipls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'url_a', 'Action': 'filter', 'filter': 'visit_url', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[200]原语 url_a = filter visit_url by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'url_a.auto_merge', 'Action': 'lambda', 'lambda': 'auto_merge', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[202]原语 url_a.auto_merge = lambda auto_merge by (x:x[1:-1]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'url_a.auto_merge', 'Action': 'lambda', 'lambda': 'auto_merge', 'by': 'x:x.split(", ")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[203]原语 url_a.auto_merge = lambda auto_merge by (x:x.split... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'url_a', 'Action': '@udf', '@udf': 'url_a', 'by': 'udf0.df_l2cs', 'with': 'auto_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[204]原语 url_a = @udf url_a by udf0.df_l2cs with auto_merge... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'url_a', 'Action': '@udf', '@udf': 'url_a', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[205]原语 url_a = @udf url_a by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'url_a', 'Action': 'loc', 'loc': 'url_a', 'by': 'drop', 'drop': 'url,index,auto_merge'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[206]原语 url_a = loc url_a by drop url,index,auto_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'url_a', 'Action': '@udf', '@udf': 'url_a', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[207]原语 url_a = @udf url_a by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'url_a', 'as': "0:'url'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[208]原语 rename url_a as (0:"url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'url_a.url', 'Action': 'lambda', 'lambda': 'url', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[209]原语 url_a.url = lambda url by (x:x[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'url_a', 'by': '"url":"原接口"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[210]原语 rename url_a by ("url":"原接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'url_a', 'Action': 'filter', 'filter': 'url_a', 'by': "原接口 != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[211]原语 url_a = filter url_a by 原接口 != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'url_a', 'to': 'ssdb', 'with': 'z:@id:url_a'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[212]原语 store url_a to ssdb with z:@id:url_a 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'zts', 'Action': 'filter', 'filter': 'sensitive_data', 'by': 'url == """@url"""'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[214]原语 zts = filter sensitive_data by (url == "@url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'zts', 'Action': 'filter', 'filter': 'zts', 'by': "app != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[216]原语 zts = filter zts by app != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts1', 'Action': 'loc', 'loc': 'zts', 'by': 'app,src_ip,account,type,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[217]原语 zts1 = loc zts by app,src_ip,account,type,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'zts1', 'Action': 'order', 'order': 'zts1', 'by': 'key', 'with': 'desc limit 500'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[218]原语 zts1 = order zts1 by key with desc limit 500 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'zts1', 'Action': 'filter', 'filter': 'zts1', 'by': "key != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[219]原语 zts1 = filter zts1 by key != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts1', 'by': "'key':'敏感类型','type':'标签','app':'应用','src_ip':'终端','account':'账号'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[220]原语 rename zts1 by ("key":"敏感类型","type":"标签","app":"应用... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zts:@id:sens'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[221]原语 store zts1 to ssdb by ssdb0 with zts:@id:sens 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zts2', 'Action': 'loc', 'loc': 'zts', 'by': 'id,url,app,src_ip,account,type,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[223]原语 zts2 = loc zts by id,url,app,src_ip,account,type,k... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts2', 'as': "'id':'_id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[224]原语 rename zts2 as ("id":"_id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'zts2', 'Action': 'filter', 'filter': 'zts2', 'by': "key != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[225]原语 zts2 = filter zts2 by key != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'zts2', 'Action': 'order', 'order': 'zts2', 'by': '_id', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[226]原语 zts2 = order zts2 by _id with desc limit 1000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts2', 'to': 'pq', 'by': 'dt_table/api_zts_@id.pq'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[228]原语 store zts2 to pq by dt_table/api_zts_@id.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zts2', 'as': "'url':'接口','key':'敏感类型','type':'标签','app':'应用','src_ip':'终端','account':'账号'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[230]原语 rename zts2 as ("url":"接口","key":"敏感类型","type":"标签... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,api_zts_@id,-,-'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[232]原语 b = load ssdb by ssdb0 query qclear,api_zts_@id,-,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zts2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_zts_@id', 'as': 'Q'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[234]原语 store zts2 to ssdb by ssdb0 with api_zts_@id as Q 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'zts2'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[第89行foreach语句中]执行第[235]原语 drop zts2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_89

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



