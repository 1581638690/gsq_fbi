#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: data_sensitive_portal
#datetime: 2024-08-30T16:10:53.205543
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
		add_the_error('[data_sensitive_portal.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from sen_http_count limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[15]原语 ccc = load ckh by ckh with select app from sen_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[data_sensitive_portal.fbi]执行第[16]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[16]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_key', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[22]原语 sen_key = load pq by sensitive/sens_data.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'sen_key.index.size == 0', 'with': 'sen_key = @udf udf0.new_df with app,url,src_ip,account,type,key,num'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=23
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[23]原语 if sen_key.index.size == 0 with sen_key = @udf udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sen_key', 'Action': 'group', 'group': 'sen_key', 'by': 'key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[24]原语 sen_key = group sen_key by key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_key', 'Action': '@udf', '@udf': 'sen_key', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[25]原语 sen_key = @udf sen_key by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_key', 'as': "'key':'data','num_sum':'count'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[26]原语 rename sen_key as ("key":"data","num_sum":"count")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[28]原语 label = load ssdb by ssdb0 with dd:reqs_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_key0', 'Action': 'join', 'join': 'label,sen_key', 'by': 'data,data', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[29]原语 sen_key0 = join label,sen_key by data,data with le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_key0', 'Action': '@udf', '@udf': 'sen_key0', 'by': 'udf0.df_fillna_cols', 'with': 'count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[31]原语 sen_key0 = @udf sen_key0 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_key0', 'Action': 'filter', 'filter': 'sen_key0', 'by': "count != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[32]原语 sen_key0 = filter sen_key0 by count != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_key0', 'Action': 'eval', 'eval': 'sen_key0', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[33]原语 sen_key0 = eval sen_key0 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_key1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '敏感数据类型'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[34]原语 sen_key1 = @udf udf0.new_df with 敏感数据类型 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_key1', 'Action': '@udf', '@udf': 'sen_key1', 'by': 'udf0.df_append', 'with': '$sen_key0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[35]原语 sen_key1 = @udf sen_key1 by udf0.df_append with $s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_key1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_keycount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[36]原语 store sen_key1 to ssdb by ssdb0 with data_sensitiv... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_today', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as count from sen_http_count where timestamp > toDate(today())'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[39]原语 sen_today = load ckh by ckh with select count(*) a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ccc', 'Action': 'loc', 'loc': 'sen_today', 'by': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[40]原语 ccc = loc sen_today by count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'eval', 'eval': 'sen_today', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[41]原语 aa = eval sen_today by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$aa > 10000'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[42]原语 aa = @sdf sys_eval with $aa > 10000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$aa,"sen_today.count = lambda count by (x:round(x/10000,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[43]原语 aa = @sdf sys_if_run with ($aa,"sen_today.count = ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_today.count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[44]原语 alter sen_today.count as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$aa,"sen_today.count = lambda count by (x:x+\'万\')"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[45]原语 aa = @sdf sys_if_run with ($aa,"sen_today.count = ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_today', 'by': '"count":"今日发现敏感信息数"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[46]原语 rename sen_today by ("count":"今日发现敏感信息数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_today', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_today'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[47]原语 store sen_today to ssdb by ssdb0 with data_sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:reqs_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[49]原语 label = load ssdb by ssdb0 with dd:reqs_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label', 'as': "'value':'data'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[50]原语 rename label as ("value":"data") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'label', 'Action': 'join', 'join': 'label,sen_key', 'by': 'data,data', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[51]原语 label = join label,sen_key by data,data with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'label', 'Action': '@udf', '@udf': 'label', 'by': 'udf0.df_fillna_cols', 'with': 'count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[53]原语 label = @udf label by udf0.df_fillna_cols with cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'label.详情', 'Action': 'lambda', 'lambda': 'data', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[54]原语 label.详情 = lambda data by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'label1', 'Action': 'filter', 'filter': 'label', 'by': 'count > 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[55]原语 label1 = filter label by count > 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'label1', 'Action': 'loc', 'loc': 'label1', 'by': 'data', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[56]原语 label1 = loc label1 by data to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'label1', 'Action': 'order', 'order': 'label1', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[57]原语 label1 = order label1 by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'label1', 'by': "'count':'敏感类型数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[58]原语 rename label1 by ("count":"敏感类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'label1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_senstive_label'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[59]原语 store label1 to ssdb by ssdb0 with data_senstive_l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive_data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as sens from sen_http_count'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[63]原语 sensitive_data = load ckh by ckh with select count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive_data', 'by': 'sens:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[64]原语 alter sensitive_data by sens:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aaa', 'Action': 'loc', 'loc': 'sensitive_data', 'by': 'sens'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[65]原语 aaa = loc sensitive_data by sens 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'eval', 'eval': 'sensitive_data', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[66]原语 aa = eval sensitive_data by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$aa > 10000'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[67]原语 aa = @sdf sys_eval with $aa > 10000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$aa,"sensitive_data.sens = lambda sens by (x:round(x/10000,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[68]原语 aa = @sdf sys_if_run with ($aa,"sensitive_data.sen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive_data.sens', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[69]原语 alter sensitive_data.sens as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$aa,"sensitive_data.sens = lambda sens by (x:x+\'万\')"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[70]原语 aa = @sdf sys_if_run with ($aa,"sensitive_data.sen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sensitive_data', 'by': "'sens':'应用敏感数据总数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[71]原语 rename sensitive_data by ("sens":"应用敏感数据总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sensitive_data', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[72]原语 store sensitive_data to ssdb by ssdb0 with sens:da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select rekey as data,count(*) as count from datafilter group by rekey'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[75]原语 datafilter = load ckh by ckh with select rekey as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'datafilter', 'by': 'data:str,count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[76]原语 alter datafilter by data:str,count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datafilter', 'Action': '@udf', '@udf': 'datafilter', 'by': 'udf0.df_fillna_cols', 'with': "data:'',count:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[78]原语 datafilter = @udf datafilter by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datafilter1', 'Action': 'loc', 'loc': 'datafilter', 'by': 'count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[79]原语 datafilter1 = loc datafilter by count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'datafilter1', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[80]原语 datafilter1 = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'datafilter1', 'Action': 'group', 'group': 'datafilter1', 'by': 'aa', 'agg': 'count:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[81]原语 datafilter1 = group datafilter1 by aa agg count:su... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'datafilter1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[82]原语 aa_num = eval datafilter1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num == 0', 'with': 'datafilter1 = @udf datafilter1 by udf0.df_append with 0'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=83
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[83]原语 if $aa_num == 0 with datafilter1 = @udf datafilter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datafilter1', 'by': '"count_sum":"敏感文件数据总数"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[84]原语 rename datafilter1 by ("count_sum":"敏感文件数据总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'datafilter1', 'Action': 'add', 'add': 'tips', 'by': '"敏感文件包含敏感信息的总数"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[85]原语 datafilter1 = add tips by ("敏感文件包含敏感信息的总数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datafilter1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'wj:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[86]原语 store datafilter1 to ssdb by ssdb0 with wj:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'datafilter', 'Action': 'filter', 'filter': 'datafilter', 'by': "data != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[90]原语 datafilter = filter datafilter by data != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datafilter.详情', 'Action': 'lambda', 'lambda': 'data', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[91]原语 datafilter.详情 = lambda data by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datafilter', 'Action': 'loc', 'loc': 'datafilter', 'by': 'data', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[92]原语 datafilter = loc datafilter by data to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'datafilter', 'Action': 'order', 'order': 'datafilter', 'by': 'count', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[93]原语 datafilter = order datafilter by count with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datafilter', 'by': "'count':'敏感类型数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[94]原语 rename datafilter by ("count":"敏感类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datafilter', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'datafilter_label'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[95]原语 store datafilter to ssdb by ssdb0 with datafilter_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens1', 'Action': 'eval', 'eval': 'datafilter', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[97]原语 sens1 = eval datafilter by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '敏感文件所含数据类型'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[98]原语 sens = @udf udf0.new_df with 敏感文件所含数据类型 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_append', 'with': '$sens1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[99]原语 sens = @udf sens by udf0.df_append with $sens1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'datafilter_keycount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[100]原语 store sens to ssdb by ssdb0 with datafilter_keycou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_today1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select count(*) as count from datafilter where rekey != '' and toDate(timestamp) > toDate(today()-1)"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[102]原语 sen_today1 = load ckh by ckh with select count(*) ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_today1', 'by': 'count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[103]原语 alter sen_today1 by count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_today1', 'by': '"count":"今日发现敏感文件数"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[104]原语 rename sen_today1 by ("count":"今日发现敏感文件数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_today1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'datafilter_today'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[105]原语 store sen_today1 to ssdb by ssdb0 with datafilter_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_app', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_app.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[112]原语 sens_app = load pq by sensitive/sensitive_app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_app', 'by': 'app:str,url_count:int,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[113]原语 alter sens_app by app:str,url_count:int,srcip_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'sens_app', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[114]原语 num = eval sens_app by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_app', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[115]原语 sens_app = @udf udf0.new_df with value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_app', 'Action': '@udf', '@udf': 'sens_app', 'by': 'udf0.df_append', 'with': '$num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[116]原语 sens_app = @udf sens_app by udf0.df_append with $n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_app', 'Action': 'add', 'add': 'name', 'by': "'敏感应用数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[117]原语 sens_app = add name by ("敏感应用数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_app', 'Action': 'add', 'add': 'details', 'by': "'敏感数据所含敏感应用数量'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[118]原语 sens_app = add details by ("敏感数据所含敏感应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_app', 'Action': 'add', 'add': 'icon', 'by': "'F150'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[119]原语 sens_app = add icon by ("F150") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_api', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_api.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[122]原语 sens_api = load pq by sensitive/sensitive_api.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens_api', 'by': 'url:str,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[123]原语 alter sens_api by url:str,srcip_count:int,account_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'sens_api', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[124]原语 num = eval sens_api by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_api', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[125]原语 sens_api = @udf udf0.new_df with value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_api', 'Action': '@udf', '@udf': 'sens_api', 'by': 'udf0.df_append', 'with': '$num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[126]原语 sens_api = @udf sens_api by udf0.df_append with $n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_api', 'Action': 'add', 'add': 'name', 'by': "'敏感接口数'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[127]原语 sens_api = add name by ("敏感接口数") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_api', 'Action': 'add', 'add': 'details', 'by': "'敏感数据所含敏感接口数量'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[128]原语 sens_api = add details by ("敏感数据所含敏感接口数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_api', 'Action': 'add', 'add': 'icon', 'by': "'F307'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[129]原语 sens_api = add icon by ("F307") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens_1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(*) as value from sen_http_count'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[131]原语 sens_1 = load ckh by ckh with select count(*) as v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'sens_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[132]原语 aa_num = eval sens_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'sens_1.value = lambda value by (x:round(x/10000,2))'}
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
		add_the_error('[data_sensitive_portal.fbi]执行第[133]原语 if $aa_num > 100000 with sens_1.value = lambda val... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "sens_1 = add name by ('敏感数据访问数(万)')"}
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
		add_the_error('[data_sensitive_portal.fbi]执行第[134]原语 if $aa_num > 100000 with sens_1 = add name by ("敏感... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "sens_1 = add name by ('敏感数据访问数')"}
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
		add_the_error('[data_sensitive_portal.fbi]执行第[135]原语 if $aa_num <= 100000 with sens_1 = add name by ("敏... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_1', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[136]原语 sens_1 = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens_1', 'Action': 'add', 'add': 'icon', 'by': "'F209'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[137]原语 sens_1 = add icon by ("F209") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'aaa', 'as': "'sens':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[140]原语 rename aaa as ("sens":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'aaa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[141]原语 aa_num = eval aaa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'aaa.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=142
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[142]原语 if $aa_num > 100000 with aaa.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "aaa = add name by ('应用敏感数据数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=143
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[143]原语 if $aa_num > 100000 with aaa = add name by ("应用敏感数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "aaa = add name by ('应用敏感数据数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=144
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[144]原语 if $aa_num <= 100000 with aaa = add name by ("应用敏感... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'aaa', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[145]原语 aaa = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'aaa', 'Action': 'add', 'add': 'icon', 'by': "'F353'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[146]原语 aaa = add icon by ("F353") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bbb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[148]原语 bbb = @udf udf0.new_df with value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bbb', 'Action': '@udf', '@udf': 'bbb', 'by': 'udf0.df_append', 'with': '$sen_key0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[149]原语 bbb = @udf bbb by udf0.df_append with $sen_key0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'bbb', 'Action': 'add', 'add': 'name', 'by': "'数据敏感类型'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[150]原语 bbb = add name by ("数据敏感类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'bbb', 'Action': 'add', 'add': 'details', 'by': "'应用数据所包含的敏感数据类型'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[151]原语 bbb = add details by ("应用数据所包含的敏感数据类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'bbb', 'Action': 'add', 'add': 'icon', 'by': "'F133'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[152]原语 bbb = add icon by ("F133") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ccc', 'as': "'count':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[155]原语 rename ccc as ("count":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'ccc', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[156]原语 aa_num = eval ccc by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'ccc.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=157
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[157]原语 if $aa_num > 100000 with ccc.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "ccc = add name by ('今日敏感数据数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=158
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[158]原语 if $aa_num > 100000 with ccc = add name by ("今日敏感数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "ccc = add name by ('今日发现敏感数据数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=159
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[159]原语 if $aa_num <= 100000 with ccc = add name by ("今日发现... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ccc', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[160]原语 ccc = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ccc', 'Action': 'add', 'add': 'icon', 'by': "'F457'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[161]原语 ccc = add icon by ("F457") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'datafilter', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select count(distinct src_ip) as value,count(distinct app_proto) as value1,min(timestamp) as time from datafilter'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[163]原语 datafilter = load ckh by ckh with select count(dis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'datafilter1', 'by': '敏感文件数据总数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[183]原语 ddd = loc datafilter1 by 敏感文件数据总数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ddd', 'as': "'敏感文件数据总数':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[184]原语 rename ddd as ("敏感文件数据总数":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'ddd', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[185]原语 aa_num = eval ddd by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'ddd.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=186
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[186]原语 if $aa_num > 100000 with ddd.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "ddd = add name by ('敏感文件数据数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=187
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[187]原语 if $aa_num > 100000 with ddd = add name by ("敏感文件数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "ddd = add name by ('敏感文件数据数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=188
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[188]原语 if $aa_num <= 100000 with ddd = add name by ("敏感文件... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ddd', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[189]原语 ddd = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ddd', 'Action': 'add', 'add': 'icon', 'by': "'F182'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[190]原语 ddd = add icon by ("F182") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'eee', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'value'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[192]原语 eee = @udf udf0.new_df with value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'eee', 'Action': '@udf', '@udf': 'eee', 'by': 'udf0.df_append', 'with': '$sens1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[193]原语 eee = @udf eee by udf0.df_append with $sens1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'eee', 'Action': 'add', 'add': 'name', 'by': "'文件敏感类型'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[194]原语 eee = add name by ("文件敏感类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'eee', 'Action': 'add', 'add': 'details', 'by': "'敏感文件所包含的敏感数据类型'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[195]原语 eee = add details by ("敏感文件所包含的敏感数据类型") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'eee', 'Action': 'add', 'add': 'icon', 'by': "'F203'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[196]原语 eee = add icon by ("F203") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'fff', 'Action': 'loc', 'loc': 'sen_today1', 'by': '今日发现敏感文件数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[198]原语 fff = loc sen_today1 by 今日发现敏感文件数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'fff', 'as': "'今日发现敏感文件数':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[199]原语 rename fff as ("今日发现敏感文件数":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'fff', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[200]原语 aa_num = eval fff by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': 'fff.value = lambda value by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=201
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[201]原语 if $aa_num > 100000 with fff.value = lambda value ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num > 100000', 'with': "fff = add name by ('今日敏感文件数(万)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=202
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[202]原语 if $aa_num > 100000 with fff = add name by ("今日敏感文... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num <= 100000', 'with': "fff = add name by ('今日发现敏感文件数')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=203
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[203]原语 if $aa_num <= 100000 with fff = add name by ("今日发现... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fff', 'Action': 'add', 'add': 'details', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[204]原语 fff = add details by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fff', 'Action': 'add', 'add': 'icon', 'by': "'F360'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[205]原语 fff = add icon by ("F360") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sss', 'Action': 'union', 'union': 'aaa,bbb,ccc,ddd,eee,fff'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[207]原语 sss = union aaa,bbb,ccc,ddd,eee,fff 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sss', 'Action': 'loc', 'loc': 'sss', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[208]原语 sss = loc sss by name,value,icon,details 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sss', 'Action': 'add', 'add': 'pageid', 'by': "'qes:sen_http_count','','','qes:datafilter','',''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[209]原语 sss = add pageid by ("qes:sen_http_count","","","q... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sss', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_sss'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[210]原语 store sss to ssdb by ssdb0 with data_sensitive_sss... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sensitive', 'Action': 'union', 'union': 'sens_app,sens_api,sens_1,aaa,bbb,ccc'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[212]原语 sensitive = union sens_app,sens_api,sens_1,aaa,bbb... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sensitive', 'Action': 'loc', 'loc': 'sensitive', 'by': 'name,value,icon,details'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[214]原语 sensitive = loc sensitive by name,value,icon,detai... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sensitive', 'Action': 'add', 'add': 'pageid', 'by': "'dashboard7:sensitive_app2','dashboard7:sensitive_url2','qes:sen_http_count','qes:sen_http_count','',''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[215]原语 sensitive = add pageid by ("dashboard7:sensitive_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sensitive', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[217]原语 store sensitive to ssdb by ssdb0 with data_sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_app', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_app.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[223]原语 sen_app = load pq by sensitive/sensitive_app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_app', 'by': 'app:str,url_count:int,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[224]原语 alter sen_app by app:str,url_count:int,srcip_count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_app', 'Action': 'loc', 'loc': 'sen_app', 'by': 'app,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[225]原语 sen_app = loc sen_app by app,sensitive_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_app', 'as': "'sensitive_count':'count'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[226]原语 rename sen_app as ("sensitive_count":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_app0', 'Action': 'eval', 'eval': 'sen_app', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[227]原语 sen_app0 = eval sen_app by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_app1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '敏感应用数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[228]原语 sen_app1 = @udf udf0.new_df with 敏感应用数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_app1', 'Action': '@udf', '@udf': 'sen_app1', 'by': 'udf0.df_append', 'with': '$sen_app0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[229]原语 sen_app1 = @udf sen_app1 by udf0.df_append with $s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_app1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_appcount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[230]原语 store sen_app1 to ssdb by ssdb0 with data_sensitiv... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_app', 'Action': 'loc', 'loc': 'sen_app', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[231]原语 sen_app = loc sen_app by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_app', 'Action': 'loc', 'loc': 'sen_app', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[232]原语 sen_app = loc sen_app drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_apptop10', 'Action': 'filter', 'filter': 'sen_app', 'by': 'index <10'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[233]原语 sen_apptop10 = filter sen_app by index <10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_apptop10', 'as': "'app':'应用名','count':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[234]原语 rename sen_apptop10 as ("app":"应用名","count":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_apptop10', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_apptop'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[235]原语 store sen_apptop10 to ssdb by ssdb0 with data_sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_url', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_api.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[240]原语 sen_url = load pq by sensitive/sensitive_api.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_url', 'by': 'url:str,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[241]原语 alter sen_url by url:str,srcip_count:int,account_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_url', 'Action': 'loc', 'loc': 'sen_url', 'by': 'url,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[242]原语 sen_url = loc sen_url by url,sensitive_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_url', 'as': "'sensitive_count':'count'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[243]原语 rename sen_url as ("sensitive_count":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_url0', 'Action': 'eval', 'eval': 'sen_url', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[244]原语 sen_url0 = eval sen_url by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_url1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '敏感接口数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[245]原语 sen_url1 = @udf udf0.new_df with 敏感接口数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_url1', 'Action': '@udf', '@udf': 'sen_url1', 'by': 'udf0.df_append', 'with': '$sen_url0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[246]原语 sen_url1 = @udf sen_url1 by udf0.df_append with $s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_url1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_urlcount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[247]原语 store sen_url1 to ssdb by ssdb0 with data_sensitiv... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_url', 'Action': 'loc', 'loc': 'sen_url', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[248]原语 sen_url = loc sen_url by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_url', 'Action': 'loc', 'loc': 'sen_url', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[249]原语 sen_url = loc sen_url drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_urltop10', 'Action': 'filter', 'filter': 'sen_url', 'by': 'index <10'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[250]原语 sen_urltop10 = filter sen_url by index <10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_urltop10', 'as': "'url':'接口','count':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[251]原语 rename sen_urltop10 as ("url":"接口","count":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_urltop10', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_urltop'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[252]原语 store sen_urltop10 to ssdb by ssdb0 with data_sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_srcip', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_ip.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[257]原语 sen_srcip = load pq by sensitive/sensitive_ip.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_srcip', 'by': 'srcip:str,url_count:int,app_count:int,account:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[258]原语 alter sen_srcip by srcip:str,url_count:int,app_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_srcip', 'Action': 'loc', 'loc': 'sen_srcip', 'by': 'srcip,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[259]原语 sen_srcip = loc sen_srcip by srcip,sensitive_count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_srcip', 'as': "'sensitive_count':'count'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[260]原语 rename sen_srcip as ("sensitive_count":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_srcip0', 'Action': 'eval', 'eval': 'sen_srcip', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[261]原语 sen_srcip0 = eval sen_srcip by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_srcip1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '敏感终端数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[262]原语 sen_srcip1 = @udf udf0.new_df with 敏感终端数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_srcip1', 'Action': '@udf', '@udf': 'sen_srcip1', 'by': 'udf0.df_append', 'with': '$sen_srcip0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[263]原语 sen_srcip1 = @udf sen_srcip1 by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_srcip1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_srcipcount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[264]原语 store sen_srcip1 to ssdb by ssdb0 with data_sensit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_srcip', 'Action': 'loc', 'loc': 'sen_srcip', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[265]原语 sen_srcip = loc sen_srcip by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_srcip', 'Action': 'loc', 'loc': 'sen_srcip', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[266]原语 sen_srcip = loc sen_srcip drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_srciptop10', 'Action': 'filter', 'filter': 'sen_srcip', 'by': 'index <10'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[267]原语 sen_srciptop10 = filter sen_srcip by index <10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_srciptop10', 'as': "'srcip':'终端IP','count':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[268]原语 rename sen_srciptop10 as ("srcip":"终端IP","count":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_srciptop10', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sens_top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[269]原语 store sen_srciptop10 to ssdb by ssdb0 with data_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_srciptop10.详情', 'Action': 'lambda', 'lambda': '终端IP', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[270]原语 sen_srciptop10.详情 = lambda 终端IP by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_srciptop10', 'Action': '@udf', '@udf': 'sen_srciptop10', 'by': 'udf0.df_set_index', 'with': '终端IP'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[271]原语 sen_srciptop10 = @udf sen_srciptop10 by udf0.df_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sen_srciptop10', 'Action': 'order', 'order': 'sen_srciptop10', 'by': '数量', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[272]原语 sen_srciptop10 = order  sen_srciptop10 by 数量 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_srciptop10', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_srctop'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[273]原语 store sen_srciptop10 to ssdb by ssdb0 with data_se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_account', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_account.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[278]原语 sen_account = load pq by sensitive/sensitive_accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_account', 'by': 'account:str,url_count:int,srcip_count:int,app_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[279]原语 alter sen_account by account:str,url_count:int,src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_account', 'Action': 'loc', 'loc': 'sen_account', 'by': 'account,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[280]原语 sen_account = loc sen_account by account,sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_account', 'as': "'sensitive_count':'count'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[281]原语 rename sen_account as ("sensitive_count":"count") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_account0', 'Action': 'eval', 'eval': 'sen_account', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[282]原语 sen_account0 = eval sen_account by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_account1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '敏感账号数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[283]原语 sen_account1 = @udf udf0.new_df with 敏感账号数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_account1', 'Action': '@udf', '@udf': 'sen_account1', 'by': 'udf0.df_append', 'with': '$sen_account0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[284]原语 sen_account1 = @udf sen_account1 by udf0.df_append... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_account1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_accountcount'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[285]原语 store sen_account1 to ssdb by ssdb0 with data_sens... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_account', 'Action': 'loc', 'loc': 'sen_account', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[286]原语 sen_account = loc sen_account by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_account', 'Action': 'loc', 'loc': 'sen_account', 'drop': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[287]原语 sen_account = loc sen_account drop aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_accounttop10', 'Action': 'filter', 'filter': 'sen_account', 'by': 'index <10'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[288]原语 sen_accounttop10 = filter sen_account by index <10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_accounttop10', 'as': "'account':'账号','count':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[289]原语 rename sen_accounttop10 as ("account":"账号","count"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_accounttop10', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_sensitive_accounttop'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[290]原语 store sen_accounttop10 to ssdb by ssdb0 with data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_accounttop10.详情', 'Action': 'lambda', 'lambda': '账号', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[292]原语 sen_accounttop10.详情 = lambda 账号 by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sen_accounttop10', 'by': '账号', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[293]原语 sens = loc sen_accounttop10 by 账号 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sens', 'Action': 'order', 'order': 'sens', 'by': '数量', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[294]原语 sens = order sens by 数量 with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sensxx:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[295]原语 store sens to ssdb by ssdb0 with sensxx:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[300]原语 hour1 = @sdf sys_now with -1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour1,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[301]原语 hour1 = @sdf format_now with ($hour1,"%Y-%m-%d %H:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[302]原语 hour2 = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'hour2', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$hour2,"%Y-%m-%d %H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[303]原语 hour2 = @sdf format_now with ($hour2,"%Y-%m-%d %H:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'hour', 'Action': '@udf', '@udf': 'udf0.new_df_timerange', 'with': '$hour1,$hour2,1H'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[304]原语 hour = @udf udf0.new_df_timerange with ($hour1,$ho... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.hour', 'Action': 'lambda', 'lambda': 'end_time', 'by': 'x:x[11:13]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[305]原语 hour.hour = lambda end_time by (x:x[11:13]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'hour.hour1', 'Action': 'lambda', 'lambda': 'hour', 'by': "x:x+'时'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[306]原语 hour.hour1 = lambda hour by (x:x+"时") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'hour', 'Action': 'loc', 'loc': 'hour', 'by': 'hour1,hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[307]原语 hour = loc hour by hour1,hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,response_count as res_type,count(*) as num from sen_http_count where timestamp >= toDate(today()) group by hour,res_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[309]原语 sens = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens.res_type', 'Action': 'str', 'str': 'res_type', 'by': "replace(' ','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[310]原语 sens.res_type = str res_type by replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_fillna_cols', 'with': "res_type:'',num:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[312]原语 sens = @udf sens by udf0.df_fillna_cols with res_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "res_type != '' and res_type != 'null' and res_type != 'None'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[313]原语 sens = filter sens by res_type != "" and res_type ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.res_type', 'Action': 'lambda', 'lambda': 'res_type', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[314]原语 sens.res_type = lambda res_type by (x:x[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.res_type', 'Action': 'lambda', 'lambda': 'res_type', 'by': 'x:x.split(",")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[315]原语 sens.res_type = lambda res_type by (x:x.split(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_l2df', 'with': 'res_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[316]原语 sens_1 = @udf sens by udf0.df_l2df with res_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens_1', 'as': "'res_type':'res'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[317]原语 rename sens_1 as ("res_type":"res") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens', 'Action': 'join', 'join': 'sens,sens_1', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[318]原语 sens = join sens,sens_1 by index,index with outer 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.res', 'Action': 'lambda', 'lambda': 'res', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[319]原语 sens.res = lambda res by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_l2cs', 'with': 'res'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[320]原语 sens = @udf sens by udf0.df_l2cs with res 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': "'n100':'key','n101':'res_key_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[321]原语 rename sens as ("n100":"key","n101":"res_key_num")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'hour,num,key,res_key_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[322]原语 sens = loc sens by hour,num,key,res_key_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.key', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[323]原语 sens.key = lambda key by (x:x[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens.num.res_key_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[324]原语 alter sens.num.res_key_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'key_num', 'by': 'df["num"] * df["res_key_num"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[325]原语 sens = add key_num by df["num"] * df["res_key_num"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens', 'by': 'hour,key,key_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[326]原语 sens1 = loc sens by hour,key,key_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select substring(toString(timestamp),12,2) as hour,request_count as req_type,count(*) as num from sen_http_count where timestamp >= toDate(today()) group by hour,req_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[328]原语 sens = load ckh by ckh with select substring(toStr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens.req_type', 'Action': 'str', 'str': 'req_type', 'by': "replace(' ','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[329]原语 sens.req_type = str req_type by replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_fillna_cols', 'with': "req_type:'',num:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[331]原语 sens = @udf sens by udf0.df_fillna_cols with req_t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "req_type != '' and req_type != 'null' and req_type != 'None'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[332]原语 sens = filter sens by req_type != "" and req_type ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.req_type', 'Action': 'lambda', 'lambda': 'req_type', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[333]原语 sens.req_type = lambda req_type by (x:x[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.req_type', 'Action': 'lambda', 'lambda': 'req_type', 'by': 'x:x.split(",")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[334]原语 sens.req_type = lambda req_type by (x:x.split(",")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens_1', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_l2df', 'with': 'req_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[335]原语 sens_1 = @udf sens by udf0.df_l2df with req_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens_1', 'as': "'req_type':'req'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[336]原语 rename sens_1 as ("req_type":"req") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens', 'Action': 'join', 'join': 'sens,sens_1', 'by': 'index,index', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[337]原语 sens = join sens,sens_1 by index,index with outer 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.req', 'Action': 'lambda', 'lambda': 'req', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[338]原语 sens.req = lambda req by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_l2cs', 'with': 'req'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[339]原语 sens = @udf sens by udf0.df_l2cs with req 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': "'n100':'key','n101':'req_key_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[340]原语 rename sens as ("n100":"key","n101":"req_key_num")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'hour,num,key,req_key_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[341]原语 sens = loc sens by hour,num,key,req_key_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sens.key', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[342]原语 sens.key = lambda key by (x:x[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens.num.req_key_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[343]原语 alter sens.num.req_key_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'key_num', 'by': 'df["num"] * df["req_key_num"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[344]原语 sens = add key_num by df["num"] * df["req_key_num"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens2', 'Action': 'loc', 'loc': 'sens', 'by': 'hour,key,key_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[345]原语 sens2 = loc sens by hour,key,key_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sens', 'Action': 'union', 'union': 'sens1,sens2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[347]原语 sens = union sens1,sens2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens', 'Action': 'group', 'group': 'sens', 'by': 'hour,key', 'agg': 'key_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[348]原语 sens = group sens by hour,key agg key_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[349]原语 sens = @udf sens by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': "'key':'data','key_num_sum':'num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[350]原语 rename sens as ("key":"data","key_num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "data !='婚姻状况' and data !='宗教信仰'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[351]原语 sens = filter sens by data !="婚姻状况" and data !="宗教... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens0', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'hour1,hour,data,num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[352]原语 sens0 = @udf udf0.new_df with hour1,hour,data,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'data', 'Action': 'group', 'group': 'sens', 'by': 'data', 'agg': 'data:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[353]原语 data = group sens by data agg data:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data', 'Action': 'loc', 'loc': 'data', 'by': 'index', 'to': 'data'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[354]原语 data = loc data by index to data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'data', 'with': 'data = $1', 'run': '""\nsens1 = filter sens by data == \'@data\'\n#sens1 = filter sens by data == \'手机号\'\nsens1 = join hour,sens1 by hour,hour with left\n#sens1 = @udf sens1 by udf0.df_fillna with 0\n#sens1.data = lambda data by (x:\'@data\' if x == 0 else x)\nsens1 = @udf sens1 by udf0.df_fillna_cols with data:\'@data\',num:0\nsens0 = union sens0,sens1\n""'}
	try:
		ptree['lineno']=355
		ptree['funs']=block_foreach_355
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[355]原语 foreach data run "sens1 = filter sens by data == "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens', 'Action': 'group', 'group': 'sens0', 'by': 'hour,data', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[364]原语 sens = group sens0 by hour,data agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_unstack', 'with': 'num_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[365]原语 sens = @udf sens by udf0.df_unstack with num_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'index', 'to': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[366]原语 sens = loc sens by index to hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens', 'Action': 'join', 'join': 'hour,sens', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[367]原语 sens = join hour,sens by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'hour1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[368]原语 sens = loc sens by hour1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'drop': 'hour'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[369]原语 sens = loc sens drop hour 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[370]原语 sens = @udf sens by udf0.df_fillna with (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens_24l:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[371]原语 store sens to ssdb by ssdb0 with sens_24l:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'id', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[375]原语 id = @udf udf0.new_df with (id) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'id', 'Action': '@udf', '@udf': 'id', 'by': 'udf0.df_append', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[376]原语 id = @udf id by udf0.df_append with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'id', 'Action': '@udf', '@udf': 'id', 'by': 'udf0.df_append', 'with': '1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[377]原语 id = @udf id by udf0.df_append with 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'id', 'Action': '@udf', '@udf': 'id', 'by': 'udf0.df_append', 'with': '2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[378]原语 id = @udf id by udf0.df_append with 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'id', 'Action': '@udf', '@udf': 'id', 'by': 'udf0.df_append', 'with': '3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[379]原语 id = @udf id by udf0.df_append with 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sen_key_4', 'Action': 'order', 'order': 'sen_key', 'by': 'count', 'limit': '4'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[380]原语 sen_key_4 = order sen_key by count limit 4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_key_4', 'Action': 'loc', 'loc': 'sen_key_4', 'by': 'index', 'to': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[381]原语 sen_key_4 = loc sen_key_4 by index to aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sen_key_4', 'Action': 'join', 'join': 'id,sen_key_4', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[382]原语 sen_key_4 = join id,sen_key_4 by index,index with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_key_4', 'Action': 'loc', 'loc': 'sen_key_4', 'by': 'data,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[383]原语 sen_key_4 = loc sen_key_4 by data,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sen_key_4', 'Action': '@udf', '@udf': 'sen_key_4', 'by': 'udf0.df_fillna_cols', 'with': "data:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[385]原语 sen_key_4 = @udf sen_key_4 by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sen_srcip', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_ip.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[387]原语 sen_srcip = load pq by sensitive/sensitive_ip.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sen_srcip', 'by': 'srcip:str,url_count:int,app_count:int,account:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[388]原语 alter sen_srcip by srcip:str,url_count:int,app_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'sen_srcip.index.size == 0', 'with': 'sen_srcip = @udf udf0.new_df with srcip,app_count,url_count,account_count,sensitive_count,s_num_sum,_id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=389
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[389]原语 if sen_srcip.index.size == 0 with sen_srcip = @udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'sen_key_4', 'with': 'data = $1,id = $2', 'run': '""\n## 排名分布\nsen_srcip_4 = filter sen_srcip by s_num_sum like @data\nsen_srcip_4 = order sen_srcip_4 by sensitive_count with desc limit 10\nsen_srcip_4 = loc sen_srcip_4 by srcip,sensitive_count\nrename sen_srcip_4 as (\'sensitive_count\':\'数量\')\nsen_srcip_4 = order sen_srcip_4 by 数量 with asc\nsen_srcip_4.详情 = lambda srcip by (x:x)\nsen_srcip_4 = loc sen_srcip_4 by srcip to index\nstore sen_srcip_4 to ssdb by ssdb0 with sen_srcip_4:@id\n##：标题\naa = @udf udf0.new_df with (title)\nif \'@data\' != \'\' with aa = @udf aa by udf0.df_append with @data\nif \'@data\' != \'\' with aa.title = str title by (slice(0,6))\nif \'@data\' != \'\' with aa.title = lambda title by (x:\'涉及\'+x+\'的终端分布\')\nstore aa to ssdb by ssdb0 with title:@id\n""'}
	try:
		ptree['lineno']=391
		ptree['funs']=block_foreach_391
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[391]原语 foreach sen_key_4 run "## 排名分布sen_srcip_4 = filter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[data_sensitive_portal.fbi]执行第[411]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],411

#主函数结束,开始块函数

def block_foreach_355(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens1', 'Action': 'filter', 'filter': 'sens', 'by': "data == '@data'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第355行foreach语句中]执行第[356]原语 sens1 = filter sens by data == "@data" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sens1', 'Action': 'join', 'join': 'hour,sens1', 'by': 'hour,hour', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第355行foreach语句中]执行第[358]原语 sens1 = join hour,sens1 by hour,hour with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens1', 'Action': '@udf', '@udf': 'sens1', 'by': 'udf0.df_fillna_cols', 'with': "data:'@data',num:0"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第355行foreach语句中]执行第[361]原语 sens1 = @udf sens1 by udf0.df_fillna_cols with dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sens0', 'Action': 'union', 'union': 'sens0,sens1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第355行foreach语句中]执行第[362]原语 sens0 = union sens0,sens1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_355

def block_foreach_391(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sen_srcip_4', 'Action': 'filter', 'filter': 'sen_srcip', 'by': 's_num_sum like @data'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[393]原语 sen_srcip_4 = filter sen_srcip by s_num_sum like @... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sen_srcip_4', 'Action': 'order', 'order': 'sen_srcip_4', 'by': 'sensitive_count', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[394]原语 sen_srcip_4 = order sen_srcip_4 by sensitive_count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_srcip_4', 'Action': 'loc', 'loc': 'sen_srcip_4', 'by': 'srcip,sensitive_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[395]原语 sen_srcip_4 = loc sen_srcip_4 by srcip,sensitive_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sen_srcip_4', 'as': "'sensitive_count':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[396]原语 rename sen_srcip_4 as ("sensitive_count":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sen_srcip_4', 'Action': 'order', 'order': 'sen_srcip_4', 'by': '数量', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[397]原语 sen_srcip_4 = order sen_srcip_4 by 数量 with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sen_srcip_4.详情', 'Action': 'lambda', 'lambda': 'srcip', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[398]原语 sen_srcip_4.详情 = lambda srcip by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sen_srcip_4', 'Action': 'loc', 'loc': 'sen_srcip_4', 'by': 'srcip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[399]原语 sen_srcip_4 = loc sen_srcip_4 by srcip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sen_srcip_4', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sen_srcip_4:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[400]原语 store sen_srcip_4 to ssdb by ssdb0 with sen_srcip_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'title'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[402]原语 aa = @udf udf0.new_df with (title) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'@data' != ''", 'with': 'aa = @udf aa by udf0.df_append with @data'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=403
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[403]原语 if "@data" != "" with aa = @udf aa by udf0.df_appe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'@data' != ''", 'with': 'aa.title = str title by (slice(0,6))'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	try:
		ptree['lineno']=404
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[404]原语 if "@data" != "" with aa.title = str title by (sli... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'@data' != ''", 'with': "aa.title = lambda title by (x:'涉及'+x+'的终端分布')"}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	try:
		ptree['lineno']=405
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[405]原语 if "@data" != "" with aa.title = lambda title by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'title:@id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第391行foreach语句中]执行第[406]原语 store aa to ssdb by ssdb0 with title:@id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_391

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



