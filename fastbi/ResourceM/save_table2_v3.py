#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: ResourceM/save_table2
#datetime: 2024-08-30T16:10:56.490263
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
		add_the_error('[ResourceM/save_table2.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[12]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[18]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'b', 'by': 'b.index.size >0', 'as': 'break', 'to': '保存成功！', 'with': '保存失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[ResourceM/save_table2.fbi]执行第[20]原语 assert b by b.index.size ... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[20]原语 assert b by b.index.size >0 as break to 保存成功！ with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd', 'Action': '@udf', '@udf': 'CRUD.load_mysql_sql', 'with': '@link,select gid,gname from @table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[23]原语 dd = @udf  CRUD.load_mysql_sql with @link,select g... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'dd', 'by': 'gid', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[24]原语 dd = loc dd by gid to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dd', 'as': '{"gname":"value"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[25]原语 rename dd as {"gname":"value"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:resource_group'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[26]原语 store dd to ssdb by ssdb0 with dd:resource_group 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[30]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[ResourceM/save_table2.fbi]执行第[32]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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



