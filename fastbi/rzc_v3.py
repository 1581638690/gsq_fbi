#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: rzc
#datetime: 2024-08-30T16:10:55.028901
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'df', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,app,url from data_api_new where app = "10.18.80.25:8215"'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[2]原语 df=load db by mysql1 with select id,app,url from d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df', 'to': 'pkl', 'by': 'aa.pkl'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[3]原语 store df to pkl by aa.pkl 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df.app2', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x.replace("10.18.80.25","59.202.68.95")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[4]原语 df.app2 = lambda app by x:x.replace("10.18.80.25",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df.url2', 'Action': 'lambda', 'lambda': 'url', 'by': 'x:x.replace("10.18.80.25","59.202.68.95")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[5]原语 df.url2 = lambda url by x:x.replace("10.18.80.25",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df', 'Action': 'loc', 'loc': 'df', 'drop': 'url,app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[6]原语 df = loc df drop (url,app) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'df', 'as': '"url2":"url","app2":"app"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[7]原语 rename df as ("url2":"url","app2":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'df', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[8]原语 df = @udf df by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'df', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[rzc.fbi]执行第[9]原语 aa = @udf df by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],9

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



