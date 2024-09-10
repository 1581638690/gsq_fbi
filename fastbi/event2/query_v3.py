#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: event2/query
#datetime: 2024-08-30T16:10:56.297725
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
		add_the_error('[event2/query.fea]执行第[11]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[12]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'order_by', 'by': "'timestamp desc'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[13]原语 a = add order_by by ("timestamp desc") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'atemp'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[14]原语 store a to ssdb by ssdb0 with atemp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'temp', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'SJGL'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[15]原语 temp=load ssdb by ssdb0 with SJGL 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'temp', 'Action': 'filter', 'filter': 'temp', 'by': "enable==1 and classtype=='alert'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[16]原语 temp=filter temp by enable==1 and classtype=="aler... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('temp',ptree)", 'as': 'exit', 'with': '规则未启用'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[event2/query.fea]执行第[17]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[17]原语 assert find_df_have_data("temp",ptree) as exit wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'temp', 'Action': '@udf', '@udf': 'temp', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[18]原语 temp= @udf temp by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'level10', 'Action': 'eval', 'eval': 'temp', 'by': "get_value(0,'priority')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[19]原语 level10=eval temp by (get_value(0,"priority")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sql00', 'Action': '@udf', '@udf': 'temp', 'by': 'Rule.rule', 'with': 'http'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[20]原语 sql00=@udf temp by Rule.rule with http 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pd', 'Action': 'eval', 'eval': 'sql00', 'by': 'index.size>0'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[22]原语 pd = eval sql00 by index.size>0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'wwer', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$pd,"""\nsqltem=loc sql00 by val\nsqltem=filter sqltem by val!="a"\nsqltem.val = lambda val by (x:x.replace("=","\\="))\nbase_df = @udf udf0.new_df with (_index,_id,timestamp,level,dest_ip,dest_port,http.hostname,http.url,http.http_method,http.status,http.http_refer)\nstore base_df to ssdb by ssdb0 with base_df\nforeach sqltem run ruleLevel.fbi with (@val=$1)\nnowq= load ssdb by ssdb0 with base_df\ntb=eval sql00 by (get_value(0,\'value\'))\na= @udf a by Rule.sql with $tb\nsql_df = @udf a by CRUD.get_sql with (@table)\nsql_count=eval sql_df by (iloc[0,1])\nb2=load es by es7 with $sql_count\nsql_str= eval sql_df by (iloc[0,0])\n"""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
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
		add_the_error('[event2/query.fea]执行第[23]原语 wwer = @sdf sys_if_run with ($pd,"sqltem=loc sql00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'wwer', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$pd,"""\na= @udf a by Rule.sql\na.con = lambda con by (x: x[0:-4])\nsql_df = @udf a by CRUD.get_sql with (@table)\nsql_str= eval sql_df by (iloc[0,0])\nnowq=load es by es7 with $sql_str\nnowq= add level by (\'$level10\')\nsql_count=eval sql_df by (iloc[0,1])\nb2=load es by es7 with $sql_count\n"""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
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
		add_the_error('[event2/query.fea]执行第[38]原语 wwer = @sdf sys_unif_run with ($pd,"a= @udf a by R... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'nowq.timestamp', 'Action': 'lambda', 'lambda': 'timestamp', 'by': 'x: x[0:23]+"Z"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[48]原语 nowq.timestamp = lambda timestamp by (x: x[0:23]+"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'fix_tname(ptree, "nowq") in global_table', 'as': 'break', 'with': '查询失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[event2/query.fea]执行第[49]原语 assert "fix_tname(ptree, ... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[49]原语 assert "fix_tname(ptree, "nowq") in global_table" ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'nowq', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[50]原语 push nowq as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b2', 'as': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[51]原语 push b2 as count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'type', 'by': '"HTTP事件"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[75]原语 a = add type by ("HTTP事件") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'key:qes:event'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[76]原语 store a to ssdb by ssdb0 with key:qes:event 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'con', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'con']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[77]原语 con = eval a by loc[0,"con"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.s_time', 'Action': 'lambda', 'lambda': 'con', 'by': 'x:x[12:22]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[79]原语 a.s_time = lambda con by (x:x[12:22]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.e_time', 'Action': 'lambda', 'lambda': 'con', 'by': 'x:x[52:62]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[80]原语 a.e_time = lambda con by (x:x[52:62]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'s_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[83]原语 s_time = eval a by loc[0,"s_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'e_time', 'Action': 'eval', 'eval': 'a', 'by': "loc[0,'e_time']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[84]原语 e_time = eval a by loc[0,"e_time"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_src_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'src_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[87]原语 df_src_base = @udf udf0.new_df with (src_ip,count)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_src', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by src_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[88]原语 df_src = load es by es7 with select * from event* ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_src', 'Action': 'union', 'union': 'df_src,df_src_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[89]原语 df_src = union df_src,df_src_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_src', 'Action': 'limit', 'limit': 'df_src', 'by': '5'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[90]原语 df_src = limit df_src by 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_src', 'Action': 'loc', 'loc': 'df_src', 'by': 'src_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[91]原语 df_src = loc df_src by src_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df_src', 'Action': 'order', 'order': 'df_src', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[92]原语 df_src = order df_src by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_src', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:src'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[93]原语 store df_src to ssdb by ssdb0 with tital_temporary... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_dst_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_ip,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[96]原语 df_dst_base = @udf udf0.new_df with (dest_ip,count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_dst', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by dest_ip.keyword'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[97]原语 df_dst = load es by es7 with select * from event* ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_dst', 'Action': 'union', 'union': 'df_dst,df_dst_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[98]原语 df_dst = union df_dst,df_dst_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_dst', 'Action': 'limit', 'limit': 'df_dst', 'by': '5'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[99]原语 df_dst = limit df_dst by 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_dst', 'Action': 'loc', 'loc': 'df_dst', 'by': 'dest_ip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[100]原语 df_dst = loc df_dst by dest_ip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'df_dst', 'Action': 'order', 'order': 'df_dst', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[101]原语 df_dst = order df_dst by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_dst', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:dst'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[102]原语 store df_dst to ssdb by ssdb0 with tital_temporary... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_port_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'dest_port,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[105]原语 df_port_base = @udf udf0.new_df with (dest_port,co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_port', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* where $con group by dest_port'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[106]原语 df_port = load es by es7 with select * from event*... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_port', 'Action': 'union', 'union': 'df_port,df_port_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[107]原语 df_port = union df_port,df_port_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_port', 'Action': 'limit', 'limit': 'df_port', 'by': '5'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[108]原语 df_port = limit df_port by 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_port', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:dest_port'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[109]原语 store df_port to ssdb by ssdb0 with tital_temporar... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'date_df', 'Action': '@udf', '@udf': 'udf0.new_df_daterange', 'with': '$s_time,$e_time,1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[112]原语 date_df = @udf udf0.new_df_daterange with ($s_time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'date_df', 'Action': 'loc', 'loc': 'date_df', 'by': 'start_day'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[113]原语 date_df = loc date_df by start_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'date_df.start_day', 'Action': 'lambda', 'lambda': 'start_day', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[114]原语 date_df.start_day = lambda start_day by (x:x[5:10]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_day_base', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'timestamp,timestamp_string,count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[116]原语 df_day_base = @udf udf0.new_df with (timestamp,tim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_day', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select count(*) from event* where $con group by timestamp.date_histogram[{interval:1d}]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[117]原语 df_day = load es by es7 with select count(*) from ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_day', 'Action': 'union', 'union': 'df_day,df_day_base'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[118]原语 df_day = union df_day,df_day_base 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df_day.timestamp_string', 'Action': 'lambda', 'lambda': 'timestamp_string', 'by': 'x:x[5:10]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[119]原语 df_day.timestamp_string = lambda timestamp_string ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df_day', 'Action': 'join', 'join': 'df_day,date_df', 'by': 'timestamp_string,start_day', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[120]原语 df_day = join df_day,date_df by timestamp_string,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_day', 'Action': '@udf', '@udf': 'df_day', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[121]原语 df_day = @udf df_day by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_day', 'Action': 'loc', 'loc': 'df_day', 'by': 'start_day,count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[122]原语 df_day = loc df_day by start_day,count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_day', 'Action': 'loc', 'loc': 'df_day', 'by': 'start_day', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[123]原语 df_day = loc df_day by start_day to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_day', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'tital_temporary:day'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[124]原语 store df_day to ssdb by ssdb0 with tital_temporary... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'event_type', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': 'select * from event* group by event_type.keyword'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[128]原语 event_type = load es by es7 with (select * from ev... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'event_type', 'Action': 'add', 'add': 'value', 'by': 'event_type["event_type"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[129]原语 event_type = add value by (event_type["event_type"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'event_type', 'Action': '@udf', '@udf': 'event_type', 'by': 'udf0.df_set_index', 'with': 'event_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[130]原语 event_type = @udf event_type by udf0.df_set_index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'event_type', 'Action': 'loc', 'loc': 'event_type', 'drop': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[131]原语 event_type = loc event_type drop count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'event_type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:event_type'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[132]原语 store event_type to ssdb by ssdb0 with dd:event_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[event2/query.fea]执行第[135]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],135

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



