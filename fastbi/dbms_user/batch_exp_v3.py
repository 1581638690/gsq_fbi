#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: dbms_user/batch_exp
#datetime: 2024-08-30T16:10:56.951887
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
		add_the_error('[dbms_user/batch_exp.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'v', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '@ids,replace("|",",")'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[17]原语 v = @sdf sys_str with (@ids,replace("|",",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ids1', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '@ids==""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[19]原语 ids1 = @sdf sys_eval with (@ids=="") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'a', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$ids1,"datas =@udf CRUD.load_mysql_sql with (@link,select * from @table)"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[22]原语 a = @sdf sys_if_run with ($ids1,"datas =@udf CRUD.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'a', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$ids1,"datas =@udf CRUD.load_mysql_sql with (@link,select * from @table where id in ($v))"'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[25]原语 a = @sdf sys_unif_run with ($ids1,"datas =@udf CRU... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'gmt_create,gmt_modified,creator,owner,id,a,b,req_label,res_llabel'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[27]原语 datas = loc datas drop gmt_create,gmt_modified,cre... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.first', 'Action': 'lambda', 'lambda': 'first_time', 'by': 'x:x[0:19]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[28]原语 datas.first = lambda first_time by (x:x[0:19]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'datas.last', 'Action': 'lambda', 'lambda': 'last_time', 'by': 'x:x[0:19]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[29]原语 datas.last = lambda last_time by (x:x[0:19]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'first_time,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[30]原语 datas = loc datas drop first_time,last_time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[31]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'active', 'Action': 'add', 'add': 'id', 'by': 'active.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[32]原语 active  = add id by active.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'active', 'as': '"value":"活跃状态"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[33]原语 rename active as ("value":"活跃状态") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'datas', 'Action': 'alter', 'alter': 'datas.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[34]原语 datas = alter datas.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,active', 'by': 'active,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[35]原语 datas = join datas,active by active,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:sensitive_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[37]原语 sens = load ssdb by ssdb0 with dd:sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'id', 'by': 'sens.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[38]原语 sens = add id by sens.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': '"value":"敏感等级"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[39]原语 rename sens as ("value":"敏感等级") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= alter', 'Ta': 'datas', 'Action': 'alter', 'alter': 'datas.sensitive_label', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[40]原语 datas = alter datas.sensitive_label as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'datas', 'Action': 'join', 'join': 'datas,sens', 'by': 'sensitive_label,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[41]原语 datas = join datas,sens by sensitive_label,id with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'datas', 'Action': 'loc', 'loc': 'datas', 'drop': 'sensitive_label,active,id_x,id_y'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[42]原语 datas = loc datas drop sensitive_label,active,id_x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'datas', 'Action': '@udf', '@udf': 'datas', 'by': 'udf0.df_fillna', 'with': '无'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[43]原语 datas = @udf datas by udf0.df_fillna with (无) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'datas', 'as': '"user":"访问账号","dbms_obj":"数据库","db_type":"数据库类型","first":"首次被访问时间","last":"最后一次被访问时间","res_llabel_count":"返回标签及其数量","req_label_count":"请求标签及其数量","comment":"备注","count":"被访问量(次)"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[44]原语 rename datas as ("user":"访问账号","dbms_obj":"数据库","d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'datas', 'to': 'csv', 'by': '@file_name'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[46]原语 store datas to csv by @file_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[dbms_user/batch_exp.fbi]执行第[47]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],47

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



