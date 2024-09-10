#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sensitive_api_search
#datetime: 2024-08-30T16:10:54.548294
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
		add_the_error('[sensitive_api_search.fbi]执行第[10]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@datakey'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[12]原语 ss = load ssdb by ssdb0 with @datakey 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sensitive_api.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[15]原语 a = load pq by sensitive/sensitive_api.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a', 'by': 'url:str,srcip_count:int,account_count:int,sensitive_count:int,s_num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[16]原语 alter a by url:str,srcip_count:int,account_count:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'index', 'to': '__index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[17]原语 a = loc a by index to __index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ppp', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@filterKey'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[21]原语 ppp = load ssdb by ssdb0 with @filterKey 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ppp', 'Action': 'filter', 'filter': 'ppp', 'by': "api != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[22]原语 ppp = filter ppp by api != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ppp_num', 'Action': 'eval', 'eval': 'ppp', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[23]原语 ppp_num = eval ppp by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ppp_num', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$ppp_num != 0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[24]原语 ppp_num = @sdf sys_eval with $ppp_num != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'q', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$ppp_num, "api = eval ppp by iloc[0,0]"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[26]原语 q = @sdf sys_if_run with ($ppp_num, "api = eval pp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'q', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$ppp_num, "a = filter a with $api"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[27]原语 q = @sdf sys_if_run with ($ppp_num, "a = filter a ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sss_num', 'Action': 'eval', 'eval': 'ss', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[31]原语 sss_num = eval ss by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'sss_num', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$sss_num != 0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[32]原语 sss_num = @sdf sys_eval with $sss_num != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'q', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$sss_num, "ss1 = eval ss by iloc[0,0]"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[33]原语 q = @sdf sys_if_run with ($sss_num, "ss1 = eval ss... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'q', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$sss_num, "a = filter a by $ss1"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[34]原语 q = @sdf sys_if_run with ($sss_num, "a = filter a ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'b', 'Action': 'loc', 'loc': 'a', 'by': 'url,srcip_count,account_count,sensitive_count,s_num_sum,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[38]原语 b = loc a by url,srcip_count,account_count,sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'eval', 'eval': 'b', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[39]原语 count = eval b by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[40]原语 c = @udf udf0.new_df with count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_append', 'with': '$count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[41]原语 c = @udf c by udf0.df_append with $count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'limit', 'limit': 'b', 'by': '1000'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[42]原语 b = limit b by 1000 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'b', 'as': '"url":"接口","srcip_count":"终端数量","account_count":"账号数量","sensitive_count":"敏感数据数量","s_num_sum":"敏感数据分类数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[43]原语 rename b as ("url":"接口","srcip_count":"终端数量","acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[45]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'c', 'as': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[46]原语 push c as count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_api_search.fbi]执行第[48]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],48

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



