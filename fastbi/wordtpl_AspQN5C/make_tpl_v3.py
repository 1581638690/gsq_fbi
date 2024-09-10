#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_AspQN5C/make_tpl
#datetime: 2024-08-30T16:10:57.323070
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[27]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[31]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'a', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[33]原语 a_num = eval a by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'a = @udf udf0.new_df with name,status'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=34
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[34]原语 if $a_num == 0 with a = @udf udf0.new_df with name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'a = @udf a by udf0.df_append with (,正在生成报告)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=35
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[35]原语 if $a_num == 0 with a = @udf a by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[37]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$now,"%Y-%m-%dT%H:%M:%S"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[38]原语 now = @sdf format_now with ($now,"%Y-%m-%dT%H:%M:%... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"@report_name".strip() in ["","undefined"]', 'with': '""\nset param by define as report_name with @zh-$now\n"', 'else': '"\nset param by define as report_name with @report_name-$now\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=41
		ptree['funs']=block_if_41
		ptree['funs2']=block_if_else_41
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[41]原语 if "@report_name".strip() in ["","undefined"] with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'name', 'by': "'@report_name'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[47]原语 a = add name by  ("@report_name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[51]原语 t = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'True', 'as': 'notice', 'to': '@report_name 报告开始生成!', 'with': '报告生成发现错误!'}
	ptree['to'] = replace_ps(ptree['to'],runtime)
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[52]原语 assert True as notice to @report_name 报告开始生成! with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'trend'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[55]原语 aa = @udf udf0.new_df with trend 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '上升'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[56]原语 aa = @udf aa by udf0.df_append with (上升) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '无变化'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[57]原语 aa = @udf aa by udf0.df_append with (无变化) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '下降'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[58]原语 aa = @udf aa by udf0.df_append with (下降) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-2d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[61]原语 day1 = @sdf sys_now with -2d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day1,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[63]原语 day1 = @sdf format_now with ($day1,"%Y-%m-%dT00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[64]原语 day2 = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd24', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day2,"%Y-%m-%dT%H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[66]原语 dd24 = @sdf format_now with ($day2,"%Y-%m-%dT%H:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day2,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[67]原语 day2 = @sdf format_now with ($day2,"%Y-%m-%dT00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day3', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[68]原语 day3 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'time', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day3,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[69]原语 time = @sdf format_now with ($day3,"%Y-%m-%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd3', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day3,"%Y-%m-%dT%H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[70]原语 dd3 = @sdf format_now with ($day3,"%Y-%m-%dT%H:00:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day3', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day3,"%Y-%m-%dT00:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[71]原语 day3 = @sdf format_now with ($day3,"%Y-%m-%dT00:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'j_hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$dd24,$dd3,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[73]原语 j_hour = @udf udf0.new_df_timerange with ($dd24,$d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'j_hour.hour', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[74]原语 j_hour.hour = lambda end_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'j_hour', 'Action': 'loc', 'loc': 'j_hour', 'by': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[75]原语 j_hour = loc j_hour by hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[79]原语 date = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date', 'Action': '@udf', '@udf': 'date', 'by': 'udf0.df_append', 'with': '$time'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[80]原语 date = @udf date by udf0.df_append with $time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'date', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'date_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[81]原语 store date to ssdb by ssdb0 with date_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dbdk_day'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[85]原语 dbdk = load ssdb by ssdb0 with dbdk_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbdk1', 'Action': 'filter', 'filter': 'dbdk', 'by': "times == '$day1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[86]原语 dbdk1 = filter dbdk by times == "$day1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'dbdk1.index.size == 0', 'with': 'dbdk1 = @udf dbdk1 by udf0.df_append with ($day1,0,0,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=87
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[87]原语 if dbdk1.index.size == 0 with dbdk1 = @udf dbdk1 b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk1_ipackets', 'Action': 'eval', 'eval': 'dbdk1', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[88]原语 dbdk1_ipackets = eval dbdk1 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk1_ibytes', 'Action': 'eval', 'eval': 'dbdk1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[89]原语 dbdk1_ibytes = eval dbdk1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk1_imissed', 'Action': 'eval', 'eval': 'dbdk1', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[90]原语 dbdk1_imissed = eval dbdk1 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk1_cll', 'Action': 'eval', 'eval': 'dbdk1', 'by': 'iloc[0,4]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[91]原语 dbdk1_cll = eval dbdk1 by iloc[0,4] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbdk2', 'Action': 'filter', 'filter': 'dbdk', 'by': "times == '$day2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[92]原语 dbdk2 = filter dbdk by times == "$day2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'dbdk2.index.size == 0', 'with': 'dbdk2 = @udf dbdk2 by udf0.df_append with ($day2,0,0,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=93
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[93]原语 if dbdk2.index.size == 0 with dbdk2 = @udf dbdk2 b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk2_ipackets', 'Action': 'eval', 'eval': 'dbdk2', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[94]原语 dbdk2_ipackets = eval dbdk2 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk2_ibytes', 'Action': 'eval', 'eval': 'dbdk2', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[95]原语 dbdk2_ibytes = eval dbdk2 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk2_imissed', 'Action': 'eval', 'eval': 'dbdk2', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[96]原语 dbdk2_imissed = eval dbdk2 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk2_cll', 'Action': 'eval', 'eval': 'dbdk2', 'by': 'iloc[0,4]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[97]原语 dbdk2_cll = eval dbdk2 by iloc[0,4] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbdk3', 'Action': 'filter', 'filter': 'dbdk', 'by': "times == '$day3'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[98]原语 dbdk3 = filter dbdk by times == "$day3" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'dbdk3.index.size == 0', 'with': 'dbdk3 = @udf dbdk3 by udf0.df_append with ($day3,0,0,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=99
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[99]原语 if dbdk3.index.size == 0 with dbdk3 = @udf dbdk3 b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk3_ipackets', 'Action': 'eval', 'eval': 'dbdk3', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[100]原语 dbdk3_ipackets = eval dbdk3 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk3_ibytes', 'Action': 'eval', 'eval': 'dbdk3', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[101]原语 dbdk3_ibytes = eval dbdk3 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk3_imissed', 'Action': 'eval', 'eval': 'dbdk3', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[102]原语 dbdk3_imissed = eval dbdk3 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk3_cll', 'Action': 'eval', 'eval': 'dbdk3', 'by': 'iloc[0,4]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[103]原语 dbdk3_cll = eval dbdk3 by iloc[0,4] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbdk4', 'Action': 'filter', 'filter': 'dbdk', 'by': "times == '$dd3'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[104]原语 dbdk4 = filter dbdk by times == "$dd3" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'dbdk4.index.size == 0', 'with': 'dbdk4 = @udf dbdk4 by udf0.df_append with ($dd3,0,0,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=105
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[105]原语 if dbdk4.index.size == 0 with dbdk4 = @udf dbdk4 b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk4_ipackets', 'Action': 'eval', 'eval': 'dbdk4', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[106]原语 dbdk4_ipackets = eval dbdk4 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk4_ibytes', 'Action': 'eval', 'eval': 'dbdk4', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[107]原语 dbdk4_ibytes = eval dbdk4 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk4_imissed', 'Action': 'eval', 'eval': 'dbdk4', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[108]原语 dbdk4_imissed = eval dbdk4 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbdk4_cll', 'Action': 'eval', 'eval': 'dbdk4', 'by': 'iloc[0,4]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[109]原语 dbdk4_cll = eval dbdk4 by iloc[0,4] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'yes_ipackets', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk2_ipackets-$dbdk1_ipackets'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[111]原语 yes_ipackets = @sdf sys_eval with ($dbdk2_ipackets... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'yes_ibytes', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk2_ibytes-$dbdk1_ibytes'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[112]原语 yes_ibytes = @sdf sys_eval with ($dbdk2_ibytes-$db... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'yes_imissed', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk2_imissed-$dbdk1_imissed'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[113]原语 yes_imissed = @sdf sys_eval with ($dbdk2_imissed-$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tod_ipackets', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk3_ipackets-$dbdk2_ipackets'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[114]原语 tod_ipackets = @sdf sys_eval with ($dbdk3_ipackets... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tod_ibytes', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk3_ibytes-$dbdk2_ibytes'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[115]原语 tod_ibytes = @sdf sys_eval with ($dbdk3_ibytes-$db... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tod_imissed', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk3_imissed-$dbdk2_imissed'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[116]原语 tod_imissed = @sdf sys_eval with ($dbdk3_imissed-$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_daily', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[118]原语 dbdk_daily = @udf udf0.new_df with tt,yes,tod,tren... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt10', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yes_ipackets-$tod_ipackets'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[120]原语 tt10 = @sdf sys_eval with ($yes_ipackets-$tod_ipac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt10 > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=121
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[121]原语 if $tt10 > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt10 == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=122
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[122]原语 if $tt10 == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt10 < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=123
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[123]原语 if $tt10 < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_daily', 'Action': '@udf', '@udf': 'dbdk_daily', 'by': 'udf0.df_append', 'with': 'ipackets,$yes_ipackets,$tod_ipackets,$bb,$dbdk4_ipackets'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[124]原语 dbdk_daily = @udf dbdk_daily by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt11', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yes_ibytes-$tod_ibytes'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[126]原语 tt11 = @sdf sys_eval with ($yes_ibytes-$tod_ibytes... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt11 > 0', 'with': 'bb = eval aa by iloc[2,0]'}
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[127]原语 if $tt11 > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt11 == 0', 'with': 'bb = eval aa by iloc[1,0]'}
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[128]原语 if $tt11 == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt11 < 0', 'with': 'bb = eval aa by iloc[0,0]'}
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[129]原语 if $tt11 < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_daily', 'Action': '@udf', '@udf': 'dbdk_daily', 'by': 'udf0.df_append', 'with': 'ibytes,$yes_ibytes,$tod_ibytes,$bb,$dbdk4_ibytes'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[130]原语 dbdk_daily = @udf dbdk_daily by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt12', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yes_imissed-$tod_imissed'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[132]原语 tt12 = @sdf sys_eval with ($yes_imissed-$tod_imiss... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt12 > 0', 'with': 'bb = eval aa by iloc[2,0]'}
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[133]原语 if $tt12 > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt12 == 0', 'with': 'bb = eval aa by iloc[1,0]'}
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[134]原语 if $tt12 == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt12 < 0', 'with': 'bb = eval aa by iloc[0,0]'}
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
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[135]原语 if $tt12 < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_daily', 'Action': '@udf', '@udf': 'dbdk_daily', 'by': 'udf0.df_append', 'with': 'imissed,$yes_imissed,$tod_imissed,$bb,$dbdk4_imissed'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[136]原语 dbdk_daily = @udf dbdk_daily by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt13', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$dbdk2_cll-$dbdk3_cll'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[138]原语 tt13 = @sdf sys_eval with ($dbdk2_cll-$dbdk3_cll) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt13 > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=139
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[139]原语 if $tt13 > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt13 == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=140
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[140]原语 if $tt13 == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt13 < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=141
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[141]原语 if $tt13 < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_daily', 'Action': '@udf', '@udf': 'dbdk_daily', 'by': 'udf0.df_append', 'with': '处理率,$dbdk2_cll,$dbdk3_cll,$bb,$dbdk4_cll'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[142]原语 dbdk_daily = @udf dbdk_daily by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dbdk_daily', 'as': "'tt':'主题','yes':'前天','tod':'昨天','trend':'趋势','count':'当前'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[143]原语 rename dbdk_daily as ("tt":"主题","yes":"前天","tod":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dbdk_daily', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dbdk_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[144]原语 store dbdk_daily to ssdb by ssdb0 with dbdk_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbdk_24', 'Action': 'filter', 'filter': 'dbdk', 'by': "times > '$dd24'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[147]原语 dbdk_24 = filter dbdk by times > "$dd24" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'dbdk_24.times', 'Action': 'str', 'str': 'times', 'by': 'slice(11,13)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[148]原语 dbdk_24.times = str times by (slice(11,13)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dbdk_24', 'Action': 'join', 'join': 'dbdk_24,j_hour', 'by': 'times,hour', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[149]原语 dbdk_24 = join dbdk_24,j_hour by times,hour with r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbdk_24_1', 'Action': 'loc', 'loc': 'dbdk_24', 'by': 'hour,ipackets,imissed'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[152]原语 dbdk_24_1 = loc dbdk_24 by hour,ipackets,imissed 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_24_1', 'Action': '@udf', '@udf': 'dbdk_24_1', 'by': 'udf0.df_fillna_cols', 'with': "hour:'0',ipackets:'0',imissed:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[153]原语 dbdk_24_1 = @udf dbdk_24_1 by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbdk_24_1', 'Action': 'loc', 'loc': 'dbdk_24_1', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[154]原语 dbdk_24_1 = loc dbdk_24_1 by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbdk_24_1', 'Action': 'loc', 'loc': 'dbdk_24_1', 'by': 'ipackets,imissed'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[155]原语 dbdk_24_1 = loc dbdk_24_1 by ipackets,imissed 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dbdk_24_1', 'as': "'ipackets':'包数','imissed':'丢包数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[156]原语 rename dbdk_24_1 as ("ipackets":"包数","imissed":"丢包... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dbdk_24_1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dbdk_24h'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[157]原语 store dbdk_24_1 to ssdb by ssdb0 with dbdk_24h 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbdk_24_2', 'Action': 'loc', 'loc': 'dbdk_24', 'by': 'hour,ibytes'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[159]原语 dbdk_24_2 = loc dbdk_24 by hour,ibytes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbdk_24_2', 'Action': '@udf', '@udf': 'dbdk_24_2', 'by': 'udf0.df_fillna_cols', 'with': "hour:'0',ibytes:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[160]原语 dbdk_24_2 = @udf dbdk_24_2 by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbdk_24_2', 'Action': 'loc', 'loc': 'dbdk_24_2', 'by': 'hour', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[161]原语 dbdk_24_2 = loc dbdk_24_2 by hour to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbdk_24_2', 'Action': 'loc', 'loc': 'dbdk_24_2', 'by': 'ibytes'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[162]原语 dbdk_24_2 = loc dbdk_24_2 by ibytes 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dbdk_24_2', 'as': "'ibytes':'字节数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[163]原语 rename dbdk_24_2 as ("ibytes":"字节数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dbdk_24_2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dbdk1_24h'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[164]原语 store dbdk_24_2 to ssdb by ssdb0 with dbdk1_24h 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'yyyy', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '异常项,异常指标,异常详情'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[166]原语 yyyy = @udf udf0.new_df with 异常项,异常指标,异常详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dbdk', 'by': '处理率:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[168]原语 alter dbdk by 处理率:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'cll', 'Action': 'filter', 'filter': 'dbdk', 'by': '处理率 < 90'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[169]原语 cll = filter dbdk by 处理率 < 90 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'cll', 'Action': 'order', 'order': 'cll', 'by': 'times', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[170]原语 cll = order cll by times with desc limit 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'cll.index.size == 1', 'with': '""\ntt = eval cll by iloc[0,0]\ncll = loc cll by 处理率\ncll = add 异常项 by (\'处理率\')\nrename cll as (\'处理率\':\'异常指标\')\ncll = add 异常详情 by (\'$tt处理率低于90%\')\nyyyy = union yyyy,cll\n""'}
	try:
		ptree['lineno']=171
		ptree['funs']=block_if_171
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[171]原语 if cll.index.size == 1 with "tt = eval cll by iloc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'yyyy', 'Action': 'loc', 'loc': 'yyyy', 'by': '异常项,异常指标,异常详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[179]原语 yyyy = loc yyyy by 异常项,异常指标,异常详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[182]原语 xy = @udf udf0.new_df with tt,yes,tod,trend,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from api_dns where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[184]原语 y_dns = load ckh by ckh with select count(*) as ye... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_dns', 'Action': 'eval', 'eval': 'y_dns', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[185]原语 y_dns = eval y_dns by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from api_dns where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[186]原语 t_dns = load ckh by ckh with select count(*) as to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_dns', 'Action': 'eval', 'eval': 't_dns', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[187]原语 t_dns = eval t_dns by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from api_dns'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[188]原语 dns = load ckh by ckh with select count(*) as coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dns', 'Action': 'eval', 'eval': 'dns', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[189]原语 dns = eval dns by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_dns-$t_dns'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[190]原语 tt = @sdf sys_eval with ($y_dns-$t_dns) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=191
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[191]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=192
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[192]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=193
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[193]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'DNS协议,$y_dns,$t_dns,$bb,$dns'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[194]原语 xy = @udf xy by udf0.df_append with (DNS协议,$y_dns,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_dns1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_dns/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[196]原语 y_dns1 = @sdf sys_eval by ($y_dns/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=197
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[197]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_dns1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (DNS协议,$t_dns,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=198
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[198]原语 if $y_dns1 < $tt with yyyy = @udf yyyy by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_pop3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_pop3 where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[200]原语 y_pop3 = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_pop3', 'Action': 'eval', 'eval': 'y_pop3', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[201]原语 y_pop3 = eval y_pop3 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_pop3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_pop3 where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[202]原语 t_pop3 = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_pop3', 'Action': 'eval', 'eval': 't_pop3', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[203]原语 t_pop3 = eval t_pop3 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pop3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_pop3'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[204]原语 pop3 = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pop3', 'Action': 'eval', 'eval': 'pop3', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[205]原语 pop3 = eval pop3 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_pop3-$t_pop3'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[206]原语 tt = @sdf sys_eval with ($y_pop3-$t_pop3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=207
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[207]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=208
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[208]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=209
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[209]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'Pop3邮件协议,$y_pop3,$t_pop3,$bb,$pop3'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[210]原语 xy = @udf xy by udf0.df_append with (Pop3邮件协议,$y_p... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_pop31', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_pop3/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[212]原语 y_pop31 = @sdf sys_eval by ($y_pop3/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=213
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[213]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_pop31 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (Pop3邮件协议,$t_pop3,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=214
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[214]原语 if $y_pop31 < $tt with yyyy = @udf yyyy by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_imap', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_imap where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[216]原语 y_imap = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_imap', 'Action': 'eval', 'eval': 'y_imap', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[217]原语 y_imap = eval y_imap by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_imap', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_imap where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[218]原语 t_imap = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_imap', 'Action': 'eval', 'eval': 't_imap', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[219]原语 t_imap = eval t_imap by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'imap', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_imap'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[220]原语 imap = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'imap', 'Action': 'eval', 'eval': 'imap', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[221]原语 imap = eval imap by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_imap-$t_imap'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[222]原语 tt = @sdf sys_eval with ($y_imap-$t_imap) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=223
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[223]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=224
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[224]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=225
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[225]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'Imap邮件协议,$y_imap,$t_imap,$bb,$imap'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[226]原语 xy = @udf xy by udf0.df_append with (Imap邮件协议,$y_i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_imap1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_imap/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[228]原语 y_imap1 = @sdf sys_eval by ($y_imap/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=229
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[229]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_imap1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (Imap邮件协议,$t_imap,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=230
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[230]原语 if $y_imap1 < $tt with yyyy = @udf yyyy by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_smtp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_smtp where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[232]原语 y_smtp = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_smtp', 'Action': 'eval', 'eval': 'y_smtp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[233]原语 y_smtp = eval y_smtp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_smtp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_smtp where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[234]原语 t_smtp = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_smtp', 'Action': 'eval', 'eval': 't_smtp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[235]原语 t_smtp = eval t_smtp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smtp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_smtp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[236]原语 smtp = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smtp', 'Action': 'eval', 'eval': 'smtp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[237]原语 smtp = eval smtp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_smtp-$t_smtp'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[238]原语 tt = @sdf sys_eval with ($y_smtp-$t_smtp) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=239
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[239]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=240
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[240]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=241
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[241]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'Smtp邮件协议,$y_smtp,$t_smtp,$bb,$smtp'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[242]原语 xy = @udf xy by udf0.df_append with (Smtp邮件协议,$y_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_smtp1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_smtp/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[244]原语 y_smtp1 = @sdf sys_eval by ($y_smtp/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=245
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[245]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_smtp1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (Smtp邮件协议,$t_smtp,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=246
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[246]原语 if $y_smtp1 < $tt with yyyy = @udf yyyy by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_smb', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_smb where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[248]原语 y_smb = load ckh by ckh with select count(*) as nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_smb', 'Action': 'eval', 'eval': 'y_smb', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[249]原语 y_smb = eval y_smb by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_smb', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_smb where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[250]原语 t_smb = load ckh by ckh with select count(*) as nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_smb', 'Action': 'eval', 'eval': 't_smb', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[251]原语 t_smb = eval t_smb by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smb', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_smb'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[252]原语 smb = load ckh by ckh with select count(*) as num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'smb', 'Action': 'eval', 'eval': 'smb', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[253]原语 smb = eval smb by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_smb-$t_smb'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[254]原语 tt = @sdf sys_eval with ($y_smb-$t_smb) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=255
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[255]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=256
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[256]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=257
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[257]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'Windows共享,$y_smb,$t_smb,$bb,$smb'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[258]原语 xy = @udf xy by udf0.df_append with (Windows共享,$y_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_smb1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_smb/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[260]原语 y_smb1 = @sdf sys_eval by ($y_smb/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=261
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[261]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_smb1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (Windows共享,$t_smb,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=262
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[262]原语 if $y_smb1 < $tt with yyyy = @udf yyyy by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_ftp where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[264]原语 y_ftp = load ckh by ckh with select count(*) as nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_ftp', 'Action': 'eval', 'eval': 'y_ftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[265]原语 y_ftp = eval y_ftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_ftp where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[266]原语 t_ftp = load ckh by ckh with select count(*) as nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_ftp', 'Action': 'eval', 'eval': 't_ftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[267]原语 t_ftp = eval t_ftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_ftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[268]原语 ftp = load ckh by ckh with select count(*) as num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ftp', 'Action': 'eval', 'eval': 'ftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[269]原语 ftp = eval ftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_ftp-$t_ftp'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[270]原语 tt = @sdf sys_eval with ($y_ftp-$t_ftp) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=271
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[271]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=272
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[272]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=273
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[273]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'Ftp文件传输,$y_ftp,$t_ftp,$bb,$ftp'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[274]原语 xy = @udf xy by udf0.df_append with (Ftp文件传输,$y_ft... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_ftp1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_ftp/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[276]原语 y_ftp1 = @sdf sys_eval by ($y_ftp/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=277
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[277]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_smtp1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (Ftp文件传输,$t_ftp,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=278
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[278]原语 if $y_smtp1 < $tt with yyyy = @udf yyyy by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_tftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_tftp where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[280]原语 y_tftp = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_tftp', 'Action': 'eval', 'eval': 'y_tftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[281]原语 y_tftp = eval y_tftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_tftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_tftp where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[282]原语 t_tftp = load ckh by ckh with select count(*) as n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_tftp', 'Action': 'eval', 'eval': 't_tftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[283]原语 t_tftp = eval t_tftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tftp', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_tftp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[284]原语 tftp = load ckh by ckh with select count(*) as num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tftp', 'Action': 'eval', 'eval': 'tftp', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[285]原语 tftp = eval tftp by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_tftp-$t_tftp'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[286]原语 tt = @sdf sys_eval with ($y_tftp-$t_tftp) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=287
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[287]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=288
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[288]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=289
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[289]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': 'Tftp文件传输,$y_tftp,$t_tftp,$bb,$tftp'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[290]原语 xy = @udf xy by udf0.df_append with (Tftp文件传输,$y_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_tftp1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_tftp/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[292]原语 y_tftp1 = @sdf sys_eval by ($y_tftp/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=293
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[293]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_tftp1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (Tftp文件传输,$t_tftp,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=294
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[294]原语 if $y_tftp1 < $tt with yyyy = @udf yyyy by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_fileinfo where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[296]原语 y_fileinfo = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_fileinfo', 'Action': 'eval', 'eval': 'y_fileinfo', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[297]原语 y_fileinfo = eval y_fileinfo by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as num from api_fileinfo where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[298]原语 t_fileinfo = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_fileinfo', 'Action': 'eval', 'eval': 't_fileinfo', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[299]原语 t_fileinfo = eval t_fileinfo by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as num from api_fileinfo'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[300]原语 fileinfo = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'eval', 'eval': 'fileinfo', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[301]原语 fileinfo = eval fileinfo by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_fileinfo-$t_fileinfo'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[302]原语 tt = @sdf sys_eval with ($y_fileinfo-$t_fileinfo) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=303
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[303]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=304
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[304]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=305
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[305]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xy', 'Action': '@udf', '@udf': 'xy', 'by': 'udf0.df_append', 'with': '文件信息,$y_fileinfo,$t_fileinfo,$bb,$fileinfo'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[306]原语 xy = @udf xy by udf0.df_append with (文件信息,$y_filei... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_fileinfo1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_fileinfo/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[308]原语 y_fileinfo1 = @sdf sys_eval by ($y_fileinfo/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=309
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[309]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_fileinfo1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (文件信息,$t_fileinfo,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=310
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[310]原语 if $y_fileinfo1 < $tt with yyyy = @udf yyyy by udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'xy', 'as': "'tt':'协议','yes':'前天','tod':'昨天','trend':'趋势','count':'总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[312]原语 rename xy as ("tt":"协议","yes":"前天","tod":"昨天","tre... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'xy', 'by': '总数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[313]原语 alter xy by 总数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'xy.counts', 'Action': 'lambda', 'lambda': '总数', 'by': 'x:round(x/10000,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[314]原语 xy.counts = lambda 总数 by (x:round(x/10000,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sss', 'Action': 'loc', 'loc': 'xy', 'by': '协议,counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[315]原语 sss = loc xy by 协议,counts 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'xy', 'Action': 'loc', 'loc': 'xy', 'by': '协议,前天,昨天,趋势,总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[316]原语 xy = loc xy by 协议,前天,昨天,趋势,总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'xy', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'xy_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[317]原语 store xy to ssdb by ssdb0 with xy_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sss', 'Action': 'loc', 'loc': 'sss', 'by': '协议', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[324]原语 sss = loc sss by 协议 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sss', 'as': "'counts':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[325]原语 rename sss as ("counts":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sss', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[326]原语 store sss to ssdb by ssdb0 with api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dddd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[329]原语 dddd = @udf udf0.new_df with tt,yes,tod,trend,coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as yes from data_app_new where first_time >= '$day1' and first_time < '$day2' and merge_state != 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[331]原语 y_app = load db by mysql1 with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_app', 'Action': 'eval', 'eval': 'y_app', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[332]原语 y_app = eval y_app by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as tod from data_app_new where first_time >= '$day2' and first_time < '$day3' and merge_state != 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[333]原语 t_app = load db by mysql1 with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_app', 'Action': 'eval', 'eval': 't_app', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[334]原语 t_app = eval t_app by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as count from data_app_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[335]原语 app = load db by mysql1 with select count(*) as co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'eval', 'eval': 'app', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[336]原语 app = eval app by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_app-$t_app'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[337]原语 tt = @sdf sys_eval with ($y_app-$t_app) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=338
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[338]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=339
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[339]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=340
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[340]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dddd', 'Action': '@udf', '@udf': 'dddd', 'by': 'udf0.df_append', 'with': '应用(新增),$y_app,$t_app,$bb,$app'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[341]原语 dddd = @udf dddd by udf0.df_append with (应用(新增),$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_app1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_app/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[343]原语 y_app1 = @sdf sys_eval by ($y_app/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=344
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[344]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_app1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (应用,$t_app,昨天新增应用数比前天新增应用数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=345
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[345]原语 if $y_app1 < $tt with yyyy = @udf yyyy by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as yes from data_api_new where first_time >= '$day1' and first_time < '$day2' and merge_state != 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[347]原语 y_api = load db by mysql1 with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_api', 'Action': 'eval', 'eval': 'y_api', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[348]原语 y_api = eval y_api by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as tod from data_api_new where first_time >= '$day2' and first_time < '$day3' and merge_state != 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[349]原语 t_api = load db by mysql1 with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_api', 'Action': 'eval', 'eval': 't_api', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[350]原语 t_api = eval t_api by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as count from data_api_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[351]原语 api = load db by mysql1 with select count(*) as co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'eval', 'eval': 'api', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[352]原语 api = eval api by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_api-$t_api'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[353]原语 tt = @sdf sys_eval with ($y_api-$t_api) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=354
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[354]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=355
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[355]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=356
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[356]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dddd', 'Action': '@udf', '@udf': 'dddd', 'by': 'udf0.df_append', 'with': '接口(新增),$y_api,$t_api,$bb,$api'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[357]原语 dddd = @udf dddd by udf0.df_append with (接口(新增),$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_api1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_api/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[359]原语 y_api1 = @sdf sys_eval by ($y_api/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=360
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[360]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_api1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (接口,$t_api,昨天新增接口数比前天新增接口数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=361
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[361]原语 if $y_api1 < $tt with yyyy = @udf yyyy by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_ip', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as yes from data_ip_new where firsttime >= '$day1' and firsttime < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[363]原语 y_ip = load db by mysql1 with select count(*) as y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_ip', 'Action': 'eval', 'eval': 'y_ip', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[364]原语 y_ip = eval y_ip by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_ip', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as tod from data_ip_new where firsttime >= '$day2' and firsttime < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[365]原语 t_ip = load db by mysql1 with select count(*) as t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_ip', 'Action': 'eval', 'eval': 't_ip', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[366]原语 t_ip = eval t_ip by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as count from data_ip_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[367]原语 ip = load db by mysql1 with select count(*) as cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'eval', 'eval': 'ip', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[368]原语 ip = eval ip by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_ip-$t_ip'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[369]原语 tt = @sdf sys_eval with ($y_ip-$t_ip) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=370
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[370]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=371
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[371]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=372
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[372]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dddd', 'Action': '@udf', '@udf': 'dddd', 'by': 'udf0.df_append', 'with': '终端(新增),$y_ip,$t_ip,$bb,$ip'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[373]原语 dddd = @udf dddd by udf0.df_append with (终端(新增),$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_ip1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_ip/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[375]原语 y_ip1 = @sdf sys_eval by ($y_ip/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=376
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[376]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_ip1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (终端,$t_ip,昨天新增终端数比前天新增终端数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=377
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[377]原语 if $y_ip1 < $tt with yyyy = @udf yyyy by udf0.df_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_account', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as yes from data_account_new where firsttime >= '$day1' and firsttime < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[379]原语 y_account = load db by mysql1 with select count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_account', 'Action': 'eval', 'eval': 'y_account', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[380]原语 y_account = eval y_account by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_account', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select count(*) as tod from data_account_new where firsttime >= '$day2' and firsttime < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[381]原语 t_account = load db by mysql1 with select count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_account', 'Action': 'eval', 'eval': 't_account', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[382]原语 t_account = eval t_account by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as count from data_account_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[383]原语 account = load db by mysql1 with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account', 'Action': 'eval', 'eval': 'account', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[384]原语 account = eval account by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_account-$t_account'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[385]原语 tt = @sdf sys_eval with ($y_account-$t_account) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=386
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[386]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=387
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[387]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=388
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[388]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dddd', 'Action': '@udf', '@udf': 'dddd', 'by': 'udf0.df_append', 'with': '账号(新增),$y_account,$t_account,$bb,$account'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[389]原语 dddd = @udf dddd by udf0.df_append with (账号(新增),$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dddd', 'as': "'tt':'对象','yes':'前天','tod':'昨天','trend':'趋势','count':'总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[390]原语 rename dddd as ("tt":"对象","yes":"前天","tod":"昨天","t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dddd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dddd_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[391]原语 store dddd to ssdb by ssdb0 with dddd_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_account1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_account/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[393]原语 y_account1 = @sdf sys_eval by ($y_account/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=394
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[394]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_account1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (账号,$t_account,昨天新增账号数比前天新增账号数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=395
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[395]原语 if $y_account1 < $tt with yyyy = @udf yyyy by udf0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dddd', 'Action': 'loc', 'loc': 'dddd', 'by': '对象,总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[398]原语 dddd = loc dddd by 对象,总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dddd.对象', 'Action': 'lambda', 'lambda': '对象', 'by': 'x:x[0:2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[399]原语 dddd.对象 = lambda 对象 by (x:x[0:2]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dddd', 'Action': 'loc', 'loc': 'dddd', 'by': '对象', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[400]原语 dddd = loc dddd by 对象 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dddd', 'as': "'总数':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[401]原语 rename dddd as ("总数":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dddd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dddd_num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[402]原语 store dddd to ssdb by ssdb0 with dddd_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sj', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[420]原语 sj = @udf udf0.new_df with tt,yes,tod,trend,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yapp_num', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select sum(ysjjk) as yes from audit_statistics where gmt_create >= '$day1' and gmt_create < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[422]原语 yapp_num = load db by mysql1 with select sum(ysjjk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'yapp_num', 'Action': '@udf', '@udf': 'yapp_num', 'by': 'udf0.df_fillna_cols', 'with': "yes:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[423]原语 yapp_num = @udf yapp_num by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'yapp_num.yes', 'Action': 'lambda', 'lambda': 'yes', 'by': "x:x if x != '' else 0"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[424]原语 yapp_num.yes = lambda yes by (x:x if x != "" else ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yapp_num', 'Action': 'eval', 'eval': 'yapp_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[425]原语 yapp_num = eval yapp_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tapp_num', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select sum(ysjjk) as tod from audit_statistics where gmt_create >= '$day2' and gmt_create < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[426]原语 tapp_num = load db by mysql1 with select sum(ysjjk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tapp_num', 'Action': '@udf', '@udf': 'tapp_num', 'by': 'udf0.df_fillna_cols', 'with': "tod:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[427]原语 tapp_num = @udf tapp_num by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'tapp_num.tod', 'Action': 'lambda', 'lambda': 'tod', 'by': "x:x if x != '' else 0"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[428]原语 tapp_num.tod = lambda tod by (x:x if x != "" else ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tapp_num', 'Action': 'eval', 'eval': 'tapp_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[429]原语 tapp_num = eval tapp_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_num', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select sum(ysjjk) as count from audit_statistics'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[430]原语 app_num = load db by mysql1 with select sum(ysjjk)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_num', 'Action': '@udf', '@udf': 'app_num', 'by': 'udf0.df_fillna_cols', 'with': "count:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[431]原语 app_num = @udf app_num by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_num.count', 'Action': 'lambda', 'lambda': 'count', 'by': "x:x if x != '' else 0"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[432]原语 app_num.count = lambda count by (x:x if x != "" el... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_num', 'by': 'count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[433]原语 alter app_num by count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_num', 'Action': 'eval', 'eval': 'app_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[434]原语 app_num = eval app_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yapp_num-$tapp_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[436]原语 tt = @sdf sys_eval with ($yapp_num-$tapp_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=437
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[437]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=438
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[438]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=439
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[439]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sj', 'Action': '@udf', '@udf': 'sj', 'by': 'udf0.df_append', 'with': '应用审计,$yapp_num,$tapp_num,$bb,$app_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[440]原语 sj = @udf sj by udf0.df_append with (应用审计,$yapp_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yapi_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count() as yes from api_monitor where time >= '$day1' and time < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[445]原语 yapi_num = load ckh by ckh with select count() as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yapi_num', 'Action': 'eval', 'eval': 'yapi_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[446]原语 yapi_num = eval yapi_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tapi_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count() as tod from api_monitor where time >= '$day2' and time < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[447]原语 tapi_num = load ckh by ckh with select count() as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tapi_num', 'Action': 'eval', 'eval': 'tapi_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[448]原语 tapi_num = eval tapi_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count() as count from api_monitor'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[449]原语 api_num = load ckh by ckh with select count() as c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_num', 'Action': 'eval', 'eval': 'api_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[450]原语 api_num = eval api_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$yapi_num-$tapi_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[452]原语 tt = @sdf sys_eval with ($yapi_num-$tapi_num) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=453
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[453]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=454
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[454]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=455
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[455]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sj', 'Action': '@udf', '@udf': 'sj', 'by': 'udf0.df_append', 'with': '接口审计,$yapi_num,$tapi_num,$bb,$api_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[456]原语 sj = @udf sj by udf0.df_append with (接口审计,$yapi_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sj', 'as': "'tt':'审计对象','yes':'前天','tod':'昨天','trend':'趋势','count':'总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[457]原语 rename sj as ("tt":"审计对象","yes":"前天","tod":"昨天","t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sj', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sj_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[458]原语 store sj to ssdb by ssdb0 with sj_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sj1', 'Action': 'loc', 'loc': 'sj', 'by': '审计对象,总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[464]原语 sj1 = loc sj by 审计对象,总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sj1', 'Action': 'loc', 'loc': 'sj1', 'by': '审计对象', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[465]原语 sj1 = loc sj1 by 审计对象 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sj1', 'as': "'总数':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[466]原语 rename sj1 as ("总数":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sj1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sj_num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[467]原语 store sj1 to ssdb by ssdb0 with sj_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[481]原语 sens1 = @udf udf0.new_df with tt,yes,tod,trend,cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_sens_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from sen_http_count where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[483]原语 y_sens_1 = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_sens_1', 'Action': 'eval', 'eval': 'y_sens_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[484]原语 y_sens_1 = eval y_sens_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_sens_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from sen_http_count where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[485]原语 t_sens_1 = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_sens_1', 'Action': 'eval', 'eval': 't_sens_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[486]原语 t_sens_1 = eval t_sens_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from sen_http_count'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[487]原语 sens_1 = load ckh by ckh with select count(*) as c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_1', 'Action': 'eval', 'eval': 'sens_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[488]原语 sens_1 = eval sens_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_sens_1-$t_sens_1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[489]原语 tt = @sdf sys_eval with ($y_sens_1-$t_sens_1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=490
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[490]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=491
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[491]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=492
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[492]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_append', 'with': '敏感数据监控,$y_sens_1,$t_sens_1,$bb,$sens_1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[493]原语 sens1 = @udf sens1 by udf0.df_append with (敏感数据监控,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_sens_11', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_sens_1/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[495]原语 y_sens_11 = @sdf sys_eval by ($y_sens_1/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=496
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[496]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_sens_11 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (敏感数据监控,$t_sens_1,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=497
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[497]原语 if $y_sens_11 < $tt with yyyy = @udf yyyy by udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_fil_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from datafilter where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[515]原语 y_fil_1 = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_fil_1', 'Action': 'eval', 'eval': 'y_fil_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[516]原语 y_fil_1 = eval y_fil_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_fil_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from datafilter where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[517]原语 t_fil_1 = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_fil_1', 'Action': 'eval', 'eval': 't_fil_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[518]原语 t_fil_1 = eval t_fil_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fil_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from datafilter'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[519]原语 fil_1 = load ckh by ckh with select count(*) as co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fil_1', 'Action': 'eval', 'eval': 'fil_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[520]原语 fil_1 = eval fil_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_fil_1 - $t_fil_1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[521]原语 tt = @sdf sys_eval with ($y_fil_1 - $t_fil_1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=522
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[522]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=523
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[523]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=524
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[524]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_append', 'with': '敏感文件监控,$y_fil_1,$t_fil_1,$bb,$fil_1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[525]原语 sens1 = @udf sens1 by udf0.df_append with (敏感文件监控,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_fil_11', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_fil_1/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[527]原语 y_fil_11 = @sdf sys_eval by ($y_fil_1/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=528
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[528]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_fil_11 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (敏感文件监控,$t_fil_1,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=529
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[529]原语 if $y_fil_11 < $tt with yyyy = @udf yyyy by udf0.d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens1', 'as': "'tt':'敏感数据','yes':'前天','tod':'昨天','trend':'趋势','count':'总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[547]原语 rename sens1 as ("tt":"敏感数据","yes":"前天","tod":"昨天"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens1', 'by': '总数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[548]原语 alter sens1 by 总数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens1', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[549]原语 sens1 = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'pj', 'Action': 'group', 'group': 'sens1', 'by': 'aa', 'agg': '总数:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[550]原语 pj = group sens1 by aa agg 总数:mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pj', 'Action': 'eval', 'eval': 'pj', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[551]原语 pj = eval pj by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj >= 100000', 'with': 'sens1.counts = lambda 总数 by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=552
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[552]原语 if $pj >= 100000 with sens1.counts = lambda 总数 by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj < 100000', 'with': 'sens1.counts = lambda 总数 by (x:x)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=553
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[553]原语 if $pj < 100000 with sens1.counts = lambda 总数 by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'eeee', 'Action': 'loc', 'loc': 'sens1', 'by': '敏感数据,counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[554]原语 eeee = loc sens1 by 敏感数据,counts 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens1', 'by': '敏感数据,前天,昨天,趋势,总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[555]原语 sens1 = loc sens1 by 敏感数据,前天,昨天,趋势,总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[556]原语 store sens1 to ssdb by ssdb0 with sens_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dw', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dw'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[559]原语 dw = @udf udf0.new_df with dw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj >= 100000', 'with': 'dw = @udf dw by udf0.df_append with ((万))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=560
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[560]原语 if $pj >= 100000 with dw = @udf dw by udf0.df_appe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj < 100000', 'with': 'dw = @udf dw by udf0.df_append with ()'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=561
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[561]原语 if $pj < 100000 with dw = @udf dw by udf0.df_appen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dw', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens_dw'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[562]原语 store dw to ssdb by ssdb0 with sens_dw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'eeee', 'Action': 'loc', 'loc': 'eeee', 'by': '敏感数据', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[566]原语 eeee = loc eeee by 敏感数据 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'eeee', 'as': "'counts':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[567]原语 rename eeee as ("counts":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'eeee', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens_num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[568]原语 store eeee to ssdb by ssdb0 with sens_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[585]原语 risk = @udf udf0.new_df with tt,yes,tod,trend,coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'model_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:model_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[586]原语 model_type = load ssdb by ssdb0 with dd:model_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'model_type', 'Action': 'loc', 'loc': 'model_type', 'by': 'index', 'to': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[587]原语 model_type = loc model_type by index to type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'model_type', 'with': 'tt=$1,type=$2', 'run': '""\ny_model = load ckh by ckh with select count(*) as yes from api_model where timestamp >= \'$day1\' and timestamp < \'$day2\' and type = \'@tt\'\ny_model = eval y_model by iloc[0,0]\nt_model = load ckh by ckh with select count(*) as tod from api_model where timestamp >= \'$day2\' and timestamp < \'$day3\' and type = \'@tt\'\nt_model = eval t_model by iloc[0,0]\nmodel = load ckh by ckh with select count(*) as count from api_model where type = \'@tt\'\nmodel = eval model by iloc[0,0]\ntt = @sdf sys_eval with ($y_model-$t_model)\nif $tt > 0 with bb = eval aa by iloc[2,0]\nif $tt == 0 with bb = eval aa by iloc[1,0]\nif $tt < 0 with bb = eval aa by iloc[0,0]\nrisk = @udf risk by udf0.df_append with (@type,$y_model,$t_model,$bb,$model)\n###敏感文件异常\ny_model1 = @sdf sys_eval by ($y_model/2)\nif $tt < 0 with tt = @sdf sys_eval by ($tt * -1)\nif $y_model1 < $tt with yyyy = @udf yyyy by udf0.df_append with (@type,$t_model,昨天新增事件数比前天新增事件数$bb超50%)\n""'}
	try:
		ptree['lineno']=588
		ptree['funs']=block_foreach_588
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[588]原语 foreach model_type run "y_model = load ckh by ckh ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk', 'as': "'tt':'告警','yes':'前天','tod':'昨天','trend':'趋势','count':'总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[606]原语 rename risk as ("tt":"告警","yes":"前天","tod":"昨天","t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'risk', 'by': '总数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[607]原语 alter risk by 总数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[608]原语 risk = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'pj', 'Action': 'group', 'group': 'risk', 'by': 'aa', 'agg': '总数:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[609]原语 pj = group risk by aa agg 总数:mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pj', 'Action': 'eval', 'eval': 'pj', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[610]原语 pj = eval pj by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj >= 100000', 'with': 'risk.counts = lambda 总数 by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=611
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[611]原语 if $pj >= 100000 with risk.counts = lambda 总数 by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj < 100000', 'with': 'risk.counts = lambda 总数 by (x:x)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=612
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[612]原语 if $pj < 100000 with risk.counts = lambda 总数 by (x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk1', 'Action': 'loc', 'loc': 'risk', 'by': '告警,counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[613]原语 risk1 = loc risk by 告警,counts 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': '告警,前天,昨天,趋势,总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[614]原语 risk = loc risk by 告警,前天,昨天,趋势,总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk1_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[615]原语 store risk to ssdb by ssdb0 with risk1_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dw', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dw'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[618]原语 dw = @udf udf0.new_df with dw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj >= 100000', 'with': 'dw = @udf dw by udf0.df_append with ((万))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=619
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[619]原语 if $pj >= 100000 with dw = @udf dw by udf0.df_appe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj < 100000', 'with': 'dw = @udf dw by udf0.df_append with ()'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=620
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[620]原语 if $pj < 100000 with dw = @udf dw by udf0.df_appen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dw', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk1_dw'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[621]原语 store dw to ssdb by ssdb0 with risk1_dw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk1', 'as': "'counts':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[625]原语 rename risk1 as ("counts":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk1', 'Action': 'loc', 'loc': 'risk1', 'by': '告警', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[626]原语 risk1 = loc risk1 by 告警 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk1_num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[627]原语 store risk1 to ssdb by ssdb0 with risk1_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'tt,yes,tod,trend,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[631]原语 risk = @udf udf0.new_df with tt,yes,tod,trend,coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_yz', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(risk_label) as yes from api_risk where first_time >= '$day1' and first_time < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[632]原语 y_yz = load ckh by ckh with select count(risk_labe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_yz', 'Action': 'eval', 'eval': 'y_yz', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[633]原语 y_yz = eval y_yz by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_yz', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(risk_label) as tod from api_risk where first_time >= '$day2' and first_time < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[634]原语 t_yz = load ckh by ckh with select count(risk_labe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_yz', 'Action': 'eval', 'eval': 't_yz', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[635]原语 t_yz = eval t_yz by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yz', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(risk_label) as count from api_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[636]原语 yz = load ckh by ckh with select count(risk_label)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yz', 'Action': 'eval', 'eval': 'yz', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[637]原语 yz = eval yz by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_yz-$t_yz'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[638]原语 tt = @sdf sys_eval with ($y_yz-$t_yz) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=639
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[639]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=640
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[640]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=641
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[641]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '阈值告警,$y_yz,$t_yz,$bb,$yz'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[642]原语 risk = @udf risk by udf0.df_append with (阈值告警,$y_y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_yz1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_yz/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[644]原语 y_yz1 = @sdf sys_eval by ($y_yz/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=645
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[645]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_yz1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (阈值告警,$t_yz,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=646
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[646]原语 if $y_yz1 < $tt with yyyy = @udf yyyy by udf0.df_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from api_delay where time >= '$day1' and time < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[648]原语 y_delay = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_delay', 'Action': 'eval', 'eval': 'y_delay', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[649]原语 y_delay = eval y_delay by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from api_delay where time >= '$day2' and time < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[650]原语 t_delay = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_delay', 'Action': 'eval', 'eval': 't_delay', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[651]原语 t_delay = eval t_delay by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from api_delay'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[652]原语 delay = load ckh by ckh with select count(*) as co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'delay', 'Action': 'eval', 'eval': 'delay', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[653]原语 delay = eval delay by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_delay-$t_delay'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[654]原语 tt = @sdf sys_eval with ($y_delay-$t_delay) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=655
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[655]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=656
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[656]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=657
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[657]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '访问耗时告警,$y_delay,$t_delay,$bb,$delay'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[658]原语 risk = @udf risk by udf0.df_append with (访问耗时告警,$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_delay1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_delay/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[660]原语 y_delay1 = @sdf sys_eval by ($y_delay/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=661
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[661]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_delay1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (访问耗时告警,$t_delay,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=662
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[662]原语 if $y_delay1 < $tt with yyyy = @udf yyyy by udf0.d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from r_req_alm where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[664]原语 y_req = load ckh by ckh with select count(*) as ye... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_req', 'Action': 'eval', 'eval': 'y_req', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[665]原语 y_req = eval y_req by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from r_req_alm where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[666]原语 t_req = load ckh by ckh with select count(*) as to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_req', 'Action': 'eval', 'eval': 't_req', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[667]原语 t_req = eval t_req by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'req', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from r_req_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[668]原语 req = load ckh by ckh with select count(*) as coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'req', 'Action': 'eval', 'eval': 'req', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[669]原语 req = eval req by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_req-$t_req'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[670]原语 tt = @sdf sys_eval with ($y_req-$t_req) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=671
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[671]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=672
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[672]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=673
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[673]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '异地访问告警,$y_req,$t_req,$bb,$req'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[674]原语 risk = @udf risk by udf0.df_append with (异地访问告警,$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_req1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_req/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[676]原语 y_req1 = @sdf sys_eval by ($y_req/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=677
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[677]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_req1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (异地访问告警,$t_req,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=678
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[678]原语 if $y_req1 < $tt with yyyy = @udf yyyy by udf0.df_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from stat_req_alm where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[680]原语 y_stat = load ckh by ckh with select count(*) as y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_stat', 'Action': 'eval', 'eval': 'y_stat', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[681]原语 y_stat = eval y_stat by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from stat_req_alm where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[682]原语 t_stat = load ckh by ckh with select count(*) as t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_stat', 'Action': 'eval', 'eval': 't_stat', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[683]原语 t_stat = eval t_stat by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from stat_req_alm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[684]原语 stat = load ckh by ckh with select count(*) as cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stat', 'Action': 'eval', 'eval': 'stat', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[685]原语 stat = eval stat by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_stat-$t_stat'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[686]原语 tt = @sdf sys_eval with ($y_stat-$t_stat) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=687
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[687]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=688
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[688]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=689
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[689]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '请求异常告警,$y_stat,$t_stat,$bb,$stat'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[690]原语 risk = @udf risk by udf0.df_append with (请求异常告警,$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_stat1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_stat/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[692]原语 y_stat1 = @sdf sys_eval by ($y_stat/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=693
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[693]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_stat1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (请求异常告警,$t_stat,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=694
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[694]原语 if $y_stat1 < $tt with yyyy = @udf yyyy by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from sensitive_data_alarm where time >= '$day1' and time < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[696]原语 y_sensitive = load ckh by ckh with select count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_sensitive', 'Action': 'eval', 'eval': 'y_sensitive', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[697]原语 y_sensitive = eval y_sensitive by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from sensitive_data_alarm where time >= '$day2' and time < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[698]原语 t_sensitive = load ckh by ckh with select count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_sensitive', 'Action': 'eval', 'eval': 't_sensitive', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[699]原语 t_sensitive = eval t_sensitive by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from sensitive_data_alarm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[700]原语 sensitive = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'eval', 'eval': 'sensitive', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[701]原语 sensitive = eval sensitive by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_sensitive-$t_sensitive'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[702]原语 tt = @sdf sys_eval with ($y_sensitive-$t_sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=703
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[703]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=704
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[704]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=705
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[705]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '敏感数据告警,$y_sensitive,$t_sensitive,$bb,$sensitive'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[706]原语 risk = @udf risk by udf0.df_append with (敏感数据告警,$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_sensitive1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_sensitive/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[708]原语 y_sensitive1 = @sdf sys_eval by ($y_sensitive/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=709
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[709]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_sensitive1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (敏感数据告警,$t_sensitive,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=710
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[710]原语 if $y_sensitive1 < $tt with yyyy = @udf yyyy by ud... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from api_abroad where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[712]原语 y_abroad = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_abroad', 'Action': 'eval', 'eval': 'y_abroad', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[713]原语 y_abroad = eval y_abroad by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from api_abroad where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[714]原语 t_abroad = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_abroad', 'Action': 'eval', 'eval': 't_abroad', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[715]原语 t_abroad = eval t_abroad by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from api_abroad'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[716]原语 abroad = load ckh by ckh with select count(*) as c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'abroad', 'Action': 'eval', 'eval': 'abroad', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[717]原语 abroad = eval abroad by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_abroad-$t_abroad'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[718]原语 tt = @sdf sys_eval with ($y_abroad-$t_abroad) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=719
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[719]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=720
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[720]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=721
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[721]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '境外访问告警,$y_abroad,$t_abroad,$bb,$abroad'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[722]原语 risk = @udf risk by udf0.df_append with (境外访问告警,$y... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_abroad1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_abroad/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[724]原语 y_abroad1 = @sdf sys_eval by ($y_abroad/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=725
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[725]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_abroad1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (境外访问告警,$t_abroad,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=726
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[726]原语 if $y_abroad1 < $tt with yyyy = @udf yyyy by udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_filter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from datafilter_alarm where timestamp >= '$day1' and timestamp < '$day2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[728]原语 y_filter = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_filter', 'Action': 'eval', 'eval': 'y_filter', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[729]原语 y_filter = eval y_filter by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_filter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from datafilter_alarm where timestamp >= '$day2' and timestamp < '$day3'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[730]原语 t_filter = load ckh by ckh with select count(*) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_filter', 'Action': 'eval', 'eval': 't_filter', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[731]原语 t_filter = eval t_filter by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'filter1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from datafilter_alarm'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[732]原语 filter1 = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'filter1', 'Action': 'eval', 'eval': 'filter1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[733]原语 filter1 = eval filter1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_filter-$t_filter'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[734]原语 tt = @sdf sys_eval with ($y_filter-$t_filter) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=735
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[735]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=736
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[736]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=737
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[737]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '文件敏感信息告警,$y_filter,$t_filter,$bb,$filter1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[738]原语 risk = @udf risk by udf0.df_append with (文件敏感信息告警,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_filter1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_filter/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[740]原语 y_filter1 = @sdf sys_eval by ($y_filter/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=741
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[741]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_filter1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (文件敏感信息告警,$t_abroad,昨天新增告警事件数比前天新增告警事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=742
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[742]原语 if $y_filter1 < $tt with yyyy = @udf yyyy by udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk', 'as': "'tt':'告警','yes':'前天','tod':'昨天','trend':'趋势','count':'总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[744]原语 rename risk as ("tt":"告警","yes":"前天","tod":"昨天","t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'risk', 'by': '总数:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[745]原语 alter risk by 总数:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'risk', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[746]原语 risk = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'pj', 'Action': 'group', 'group': 'risk', 'by': 'aa', 'agg': '总数:mean'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[747]原语 pj = group risk by aa agg 总数:mean 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pj', 'Action': 'eval', 'eval': 'pj', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[748]原语 pj = eval pj by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj >= 100000', 'with': 'risk.counts = lambda 总数 by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=749
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[749]原语 if $pj >= 100000 with risk.counts = lambda 总数 by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj < 100000', 'with': 'risk.counts = lambda 总数 by (x:x)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=750
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[750]原语 if $pj < 100000 with risk.counts = lambda 总数 by (x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk2', 'Action': 'loc', 'loc': 'risk', 'by': '告警,counts'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[751]原语 risk2 = loc risk by 告警,counts 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk', 'Action': 'loc', 'loc': 'risk', 'by': '告警,前天,昨天,趋势,总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[752]原语 risk = loc risk by 告警,前天,昨天,趋势,总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[753]原语 store risk to ssdb by ssdb0 with risk_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dw', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dw'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[756]原语 dw = @udf udf0.new_df with dw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj >= 100000', 'with': 'dw = @udf dw by udf0.df_append with ((万))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=757
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[757]原语 if $pj >= 100000 with dw = @udf dw by udf0.df_appe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pj < 100000', 'with': 'dw = @udf dw by udf0.df_append with ()'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=758
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[758]原语 if $pj < 100000 with dw = @udf dw by udf0.df_appen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dw', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_dw'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[759]原语 store dw to ssdb by ssdb0 with risk_dw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'risk2', 'Action': 'loc', 'loc': 'risk2', 'by': '告警', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[763]原语 risk2 = loc risk2 by 告警 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'risk2', 'as': "'counts':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[764]原语 rename risk2 as ("counts":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'risk2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[765]原语 store risk2 to ssdb by ssdb0 with risk_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'yyyy', 'Action': 'loc', 'loc': 'yyyy', 'by': '异常项,异常指标,异常详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[789]原语 yyyy = loc yyyy by 异常项,异常指标,异常详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'yyyy', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'yyyy_daily'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[790]原语 store yyyy to ssdb by ssdb0 with yyyy_daily 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@pics_data'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[793]原语 data=load ssdb by ssdb0 with @pics_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': '@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[795]原语 @udf data by doc.generate_pic with @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'result', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[797]原语 result=@udf data by doc.modifiy_doc with (@id,@bas... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'html', 'Action': '@udf', '@udf': 'doc.word2html', 'with': '@report_name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[800]原语 html = @udf doc.word2html with @report_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'alert', 'to': '报告生成完成!', 'with': '报告生成发现错误!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[802]原语 assert not_have_error() as alert to 报告生成完成! with 报... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 't', 'Action': 'add', 'add': 'status', 'with': "'报告生成完毕'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[805]原语 t = add status with ("报告生成完毕") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[806]原语 t = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 't', 'by': 'df.index[0] >0', 'as': 'notice', 'to': '@report_name 报告生成完毕!', 'with': '@report_name 报告生成发现错误!'}
	ptree['to'] = replace_ps(ptree['to'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[807]原语 assert t by df.index[0] >0  as notice to @report_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 't', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[809]原语 push t as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_AspQN5C/make_tpl.fbi]执行第[812]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],812

#主函数结束,开始块函数

def block_if_41(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'set', 'set': 'param', 'by': 'define', 'as': 'report_name', 'with': '@zh-$now'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[第41行if语句中]执行第[42]原语 set param by define as report_name with @zh-$now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_41

def block_if_else_41(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'set', 'set': 'param', 'by': 'define', 'as': 'report_name', 'with': '@report_name-$now'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		set_fun(ptree)
	except Exception as e:
		add_the_error('[第41行if_else语句中]执行第[41]原语 set param by define as report_name with @report_na... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_else_41

def block_if_171(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'tt', 'Action': 'eval', 'eval': 'cll', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[172]原语 tt = eval cll by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'cll', 'Action': 'loc', 'loc': 'cll', 'by': '处理率'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[173]原语 cll = loc cll by 处理率 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'cll', 'Action': 'add', 'add': '异常项', 'by': "'处理率'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[174]原语 cll = add 异常项 by ("处理率") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'cll', 'as': "'处理率':'异常指标'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[175]原语 rename cll as ("处理率":"异常指标") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'cll', 'Action': 'add', 'add': '异常详情', 'by': "'$tt处理率低于90%'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[176]原语 cll = add 异常详情 by ("$tt处理率低于90%") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'yyyy', 'Action': 'union', 'union': 'yyyy,cll'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第171行if语句中]执行第[177]原语 yyyy = union yyyy,cll 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_171

def block_foreach_588(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'y_model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as yes from api_model where timestamp >= '$day1' and timestamp < '$day2' and type = '@tt'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[589]原语 y_model = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'y_model', 'Action': 'eval', 'eval': 'y_model', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[590]原语 y_model = eval y_model by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as tod from api_model where timestamp >= '$day2' and timestamp < '$day3' and type = '@tt'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[591]原语 t_model = load ckh by ckh with select count(*) as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_model', 'Action': 'eval', 'eval': 't_model', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[592]原语 t_model = eval t_model by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'model', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as count from api_model where type = '@tt'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[593]原语 model = load ckh by ckh with select count(*) as co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'model', 'Action': 'eval', 'eval': 'model', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[594]原语 model = eval model by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'tt', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$y_model-$t_model'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[595]原语 tt = @sdf sys_eval with ($y_model-$t_model) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt > 0', 'with': 'bb = eval aa by iloc[2,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=596
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[596]原语 if $tt > 0 with bb = eval aa by iloc[2,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt == 0', 'with': 'bb = eval aa by iloc[1,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=597
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[597]原语 if $tt == 0 with bb = eval aa by iloc[1,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'bb = eval aa by iloc[0,0]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=598
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[598]原语 if $tt < 0 with bb = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'risk', 'Action': '@udf', '@udf': 'risk', 'by': 'udf0.df_append', 'with': '@type,$y_model,$t_model,$bb,$model'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[599]原语 risk = @udf risk by udf0.df_append with (@type,$y_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'y_model1', 'Action': '@sdf', '@sdf': 'sys_eval', 'by': '$y_model/2'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[601]原语 y_model1 = @sdf sys_eval by ($y_model/2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$tt < 0', 'with': 'tt = @sdf sys_eval by ($tt * -1)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=602
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[602]原语 if $tt < 0 with tt = @sdf sys_eval by ($tt * -1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$y_model1 < $tt', 'with': 'yyyy = @udf yyyy by udf0.df_append with (@type,$t_model,昨天新增事件数比前天新增事件数$bb超50%)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=603
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第588行foreach语句中]执行第[603]原语 if $y_model1 < $tt with yyyy = @udf yyyy by udf0.d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_588

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



