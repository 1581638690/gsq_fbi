#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: app_dst3
#datetime: 2024-08-30T16:10:53.282417
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
		add_the_error('[app_dst3.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_dst', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app apps,dstip from data_app_new where dstip not like '%%,%%' and merge_state = 0 and app_type =1"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[54]原语 app_dst = load db by mysql1 with select app apps,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_dst', 'by': 'apps:string,dstip:string'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[55]原语 alter app_dst by apps:string,dstip:string 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps', 'Action': 'lambda', 'lambda': 'apps', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[57]原语 app_dst.apps = lambda apps by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app_dst', 'Action': 'group', 'group': 'app_dst', 'by': 'dstip', 'agg': 'apps:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[58]原语 app_dst = group app_dst by dstip agg apps:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps_sum', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:x[0:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[59]原语 app_dst.apps_sum = lambda apps_sum by x:x[0:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_dst', 'Action': '@udf', '@udf': 'app_dst', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[60]原语 app_dst = @udf app_dst by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.tf', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': "x:'t' if ',' in x else 'f'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[61]原语 app_dst.tf = lambda apps_sum by x:"t" if "," in x ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_dst', 'Action': 'filter', 'filter': 'app_dst', 'by': "tf == 't'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[62]原语 app_dst = filter app_dst by tf == "t" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_dst', 'Action': 'loc', 'loc': 'app_dst', 'by': 'dstip,apps_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[63]原语 app_dst = loc app_dst by dstip,apps_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_dst', 'as': '"dstip":"app"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[64]原语 rename app_dst as ("dstip":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps_sum', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[82]原语 app_dst.apps_sum = lambda apps_sum by x:set(x.spli... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_dst', 'by': 'apps_sum:string'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[83]原语 alter app_dst by apps_sum:string 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps_sum', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:x.replace("{","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[84]原语 app_dst.apps_sum = lambda apps_sum by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps_sum', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:x.replace("}","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[85]原语 app_dst.apps_sum = lambda apps_sum by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps_sum', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:x.replace("\'","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[86]原语 app_dst.apps_sum = lambda apps_sum by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dst.apps_sum', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:x.replace(" ","")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[87]原语 app_dst.apps_sum = lambda apps_sum by x:x.replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_dsts', 'Action': 'loc', 'loc': 'app_dst', 'by': 'app,apps_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[88]原语 app_dsts = loc app_dst by app,apps_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_dstss', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'app,apps_sum'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[89]原语 app_dstss = @udf udf0.new_df with app,apps_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'app_dst', 'with': 'app=$1,apps_sum=$2', 'run': '""\napp_dsts.tf = lambda apps_sum by x:\'t\' if set(\'@apps_sum\'.split(\',\')).intersection(x.split(",")) else \'f\'\napp_dsts2 = filter app_dsts by tf ==\'t\'\napp_dsts = filter app_dsts by tf ==\'f\'\napp_dsts2.tf = lambda app by x:\'t\' if \'@app\' == x else \'f\'\napp_dsts3 = filter app_dsts2 by tf ==\'t\'\napp_dstss = union app_dstss,app_dsts3\n""'}
	try:
		ptree['lineno']=90
		ptree['funs']=block_foreach_90
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[90]原语 foreach app_dst run "app_dsts.tf = lambda apps_sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_dst3', 'Action': 'loc', 'loc': 'app_dstss', 'by': 'app,apps_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[101]原语 app_dst3 = loc app_dstss by app,apps_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'app_dst3', 'with': 'app=$1,apps_sum=$2', 'run': '""\napps = @sdf sys_eval with (\'@apps_sum\'.split(\',\'))\napps = @sdf sys_eval with (str($apps)[1:-1])\napi_all = load db by mysql1 with select id,app_merges app from data_api_new where app in ($apps)\napi_all = add app_merges by (\'\')\napi_all = @udf api_all by udf0.df_set_index with id\n@udf api_all by CRUD.save_table with (mysql1,data_api_new)\napp_all = load db by mysql1 with select id,merge_state,visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active from data_app_new where app in ($apps) and merge_state =0 and app_type =1\napp = loc app_all by id,merge_state\napp = add merge_state by 1\napp = @udf app by udf0.df_set_index with id\napp = add app_merges by (\'@app\')\n@udf app by CRUD.save_table with (mysql1,data_app_new)\napp2 = loc app_all by visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active\napp2 = add app_merges by (\'@app\')\napp2 = add app by (\'@app\')\nalter app2.active as str\nalter app2.app_type as str\napp2 = group app2 by app agg visits_num:sum,visits_flow:sum,sj_num:sum,monitor_flow:sum,api_num:sum,imp_api_num:sum,srcip_num:sum,account_num:sum,dstip_num:sum,sensitive_label:sum,app_type:sum,app_status:sum,active:sum\napp2 = @udf app2 by udf0.df_reset_index\nrename app2 by ("visits_num_sum":"visits_num","visits_flow_sum":"visits_flow","sj_num_sum":"sj_num","monitor_flow_sum":"monitor_flow","api_num_sum":"api_num","imp_api_num_sum":"imp_api_num","srcip_num_sum":"srcip_num","account_num_sum":"account_num","dstip_num_sum":"dstip_num","sensitive_label_sum":"sensitive_label","app_type_sum":"app_type","app_status_sum":"app_status","active_sum":"active")\napp2 = add merge_state by 2\napp2.sensitive_label = lambda sensitive_label by x:1 if "1" in x else 0\napp2.app_type = lambda app_type by x:1 if "1" in x else 0\napp2.app_status = lambda app_status by x:1 if "1" in x else 0\napp2.active = lambda active by x:\'3\' if "3" in x else \'0\'\napp2.active = lambda active by x:\'1\' if "1" in x else \'0\'\nalter app2 by active:int,app_status:string,sensitive_label:string\n#alter app2.app_status as str\n#alter app2.sensitive_label as str\napp2 = add app_sum by (\'@apps_sum\')\napp2 = add first_time by str(datetime.now())\napp_merges = load db by mysql1 with select id,app from data_app_new where app = \'@app\' and merge_state = 2 and app_type =1\napp2 = join app2,app_merges by app,app with left\napp2 = @udf app2 by udf0.df_fillna with 0\napp2 = @udf app2 by udf0.df_set_index with id\n@udf app2 by CRUD.save_table with (mysql1,data_app_new)\n\n""'}
	try:
		ptree['lineno']=102
		ptree['funs']=block_foreach_102
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[102]原语 foreach app_dst3 run "apps = @sdf sys_eval with ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,app_sum from data_app_new where merge_state = 2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[142]原语 app =  @udf RS.load_mysql_sql with (mysql1,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[143]原语 app = @udf app by udf0.df_set_index with app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app', 'by': 'app.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[144]原语 app = add app by (app.index) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'SSDB.hclear', 'with': 'app_merge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[145]原语 a=@udf SSDB.hclear with app_merge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_merge', 'as': 'H'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[146]原语 store app to ssdb by ssdb0 with app_merge as H 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[app_dst3.fbi]执行第[152]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],152

#主函数结束,开始块函数

def block_foreach_90(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dsts.tf', 'Action': 'lambda', 'lambda': 'apps_sum', 'by': 'x:\'t\' if set(\'@apps_sum\'.split(\',\')).intersection(x.split(",")) else \'f\''}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[91]原语 app_dsts.tf = lambda apps_sum by x:"t" if set("@ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_dsts2', 'Action': 'filter', 'filter': 'app_dsts', 'by': "tf =='t'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[92]原语 app_dsts2 = filter app_dsts by tf =="t" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_dsts', 'Action': 'filter', 'filter': 'app_dsts', 'by': "tf =='f'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[93]原语 app_dsts = filter app_dsts by tf =="f" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_dsts2.tf', 'Action': 'lambda', 'lambda': 'app', 'by': "x:'t' if '@app' == x else 'f'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[94]原语 app_dsts2.tf = lambda app by x:"t" if "@app" == x ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_dsts3', 'Action': 'filter', 'filter': 'app_dsts2', 'by': "tf =='t'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[95]原语 app_dsts3 = filter app_dsts2 by tf =="t" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app_dstss', 'Action': 'union', 'union': 'app_dstss,app_dsts3'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第90行foreach语句中]执行第[96]原语 app_dstss = union app_dstss,app_dsts3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_90

def block_foreach_102(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'apps', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': "'@apps_sum'.split(',')"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[103]原语 apps = @sdf sys_eval with ("@apps_sum".split(","))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'apps', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'str($apps)[1:-1]'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[104]原语 apps = @sdf sys_eval with (str($apps)[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_all', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,app_merges app from data_api_new where app in ($apps)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[105]原语 api_all = load db by mysql1 with select id,app_mer... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api_all', 'Action': 'add', 'add': 'app_merges', 'by': "''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[106]原语 api_all = add app_merges by ("") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_all', 'Action': '@udf', '@udf': 'api_all', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[107]原语 api_all = @udf api_all by udf0.df_set_index with i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'api_all', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[108]原语 @udf api_all by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_all', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,merge_state,visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active from data_app_new where app in ($apps) and merge_state =0 and app_type =1'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[109]原语 app_all = load db by mysql1 with select id,merge_s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app_all', 'by': 'id,merge_state'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[110]原语 app = loc app_all by id,merge_state 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'merge_state', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[111]原语 app = add merge_state by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[112]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'app_merges', 'by': "'@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[113]原语 app = add app_merges by ("@app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[114]原语 @udf app by CRUD.save_table with (mysql1,data_app_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app2', 'Action': 'loc', 'loc': 'app_all', 'by': 'visits_num,visits_flow,sj_num,monitor_flow,api_num,imp_api_num,srcip_num,account_num,dstip_num,sensitive_label,app_type,app_status,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[115]原语 app2 = loc app_all by visits_num,visits_flow,sj_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app_merges', 'by': "'@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[116]原语 app2 = add app_merges by ("@app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app', 'by': "'@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[117]原语 app2 = add app by ("@app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[118]原语 alter app2.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2.app_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[119]原语 alter app2.app_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app2', 'Action': 'group', 'group': 'app2', 'by': 'app', 'agg': 'visits_num:sum,visits_flow:sum,sj_num:sum,monitor_flow:sum,api_num:sum,imp_api_num:sum,srcip_num:sum,account_num:sum,dstip_num:sum,sensitive_label:sum,app_type:sum,app_status:sum,active:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[120]原语 app2 = group app2 by app agg visits_num:sum,visits... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[121]原语 app2 = @udf app2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app2', 'by': '"visits_num_sum":"visits_num","visits_flow_sum":"visits_flow","sj_num_sum":"sj_num","monitor_flow_sum":"monitor_flow","api_num_sum":"api_num","imp_api_num_sum":"imp_api_num","srcip_num_sum":"srcip_num","account_num_sum":"account_num","dstip_num_sum":"dstip_num","sensitive_label_sum":"sensitive_label","app_type_sum":"app_type","app_status_sum":"app_status","active_sum":"active"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[122]原语 rename app2 by ("visits_num_sum":"visits_num","vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'merge_state', 'by': '2'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[123]原语 app2 = add merge_state by 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.sensitive_label', 'Action': 'lambda', 'lambda': 'sensitive_label', 'by': 'x:1 if "1" in x else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[124]原语 app2.sensitive_label = lambda sensitive_label by x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.app_type', 'Action': 'lambda', 'lambda': 'app_type', 'by': 'x:1 if "1" in x else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[125]原语 app2.app_type = lambda app_type by x:1 if "1" in x... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.app_status', 'Action': 'lambda', 'lambda': 'app_status', 'by': 'x:1 if "1" in x else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[126]原语 app2.app_status = lambda app_status by x:1 if "1" ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.active', 'Action': 'lambda', 'lambda': 'active', 'by': 'x:\'3\' if "3" in x else \'0\''}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[127]原语 app2.active = lambda active by x:"3" if "3" in x e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app2.active', 'Action': 'lambda', 'lambda': 'active', 'by': 'x:\'1\' if "1" in x else \'0\''}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[128]原语 app2.active = lambda active by x:"1" if "1" in x e... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app2', 'by': 'active:int,app_status:string,sensitive_label:string'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[129]原语 alter app2 by active:int,app_status:string,sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'app_sum', 'by': "'@apps_sum'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[132]原语 app2 = add app_sum by ("@apps_sum") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app2', 'Action': 'add', 'add': 'first_time', 'by': 'str(datetime.now())'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[133]原语 app2 = add first_time by str(datetime.now()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_merges', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,app from data_app_new where app = '@app' and merge_state = 2 and app_type =1"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[134]原语 app_merges = load db by mysql1 with select id,app ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app2', 'Action': 'join', 'join': 'app2,app_merges', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[135]原语 app2 = join app2,app_merges by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[136]原语 app2 = @udf app2 by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app2', 'Action': '@udf', '@udf': 'app2', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[137]原语 app2 = @udf app2 by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'app2', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第102行foreach语句中]执行第[138]原语 @udf app2 by CRUD.save_table with (mysql1,data_app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_102

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



