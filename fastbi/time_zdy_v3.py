#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: time_zdy
#datetime: 2024-08-30T16:10:55.075797
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
		add_the_error('[time_zdy.fbi]执行第[7]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[9]原语 dd = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'dd', 'by': 'udf0.df_append', 'with': '@day'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[10]原语 dd = @udf dd by udf0.df_append with @day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'dd.time1', 'Action': 'str', 'str': 'time', 'by': 'slice(0,19)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[11]原语 dd.time1 = str time by (slice(0,19)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'dd.time2', 'Action': 'str', 'str': 'time', 'by': 'slice(-19,)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[12]原语 dd.time2 = str time by (slice(-19,)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'dd', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[13]原语 time1 = eval dd by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'dd', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[14]原语 time2 = eval dd by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[16]原语 day = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[17]原语 day = @sdf format_now with ($day,"%Y-%m-%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select sum(visit_num) as visit_count,sum(visit_flow) as flow,left(toString(min(time)),19) as min_time,left(toString(max(time)),19) as max_time from api_visit_hour where time >= toDateTime('$time1') and time <= toDateTime('$time2')"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[19]原语 visit1 = load ckh by ckh with select sum(visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'visit1 = @udf visit1 by udf0.df_append with (0,0,,)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=20
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[20]原语 if visit1.index.size == 0 with visit1 = @udf visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'alter visit1.visit_count.flow as int'}
	try:
		ptree['lineno']=21
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[21]原语 if visit1.index.size == 0 with alter visit1.visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'max_visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select left(toString(time),10) as day,sum(visit_num) as visit_count,sum(visit_flow) as flow from api_visit_hour where time >= toDateTime('$time1') and time <= toDateTime('$time2') group by day"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[22]原语 max_visit1 = load ckh by ckh with select left(toSt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't_visit1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'day'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[24]原语 t_visit1 = @udf udf0.new_df with day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't_visit1', 'Action': '@udf', '@udf': 't_visit1', 'by': 'udf0.df_append', 'with': '$day'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[25]原语 t_visit1 = @udf t_visit1 by udf0.df_append with $d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 't_visit1', 'Action': 'join', 'join': 't_visit1,max_visit1', 'by': 'day,day', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[26]原语 t_visit1 = join t_visit1,max_visit1 by day,day wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't_visit1', 'Action': 'loc', 'loc': 't_visit1', 'by': 'visit_count,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[27]原语 t_visit1 = loc t_visit1 by visit_count,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't_visit1', 'Action': '@udf', '@udf': 't_visit1', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[28]原语 t_visit1 = @udf t_visit1 by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't_num', 'Action': 'eval', 'eval': 't_visit1', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[29]原语 t_num = eval t_visit1 by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$t_num == 0', 'with': "t_visit1 = load ckh by ckh with select sum(visit_num) as visit_count,sum(visit_flow) as flow from api_visit_hour where left(toString(time),10) = '$day'"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=30
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[30]原语 if $t_num == 0 with t_visit1 = load ckh by ckh wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[34]原语 visit_1 = loc visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_1', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[35]原语 rename visit_1 as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[36]原语 aa_num = eval visit_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_1 = add name by ('总访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=37
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[37]原语 if $aa_num < 100000 with visit_1 = add name by ("总... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=38
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[38]原语 if 100000 <= $aa_num < 1000000000 with visit_1.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_1 = add name by ('总访问量(万次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=39
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[39]原语 if 100000 <= $aa_num < 1000000000 with visit_1 = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_1.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=40
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[40]原语 if $aa_num >= 1000000000 with visit_1.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_1 = add name by ('总访问量(亿次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=41
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[41]原语 if $aa_num >= 1000000000 with visit_1 = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'icon', 'by': "'F396'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[42]原语 visit_1 = add icon by ("F396") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt1', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[43]原语 tt1 = eval visit1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt2', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[44]原语 tt2 = eval visit1 by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_1', 'Action': 'add', 'add': 'details', 'by': '"自$tt1至$tt2以来的总访问次数(HTTP协议)"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[45]原语 visit_1 = add details by ("自$tt1至$tt2以来的总访问次数(HTTP... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_1', 'Action': 'loc', 'loc': 'visit_1', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[46]原语 visit_1 = loc visit_1 by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[52]原语 flow = loc visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[53]原语 aa_num = eval flow by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $aa_num < 1024', 'with': "flow = add name by ('应用总流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=54
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[54]原语 if 0 <= $aa_num < 1024  with flow = add name by ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': 'flow.flow = lambda flow by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=55
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[55]原语 if 1024 <= $aa_num < 1048576  with flow.flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $aa_num < 1048576', 'with': "flow = add name by ('应用总流量(KB)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=56
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[56]原语 if 1024 <= $aa_num < 1048576  with flow = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': 'flow.flow = lambda flow by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=57
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[57]原语 if 1048576 <= $aa_num < 1073741824  with flow.flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $aa_num < 1073741824', 'with': "flow = add name by ('应用总流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=58
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[58]原语 if 1048576 <= $aa_num < 1073741824  with flow = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=59
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[59]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow = add name by ('应用总流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=60
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[60]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow.flow = lambda flow by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=61
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[61]原语 if $aa_num > 10995116277760 with flow.flow = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow = add name by ('应用总流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=62
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[62]原语 if $aa_num > 10995116277760 with flow = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[63]原语 rename flow as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'icon', 'by': "'F352'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[64]原语 flow = add icon by ("F352") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow', 'Action': 'add', 'add': 'details', 'by': "'自$tt1至$tt2以来的总访问流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[65]原语 flow = add details by ("自$tt1至$tt2以来的总访问流量(HTTP协议)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'flow', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[68]原语 flow = loc flow by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'max_visit1 = @udf max_visit1 by udf0.df_append with (,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=70
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[70]原语 if max_visit1.index.size == 0 with max_visit1 = @u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'max_visit1.index.size == 0', 'with': 'alter max_visit1.visit_count.flow as int'}
	try:
		ptree['lineno']=71
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[71]原语 if max_visit1.index.size == 0 with alter max_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'visit_count', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[72]原语 visit_m = order max_visit1 by visit_count with des... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[73]原语 dd = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_m', 'Action': 'loc', 'loc': 'visit_m', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[74]原语 visit_m = loc visit_m by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_m', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[75]原语 rename visit_m as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[76]原语 aa_num = eval visit_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_m = add name by ('日最大访问量')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=77
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[77]原语 if $aa_num < 100000 with visit_m = add name by ("日... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=78
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[78]原语 if 100000 <= $aa_num < 1000000000 with visit_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 1000000000', 'with': "visit_m = add name by ('日最大访问量(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=79
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[79]原语 if 100000 <= $aa_num < 1000000000 with visit_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': 'visit_m.value = lambda value by (x:round(x/100000000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=80
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[80]原语 if $aa_num >= 1000000000 with visit_m.value = lamb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 1000000000', 'with': "visit_m = add name by ('日最大访问量(亿)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=81
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[81]原语 if $aa_num >= 1000000000 with visit_m = add name b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'icon', 'by': "'F156'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[82]原语 visit_m = add icon by ("F156") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大访问量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[83]原语 visit_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大访... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'flow_m', 'Action': 'order', 'order': 'max_visit1', 'by': 'flow', 'with': 'desc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[85]原语 flow_m = order max_visit1 by flow with desc limit ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dd', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[86]原语 dd = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_m', 'Action': 'loc', 'loc': 'flow_m', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[87]原语 flow_m = loc flow_m by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_m', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[88]原语 rename flow_m as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_m', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[89]原语 aa_num = eval flow_m by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_m = add name by ('日最大流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=90
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[90]原语 if $aa_num <= 1024 with flow_m = add name by ("日最大... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_m.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=91
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[91]原语 if 1024 < $aa_num <= 1048576 with flow_m.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_m = add name by ('日最大流量(k)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=92
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[92]原语 if 1024 < $aa_num <= 1048576 with flow_m = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_m.value = lambda value by (x:round(x/1048576,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=93
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[93]原语 if 1048576 < $aa_num <= 1073741824 with flow_m.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_m = add name by ('日最大流量(M)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=94
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[94]原语 if 1048576 < $aa_num <= 1073741824 with flow_m = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=95
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[95]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_m = add name by ('日最大流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=96
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[96]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_m.value = lambda value by (x:round(x/1099511627776,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=97
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[97]原语 if $aa_num > 10995116277760 with flow_m.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_m = add name by ('日最大流量(T)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=98
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[98]原语 if $aa_num > 10995116277760 with flow_m = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'icon', 'by': "'F159'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[99]原语 flow_m = add icon by ("F159") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_m', 'Action': 'add', 'add': 'details', 'by': "'$dd产生了自$tt1至$tt2以来的日最大流量(HTTP协议)'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[100]原语 flow_m = add details by ("$dd产生了自$tt1至$tt2以来的日最大流量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 't_visit1.index.size == 0', 'with': 't_visit1 = @udf t_visit1 by udf0.df_append with (0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=103
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[103]原语 if t_visit1.index.size == 0 with t_visit1 = @udf t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 't_visit1.index.size == 0', 'with': 'alter t_visit1.visit_count.flow as int'}
	try:
		ptree['lineno']=104
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[104]原语 if t_visit1.index.size == 0 with alter t_visit1.vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_t', 'Action': 'loc', 'loc': 't_visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[105]原语 visit_t = loc t_visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_t', 'as': "'visit_count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[106]原语 rename visit_t as ("visit_count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'visit_t', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[107]原语 aa_num = eval visit_t by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 100000', 'with': "visit_t = add name by ('今日访问量')"}
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
		add_the_error('[time_zdy.fbi]执行第[108]原语 if $aa_num < 100000 with visit_t = add name by ("今... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 100000000', 'with': 'visit_t.value = lambda value by (x:round(x/10000,2))'}
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
		add_the_error('[time_zdy.fbi]执行第[109]原语 if 100000 <= $aa_num < 100000000 with visit_t.valu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '100000 <= $aa_num < 100000000', 'with': "visit_t = add name by ('今日访问量(万)')"}
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
		add_the_error('[time_zdy.fbi]执行第[110]原语 if 100000 <= $aa_num < 100000000 with visit_t = ad... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 100000000', 'with': 'visit_t.value = lambda value by (x:round(x/100000000,2))'}
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
		add_the_error('[time_zdy.fbi]执行第[111]原语 if $aa_num >= 100000000 with visit_t.value = lambd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 100000000', 'with': "visit_t = add name by ('今日访问量(亿)')"}
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
		add_the_error('[time_zdy.fbi]执行第[112]原语 if $aa_num >= 100000000 with visit_t = add name by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_t', 'Action': 'add', 'add': 'icon', 'by': "'F171'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[113]原语 visit_t = add icon by ("F171") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit_t', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[114]原语 visit_t = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_t', 'Action': 'loc', 'loc': 't_visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[116]原语 flow_t = loc t_visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_t', 'as': "'flow':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[117]原语 rename flow_t as ("flow":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'flow_t', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[118]原语 aa_num = eval flow_t by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 1024', 'with': "flow_t = add name by ('今日流量(B)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=119
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[119]原语 if $aa_num <= 1024 with flow_t = add name by ("今日流... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': 'flow_t.value = lambda value by (x:round(x/1024,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=120
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[120]原语 if 1024 < $aa_num <= 1048576 with flow_t.value = l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 < $aa_num <= 1048576', 'with': "flow_t = add name by ('今日流量(k)')"}
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
		add_the_error('[time_zdy.fbi]执行第[121]原语 if 1024 < $aa_num <= 1048576 with flow_t = add nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': 'flow_t.value = lambda value by (x:round(x/1048576,2))'}
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
		add_the_error('[time_zdy.fbi]执行第[122]原语 if 1048576 < $aa_num <= 1073741824 with flow_t.val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 < $aa_num <= 1073741824', 'with': "flow_t = add name by ('今日流量(M)')"}
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
		add_the_error('[time_zdy.fbi]执行第[123]原语 if 1048576 < $aa_num <= 1073741824 with flow_t = a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': 'flow_t.value = lambda value by (x:round(x/1073741824,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=124
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[124]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 < $aa_num <= 10995116277760', 'with': "flow_t = add name by ('今日流量(G)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=125
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[125]原语 if 1073741824 < $aa_num <= 10995116277760 with flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': 'flow_t.value = lambda value by (x:round(x/1099511627776,2))'}
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
		add_the_error('[time_zdy.fbi]执行第[126]原语 if $aa_num > 10995116277760 with flow_t.value = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 10995116277760', 'with': "flow_t = add name by ('今日流量(T)')"}
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
		add_the_error('[time_zdy.fbi]执行第[127]原语 if $aa_num > 10995116277760 with flow_t = add name... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_t', 'Action': 'add', 'add': 'icon', 'by': "'F172'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[128]原语 flow_t = add icon by ("F172") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_t', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[129]原语 flow_t = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tj', 'Action': 'union', 'union': 'visit_1,flow,visit_m,flow_m,visit_t,flow_t'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[131]原语 tj = union visit_1,flow,visit_m,flow_m,visit_t,flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tj', 'Action': 'loc', 'loc': 'tj', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[132]原语 tj = loc tj by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'tj', 'as': 'visit_days:tj_zdy_自定义时间'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[135]原语 push tj as visit_days:tj_zdy_自定义时间 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[time_zdy.fbi]执行第[138]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],138

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



