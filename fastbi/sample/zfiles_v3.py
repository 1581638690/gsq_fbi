#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/zfiles
#datetime: 2024-08-30T16:10:57.223644
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'ZFile.list_dir'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[6]原语 a = @udf ZFile.list_dir 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a1', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'data'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[8]原语 a1 = @udf ZFile.list_dir with data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'ZFile.list_file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[11]原语 aa = @udf ZFile.list_file 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a2', 'Action': '@udf', '@udf': 'ZFile.list_file2', 'with': 'dataset_2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[13]原语 a2 = @udf ZFile.list_file2 with dataset_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'ZFile.un_rar'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[16]原语 b = @udf a by ZFile.un_rar 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'ZFile.un_zip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[19]原语 b = @udf a by ZFile.un_zip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'ZFile.un_gz'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[22]原语 b = @udf a by ZFile.un_gz 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'ZFile.un_tar'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[25]原语 b = @udf a by ZFile.un_tar 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'ZFile.mk_dir', 'with': 'dd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[28]原语 @udf ZFile.mk_dir with dd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'xxxx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/zfiles.fbi]执行第[31]原语 @udf ZFile.rm_file with xxxx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],32

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



