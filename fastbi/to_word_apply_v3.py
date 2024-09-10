#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: to_word_apply
#datetime: 2024-08-30T16:10:53.787209
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
		add_the_error('[to_word_apply.fea]执行第[6]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'base_df', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'key:qes:event'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[8]原语 base_df = load ssdb by ssdb0 with key:qes:event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'con', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(0,"con")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[9]原语 con = eval base_df by get_value(0,"con") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(0,"type")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[10]原语 type = eval base_df by get_value(0,"type") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'base_df.stimez', 'Action': 'lambda', 'lambda': 'con', 'by': 'x:x[11:35]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[11]原语 base_df.stimez = lambda con by (x:x[11:35]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'base_df.etimez', 'Action': 'lambda', 'lambda': 'con', 'by': 'x:x[51:76]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[12]原语 base_df.etimez = lambda con by (x:x[51:76]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'stimez', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(0,"stimez")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[13]原语 stimez = eval base_df by get_value(0,"stimez") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'etimez', 'Action': 'eval', 'eval': 'base_df', 'by': 'get_value(0,"etimez")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[14]原语 etimez = eval base_df by get_value(0,"etimez") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'stime', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$stimez, x:x.replace("T"," ").replace(".000Z","")'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[16]原语 stime = @sdf sys_lambda with ($stimez, x:x.replace... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'etime', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$etimez, x:x.replace("T"," ").replace(".999Z","")'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[17]原语 etime = @sdf sys_lambda with ($etimez, x:x.replace... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[19]原语 date = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[to_word_apply.fea]执行第[20]原语 date = @sdf format_now with ($date,"%Y-%m-%d %H:%M... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user_name', 'Action': '@udf', '@udf': 'udfA.get_user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[22]原语 user_name = @udf udfA.get_user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'user_names', 'Action': 'eval', 'eval': 'user_name', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[23]原语 user_names = eval user_name by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'name', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$date,x:"$type_"+x[0:10]+\'_\'+x[11:23]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[25]原语 name = @sdf sys_lambda with ($date,x:"$type_"+x[0:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[to_word_apply.fea]执行第[26]原语 name_all = @sdf sys_lambda with ($name,x:x+".docx"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'table', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'user,filename,starttime,endtime,filenotes,formtime,status'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[30]原语 table = @udf udf0.new_df with (user,filename,start... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'table', 'Action': '@udf', '@udf': 'table', 'by': 'udf0.df_append', 'with': '$user_names,$name_all,$stime,$etime,$type,$date,生成中'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[31]原语 table = @udf table by udf0.df_append with ($user_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'save', 'Action': '@udf', '@udf': 'table', 'by': 'CRUD.save_table', 'with': 'mysql4,pot_words'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[32]原语 save = @udf table by CRUD.save_table with (mysql4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df1', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from event* where $con'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[36]原语 df1 = load es by es7 with select count(*) from eve... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'stime', 'by': "'$stime'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[37]原语 df1 = add stime by ("$stime") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df1', 'Action': 'add', 'add': 'etime', 'by': "'$etime'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[38]原语 df1 = add etime by ("$etime") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'event_type,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[41]原语 df2_base = @udf udf0.new_df with (event_type,count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df2', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by event_type.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[42]原语 df2 = load es by es7 with select * from event* whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df2', 'Action': 'union', 'union': 'df2_base,df2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[43]原语 df2 = union df2_base,df2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df7_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'src_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[47]原语 df7_base = @udf udf0.new_df with (src_ip,count) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df7', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by src_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[48]原语 df7 = load es by es7 with select * from event* whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df7', 'Action': 'union', 'union': 'df7_base,df7'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[49]原语 df7 = union df7_base,df7 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df7', 'Action': 'limit', 'limit': 'df7', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[50]原语 df7 = limit df7 by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df3', 'Action': 'loc', 'loc': 'df7', 'by': 'src_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[51]原语 df3 = loc df7 by src_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df3', 'Action': 'order', 'order': 'df3', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[52]原语 df3 = order df3 by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df8_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[55]原语 df8_base = @udf udf0.new_df with (dest_ip,count) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df8', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by dest_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[56]原语 df8 = load es by es7 with select * from event* whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df8', 'Action': 'union', 'union': 'df8_base,df8'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[57]原语 df8 = union df8_base,df8 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df8', 'Action': 'limit', 'limit': 'df8', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[58]原语 df8 = limit df8 by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df4', 'Action': 'loc', 'loc': 'df8', 'by': 'dest_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[59]原语 df4 = loc df8 by dest_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df4', 'Action': 'order', 'order': 'df4', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[60]原语 df4 = order df4 by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df9_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'src_ip,dest_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[63]原语 df9_base = @udf udf0.new_df with (src_ip,dest_ip,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df9', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by src_ip.keyword,dest_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[64]原语 df9 = load es by es7 with select * from event* whe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df9', 'Action': 'union', 'union': 'df9_base,df9'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[65]原语 df9 = union df9_base,df9 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df9', 'Action': '@udf', '@udf': 'df9', 'by': 'udf0.df_row_lambda', 'with': "x: x['src_ip'] if x['dest_ip']>x['src_ip'] else x['dest_ip'] "}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[66]原语 df9 = @udf df9 by udf0.df_row_lambda with (x: x["s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df9', 'as': '"lambda1":"src"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[67]原语 rename df9 as ("lambda1":"src") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df9', 'Action': '@udf', '@udf': 'df9', 'by': 'udf0.df_row_lambda', 'with': "x: x['src_ip'] if x['src']==x['dest_ip'] else x['dest_ip'] "}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[68]原语 df9 = @udf df9 by udf0.df_row_lambda with (x: x["s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df9', 'as': '"lambda1":"dst"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[69]原语 rename df9 as ("lambda1":"dst") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'df9', 'Action': 'group', 'group': 'df9', 'by': 'src,dst', 'agg': 'count:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[70]原语 df9 = group df9 by src,dst agg count:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df9', 'Action': 'order', 'order': 'df9', 'by': 'count_sum', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[71]原语 df9 = order df9 by count_sum with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df9', 'Action': '@udf', '@udf': 'df9', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[72]原语 df9 = @udf df9 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df9', 'Action': 'limit', 'limit': 'df9', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[73]原语 df9 = limit df9 by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_time_event', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[76]原语 store df1 to ssdb by ssdb0 with pot_baobiao_time_e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_event_type_event', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[77]原语 store df2 to ssdb by ssdb0 with pot_baobiao_event_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_proto_event3', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[78]原语 store df3 to ssdb by ssdb0 with pot_baobiao_proto_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df4', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_all_timer_event4', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[79]原语 store df4 to ssdb by ssdb0 with pot_baobiao_all_ti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df7', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_src_ip_event', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[82]原语 store df7 to ssdb by ssdb0 with pot_baobiao_src_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df8', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_dest_ip_event', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[83]原语 store df8 to ssdb by ssdb0 with pot_baobiao_dest_i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df9', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_baobiao_src_dst_ip_event', 'as': '3000'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[84]原语 store df9 to ssdb by ssdb0 with pot_baobiao_src_ds... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'pics_dataevent_word'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[88]原语 data = load ssdb by ssdb0 with pics_dataevent_word... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'x', 'Action': '@udf', '@udf': 'data', 'by': 'doc.generate_pic', 'with': 'event_word'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[90]原语 x = @udf data by doc.generate_pic with event_word 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'report_status', 'Action': '@udf', '@udf': 'data', 'by': 'doc.modifiy_doc', 'with': 'event_word,baseevent_word,title_dataevent_word,table_dataevent_word,$name'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[93]原语 report_status = @udf data by doc.modifiy_doc with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pstatus', 'Action': 'eval', 'eval': 'report_status', 'by': 'get_value(0,"status")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[94]原语 pstatus = eval report_status by (get_value(0,"stat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'to_html', 'Action': '@udf', '@udf': 'udfG.word2pdf', 'with': 'report/$name.docx'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[97]原语 to_html = @udf udfG.word2pdf with report/$name.doc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'mysql_df', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql4 ,select * from pot_words where filename='$name_all'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[101]原语 mysql_df = @udf RS.load_mysql_sql with (mysql4 ,se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mysql_df', 'Action': 'loc', 'loc': 'mysql_df', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[102]原语 mysql_df = loc mysql_df by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'mysql_df', 'Action': 'loc', 'loc': 'mysql_df', 'by': 'drop', 'drop': 'gmt_create,gmt_modified'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[103]原语 mysql_df = loc mysql_df by drop (gmt_create,gmt_mo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.status', 'Action': 'lambda', 'lambda': 'status', 'by': 'x:$pstatus'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[104]原语 mysql_df.status = lambda status by (x:$pstatus) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.status', 'Action': 'lambda', 'lambda': 'status', 'by': "x:'成功' if x==1 else '失败'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[105]原语 mysql_df.status = lambda status by (x:"成功" if x==1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.formtime', 'Action': 'lambda', 'lambda': 'formtime', 'by': "x:str(x)[0:10]+' '+str(x)[11:23]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[106]原语 mysql_df.formtime = lambda formtime by (x:str(x)[0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.starttime', 'Action': 'lambda', 'lambda': 'starttime', 'by': "x:str(x)[0:10]+' '+str(x)[11:23]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[107]原语 mysql_df.starttime = lambda starttime by (x:str(x)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'mysql_df.endtime', 'Action': 'lambda', 'lambda': 'endtime', 'by': "x:str(x)[0:10]+' '+str(x)[11:23]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[108]原语 mysql_df.endtime = lambda endtime by (x:str(x)[0:1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'x', 'Action': '@udf', '@udf': 'mysql_df', 'by': 'CRUD.save_table', 'with': 'mysql4,pot_words'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[109]原语 x = @udf mysql_df by CRUD.save_table with (mysql4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[to_word_apply.fea]执行第[112]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],112

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



