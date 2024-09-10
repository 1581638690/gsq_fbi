#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: system/user_man/delete_users
#datetime: 2024-08-30T16:10:56.647272
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
		add_the_error('[system/user_man/delete_users.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'users1', 'Action': '@sdf', '@sdf': 'sys_define', 'with': '@users'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[15]原语 users1 = @sdf sys_define with @users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[16]原语 df1 = @udf udf0.new_df with (name) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df1', 'by': 'udf0.df_append', 'with': '$users1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[17]原语 df2 = @udf df1 by udf0.df_append with ($users1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'df2.name', 'Action': 'str', 'str': 'name', 'by': 'split("|")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[18]原语 df2.name=str name by (split("|")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_l2df', 'with': 'name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[19]原语 df3 = @udf df2 by udf0.df_l2df with name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_set_index', 'with': 'Seq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[20]原语 df3 = @udf df3 by udf0.df_set_index with (Seq) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd1', 'Action': '@udf', '@udf': 'df3', 'by': 'udfA.drop_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[22]原语 dd1=@udf df3 by udfA.drop_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd2', 'Action': '@udf', '@udf': 'df3', 'by': 'SSDB2.del_option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[24]原语 dd2=@udf df3 by SSDB2.del_option 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dd3', 'Action': '@udf', '@udf': 'df3', 'by': 'CRUD.batch_delete_users', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[26]原语 dd3 = @udf df3 by CRUD.batch_delete_users with (@l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[system/user_man/delete_users.fbi]执行第[28]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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



