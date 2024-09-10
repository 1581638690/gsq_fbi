#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: account_portrait_compute
#datetime: 2024-08-30T16:10:55.306883
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
		add_the_error('[account_portrait_compute.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'account_portrait_compute'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[12]原语 aa = load ssdb by ssdb0 with account_portrait_comp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[14]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_visit_hour'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=15
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[15]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[16]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[18]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[19]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_portrait_compute'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[20]原语 store aa to ssdb by ssdb0 with account_portrait_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_visits_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account ,sum(visit_num) as visit_num1 from api_visit_hour where time >= '$time1' and time < '$time2' and account is not null group by account"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[24]原语 account_visits_num = load ckh by ckh with select a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_api_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select a.account, count(a.account) as api_num from (select url,account from api_visit_hour where account != '' group by url,account ) a group by a.account"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[26]原语 account_api_num = load ckh by ckh with select a.ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account_api', 'Action': 'join', 'join': 'account_visits_num,account_api_num', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[27]原语 account_api = join account_visits_num,account_api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_visits_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[28]原语 drop account_visits_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_api_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[29]原语 drop account_api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_ip_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select a.account, count(a.account) as ip_num from (select account,srcip from api_visit_hour where account != '' group by account,srcip ) a group by a.account"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[31]原语 account_ip_num = load ckh by ckh with select a.acc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account_api', 'Action': 'join', 'join': 'account_api,account_ip_num', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[32]原语 account_api = join account_api,account_ip_num by a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_ip_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[33]原语 drop account_ip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_app_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select a.account, count(a.account) as app_num from (select app,account from api_visit_hour where account != '' group by app,account ) a group by a.account"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[35]原语 account_app_num = load ckh by ckh with select a.ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account_api', 'Action': 'join', 'join': 'account_api,account_app_num', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[36]原语 account_api = join account_api,account_app_num by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_app_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[37]原语 drop account_app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_visits_flow', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account, sum(visit_flow) as visit_flow1 from api_visit_hour where time >= '$time1' and time < '$time2' and account != '' group by account"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[39]原语 account_visits_flow = load ckh by ckh with select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account_api', 'Action': 'join', 'join': 'account_api,account_visits_flow', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[40]原语 account_api = join account_api,account_visits_flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_visits_flow'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[41]原语 drop account_visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_lasttime', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select account, MAX(`time`) as lasttime from api_visit_hour where account != '' group by account"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[43]原语 account_lasttime = load ckh by ckh with select acc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'account_lasttime', 'by': 'lasttime:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[44]原语 alter account_lasttime by lasttime:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account_api', 'Action': 'join', 'join': 'account_api,account_lasttime', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[45]原语 account_api = join account_api,account_lasttime by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_lasttime'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[46]原语 drop account_lasttime 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'accountlist1', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select id,account,flag,dept,firsttime,visit_num as visit_num2,visit_flow as visit_flow2 from data_account_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[48]原语 accountlist1 = @udf RS.load_mysql_sql with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'accountlist1', 'Action': '@udf', '@udf': 'accountlist1', 'by': 'udf0.df_fillna_cols', 'with': 'account:0,flag:0,dept:0,visit_num2:0,visit_flow2:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[49]原语 accountlist1 = @udf accountlist1 by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'accountlist1', 'Action': 'join', 'join': 'accountlist1,account_api', 'by': 'account,account'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[50]原语 accountlist1 = join accountlist1,account_api by ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'accountlist1', 'Action': 'add', 'add': 'visit_num', 'by': 'df["visit_num1"]+df["visit_num2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[51]原语 accountlist1 = add visit_num by df["visit_num1"]+d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'accountlist1', 'Action': 'add', 'add': 'visit_flow', 'by': 'df["visit_flow1"]+df["visit_flow2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[52]原语 accountlist1 = add visit_flow by df["visit_flow1"]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'accountlist1', 'Action': 'loc', 'loc': 'accountlist1', 'by': 'id,account,flag,dept,firsttime,visit_num,visit_flow,lasttime,app_num,api_num,ip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[53]原语 accountlist1 = loc accountlist1 by id,account,flag... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'account_api'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[54]原语 drop account_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'accountlist1', 'Action': '@udf', '@udf': 'accountlist1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[55]原语 accountlist1 = @udf accountlist1 by udf0.df_set_in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'accountlist1', 'Action': '@udf', '@udf': 'accountlist1', 'by': 'CRUD.save_table', 'with': 'mysql1,data_account_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[56]原语 accountlist1 = @udf accountlist1 by CRUD.save_tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[account_portrait_compute.fbi]执行第[59]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],59

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



