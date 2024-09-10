#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: appmMKRv6gBtJ/query_table
#datetime: 2024-08-30T16:10:57.440216
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
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_df', 'Action': '@udf', '@udf': 'ssh_iptables.get_iptables_input'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[14]原语 data_df = @udf ssh_iptables.get_iptables_input 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'eval', 'eval': 'data_df', 'by': 'index.size>0'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[15]原语 a=eval data_df by index.size>0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'if_run', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$a, """\ndata_df = @udf data_df by udf0.df_fillna with ()\ndata_df.port = str port by ( findall( \'(\\d.*)\' ) )\nalter data_df.port as str\ndata_df.port = str port by ( replace("\'","" ) )\ndata_df.port = str port by ( replace("[","" ) )\ndata_df.port = str port by ( replace("]","" ) )\ndata_df = loc data_df drop (Pro)\npd2=eval data_df by (index.size>0)\nif_run = @sdf sys_if_run with ($pd2, "run pot_get_fire.fbi")\n\n"""'}
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
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[16]原语 if_run = @sdf sys_if_run with ($a, "data_df = @udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'count', 'Action': 'eval', 'eval': 'data_df', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[36]原语 count = eval data_df by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[37]原语 count = @udf udf0.new_df with (count) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'count', 'Action': '@udf', '@udf': 'count', 'by': 'udf0.df_append', 'with': '$count'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[38]原语 count = @udf count by udf0.df_append with ($count)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'fix_tname(ptree, "data_df") in global_table', 'as': 'alert', 'with': '数据查询失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[40]原语 assert "fix_tname(ptree, "data_df") in global_tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_df', 'to': 'ssdb', 'by': 'ssdb0', 'with': '@table:query:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[43]原语 store data_df to ssdb by ssdb0 with @table:query:@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'data_df', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[44]原语 push data_df as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'count', 'to': 'ssdb', 'by': 'ssdb0', 'with': '@table:query_count:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[46]原语 store count to ssdb by ssdb0 with @table:query_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'count', 'as': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[47]原语 push count as count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[appmMKRv6gBtJ/query_table.fea]执行第[50]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],50

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



