#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: dpdk_7day
#datetime: 2024-08-30T16:10:54.531593
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
		add_the_error('[dpdk_7day.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[7]原语 day = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day,"%Y-%m-%dT%H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[8]原语 day = @sdf format_now with ($day,"%Y-%m-%dT%H:00:0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-7d'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[9]原语 day1 = @sdf sys_now with -7d 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'day1', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$day1,"%Y-%m-%dT%H:00:00"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[10]原语 day1 = @sdf format_now with ($day1,"%Y-%m-%dT%H:00... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'ZNSM.dpdk_stats'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[12]原语 aa = @udf ZNSM.dpdk_stats 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= assert', 'Ta': 'dd', 'Action': 'assert', 'assert': "find_df('aa',ptree)", 'as': 'altert', 'with': '数据库查询失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[14]原语 dd = assert find_df("aa",ptree) as altert with 数据库... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'not dd', 'with': 'aa = @udf udf0.new_df with ipackets,ibytes,imissed,处理率'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=15
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[15]原语 if not dd with aa = @udf udf0.new_df with ipackets... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'aa.index.size == 0', 'with': 'aa = @udf aa by udf0.df_append with (0,0,0,0)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=16
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[16]原语 if aa.index.size == 0 with aa = @udf aa by udf0.df... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'aa', 'Action': 'add', 'add': 'times', 'by': "'$day'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[17]原语 aa = add times by ("$day") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'bb', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dbdk_day'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[19]原语 bb = load ssdb by ssdb0 with dbdk_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'bb', 'Action': 'filter', 'filter': 'bb', 'by': "times >= '$day1'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[21]原语 bb = filter bb by times >= "$day1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'dd', 'Action': 'union', 'union': 'aa,bb'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[23]原语 dd = union aa,bb 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dd', 'Action': 'loc', 'loc': 'dd', 'by': 'times,ipackets,ibytes,imissed,处理率'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[24]原语 dd = loc dd by times,ipackets,ibytes,imissed,处理率 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'dd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dbdk_day'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[26]原语 store dd to ssdb by ssdb0 with dbdk_day 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'loginl as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[31]原语 a = load ssdb by ssdb0 with loginl as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["login_pwdTime"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[32]原语 b = jaas a by a["login_pwdTime"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'user', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select name,left(gmt_modified,10) gmt_modified,curdate() now from user'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[33]原语 user = load db by mysql1 with select name,left(gmt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udfA.get_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[34]原语 user = @udf udfA.get_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'user', 'Action': 'loc', 'loc': 'user', 'by': 'name,modificationdate'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[35]原语 user = loc user by name,modificationdate 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'now', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[36]原语 now = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'user', 'Action': 'add', 'add': 'now', 'by': "'$now'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[37]原语 user = add now by ("$now") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'user.modificationdate', 'Action': 'lambda', 'lambda': 'modificationdate', 'by': 'x: int(str(x).split(".")[0])'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[38]原语 user.modificationdate = lambda modificationdate by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'user.modificationdate', 'Action': 'lambda', 'lambda': 'modificationdate', 'by': 'x:time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(x))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[39]原语 user.modificationdate = lambda modificationdate by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'user', 'by': '"modificationdate":"gmt_modified"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[40]原语 rename user by ("modificationdate":"gmt_modified")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'user.gmt_modified', 'Action': 'lambda', 'lambda': 'gmt_modified', 'by': 'x: x.split(" ")[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[41]原语 user.gmt_modified = lambda gmt_modified by x: x.sp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'user.now', 'Action': 'lambda', 'lambda': 'now', 'by': 'x: x.split(" ")[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[42]原语 user.now = lambda now by x: x.split(" ")[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'user', 'Action': 'add', 'add': 'time', 'by': '$b - 10'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[43]原语 user = add time by $b - 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'user.gmt_modified', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[44]原语 alter user.gmt_modified as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'user.now', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[45]原语 alter user.now as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_row_lambda', 'with': "x:'t' if (x[2] - x[1]).days >= x[3] else 'f'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[46]原语 user = @udf user by udf0.df_row_lambda with x:"t" ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'user', 'Action': 'filter', 'filter': 'user', 'by': "lambda1 == 't'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[47]原语 user = filter user by lambda1 == "t" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'user', 'Action': 'filter', 'filter': 'user', 'by': "name != 'superFBI'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[48]原语 user = filter user by name != "superFBI" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'user', 'with': 'name = $1', 'run': '""\ntime = eval user by iloc[0,3]\nassert False as notice push @name with 密码即将到期，请及时修改密码！\n""'}
	try:
		ptree['lineno']=49
		ptree['funs']=block_foreach_49
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[49]原语 foreach user run "time = eval user by iloc[0,3]ass... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[dpdk_7day.fbi]执行第[54]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],54

#主函数结束,开始块函数

def block_foreach_49(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'time', 'Action': 'eval', 'eval': 'user', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[50]原语 time = eval user by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'False', 'as': 'notice', 'push': '@name', 'with': '密码即将到期，请及时修改密码！'}
	ptree['push'] = replace_ps(ptree['push'],runtime)
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[第49行foreach语句中]执行第[51]原语 assert False as notice push @name with 密码即将到期，请及时修... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_49

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



