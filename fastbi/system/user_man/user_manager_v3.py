#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: system/user_man/user_manager
#datetime: 2024-08-30T16:10:56.625268
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
		add_the_error('[system/user_man/user_manager.fbi]执行第[17]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udfA.get_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[21]原语 aa = @udf udfA.get_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'SSDB2.scan_user_option', 'with': 'user_option:,1000'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[23]原语 bb =@udf SSDB2.scan_user_option with (user_option:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 's_r', 'Action': 'join', 'join': 'aa,bb', 'by': '[name],[name]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[25]原语 s_r = join aa,bb by  [name],[name] with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's_r', 'Action': '@udf', '@udf': 's_r', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[27]原语 s_r = @udf s_r by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'm_r', 'Action': '@udf', '@udf': 'CRUD.load_mysql_sql', 'with': '@link,select id,name from @table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[31]原语 m_r = @udf CRUD.load_mysql_sql with (@link,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'join_r', 'Action': 'join', 'join': 's_r,m_r', 'by': '[name],[name]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[33]原语 join_r = join s_r,m_r by  [name],[name] with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_r', 'Action': '@udf', '@udf': 'join_r', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[35]原语 join_r = @udf join_r by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'join_r', 'Action': 'loc', 'loc': 'join_r', 'by': 'drop', 'drop': 'analyst'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[37]原语 join_r = loc join_r by drop analyst 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'join_r', 'Action': '@udf', '@udf': 'join_r', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[40]原语 join_r = @udf join_r by udf0.df_set_index with (id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'r', 'Action': '@udf', '@udf': 'join_r', 'by': 'CRUD.save_object_mtable', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[42]原语 r = @udf join_r by CRUD.save_object_mtable with (@... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's_r', 'Action': '@udf', '@udf': 's_r', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[45]原语 s_r=@udf s_r by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'd_r', 'Action': 'join', 'join': 's_r,m_r', 'by': '[name],[name]', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[47]原语 d_r = join s_r,m_r by  [name],[name] with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd_r', 'Action': '@udf', '@udf': 'd_r', 'by': 'udf0.df_fillna', 'with': '-1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[49]原语 d_r=@udf d_r by udf0.df_fillna with (-1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'd_r1', 'Action': 'filter', 'filter': 'd_r', 'by': 'index==-1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[50]原语 d_r1 = filter d_r by (index==-1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd_r2', 'Action': '@udf', '@udf': 'd_r1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[51]原语 d_r2 = @udf d_r1 by udf0.df_set_index with (id) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd_r3', 'Action': '@udf', '@udf': 'd_r2', 'by': 'CRUD.delete_mobject_mtable', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[53]原语 d_r3 = @udf d_r2 by CRUD.delete_mobject_mtable wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[system/user_man/user_manager.fbi]执行第[55]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],55

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



