#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: copyright2/init
#datetime: 2024-08-30T16:10:57.011258
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
	
	
	ptree={'runtime': runtime, 'Action': 'use', 'use': 'copyright2'}
	try:
		use_fun(ptree)
		workspace=ptree['work_space']
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[10]原语 use  copyright2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'udfG.copyright'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[12]原语 c = @udf udfG.copyright 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'kernel'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[13]原语 a = @udf udf0.new_df with kernel 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '云信应用数据安全监测系统'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[14]原语 a = @udf a by udf0.df_append with 云信应用数据安全监测系统 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a', 'Action': 'join', 'join': 'a,c', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[15]原语 a = join a,c by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'xl', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'xlh'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[16]原语 xl = load ssdb by ssdb0 with xlh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'xll', 'Action': 'eval', 'eval': 'xl', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[17]原语 xll = eval xl by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$xll ==0', 'with': 'xl = @udf xl by udf0.new_df with xl'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=18
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[18]原语 if $xll ==0 with xl = @udf xl by udf0.new_df with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$xll ==0', 'with': 'xl = @udf xl by udf0.df_append with ()'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=19
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[19]原语 if $xll ==0 with xl = @udf xl by udf0.df_append wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a', 'Action': 'join', 'join': 'a,xl', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[20]原语 a = join a,xl by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'udfA.get_vbs', 'with': 'APP-DLP-SE'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[22]原语 b =@udf udfA.get_vbs with APP-DLP-SE 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a', 'Action': 'join', 'join': 'a,b', 'by': 'index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[23]原语 a = join a,b by index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'a', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[26]原语 push a as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': 'copyright2'}
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[copyright2/init.fbi]执行第[28]原语 clear copyright2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],28

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



