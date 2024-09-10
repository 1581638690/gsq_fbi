#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: auth_update
#datetime: 2024-08-30T16:10:55.192371
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
		add_the_error('[auth_update.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url,auth_type from data_api_new where auth_type=0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[6]原语 url_type=load db by mysql1 with select id,url,auth... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'new_data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select urld,auth_type,max(time) as latest_date from api_monitor where auth_type!=0 group by urld,auth_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[9]原语 new_data=load ckh by ckh with select urld,auth_typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'join_data', 'Action': 'join', 'join': 'url_type,new_data', 'by': 'url,urld', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[11]原语 join_data=join url_type,new_data by url,urld with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'join_data2', 'Action': 'filter', 'filter': 'join_data', 'by': 'urld not null'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[15]原语 join_data2=filter join_data by (urld not null) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_data2', 'Action': '@udf', '@udf': 'join_data2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[16]原语 join_data2= @udf join_data2 by udf0.df_set_index w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'store_data', 'Action': 'loc', 'loc': 'join_data2', 'drop': 'urld,latest_date,auth_type_x'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[18]原语 store_data=loc join_data2 drop (urld,latest_date,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'store_data', 'as': '{"auth_type_y":"auth_type"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[19]原语 rename store_data as {"auth_type_y":"auth_type"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'store_data.auth_type', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[21]原语 alter store_data.auth_type as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'store_data', 'Action': '@udf', '@udf': 'store_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[23]原语 store_data = @udf store_data by CRUD.save_table wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_type'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[25]原语 drop url_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'new_data'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[26]原语 drop new_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'join_data'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[27]原语 drop join_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'join_data2'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[28]原语 drop join_data2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[auth_update.fbi]执行第[30]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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



