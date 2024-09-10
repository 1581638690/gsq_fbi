#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: wordtpl_remrGO/make_tpl
#datetime: 2024-08-30T16:10:58.650789
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
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[6]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'base_df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'baseremrGO'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[8]原语 base_df = load ssdb by ssdb0 with baseremrGO 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stime', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(0,"value")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[9]原语 stime = eval base_df by get_value(0,"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'etime', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(1,"value")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[10]原语 etime = eval base_df by get_value(1,"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'filenotes', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(5,"value").strip()'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[11]原语 filenotes = eval base_df by get_value(5,"value").s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'stimez', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$stime, x:x.replace(" ","T")+".000000"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[13]原语 stimez = @sdf sys_lambda with ($stime, x:x.replace... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'etimez', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$etime, x:x.replace(" ","T")+".000000"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[14]原语 etimez = @sdf sys_lambda with ($etime, x:x.replace... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'src_df', 'Action': 'filter', 'filter': 'base_df', 'by': 'name=="src"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[17]原语 src_df = filter base_df by name=="src" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dst_df', 'Action': 'filter', 'filter': 'base_df', 'by': 'name=="dst"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[18]原语 dst_df = filter base_df by name=="dst" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'event_df', 'Action': 'filter', 'filter': 'base_df', 'by': 'name=="event_type"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[19]原语 event_df = filter base_df by name=="event_type" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'src_df.new', 'Action': 'lambda', 'lambda': 'value', 'by': 'x:"and src_ip in ("+x.strip()+")" if x.strip()!="" else ""'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[21]原语 src_df.new = lambda value by (x:"and src_ip in ("+... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dst_df.new', 'Action': 'lambda', 'lambda': 'value', 'by': 'x:"and dest_ip in ("+x.strip()+")" if x.strip()!="" else ""'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[22]原语 dst_df.new = lambda value by (x:"and dest_ip in ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'event_df.new', 'Action': 'lambda', 'lambda': 'value', 'by': 'x:"and event_type in ("+x.strip()+")" if x.strip()!="" else "and event_type in (dns,http,alert,ftp,pop3,smtp,telnet)"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[23]原语 event_df.new = lambda value by (x:"and event_type ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'src_new', 'Action': 'eval', 'eval': 'src_df', 'by': 'get_value(2,"new")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[25]原语 src_new = eval src_df by get_value(2,"new") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dst_new', 'Action': 'eval', 'eval': 'dst_df', 'by': 'get_value(3,"new")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[26]原语 dst_new = eval dst_df by get_value(3,"new") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'event_type_new', 'Action': 'eval', 'eval': 'event_df', 'by': 'get_value(4,"new")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[27]原语 event_type_new = eval event_df by get_value(4,"new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[30]原语 date = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$date,"%Y-%m-%d %H:%M:%S"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[31]原语 date = @sdf format_now with ($date,"%Y-%m-%d %H:%M... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user_name', 'Action': '@udf', '@udf': 'udfA.get_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[33]原语 user_name = @udf udfA.get_user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'user_names', 'Action': 'eval', 'eval': 'user_name', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[34]原语 user_names = eval user_name by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'name', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$date,x:"综合报告_"+x[0:10]+\'_\'+x[11:23]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[36]原语 name = @sdf sys_lambda with ($date,x:"综合报告_"+x[0:1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'name_all', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$name,x:x+".docx"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[37]原语 name_all = @sdf sys_lambda with ($name,x:x+".docx"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'table', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'user,filename,starttime,endtime,filenotes,formtime,status'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[41]原语 table = @udf udf0.new_df with (user,filename,start... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'table', 'Action': '@udf', '@udf': 'table', 'by': 'udf0.df_append', 'with': '$user_names,$name_all,$stime,$etime,$filenotes,$date,生成中'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[42]原语 table = @udf table by udf0.df_append with ($user_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'save', 'Action': '@udf', '@udf': 'table', 'by': 'CRUD.save_table', 'with': 'mysql4,pot_words'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[43]原语 save = @udf table by CRUD.save_table with (mysql4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[47]原语 df1 = load es by es7 with select count(*) from eve... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'stime', 'by': "'$stime'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[48]原语 df1 = add stime by ("$stime") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'etime', 'by': "'$etime'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[49]原语 df1 = add etime by ("$etime") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'event_type,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[52]原语 df2_base = @udf udf0.new_df with (event_type,count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new group by event_type.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[53]原语 df2 = load es by es7 with select * from event* whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df2', 'Action': 'union', 'union': 'df2_base,df2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[54]原语 df2 = union df2_base,df2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'f_stime', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': ' $stime,x :(x[0:10]) '}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[58]原语 f_stime = @sdf sys_lambda with ( $stime,x :(x[0:10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'f_etime', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': ' $etime,x :(x[0:10]) '}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[59]原语 f_etime = @sdf sys_lambda with ( $etime,x :(x[0:10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date_df', 'Action': '@udf', '@udf': 'udf0.new_df_daterange', 'with': '$f_stime,$f_etime,1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[60]原语 date_df = @udf udf0.new_df_daterange with ($f_stim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'date_df', 'Action': 'loc', 'loc': 'date_df', 'by': 'start_day'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[61]原语 date_df = loc date_df by start_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'date_df.start_day', 'Action': 'lambda', 'lambda': 'start_day', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[62]原语 date_df.start_day = lambda start_day by (x:x[5:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_day_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'timestamp,timestamp_string,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[64]原语 df_day_base = @udf udf0.new_df with (timestamp,tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df3', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new group by timestamp.date_histogram[{interval:1d}]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[65]原语 df3 = load es by es7 with select count(*) from eve... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df3', 'Action': 'union', 'union': 'df_day_base,df3'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[66]原语 df3 = union df_day_base,df3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df3', 'Action': 'filter', 'filter': 'df3', 'by': 'timestamp_string notnull'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[67]原语 df3 = filter df3 by timestamp_string notnull 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df3.timestamp_string', 'Action': 'lambda', 'lambda': 'timestamp_string', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[68]原语 df3.timestamp_string = lambda timestamp_string by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'date_df,df3', 'by': 'start_day,timestamp_string', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[69]原语 df3 = join date_df,df3 by start_day,timestamp_stri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[70]原语 df3 = @udf df3 by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'by': 'start_day,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[71]原语 df3 = loc df3 by start_day,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df3', 'by': 'start_day', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[72]原语 df3 = loc df3 by start_day to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:event_type_more'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[74]原语 df = load ssdb by ssdb0 with dd:event_type_more 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df', 'Action': 'loc', 'loc': 'df', 'by': 'index', 'to': 'event_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[75]原语 df = loc df by index to event_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df', 'Action': 'loc', 'loc': 'df', 'by': 'event_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[76]原语 df = loc df by event_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df4_1_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'src_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[80]原语 df4_1_base = @udf udf0.new_df with (src_ip,count) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df4_1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new group by src_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[81]原语 df4_1 = load es by es7 with select * from event* w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df4_1', 'Action': 'union', 'union': 'df4_1_base,df4_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[82]原语 df4_1 = union df4_1_base,df4_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df4_1', 'Action': 'limit', 'limit': 'df4_1', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[83]原语 df4_1 = limit df4_1 by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df4_1', 'as': '"count":"sum"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[84]原语 rename df4_1 as ("count":"sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df4_2_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'src_ip,event_type,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[86]原语 df4_2_base = @udf udf0.new_df with (src_ip,event_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df4_2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new group by src_ip.keyword,event_type.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[87]原语 df4_2 = load es by es7 with select * from event* w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df4_2', 'Action': 'union', 'union': 'df4_2_base,df4_2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[88]原语 df4_2 = union df4_2_base,df4_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df4_2', 'Action': 'join', 'join': 'df4_1,df4_2', 'by': 'src_ip,src_ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[89]原语 df4_2 = join df4_1,df4_2 by src_ip,src_ip with lef... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df4_2', 'Action': 'loc', 'loc': 'df4_2', 'by': 'drop', 'drop': 'sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[90]原语 df4_2 = loc df4_2 by drop sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df4', 'Action': '@udf', '@udf': 'df4_2', 'by': 'udfG.df_group_mxn', 'with': 'src_ip,event_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[91]原语 df4 = @udf df4_2 by udfG.df_group_mxn with src_ip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df4', 'Action': '@udf', '@udf': 'df4', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[92]原语 df4 = @udf df4 by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df4', 'Action': 'loc', 'loc': 'df4', 'by': 'index', 'to': 'src_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[93]原语 df4 = loc df4 by index to src_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df4', 'Action': 'join', 'join': 'df4_1,df4', 'by': 'src_ip,src_ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[94]原语 df4 = join df4_1,df4 by src_ip,src_ip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df4', 'Action': 'loc', 'loc': 'df4', 'by': 'src_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[95]原语 df4 = loc df4 by src_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df4', 'as': '"count_http":"HTTP","count_alert":"ALERT","count_ftp":"FTP","count_pop3":"POP3","count_smtp":"SMTP","count_telnet":"TELNET","count_dns":"DNS"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[96]原语 rename df4 as ("count_http":"HTTP","count_alert":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df5', 'Action': 'join', 'join': 'df,df4_2', 'by': 'event_type,event_type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[99]原语 df5 = join df,df4_2 by event_type,event_type with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df5', 'Action': '@udf', '@udf': 'df5', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[100]原语 df5 = @udf df5 by udf0.df_fillna with () 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df5', 'Action': '@udf', '@udf': 'df5', 'by': 'udfG.df_group_mxn', 'with': 'src_ip,event_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[101]原语 df5 = @udf df5 by udfG.df_group_mxn with src_ip,ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df5', 'Action': '@udf', '@udf': 'df5', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[102]原语 df5 = @udf df5 by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df5', 'Action': 'filter', 'filter': 'df5', 'by': 'index!=""'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[103]原语 df5 = filter df5 by index!="" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df5', 'Action': 'loc', 'loc': 'df5', 'by': 'index', 'to': 'src_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[104]原语 df5 = loc df5 by index to src_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df5', 'Action': 'join', 'join': 'df4_1,df5', 'by': 'src_ip,src_ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[105]原语 df5 = join df4_1,df5 by src_ip,src_ip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'df5.count_ftp.count_pop3.count_smtp.count_alert.count_telnet.count_dns.count_http.sum', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[106]原语 alter df5.count_ftp.count_pop3.count_smtp.count_al... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'df5.count_ftp.count_pop3.count_smtp.count_alert.count_telnet.count_dns.count_http.sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[107]原语 alter df5.count_ftp.count_pop3.count_smtp.count_al... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df6_1_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[110]原语 df6_1_base = @udf udf0.new_df with (dest_ip,count)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df6_1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new group by dest_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[111]原语 df6_1 = load es by es7 with select * from event* w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df6_1', 'Action': 'union', 'union': 'df6_1_base,df6_1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[112]原语 df6_1 = union df6_1_base,df6_1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df6_1', 'Action': 'limit', 'limit': 'df6_1', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[113]原语 df6_1 = limit df6_1 by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df6_1', 'as': '"count":"sum"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[114]原语 rename df6_1 as ("count":"sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df6_2_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_ip,event_type,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[116]原语 df6_2_base = @udf udf0.new_df with (dest_ip,event_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df6_2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where timestamp>$stimez and timestamp<$etimez $src_new $dst_new $event_type_new group by dest_ip.keyword,event_type.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[117]原语 df6_2 = load es by es7 with select * from event* w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df6_2', 'Action': 'union', 'union': 'df6_2_base,df6_2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[118]原语 df6_2 = union df6_2_base,df6_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df6_2', 'Action': 'join', 'join': 'df6_1,df6_2', 'by': 'dest_ip,dest_ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[119]原语 df6_2 = join df6_1,df6_2 by dest_ip,dest_ip with l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df6_2', 'Action': 'loc', 'loc': 'df6_2', 'by': 'drop', 'drop': 'sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[120]原语 df6_2 = loc df6_2 by drop sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df6', 'Action': '@udf', '@udf': 'df6_2', 'by': 'udfG.df_group_mxn', 'with': 'dest_ip,event_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[121]原语 df6 = @udf df6_2 by udfG.df_group_mxn with dest_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df6', 'Action': '@udf', '@udf': 'df6', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[122]原语 df6 = @udf df6 by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df6', 'Action': 'loc', 'loc': 'df6', 'by': 'index', 'to': 'dest_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[123]原语 df6 = loc df6 by index to dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df6', 'Action': 'join', 'join': 'df6_1,df6', 'by': 'dest_ip,dest_ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[124]原语 df6 = join df6_1,df6 by dest_ip,dest_ip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df6', 'Action': 'loc', 'loc': 'df6', 'by': 'dest_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[125]原语 df6 = loc df6 by dest_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df6', 'as': '"count_http":"HTTP","count_alert":"ALERT","count_ftp":"FTP","count_pop3":"POP3","count_smtp":"SMTP","count_telnet":"TELNET","count_dns":"DNS"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[126]原语 rename df6 as ("count_http":"HTTP","count_alert":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df7', 'Action': 'join', 'join': 'df,df6_2', 'by': 'event_type,event_type', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[129]原语 df7 = join df,df6_2 by event_type,event_type with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df7', 'Action': '@udf', '@udf': 'df7', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[130]原语 df7 = @udf df7 by udf0.df_fillna with () 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df7', 'Action': '@udf', '@udf': 'df7', 'by': 'udfG.df_group_mxn', 'with': 'dest_ip,event_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[131]原语 df7 = @udf df7 by udfG.df_group_mxn with dest_ip,e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df7', 'Action': '@udf', '@udf': 'df7', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[132]原语 df7 = @udf df7 by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df7', 'Action': 'filter', 'filter': 'df7', 'by': 'index!=""'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[133]原语 df7 = filter df7 by index!="" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df7', 'Action': 'loc', 'loc': 'df7', 'by': 'index', 'to': 'dest_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[134]原语 df7 = loc df7 by index to dest_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df7', 'Action': 'join', 'join': 'df6_1,df7', 'by': 'dest_ip,dest_ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[135]原语 df7 = join df6_1,df7 by dest_ip,dest_ip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'df7.count_ftp.count_pop3.count_smtp.count_alert.count_telnet.count_dns.count_http.sum', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[136]原语 alter df7.count_ftp.count_pop3.count_smtp.count_al... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'df7.count_ftp.count_pop3.count_smtp.count_alert.count_telnet.count_dns.count_http.sum', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[137]原语 alter df7.count_ftp.count_pop3.count_smtp.count_al... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_time', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[141]原语 store df1 to ssdb by ssdb0 with pot_baobiao_time a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_event_type', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[142]原语 store df2 to ssdb by ssdb0 with pot_baobiao_event_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_all_timer', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[143]原语 store df3 to ssdb by ssdb0 with pot_baobiao_all_ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df4', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_src_bar', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[144]原语 store df4 to ssdb by ssdb0 with pot_baobiao_src_ba... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df5', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_src_ip', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[145]原语 store df5 to ssdb by ssdb0 with pot_baobiao_src_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df6', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_dest_bar', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[146]原语 store df6 to ssdb by ssdb0 with pot_baobiao_dest_b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df7', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_dest_ip', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[147]原语 store df7 to ssdb by ssdb0 with pot_baobiao_dest_i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'pics_dataremrGO'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[151]原语 data = load ssdb by ssdb0 with pics_dataremrGO 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'x', 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': 'remrGO'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[153]原语 x = @udf data by doc.generate_pic with remrGO 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'report_status', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': '@id,@base,@var_data,@tbs_data,$name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[155]原语 report_status = @udf data by doc.modifiy_doc with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pstatus', 'Action': 'eval', 'eval': 'report_status', 'by': 'get_value(0,"status")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[156]原语 pstatus = eval report_status by (get_value(0,"stat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'to_html', 'Action': '@udf', '@udf': 'udfG.word2pdf', 'with': 'report/$name.docx'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[159]原语 to_html = @udf udfG.word2pdf with report/$name.doc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'mysql_df', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql4 ,select * from pot_words where filename='$name_all'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[163]原语 mysql_df = @udf RS.load_mysql_sql with (mysql4 ,se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mysql_df', 'Action': 'loc', 'loc': 'mysql_df', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[164]原语 mysql_df = loc mysql_df by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mysql_df', 'Action': 'loc', 'loc': 'mysql_df', 'by': 'drop', 'drop': 'gmt_create,gmt_modified'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[165]原语 mysql_df = loc mysql_df by drop (gmt_create,gmt_mo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.status', 'Action': 'lambda', 'lambda': 'status', 'by': 'x:$pstatus'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[166]原语 mysql_df.status = lambda status by (x:$pstatus) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.status', 'Action': 'lambda', 'lambda': 'status', 'by': "x:'成功' if x==1 else '失败'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[167]原语 mysql_df.status = lambda status by (x:"成功" if x==1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.formtime', 'Action': 'lambda', 'lambda': 'formtime', 'by': "x:str(x)[0:10]+' '+str(x)[11:23]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[168]原语 mysql_df.formtime = lambda formtime by (x:str(x)[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.starttime', 'Action': 'lambda', 'lambda': 'starttime', 'by': "x:str(x)[0:10]+' '+str(x)[11:23]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[169]原语 mysql_df.starttime = lambda starttime by (x:str(x)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.endtime', 'Action': 'lambda', 'lambda': 'endtime', 'by': "x:str(x)[0:10]+' '+str(x)[11:23]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[170]原语 mysql_df.endtime = lambda endtime by (x:str(x)[0:1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'x', 'Action': '@udf', '@udf': 'mysql_df', 'by': 'CRUD.save_table', 'with': 'mysql4,pot_words'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[171]原语 x = @udf mysql_df by CRUD.save_table with (mysql4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'mysql_df', 'by': 'df.index.size >0', 'as': 'altert altert', 'to': '报告生成成功，请关闭弹窗。', 'with': '报告生成失败。'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[173]原语 assert mysql_df by df.index.size >0 as altert alte... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[wordtpl_remrGO/make_tpl.fea]执行第[175]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],175

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



