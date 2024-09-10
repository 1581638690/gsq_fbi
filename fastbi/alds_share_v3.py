#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: alds_share
#datetime: 2024-08-30T16:10:54.977758
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
		add_the_error('[alds_share.fbi]执行第[8]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT DISTINCT srcip,dstip,dstip ip FROM api_monitor WHERE time >= today() - 1;'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[22]原语 api = load ckh by ckh with SELECT DISTINCT srcip,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'id', 'by': 'api.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[23]原语 api = add id by api.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'api', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[24]原语 ynw = @udf api by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[25]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[26]原语 ynw = filter ynw by yn == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'srcip,dstip,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[27]原语 ynw = loc ynw by srcip,dstip,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ynw', 'as': "'srcip':'ip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[28]原语 rename ynw as ("srcip":"ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'ynw', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[29]原语 ynw = @udf ynw by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[30]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[31]原语 ynw = filter ynw by yn == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'dstip,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[32]原语 ynw = loc ynw by dstip,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[33]原语 ynw.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ynw', 'Action': 'group', 'group': 'ynw', 'by': 'yn', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[34]原语 ynw = group ynw by yn agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[35]原语 ynw.dstip_sum = lambda dstip_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[36]原语 ynw.dstip_sum = lambda dstip_sum by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'eval', 'eval': 'ynw', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[37]原语 ynw = eval ynw by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dstip from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[39]原语 data_app = load db by mysql1 with select id,dstip ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_app.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[41]原语 data_app.dstip = lambda dstip by x:set(x.split(","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_app.app_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[42]原语 data_app.app_share = lambda dstip by x:len(x.inter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_app', 'Action': 'filter', 'filter': 'data_app', 'by': 'app_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[43]原语 data_app = filter data_app by app_share != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_app', 'Action': 'loc', 'loc': 'data_app', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[44]原语 data_app = loc data_app by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_app.app_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[45]原语 data_app.app_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app', 'Action': '@udf', '@udf': 'data_app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[46]原语 data_app = @udf data_app by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app', 'Action': '@udf', '@udf': 'data_app', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[47]原语 data_app = @udf data_app by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,dstip from data_api_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[49]原语 data_api = load db by mysql1 with select id,dstip ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_api.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[51]原语 data_api.dstip = lambda dstip by x:set(x.split(","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_api.api_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[52]原语 data_api.api_share = lambda dstip by x:len(x.inter... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_api', 'Action': 'filter', 'filter': 'data_api', 'by': 'api_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[53]原语 data_api = filter data_api by api_share != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_api', 'Action': 'loc', 'loc': 'data_api', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[54]原语 data_api = loc data_api by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_api.api_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[55]原语 data_api.api_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api', 'Action': '@udf', '@udf': 'data_api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[56]原语 data_api = @udf data_api by udf0.df_set_index with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api', 'Action': '@udf', '@udf': 'data_api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[57]原语 data_api = @udf data_api by CRUD.save_table with (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'SELECT DISTINCT src_ip srcip,dest_ip dstip,dest_ip ip FROM dbms WHERE timestamp >= today() - 1;'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[59]原语 dbms = load ckh by ckh with SELECT DISTINCT src_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dbms', 'Action': 'add', 'add': 'id', 'by': 'dbms.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[60]原语 dbms = add id by dbms.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'dbms', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[61]原语 ynw = @udf dbms by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[62]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[63]原语 ynw = filter ynw by yn == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'srcip,dstip,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[64]原语 ynw = loc ynw by srcip,dstip,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ynw', 'as': "'srcip':'ip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[65]原语 rename ynw as ("srcip":"ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'ynw', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[66]原语 ynw = @udf ynw by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[67]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[68]原语 ynw = filter ynw by yn == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'dstip,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[69]原语 ynw = loc ynw by dstip,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[70]原语 ynw.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ynw', 'Action': 'group', 'group': 'ynw', 'by': 'yn', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[71]原语 ynw = group ynw by yn agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[72]原语 ynw.dstip_sum = lambda dstip_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[73]原语 ynw.dstip_sum = lambda dstip_sum by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'eval', 'eval': 'ynw', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[74]原语 ynw = eval ynw by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'dbms', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select dstip,id from dbms_obj'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[77]原语 dbms = load db by mysql1 with select dstip,id from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dbms.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[78]原语 dbms.dstip = lambda dstip by x:set(x.split(",")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dbms.api_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[79]原语 dbms.api_share = lambda dstip by x:len(x.intersect... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dbms', 'Action': 'filter', 'filter': 'dbms', 'by': 'api_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[80]原语 dbms = filter dbms by api_share != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dbms', 'Action': 'loc', 'loc': 'dbms', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[81]原语 dbms = loc dbms by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'dbms.dbms_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[82]原语 dbms.dbms_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[83]原语 dbms = @udf dbms by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dbms', 'Action': '@udf', '@udf': 'dbms', 'by': 'CRUD.save_table', 'with': 'mysql1,dbms_obj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[84]原语 dbms = @udf dbms by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select DISTINCT srcip,dstip,dstip ip from api_fileinfo where app_proto == 'http' and timestamp >= today() - 1"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[87]原语 fileinfo = load ckh by ckh with select DISTINCT sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'id', 'by': 'fileinfo.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[88]原语 fileinfo = add id by fileinfo.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[89]原语 ynw = @udf fileinfo by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[90]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[91]原语 ynw = filter ynw by yn == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'srcip,dstip,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[92]原语 ynw = loc ynw by srcip,dstip,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ynw', 'as': "'srcip':'ip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[93]原语 rename ynw as ("srcip":"ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'ynw', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[94]原语 ynw = @udf ynw by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[95]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[96]原语 ynw = filter ynw by yn == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'dstip,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[97]原语 ynw = loc ynw by dstip,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[98]原语 ynw.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ynw', 'Action': 'group', 'group': 'ynw', 'by': 'yn', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[99]原语 ynw = group ynw by yn agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[100]原语 ynw.dstip_sum = lambda dstip_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[101]原语 ynw.dstip_sum = lambda dstip_sum by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'eval', 'eval': 'ynw', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[102]原语 ynw = eval ynw by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select dstip,id from data_file_server where protocol = 'http'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[103]原语 file_server = load db by mysql1 with select dstip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[104]原语 file_server.dstip = lambda dstip by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[105]原语 file_server.file_share = lambda dstip by x:len(x.i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'file_server', 'Action': 'filter', 'filter': 'file_server', 'by': 'file_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[106]原语 file_server = filter file_server by file_share != ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[107]原语 file_server = loc file_server by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[108]原语 file_server.file_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[109]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[110]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select DISTINCT srcip,dstip,dstip ip from api_ftp where timestamp >= today() - 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[112]原语 fileinfo = load ckh by ckh with select DISTINCT sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'id', 'by': 'fileinfo.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[113]原语 fileinfo = add id by fileinfo.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[114]原语 ynw = @udf fileinfo by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[115]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[116]原语 ynw = filter ynw by yn == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'srcip,dstip,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[117]原语 ynw = loc ynw by srcip,dstip,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ynw', 'as': "'srcip':'ip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[118]原语 rename ynw as ("srcip":"ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'ynw', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[119]原语 ynw = @udf ynw by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[120]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[121]原语 ynw = filter ynw by yn == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'dstip,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[122]原语 ynw = loc ynw by dstip,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[123]原语 ynw.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ynw', 'Action': 'group', 'group': 'ynw', 'by': 'yn', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[124]原语 ynw = group ynw by yn agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[125]原语 ynw.dstip_sum = lambda dstip_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[126]原语 ynw.dstip_sum = lambda dstip_sum by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'eval', 'eval': 'ynw', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[127]原语 ynw = eval ynw by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select dstip,id from data_file_server where protocol = 'ftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[128]原语 file_server = load db by mysql1 with select dstip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[129]原语 file_server.dstip = lambda dstip by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[130]原语 file_server.file_share = lambda dstip by x:len(x.i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'file_server', 'Action': 'filter', 'filter': 'file_server', 'by': 'file_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[131]原语 file_server = filter file_server by file_share != ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[132]原语 file_server = loc file_server by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[133]原语 file_server.file_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[134]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[135]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select DISTINCT srcip,dstip,dstip ip from api_tftp where timestamp >= today() - 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[189]原语 fileinfo = load ckh by ckh with select DISTINCT sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'id', 'by': 'fileinfo.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[190]原语 fileinfo = add id by fileinfo.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[191]原语 ynw = @udf fileinfo by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[192]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[193]原语 ynw = filter ynw by yn == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'srcip,dstip,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[194]原语 ynw = loc ynw by srcip,dstip,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ynw', 'as': "'srcip':'ip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[195]原语 rename ynw as ("srcip":"ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'ynw', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[196]原语 ynw = @udf ynw by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[197]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[198]原语 ynw = filter ynw by yn == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'dstip,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[199]原语 ynw = loc ynw by dstip,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[200]原语 ynw.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ynw', 'Action': 'group', 'group': 'ynw', 'by': 'yn', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[201]原语 ynw = group ynw by yn agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[202]原语 ynw.dstip_sum = lambda dstip_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[203]原语 ynw.dstip_sum = lambda dstip_sum by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'eval', 'eval': 'ynw', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[204]原语 ynw = eval ynw by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select dstip,id from data_file_server where protocol = 'tftp'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[205]原语 file_server = load db by mysql1 with select dstip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[206]原语 file_server.dstip = lambda dstip by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[207]原语 file_server.file_share = lambda dstip by x:len(x.i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'file_server', 'Action': 'filter', 'filter': 'file_server', 'by': 'file_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[208]原语 file_server = filter file_server by file_share != ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[209]原语 file_server = loc file_server by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[210]原语 file_server.file_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[211]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[212]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'fileinfo', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select DISTINCT srcip,dstip,dstip ip from api_smb where dialect !='unknown' and timestamp >= today() - 1"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[266]原语 fileinfo = load ckh by ckh with select DISTINCT sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'fileinfo', 'Action': 'add', 'add': 'id', 'by': 'fileinfo.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[267]原语 fileinfo = add id by fileinfo.index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'fileinfo', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[268]原语 ynw = @udf fileinfo by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[269]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[270]原语 ynw = filter ynw by yn == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'srcip,dstip,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[271]原语 ynw = loc ynw by srcip,dstip,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ynw', 'as': "'srcip':'ip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[272]原语 rename ynw as ("srcip":"ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'ynw', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[273]原语 ynw = @udf ynw by ip24.repeat with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[274]原语 ynw.yn = lambda yn by x:1 if x==1 else 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ynw', 'Action': 'filter', 'filter': 'ynw', 'by': 'yn == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[275]原语 ynw = filter ynw by yn == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'dstip,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[276]原语 ynw = loc ynw by dstip,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[277]原语 ynw.dstip = lambda dstip by x:x+"," 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ynw', 'Action': 'group', 'group': 'ynw', 'by': 'yn', 'agg': 'dstip:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[278]原语 ynw = group ynw by yn agg dstip:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[279]原语 ynw.dstip_sum = lambda dstip_sum by x:x[:-1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.dstip_sum', 'Action': 'lambda', 'lambda': 'dstip_sum', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[280]原语 ynw.dstip_sum = lambda dstip_sum by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'eval', 'eval': 'ynw', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[281]原语 ynw = eval ynw by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'file_server', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select dstip,id from data_file_server where protocol = 'smb'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[282]原语 file_server = load db by mysql1 with select dstip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.dstip', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:set(x.split(","))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[283]原语 file_server.dstip = lambda dstip by x:set(x.split(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'dstip', 'by': 'x:len(x.intersection($ynw))'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[284]原语 file_server.file_share = lambda dstip by x:len(x.i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'file_server', 'Action': 'filter', 'filter': 'file_server', 'by': 'file_share != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[285]原语 file_server = filter file_server by file_share != ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'file_server', 'Action': 'loc', 'loc': 'file_server', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[286]原语 file_server = loc file_server by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'file_server.file_share', 'Action': 'lambda', 'lambda': 'id', 'by': 'x:1'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[287]原语 file_server.file_share = lambda id by x:1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[288]原语 file_server = @udf file_server by udf0.df_set_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'file_server', 'Action': '@udf', '@udf': 'file_server', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[289]原语 file_server = @udf file_server by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[alds_share.fbi]执行第[293]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],293

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



