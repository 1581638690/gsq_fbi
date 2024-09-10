#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: smpUu/query_table
#datetime: 2024-08-30T16:10:57.253722
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
		add_the_error('[smpUu/query_table.fea]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[12]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('a',ptree)", 'as': 'break', 'with': '查询参数错误！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[smpUu/query_table.fea]执行第[13]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[13]原语 assert find_df_have_data("a",ptree) as break with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[15]原语 a = loc a by name to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'st', 'Action': 'eval', 'eval': 'a', 'by': 'loc["startdate"]["value"]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[16]原语 st = eval a by loc["startdate"]["value"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'st2', 'Action': '@sdf', '@sdf': 'date_deal', 'by': '$st,-1d'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[18]原语 st2 = @sdf date_deal by $st,-1d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'st', 'Action': '@sdf', '@sdf': 'sys_str', 'by': '$st2,[0:10]'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[19]原语 st = @sdf sys_str by $st2,[0:10] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'et', 'Action': 'eval', 'eval': 'a', 'by': 'loc["enddate"]["value"][0:10]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[21]原语 et = eval a by loc["enddate"]["value"][0:10] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b,c', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qlist,@table_$st,@table_$et,100000'}
	ptree['query'] = replace_ps(ptree['query'],runtime)
	ptree['query'] = deal_sdf(workspace,ptree['query'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[23]原语 b,c =load ssdb by ssdb0 query qlist,@table_$st,@ta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'b', 'Action': 'order', 'order': 'b', 'by': 'timestamp'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[24]原语 b = order b by timestamp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c2', 'Action': 'eval', 'eval': 'b', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[25]原语 c2 = eval b by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c', 'Action': 'loc', 'loc': 'c', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[26]原语 c = loc c by name to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c2', 'Action': 'eval', 'eval': 'c', 'by': 'loc["sum"]["size"]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[28]原语 c2 = eval c by loc["sum"]["size"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[30]原语 count = @udf udf0.new_df with count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'count', 'Action': '@udf', '@udf': 'count', 'by': 'udf0.df_append', 'with': '$c2'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[31]原语 count = @udf count by udf0.df_append with $c2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'b', 'to': 'ssdb', 'by': 'ssdb0', 'with': '@table:query:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[34]原语 store b to ssdb by ssdb0 with @table:query:@FPS as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'c', 'to': 'ssdb', 'by': 'ssdb0', 'with': '@table:query_count:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[36]原语 store c to ssdb by ssdb0 with @table:query_count:@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[38]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'c', 'as': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[39]原语 push c as count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[smpUu/query_table.fea]执行第[40]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],40

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



