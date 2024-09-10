#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: pot_user/save_table
#datetime: 2024-08-30T16:10:56.350072
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
		add_the_error('[pot_user/save_table.fea]执行第[1]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[4]原语 t = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 't', 'Action': 'loc', 'loc': 't', 'by': 'drop', 'drop': 'sys_role'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[5]原语 t = loc t by drop sys_role 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'a', 'Action': 'filter', 'filter': 't', 'by': "name != 'admin'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[8]原语 a = filter t by name != "admin" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'a', 'by': 'df.index.size > 0', 'as': 'break', 'with': '不能添加admin用户，权限不足！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[pot_user/save_table.fea]执行第[10]原语 assert a by df.index.size... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[10]原语 assert a by df.index.size > 0 as break with "不能添加a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'name', 'Action': 'eval', 'eval': 'a', 'by': 'get_value(0,"name")'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[11]原语 name=eval a by (get_value(0,"name")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'g', 'Action': '@udf', '@udf': 'CRUD.exec_mysql_sql', 'with': '@link,select * from @table where name="$name"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[14]原语 g = @udf CRUD.exec_mysql_sql with (@link,select * ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'g', 'by': 'df.index.size == 0', 'as': 'break', 'with': '用户已存在！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[pot_user/save_table.fea]执行第[15]原语 assert g by df.index.size... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[15]原语 assert g by df.index.size == 0 as break with "用户已存... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 't', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[18]原语 b = @udf t by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udf0.df_fillna', 'with': "''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[19]原语 b = @udf b by udf0.df_fillna with ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udf0.df_drop_col', 'with': 'gmt_create,gmt_modified'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[20]原语 b = @udf b by udf0.df_drop_col with (gmt_create,gm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[21]原语 b = @udf b by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value,type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[23]原语 q = @udf udf0.new_df with (name,value,type) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'limit,100,sys'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[24]原语 q = @udf q by udf0.df_append with (limit,100,sys) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'q', 'by': 'udf0.df_append', 'with': 'gmt_modified,desc,order'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[25]原语 q = @udf q by udf0.df_append with (gmt_modified,de... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df,count', 'Action': '@udf', '@udf': 'q', 'by': 'CRUD.query_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[27]原语 df,count = @udf q by CRUD.query_table with (@link,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'df', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[29]原语 push df as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'count', 'to': 'count'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[30]原语 push count to count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[pot_user/save_table.fea]执行第[33]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],33

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



