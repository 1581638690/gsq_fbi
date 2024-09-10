#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/dump
#datetime: 2024-08-30T16:10:57.210739
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'SSDB.imp_keys', 'with': 'dd.db'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[6]原语 d = @udf  SSDB.imp_keys with dd.db 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'key'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[10]原语 a = @udf udf0.new_df with key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'am:am_5:smpHubfMaY6'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[11]原语 a = @udf a by udf0.df_append with am:am_5:smpHubfM... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'dd:future'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[12]原语 a = @udf a by udf0.df_append with dd:future 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'dd2:future'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[13]原语 a = @udf a by udf0.df_append with dd2:future 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'dd:Yes_or_No'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[14]原语 a = @udf a by udf0.df_append with dd:Yes_or_No 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'dd2:Yes_or_No'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[15]原语 a = @udf a by udf0.df_append with dd2:Yes_or_No 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'dashboard6:vapzit92OM'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[16]原语 a = @udf a by udf0.df_append with dashboard6:vapzi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'am:am_16:smp7zWDlM'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[17]原语 a = @udf a by udf0.df_append with am:am_16:smp7zWD... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'am:am_16:smpxh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[18]原语 a = @udf a by udf0.df_append with am:am_16:smpxh 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'modeling:ResourceM'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[19]原语 a = @udf a by udf0.df_append with modeling:Resourc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'modeling:RoleM'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[20]原语 a = @udf a by udf0.df_append with modeling:RoleM 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'am:am_7:smpaVom'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[22]原语 a = @udf a by udf0.df_append with am:am_7:smpaVom 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'a', 'by': 'SSDB.dump_keys2', 'with': 'dd1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[23]原语 c = @udf a by SSDB.dump_keys2 with dd1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[27]原语 a = @udf udf0.new_df with name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'admin'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[28]原语 a = @udf a by udf0.df_append with admin 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'pot'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[29]原语 a = @udf a by udf0.df_append with pot 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udfA.dump_users', 'with': 'user'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/dump.fbi]执行第[30]原语 a = @udf a by udfA.dump_users with user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],30

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



