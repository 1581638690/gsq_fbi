#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: hx_ip_f
#datetime: 2024-08-30T16:10:53.804185
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
	
	
	ptree={'runtime': runtime, 'Action': 'use', 'use': 'hx_f'}
	try:
		use_fun(ptree)
		workspace=ptree['work_space']
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[7]原语 use hx_f 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'gl_ip', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'gl_ip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[10]原语 gl_ip = load ssdb by ssdb0 with gl_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'gl_ip', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[11]原语 gl_ip = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[12]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'a', 'Action': 'join', 'join': 'a,gl_ip', 'by': 'srcip,srcip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[13]原语 a = join a,gl_ip by srcip,srcip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'a', 'by': 'aa'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[14]原语 aa = loc a by aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'aa', 'Action': 'filter', 'filter': 'aa', 'by': 'aa != 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[15]原语 aa = filter aa by aa != 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('aa',ptree)", 'as': 'break', 'with': '终端概览界面的终端默认开启画像！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[hx_ip_f.fbi]执行第[16]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[16]原语 assert find_df_have_data("aa",ptree) as break with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'id,srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[19]原语 a = loc a by id,srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[20]原语 alter a.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'portrait_status', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[21]原语 a = add portrait_status by (0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[22]原语 a = @udf a by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[23]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'b', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[24]原语 push b as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': 'hx_f'}
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[hx_ip_f.fbi]执行第[28]原语 clear hx_f 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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



