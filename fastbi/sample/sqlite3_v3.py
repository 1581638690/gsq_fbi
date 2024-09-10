#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/sqlite3
#datetime: 2024-08-30T16:10:57.236997
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'CRUD.init_stable', 'with': 's.db'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[8]原语 s = @udf CRUD.init_stable with (s.db) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,age'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[11]原语 a = @udf udf0.new_df with (name,age) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': 'varchar(10),int'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[12]原语 a = @udf a by udf0.df_append with (varchar(10),int... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.create_stable', 'with': 's.db,people'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[13]原语 @udf a by CRUD.create_stable with (s.db,people) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'RS.list_s3', 'with': 's.db'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[16]原语 a = @udf RS.list_s3 with s.db 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,age'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[19]原语 a = @udf udf0.new_df with (name,age) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '胡,14'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[20]原语 a = @udf a by udf0.df_append with (胡,14) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '胡,15'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[21]原语 a = @udf a by udf0.df_append with (胡,15) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '胡,16'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[22]原语 a = @udf a by udf0.df_append with (胡,16) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[24]原语 a = @udf a by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.age', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[25]原语 alter a.age as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_object_stable', 'with': 's.db,people'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[27]原语 @udf a by CRUD.save_object_stable with (s.db,peopl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'CRUD.get_object_stable', 'with': 's.db,people,3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[30]原语 a = @udf CRUD.get_object_stable with (s.db,people,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'CRUD.delete_object_stable', 'with': 's.db,people,3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/sqlite3.fbi]执行第[33]原语 a = @udf CRUD.delete_object_stable with (s.db,peop... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],35

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



