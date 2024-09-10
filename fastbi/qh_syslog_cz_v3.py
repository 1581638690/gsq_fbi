#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_syslog_cz
#datetime: 2024-08-30T16:10:53.637843
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
		add_the_error('[qh_syslog_cz.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 't', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[7]原语 t = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 't', 'Action': '@sdf', '@sdf': 'sys_str', 'by': '$t,[0:10]'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[8]原语 t = @sdf sys_str by $t,[0:10] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[9]原语 s = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_append', 'with': '$t'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[10]原语 s = @udf s by udf0.df_append with $t 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'syslog_cz'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[11]原语 sa = load ssdb by ssdb0 with syslog_cz 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'zz', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'qh_send as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[12]原语 zz = load ssdb by ssdb0 with qh_send as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'sends', 'Action': 'jaas', 'jaas': 'zz', 'by': 'zz["sends"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[13]原语 sends = jaas zz by zz["sends"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '"api_opt" in $sends', 'with': '""\naa = @udf udf0.new_df with a\naa = @udf aa by udf0.df_append with 1\na = eval aa by iloc[0,0]\n"', 'else': '"\naa = @udf udf0.new_df with a\naa = @udf aa by udf0.df_append with 0\na = eval aa by iloc[0,0]\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=14
		ptree['funs']=block_if_14
		ptree['funs2']=block_if_else_14
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[14]原语 if "api_opt" in $sends with "aa = @udf udf0.new_df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'sa.iloc[0,0] != s.iloc[0,0] and $a == 1', 'with': '""\ndata,count =load ssdb by ssdb0 query qrange,Q_log_$t,0,10000\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=24
		ptree['funs']=block_if_24
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[24]原语 if sa.iloc[0,0] != s.iloc[0,0] and $a == 1 with "d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'sa.iloc[0,0] == s.iloc[0,0] and $a == 1', 'with': '""\nc = eval sa by iloc[0,1]\ndata,count =load ssdb by ssdb0 query qrange,Q_log_$t,$c,10000\n#data = add event_type by ("operation")\n#d = @udf data by KFK.fast_store with kfk,api_send\n#c = eval count by iloc[0,1]\n#s = add count by $c\n#store s to ssdb with syslog_cz\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=28
		ptree['funs']=block_if_28
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[28]原语 if sa.iloc[0,0] == s.iloc[0,0] and $a == 1 with "c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'data', 'Action': 'add', 'add': 'event_type', 'by': '"operation"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[38]原语 data = add event_type by ("operation") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'data', 'by': 'KFK.fast_store', 'with': 'kfk,api_send'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[39]原语 d = @udf data by KFK.fast_store with kfk,api_send 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'eval', 'eval': 'count', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[40]原语 c = eval count by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'count', 'by': '$c'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[41]原语 s = add count by $c 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'syslog_cz'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[42]原语 store s to ssdb with syslog_cz 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_syslog_cz.fbi]执行第[44]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],44

#主函数结束,开始块函数

def block_if_14(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'a'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第14行if语句中]执行第[15]原语 aa = @udf udf0.new_df with a 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第14行if语句中]执行第[16]原语 aa = @udf aa by udf0.df_append with 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第14行if语句中]执行第[17]原语 a = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_14

def block_if_else_14(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'a'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第14行if_else语句中]执行第[14]原语 aa = @udf udf0.new_df with a 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第14行if_else语句中]执行第[15]原语 aa = @udf aa by udf0.df_append with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第14行if_else语句中]执行第[16]原语 a = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_else_14

def block_if_24(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'data,count', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,Q_log_$t,0,10000'}
	ptree['query'] = deal_sdf(workspace,ptree['query'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第24行if语句中]执行第[25]原语 data,count =load ssdb by ssdb0 query qrange,Q_log_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_24

def block_if_28(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'eval', 'eval': 'sa', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第28行if语句中]执行第[29]原语 c = eval sa by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data,count', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qrange,Q_log_$t,$c,10000'}
	ptree['query'] = deal_sdf(workspace,ptree['query'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第28行if语句中]执行第[30]原语 data,count =load ssdb by ssdb0 query qrange,Q_log_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_28

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



