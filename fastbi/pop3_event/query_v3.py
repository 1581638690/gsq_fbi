#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: pop3_event/query
#datetime: 2024-08-30T16:10:57.538073
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
		add_the_error('[pop3_event/query.fea]执行第[11]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[12]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'order_by', 'by': "'timestamp desc'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[13]原语 a = add order_by by ("timestamp desc") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sql_df', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.get_sql', 'with': '@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[14]原语 sql_df = @udf a by CRUD.get_sql with (@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sql_str', 'Action': 'eval', 'eval': 'sql_df', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[15]原语 sql_str= eval sql_df by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'nowq', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': '$sql_str'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[16]原语 nowq=load es by es7 with $sql_str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sql_count', 'Action': 'eval', 'eval': 'sql_df', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[17]原语 sql_count=eval sql_df by (iloc[0,1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': '$sql_count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[18]原语 b2=load es by es7 with $sql_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pd', 'Action': 'eval', 'eval': 'nowq', 'by': 'index.size>0'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[19]原语 pd = eval nowq by index.size>0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'a', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$pd,"""\nnowq.timestamp = lambda timestamp by (x: x[0:23]+"Z")\n"""'}
	ss = ptree['with'].split('\n')
	ss0 = deal_sdf(workspace,ss[0])
	ss1 = deal_sdf(workspace,ss[-1])
	ptree['with'] = '%s\n%s\n%s\n'%(ss0,'\n'.join(ss[1:-1]),ss1)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[20]原语 a = @sdf sys_if_run with ($pd,"nowq.timestamp = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'fix_tname(ptree, "nowq") in global_table', 'as': 'break', 'with': '查询失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[pop3_event/query.fea]执行第[23]原语 assert "fix_tname(ptree, ... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[23]原语 assert "fix_tname(ptree, "nowq") in global_table" ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'nowq', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[24]原语 push nowq as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b2', 'as': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[25]原语 push b2 as count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'type', 'by': '"HTTP事件"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[44]原语 a = add type by ("HTTP事件") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'key:qes:event'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[45]原语 store a to ssdb by ssdb0 with key:qes:event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'con', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'con']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[46]原语 con = eval a by loc[0,"con"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.s_time', 'Action': 'lambda', 'lambda': 'con', 'by': 'x:x[11:21]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[48]原语 a.s_time = lambda con by (x:x[11:21]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.e_time', 'Action': 'lambda', 'lambda': 'con', 'by': 'x:x[51:61]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[49]原语 a.e_time = lambda con by (x:x[51:61]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'s_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[50]原语 s_time = eval a by loc[0,"s_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'e_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'e_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[51]原语 e_time = eval a by loc[0,"e_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_src_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'src_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[54]原语 df_src_base = @udf udf0.new_df with (src_ip,count)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_src', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by src_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[55]原语 df_src = load es by es7 with select * from event* ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_src', 'Action': 'union', 'union': 'df_src,df_src_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[56]原语 df_src = union df_src,df_src_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_src', 'Action': 'limit', 'limit': 'df_src', 'by': '5'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[57]原语 df_src = limit df_src by 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_src', 'Action': 'loc', 'loc': 'df_src', 'by': 'src_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[58]原语 df_src = loc df_src by src_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df_src', 'Action': 'order', 'order': 'df_src', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[59]原语 df_src = order df_src by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_src', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:src'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[60]原语 store df_src to ssdb by ssdb0 with tital_temporary... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_dst_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[63]原语 df_dst_base = @udf udf0.new_df with (dest_ip,count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_dst', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by dest_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[64]原语 df_dst = load es by es7 with select * from event* ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_dst', 'Action': 'union', 'union': 'df_dst,df_dst_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[65]原语 df_dst = union df_dst,df_dst_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_dst', 'Action': 'limit', 'limit': 'df_dst', 'by': '5'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[66]原语 df_dst = limit df_dst by 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_dst', 'Action': 'loc', 'loc': 'df_dst', 'by': 'dest_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[67]原语 df_dst = loc df_dst by dest_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df_dst', 'Action': 'order', 'order': 'df_dst', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[68]原语 df_dst = order df_dst by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_dst', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:dst'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[69]原语 store df_dst to ssdb by ssdb0 with tital_temporary... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_port_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_port,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[72]原语 df_port_base = @udf udf0.new_df with (dest_port,co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_port', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by dest_port'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[73]原语 df_port = load es by es7 with select * from event*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_port', 'Action': 'union', 'union': 'df_port,df_port_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[74]原语 df_port = union df_port,df_port_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_port', 'Action': 'limit', 'limit': 'df_port', 'by': '5'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[75]原语 df_port = limit df_port by 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_port', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:dest_port'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[76]原语 store df_port to ssdb by ssdb0 with tital_temporar... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date_df', 'Action': '@udf', '@udf': 'udf0.new_df_daterange', 'with': '$s_time,$e_time,1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[79]原语 date_df = @udf udf0.new_df_daterange with ($s_time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'date_df', 'Action': 'loc', 'loc': 'date_df', 'by': 'start_day'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[80]原语 date_df = loc date_df by start_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'date_df.start_day', 'Action': 'lambda', 'lambda': 'start_day', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[81]原语 date_df.start_day = lambda start_day by (x:x[5:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_day_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'timestamp,timestamp_string,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[83]原语 df_day_base = @udf udf0.new_df with (timestamp,tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_day', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from event* where $con group by timestamp.date_histogram[{interval:1d}]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[84]原语 df_day = load es by es7 with select count(*) from ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_day', 'Action': 'union', 'union': 'df_day,df_day_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[85]原语 df_day = union df_day,df_day_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df_day.timestamp_string', 'Action': 'lambda', 'lambda': 'timestamp_string', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[86]原语 df_day.timestamp_string = lambda timestamp_string ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df_day', 'Action': 'join', 'join': 'df_day,date_df', 'by': 'timestamp_string,start_day', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[87]原语 df_day = join df_day,date_df by timestamp_string,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_day', 'Action': '@udf', '@udf': 'df_day', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[88]原语 df_day = @udf df_day by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_day', 'Action': 'loc', 'loc': 'df_day', 'by': 'start_day,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[89]原语 df_day = loc df_day by start_day,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_day', 'Action': 'loc', 'loc': 'df_day', 'by': 'start_day', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[90]原语 df_day = loc df_day by start_day to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_day', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:day'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[91]原语 store df_day to ssdb by ssdb0 with tital_temporary... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'event_type', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* group by event_type.keyword'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[95]原语 event_type = load es by es7 with (select * from ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'event_type', 'Action': 'add', 'add': 'value', 'by': 'event_type["event_type"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[96]原语 event_type = add value by (event_type["event_type"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'event_type', 'Action': '@udf', '@udf': 'event_type', 'by': 'udf0.df_set_index', 'with': 'event_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[97]原语 event_type = @udf event_type by udf0.df_set_index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'event_type', 'Action': 'loc', 'loc': 'event_type', 'drop': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[98]原语 event_type = loc event_type drop count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'event_type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:event_type'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[99]原语 store event_type to ssdb by ssdb0 with dd:event_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[pop3_event/query.fea]执行第[102]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],102

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



