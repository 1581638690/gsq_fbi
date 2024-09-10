#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: to_word
#datetime: 2024-08-30T16:10:54.291034
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
		add_the_error('[to_word.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'log1', 'Action': '@udf', '@udf': 'udf0.df_append', 'with': "['正在生成报告'],1,true,false"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[7]原语 log1= @udf udf0.df_append with (["正在生成报告"],1,true,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'log1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'schedule_to_word', 'as': '600'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[8]原语 store log1 to ssdb by ssdb0 with schedule_to_word ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'CMP.sleep', 'with': '2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[9]原语 t = @udf CMP.sleep with 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'to_word_apply.fea'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[11]原语 run to_word_apply.fea 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'log2', 'Action': '@udf', '@udf': 'udf0.df_append', 'with': "['完成'],2,true,true"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[13]原语 log2= @udf udf0.df_append with (["完成"],2,true,true... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'log2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'schedule_to_word', 'as': '600'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[14]原语 store log2 to ssdb by ssdb0 with schedule_to_word ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 't', 'Action': '@udf', '@udf': 'CMP.sleep', 'with': '1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[15]原语 t = @udf CMP.sleep with 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[to_word.fbi]执行第[17]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],17

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



