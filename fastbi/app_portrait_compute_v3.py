#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_portrait_compute
#datetime: 2024-08-30T16:10:54.589311
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
		add_the_error('[app_portrait_compute.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'app_portrait_compute'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[16]原语 aa = load ssdb by ssdb0 with app_portrait_compute 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[18]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_visit_hour'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=19
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[19]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[21]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[23]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[24]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_portrait_compute'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[25]原语 store aa to ssdb by ssdb0 with app_portrait_comput... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_visits_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app ,sum(visit_num) as visits_num1 from api_visit_hour where time >= '$time1' and time < '$time2' and app is not null group by app"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[29]原语 app_visits_num = load ckh by ckh with select app ,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_resl', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,count(res_llabel) as res_label from data_api_new where res_llabel != "" and app != "" group by app '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[31]原语 app_resl = @udf RS.load_mysql_sql with (mysql1,sel... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_resl,app_visits_num', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[32]原语 app_api = join app_resl,app_visits_num by app,app ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_visits_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[33]原语 drop app_visits_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_resl'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[34]原语 drop app_resl 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_reql', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,count(req_label) as req_label from data_api_new where req_label != "" and app != "" group by app '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[35]原语 app_reql = @udf RS.load_mysql_sql with (mysql1,sel... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_reql', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[36]原语 app_api = join app_api,app_reql by app,app with ou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_reql'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[37]原语 drop app_reql 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_monitor', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app,count() as sj_num from api_monitor group by app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[39]原语 app_monitor = load ckh by ckh with select app,coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_monitor', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[40]原语 app_api = join app_api,app_monitor by app,app with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_monitor'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[41]原语 drop app_monitor 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_imp', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select app,count(url) as imp_api_num from data_api_new where api_status = '1' group by app"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[43]原语 app_imp = @udf RS.load_mysql_sql with (mysql1,sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_imp', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[44]原语 app_api = join app_api,app_imp by app,app with out... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_imp'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[45]原语 drop app_imp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_fl', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select url,sum(content_length) as visits_flow from api_monitor group by url'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[47]原语 url_fl = load ckh by ckh with select url,sum(conte... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_app', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct url,app from api_monitor'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[48]原语 url_app = load ckh by ckh with select distinct url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'url_sj', 'Action': 'join', 'join': 'url_fl,url_app', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[49]原语 url_sj = join url_fl,url_app by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'url_sj', 'Action': 'distinct', 'distinct': 'url_sj', 'by': 'url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[50]原语 url_sj = distinct url_sj by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_fl'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[51]原语 drop url_fl 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'url_sj', 'Action': 'loc', 'loc': 'url_sj', 'drop': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[52]原语 url_sj = loc url_sj drop url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'url_sj', 'Action': 'group', 'group': 'url_sj', 'by': 'app', 'agg': 'visits_flow:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[53]原语 url_sj = group url_sj by app agg visits_flow:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'url_sj', 'as': '"visits_flow_sum":"monitor_flow"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[54]原语 rename url_sj as ("visits_flow_sum":"monitor_flow"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,url_sj', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[55]原语 app_api = join app_api,url_sj by app,app with oute... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_sj'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[56]原语 drop url_sj 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_api_num', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,count(url) as api_num from data_api_new where merge_state != 1 group by app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[58]原语 app_api_num = @udf RS.load_mysql_sql with (mysql1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,app_sum from data_app_new where merge_state != 0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[60]原语 app = load db by mysql1 with select app,app_sum fr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_fillna_cols', 'with': "app_sum:'0'"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[62]原语 app = @udf app by udf0.df_fillna_cols with app_sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app1', 'Action': 'filter', 'filter': 'app', 'by': "app_sum != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[63]原语 app1 = filter app by app_sum != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aaa', 'Action': 'loc', 'loc': 'app1', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[64]原语 aaa = loc app1 by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'aaa.index.size == 0', 'with': 'aaa = @udf aaa by udf0.df_append with ()'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=65
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[65]原语 if aaa.index.size == 0 with aaa = @udf aaa by udf0... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app11', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'app,api_num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[66]原语 app11 = @udf udf0.new_df with app,api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'aaa', 'with': 'app=$1', 'run': '""\napp_1 = filter app1 by app == \'@app\'\napp_1.app_sum = lambda app_sum by (x:x.split(","))\napp_1 = @udf app_1 by udf0.df_l2cs with app_sum\napp_1 = @udf app_1 by udf0.df_reset_index\napp_1 = loc app_1 drop index,app,app_sum\napp_1 = @udf app_1 by udf0.df_T\nrename app_1 as (0:\'app\')\napp_1 = join app_1,app_api_num by app,app with left\napp_1 = add aa by 1\napp_1 = group app_1 by aa agg api_num:sum\naa_num = eval app_1 by iloc[0,0]\napp11 = @udf app11 by udf0.df_append with (@app,$aa_num)\n""'}
	try:
		ptree['lineno']=67
		ptree['funs']=block_foreach_67
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[67]原语 foreach aaa run "app_1 = filter app1 by app == "@a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app_api_num', 'Action': 'union', 'union': 'app_api_num,app11'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[81]原语 app_api_num = union app_api_num,app11 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_api_num', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[83]原语 app_api = join app_api,app_api_num by app,app with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_api_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[84]原语 drop app_api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_account_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select a.app, count(a.app) as account_num from (select app,account,sum(visit_num) as num from api_visit_hour where account != '' group by app,account ) a group by a.app"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[86]原语 app_account_num = load ckh by ckh with select a.ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_account_num', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[87]原语 app_api = join app_api,app_account_num by app,app ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_account_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[88]原语 drop app_account_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_srcip_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select a.app, count(a.app) as srcip_num from (select srcip,app from api_visit_hour group by app,srcip ) a group by a.app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[90]原语 app_srcip_num = load ckh by ckh with select a.app,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_srcip_num', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[91]原语 app_api = join app_api,app_srcip_num by app,app wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_srcip_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[92]原语 drop app_srcip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_visits_flow', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app, sum(visit_flow) as visits_flow1 from api_visit_hour where time >= '$time1' and time < '$time2' group by app"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[94]原语 app_visits_flow = load ckh by ckh with select app,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_visits_flow', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[95]原语 app_api = join app_api,app_visits_flow by app,app ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_visits_flow'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[96]原语 drop app_visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_dstip_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select a.app, count(a.app) as dstip_num from (select dstip,app from api_visit_hour group by app,dstip ) a group by a.app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[98]原语 app_dstip_num = load ckh by ckh with select a.app,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_dstip_num', 'by': 'app,app', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[99]原语 app_api = join app_api,app_dstip_num by app,app wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_dstip_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[100]原语 drop app_dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_api', 'Action': '@udf', '@udf': 'app_api', 'by': 'udf0.df_fillna_cols', 'with': 'visits_num1:0,req_label:0,imp_api_num:0,account_num:0,srcip_num:0,visits_flow1:0,dstip_num:0,res_label:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[101]原语 app_api = @udf app_api by  udf0.df_fillna_cols wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_lasttime', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app, MAX(`time`) as last_time from api_visit_hour group by app'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[104]原语 app_lasttime = load ckh by ckh with select app, MA... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_lasttime', 'by': 'last_time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[105]原语 alter app_lasttime by last_time:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_api', 'Action': 'join', 'join': 'app_api,app_lasttime', 'by': 'app,app'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[106]原语 app_api = join app_api,app_lasttime by app,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app_lasttime'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[107]原语 drop app_lasttime 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist1', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select id,app,visits_num as visits_num2,visits_flow as visits_flow2 from data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[110]原语 applist1 = @udf RS.load_mysql_sql with (mysql1,sel... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist1', 'Action': '@udf', '@udf': 'applist1', 'by': 'udf0.df_fillna_cols', 'with': 'visits_num2:0,visits_flow2:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[111]原语 applist1 = @udf applist1 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'applist1', 'Action': 'join', 'join': 'applist1,app_api', 'by': 'app,app'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[113]原语 applist1 = join applist1,app_api by app,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'applist1', 'Action': 'add', 'add': 'visits_num', 'by': 'df["visits_num1"]+df["visits_num2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[115]原语 applist1 = add visits_num by df["visits_num1"]+df[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'applist1', 'Action': 'add', 'add': 'visits_flow', 'by': 'df["visits_flow1"]+df["visits_flow2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[116]原语 applist1 = add visits_flow by df["visits_flow1"]+d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'applist1', 'Action': 'loc', 'loc': 'applist1', 'by': 'id,app,dstip_num,visits_num,visits_flow,srcip_num,account_num,res_label,req_label,sj_num,imp_api_num,monitor_flow,api_num,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[117]原语 applist1 = loc applist1 by id,app,dstip_num,visits... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist1', 'Action': '@udf', '@udf': 'applist1', 'by': 'udf0.df_fillna_cols', 'with': 'api_num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[119]原语 applist1 = @udf applist1 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist1', 'Action': '@udf', '@udf': 'applist1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[120]原语 applist1 = @udf applist1 by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'applist1', 'Action': '@udf', '@udf': 'applist1', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[121]原语 applist1 = @udf applist1 by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'applist1', 'Action': 'loc', 'loc': 'applist1', 'by': 'app,visits_num,visits_flow,api_num,srcip_num,account_num,imp_api_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[122]原语 applist1 = loc applist1 by (app,visits_num,visits_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct app,dstip from api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[146]原语 app = load ckh by ckh with select distinct app,dst... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[148]原语 app.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app', 'Action': 'group', 'group': 'app', 'by': 'app', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[149]原语 app = group app by app agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[150]原语 app = @udf app by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app', 'by': '"dstip_sum":"dstip"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[151]原语 rename app by ("dstip_sum":"dstip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[152]原语 app.dstip = lambda dstip by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[153]原语 app.dstip = lambda dstip by x:set(x.split(",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app', 'by': 'dstip:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[154]原语 alter app by dstip:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:x.replace("{",\'\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[155]原语 app.dstip = lambda dstip by x:x.replace("{","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:x.replace("}",\'\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[156]原语 app.dstip = lambda dstip by x:x.replace("}","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:x.replace("\'",\'\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[157]原语 app.dstip = lambda dstip by x:x.replace(","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:x.replace(" ",\'\')'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[158]原语 app.dstip = lambda dstip by x:x.replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app2', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,id from data_app_new where app_type = 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[159]原语 app2 = load db by mysql1 with select app,id from d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dstip', 'Action': 'join', 'join': 'app2,app', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[160]原语 dstip = join app2,app by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app2'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[161]原语 drop app2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'app'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[162]原语 drop app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dstip', 'Action': '@udf', '@udf': 'dstip', 'by': 'udf0.df_fillna_cols', 'with': 'dstip:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[163]原语 dstip = @udf dstip by udf0.df_fillna_cols with dst... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dstip', 'Action': '@udf', '@udf': 'dstip', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[164]原语 dstip = @udf dstip by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dstip', 'Action': '@udf', '@udf': 'dstip', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[165]原语 dstip = @udf dstip by CRUD.save_table with (mysql1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'dstip'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[166]原语 drop dstip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_portrait_compute.fbi]执行第[190]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],190

#主函数结束,开始块函数

def block_foreach_67(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_1', 'Action': 'filter', 'filter': 'app1', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[68]原语 app_1 = filter app1 by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_1.app_sum', 'Action': 'lambda', 'lambda': 'app_sum', 'by': 'x:x.split(",")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[69]原语 app_1.app_sum = lambda app_sum by (x:x.split(","))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_l2cs', 'with': 'app_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[70]原语 app_1 = @udf app_1 by udf0.df_l2cs with app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[71]原语 app_1 = @udf app_1 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_1', 'Action': 'loc', 'loc': 'app_1', 'drop': 'index,app,app_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[72]原语 app_1 = loc app_1 drop index,app,app_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_1', 'Action': '@udf', '@udf': 'app_1', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[73]原语 app_1 = @udf app_1 by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_1', 'as': "0:'app'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[74]原语 rename app_1 as (0:"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_1', 'Action': 'join', 'join': 'app_1,app_api_num', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[75]原语 app_1 = join app_1,app_api_num by app,app with lef... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app_1', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[76]原语 app_1 = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app_1', 'Action': 'group', 'group': 'app_1', 'by': 'aa', 'agg': 'api_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[77]原语 app_1 = group app_1 by aa agg api_num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'app_1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[78]原语 aa_num = eval app_1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app11', 'Action': '@udf', '@udf': 'app11', 'by': 'udf0.df_append', 'with': '@app,$aa_num'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第67行foreach语句中]执行第[79]原语 app11 = @udf app11 by udf0.df_append with (@app,$a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_67

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



