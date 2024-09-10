#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: system/deal_ui
#datetime: 2024-08-30T16:10:56.562589
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.update_scheme'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/deal_ui.fbi]执行第[12]原语 a = @udf FBI.update_scheme 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'FBI.update_data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/deal_ui.fbi]执行第[15]原语 b = @udf FBI.update_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df_range', 'with': '1,6'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/deal_ui.fbi]执行第[18]原语 aa =@udf  udf0.new_df_range with (1,6) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'aa', 'with': 'f=$2', 'run': '""\na = load ssdb by ssdb0 with scheme:@f\na = add var by a.index\nb = @udf a by udf0.df_like_query with (var like @)\nb1 = @udf a by udf0.df_like_query with (var like g_SI_)\nb = union b,b1\nb = loc b by (value,备注)\na.var2 = str var by (findall("g_\\d{2,4}"))\na.var3 = str var2 by ([0])\nc = distinct a by var3\nc = loc c by var3\na = loc a by (value,备注,var3)\nforeach c by run system/deal_scheme.fbi with (id=$1,f=@f)\n""'}
	try:
		ptree['lineno']=19
		ptree['funs']=block_foreach_19
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[system/deal_ui.fbi]执行第[19]原语 foreach aa run   "a = load ssdb by ssdb0 with sche... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],32

#主函数结束,开始块函数

def block_foreach_19(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'scheme:@f'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[20]原语 a = load ssdb by ssdb0 with scheme:@f 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'var', 'by': 'a.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[21]原语 a = add var by a.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_like_query', 'with': 'var like @'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[22]原语 b = @udf a by udf0.df_like_query with (var like @)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b1', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_like_query', 'with': 'var like g_SI_'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[23]原语 b1 = @udf a by udf0.df_like_query with (var like g... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'b', 'Action': 'union', 'union': 'b,b1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[24]原语 b = union b,b1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'b', 'Action': 'loc', 'loc': 'b', 'by': 'value,备注'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[25]原语 b = loc b by (value,备注) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.var2', 'Action': 'str', 'str': 'var', 'by': 'findall("g_\\d{2,4}")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[26]原语 a.var2 = str var by (findall("g_\d{2,4}")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.var3', 'Action': 'str', 'str': 'var2', 'by': '[0]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[27]原语 a.var3 = str var2 by ([0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'c', 'Action': 'distinct', 'distinct': 'a', 'by': 'var3'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[28]原语 c = distinct a by var3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c', 'Action': 'loc', 'loc': 'c', 'by': 'var3'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[29]原语 c = loc c by var3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'value,备注,var3'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[30]原语 a = loc a by (value,备注,var3) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'c', 'by': 'run', 'with': 'id=$1,f=@f', 'run': 'system/deal_scheme.fbi'}
	try:
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第19行foreach语句中]执行第[31]原语 foreach c by run system/deal_scheme.fbi with (id=$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_19

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



