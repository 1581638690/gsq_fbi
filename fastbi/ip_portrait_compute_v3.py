#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: ip_portrait_compute
#datetime: 2024-08-30T16:10:56.049634
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
		add_the_error('[ip_portrait_compute.fbi]执行第[8]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'ip_portrait_compute'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[11]原语 aa = load ssdb by ssdb0 with ip_portrait_compute 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[13]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_visit_hour'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=14
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[14]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[16]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[18]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[19]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip_portrait_compute'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[20]原语 store aa to ssdb by ssdb0 with ip_portrait_compute... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip_visits_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select srcip ,sum(visit_num) as visit_num1 from api_visit_hour where time >= '$time1' and time < '$time2' group by srcip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[25]原语 srcip_visits_num = load ckh by ckh with select src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip_api_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select a.srcip, count(a.srcip) as api_num from (select url,srcip from api_visit_hour group by url,srcip ) a group by a.srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[27]原语 srcip_api_num = load ckh by ckh with select a.srci... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srcip_api', 'Action': 'join', 'join': 'srcip_visits_num,srcip_api_num', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[28]原语 srcip_api = join srcip_visits_num,srcip_api_num by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_visits_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[29]原语 drop srcip_visits_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_api_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[30]原语 drop srcip_api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip_account_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select a.srcip, count(a.srcip) as account_num from (select srcip,account from api_visit_hour where account != '' group by srcip,account ) a group by a.srcip"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[32]原语 srcip_account_num = load ckh by ckh with select a.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srcip_api', 'Action': 'join', 'join': 'srcip_api,srcip_account_num', 'by': 'srcip,srcip', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[33]原语 srcip_api = join srcip_api,srcip_account_num by sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_account_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[34]原语 drop srcip_account_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip_app_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select a.srcip, count(a.srcip) as app_num from (select app,srcip from api_visit_hour group by app,srcip ) a group by a.srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[36]原语 srcip_app_num = load ckh by ckh with select a.srci... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srcip_api', 'Action': 'join', 'join': 'srcip_api,srcip_app_num', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[37]原语 srcip_api = join srcip_api,srcip_app_num by srcip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_app_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[38]原语 drop srcip_app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip_visits_flow', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select srcip, sum(visit_flow) as visit_flow1 from api_visit_hour where time >= '$time1' and time < '$time2' group by srcip"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[40]原语 srcip_visits_flow = load ckh by ckh with select sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srcip_api', 'Action': 'join', 'join': 'srcip_api,srcip_visits_flow', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[41]原语 srcip_api = join srcip_api,srcip_visits_flow by sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_visits_flow'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[42]原语 drop srcip_visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcip_api', 'Action': '@udf', '@udf': 'srcip_api', 'by': 'udf0.df_fillna_cols', 'with': 'visit_num1:0,api_num:0,srcip:0,account_num:0,app_num:0,visit_flow1:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[43]原语 srcip_api = @udf srcip_api by udf0.df_fillna_cols ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip_lasttime', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select srcip, MAX(`time`) as lasttime from api_visit_hour group by srcip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[45]原语 srcip_lasttime = load ckh by ckh with select srcip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'srcip_lasttime', 'by': 'lasttime:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[46]原语 alter srcip_lasttime by lasttime:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srcip_api', 'Action': 'join', 'join': 'srcip_api,srcip_lasttime', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[47]原语 srcip_api = join srcip_api,srcip_lasttime by srcip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_visits_flow'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[48]原语 drop srcip_visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srciplist1', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select id,srcip,region,type,flag,firsttime,network,visit_num as visit_num2,visit_flow as visit_flow2 from data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[50]原语 srciplist1 = @udf RS.load_mysql_sql with (mysql1,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srciplist1', 'Action': '@udf', '@udf': 'srciplist1', 'by': 'udf0.df_fillna_cols', 'with': 'visit_num2:0,network:0,srcip:0,visit_flow2:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[51]原语 srciplist1 = @udf srciplist1 by udf0.df_fillna_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srciplist1', 'Action': 'join', 'join': 'srciplist1,srcip_api', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[52]原语 srciplist1 = join srciplist1,srcip_api by srcip,sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'srciplist1', 'Action': 'add', 'add': 'visit_num', 'by': 'df["visit_num1"]+df["visit_num2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[53]原语 srciplist1 = add visit_num by df["visit_num1"]+df[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'srciplist1', 'Action': 'add', 'add': 'visit_flow', 'by': 'df["visit_flow1"]+df["visit_flow2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[54]原语 srciplist1 = add visit_flow by df["visit_flow1"]+d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srciplist1', 'Action': 'loc', 'loc': 'srciplist1', 'by': 'id,srcip,region,type,flag,firsttime,network,visit_num,visit_flow,app_num,api_num,account_num,lasttime'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[55]原语 srciplist1 = loc srciplist1 by id,srcip,region,typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'srcip_api'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[56]原语 drop srcip_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srciplist1', 'Action': '@udf', '@udf': 'srciplist1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[57]原语 srciplist1 = @udf srciplist1 by udf0.df_set_index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srciplist1', 'Action': '@udf', '@udf': 'srciplist1', 'by': 'CRUD.save_table', 'with': 'mysql1,data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[58]原语 srciplist1 = @udf srciplist1 by CRUD.save_table wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[ip_portrait_compute.fbi]执行第[60]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],60

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



