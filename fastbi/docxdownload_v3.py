#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: docxdownload
#datetime: 2024-08-30T16:10:54.689549
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
		add_the_error('[docxdownload.fbi]执行第[4]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[5]原语 a= load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[6]原语 file = eval a by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'Daily_func.formatByte', 'with': '/opt/openfbi/workspace/csv/$file'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[7]原语 df2 = @udf  Daily_func.formatByte with (/opt/openf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sum', 'Action': 'eval', 'eval': 'df2', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[8]原语 sum = eval df2 by (iloc[0,1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'file,sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[9]原语 bb = @udf udf0.new_df with (file,sum) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb2', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': 'csv/$file,$sum'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[10]原语 bb2 = @udf bb by udf0.df_append with (csv/$file,$s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'bb2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_bb3:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[11]原语 store bb2 to ssdb by ssdb0 with pot_bb3:@FPS as 60... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[docxdownload.fbi]执行第[13]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],13

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



