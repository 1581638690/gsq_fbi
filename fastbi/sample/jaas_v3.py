#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/jaas
#datetime: 2024-08-30T16:10:57.206263
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'd', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dashboard2:001 as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[6]原语 d = load ssdb by ssdb0 with dashboard2:001 as json... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'j2', 'Action': 'jaas', 'jaas': 'd', 'by': 'json.dumps(d)', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[9]原语 j2 = jaas d by json.dumps(d) as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'content', 'by': "'$j2'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[11]原语 a = add content by ("$j2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[13]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'j3', 'Action': 'jaas', 'jaas': 'j3', 'by': "json.loads('$j2')"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[16]原语 j3 = jaas j3 by json.loads("$j2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'jaas', 'jaas': 'j47', 'by': 'j47["1"]=1'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[19]原语 jaas j47 by j47["1"]=1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'j3', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'test:0'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/jaas.fbi]执行第[22]原语 store j3 to ssdb by ssdb0 with test:0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],22

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



