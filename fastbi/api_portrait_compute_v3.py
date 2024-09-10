#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_portrait_compute
#datetime: 2024-08-30T16:10:53.319140
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
		add_the_error('[api_portrait_compute.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_type', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select url from data_api_new where api_type=0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[14]原语 url_type=load db by mysql1 with select url from da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'new_data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select urld,api_type,max(time) as latest_date from api_monitor where api_type!='0' group by urld,api_type"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[16]原语 new_data=load ckh by ckh with select urld,api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'join_data', 'Action': 'join', 'join': 'url_type,new_data', 'by': 'url,urld', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[18]原语 join_data=join url_type,new_data by url,urld with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'join_data2', 'Action': 'filter', 'filter': 'join_data', 'by': 'api_type not null'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[22]原语 join_data2=filter join_data by (api_type not null)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'store_data', 'Action': 'loc', 'loc': 'join_data2', 'drop': 'urld,latest_date'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[24]原语 store_data=loc join_data2 drop (urld,latest_date) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'store_data', 'by': 'api_type:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[26]原语 alter store_data by api_type:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'store_data', 'Action': '@udf', '@udf': 'store_data', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[28]原语 store_data = @udf store_data by CRUD.save_table wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_type'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[30]原语 drop url_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'new_data'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[31]原语 drop new_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'join_data'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[32]原语 drop join_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'join_data2'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[33]原语 drop join_data2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apilist11', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url,api,ltten_url from data_api_new where data_type not in ("JS","CSS","资源文件")'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[37]原语 apilist11 = load db by mysql1 with  (select id,url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'filter_df', 'Action': '@udf', '@udf': 'apilist11', 'by': 'handi_merge.ApiMerging'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[39]原语 filter_df=@udf apilist11 by handi_merge.ApiMerging... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'delete_df', 'Action': '@udf', '@udf': 'filter_df', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[41]原语 delete_df= @udf filter_df by udf0.df_set_index wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'delete_df', 'by': 'CRUD.delete_mobject_mtable', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[42]原语 @udf delete_df by CRUD.delete_mobject_mtable with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'api_portrait_compute'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[46]原语 aa = load ssdb by ssdb0 with api_portrait_compute 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[48]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_visit_hour'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=49
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[49]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[51]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[53]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[54]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_portrait_compute'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[55]原语 store aa to ssdb by ssdb0 with api_portrait_comput... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_visits_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url ,sum(visit_num) as visits_num1 from api_visit_hour where time >= '$time1' and time < '$time2' group by url"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[88]原语 url_visits_num = load ckh by ckh with select url ,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_dstip_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select a.url, count(a.url) as dstip_num from (select url,dstip from api_visit_hour group by url,dstip ) a group by a.url'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[90]原语 url_dstip_num = load ckh by ckh with select a.url,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'url_api', 'Action': 'join', 'join': 'url_visits_num,url_dstip_num', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[91]原语 url_api = join url_visits_num,url_dstip_num by url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_visits_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[92]原语 drop url_visits_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_dstip_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[93]原语 drop url_dstip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_account_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select a.url, count(a.url) as account_num from (select url,account from api_visit_hour where account is not null and account != '' group by url,account ) a group by a.url"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[95]原语 url_account_num = load ckh by ckh with select a.ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'url_api', 'Action': 'join', 'join': 'url_api,url_account_num', 'by': 'url,url', 'with': 'outer'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[96]原语 url_api = join url_api,url_account_num by url,url ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_account_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[97]原语 drop url_account_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_srcip_num', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select a.url, count(a.url) as srcip_num from (select url,srcip from api_visit_hour group by url,srcip ) a group by a.url'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[99]原语 url_srcip_num = load ckh by ckh with select a.url,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'url_api', 'Action': 'join', 'join': 'url_api,url_srcip_num', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[100]原语 url_api = join url_api,url_srcip_num by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_srcip_num'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[101]原语 drop url_srcip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_visits_flow', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select url, sum(visit_flow) as visits_flow1 from api_visit_hour where time >= '$time1' and time < '$time2' group by url"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[103]原语 url_visits_flow = load ckh by ckh with select url,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'url_api', 'Action': 'join', 'join': 'url_api,url_visits_flow', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[104]原语 url_api = join url_api,url_visits_flow by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_visits_flow'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[105]原语 drop url_visits_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url_lasttime', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select url, MAX(`time`) as last_time from api_visit_hour group by url'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[107]原语 url_lasttime = load ckh by ckh with select url, MA... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'url_lasttime', 'by': 'last_time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[108]原语 alter url_lasttime by last_time:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'url_api', 'Action': 'join', 'join': 'url_api,url_lasttime', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[109]原语 url_api = join url_api,url_lasttime by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_lasttime'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[110]原语 drop url_lasttime 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'url_api', 'Action': '@udf', '@udf': 'url_api', 'by': 'udf0.df_fillna_cols', 'with': 'visits_num1:0,dstip_num:0,account_num:0,srcip_num:0,visits_flow1:0,url:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[111]原语 url_api = @udf url_api by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apilist1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url,visits_num as visits_num2,visits_flow as visits_flow2 from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[115]原语 apilist1 = load db by mysql1 with  (select id,url,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'apilist1', 'Action': '@udf', '@udf': 'apilist1', 'by': 'udf0.df_fillna_cols', 'with': 'visits_num2:0,visits_flow2:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[116]原语 apilist1 = @udf apilist1 by udf0.df_fillna_cols wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'apilist1', 'Action': 'join', 'join': 'apilist1,url_api', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[117]原语 apilist1 = join apilist1,url_api by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'apilist1', 'Action': 'add', 'add': 'visits_num', 'by': 'df["visits_num1"]+df["visits_num2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[118]原语 apilist1 = add visits_num by df["visits_num1"]+df[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'apilist1', 'Action': 'add', 'add': 'visits_flow', 'by': 'df["visits_flow1"]+df["visits_flow2"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[119]原语 apilist1 = add visits_flow by df["visits_flow1"]+d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'apilist1', 'Action': 'loc', 'loc': 'apilist1', 'by': 'id,url,visits_flow,visits_num,dstip_num,srcip_num,account_num,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[120]原语 apilist1 = loc apilist1 by id,url,visits_flow,visi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'url_api'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[121]原语 drop url_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'apilist', 'Action': '@udf', '@udf': 'apilist1', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[123]原语 apilist = @udf apilist1 by udf0.df_set_index with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'apilist.last_time', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[124]原语 alter apilist.last_time as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'apilist', 'Action': '@udf', '@udf': 'apilist', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[125]原语 apilist = @udf apilist by CRUD.save_table with (my... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_portrait_compute.fbi]执行第[127]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],127

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



