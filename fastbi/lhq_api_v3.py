#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_api
#datetime: 2024-08-30T16:10:55.668189
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
		add_the_error('[lhq_api.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_api_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url,visits_num,visits_flow,srcip_num,dstip_num,account_num,sensitive_label,risk_level,api_type,data_type,active from data_api_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[19]原语 data_api_new = load db by mysql1 with select id,ur... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api_new', 'Action': '@udf', '@udf': 'data_api_new', 'by': 'udf0.df_fillna_cols', 'with': "visits_num:0,visits_flow:0,srcip_num:0,dstip_num:0,account_num:0,sensitive_label:0,risk_level:0,api_type:0,data_type:'',active:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[20]原语 data_api_new = @udf data_api_new by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_api_new', 'by': 'visits_num:int,visits_flow:int,srcip_num:int,dstip_num:int,account_num:int,sensitive_label:int,risk_level:int,api_type:int,data_type:str,active:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[21]原语 alter data_api_new by visits_num:int,visits_flow:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_api_new1', 'Action': 'loc', 'loc': 'data_api_new', 'by': 'id,url,visits_num,visits_flow,srcip_num,dstip_num,account_num,api_type,active,sensitive_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[26]原语 data_api_new1 = loc data_api_new by id,url,visits_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_api_new1', 'Action': 'filter', 'filter': 'data_api_new1', 'by': 'sensitive_label != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[30]原语 data_api_new1 = filter data_api_new1 by sensitive_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_api_new1', 'by': 'active:str,api_type:str,sensitive_label:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[31]原语 alter data_api_new1 by active:str,api_type:str,sen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[32]原语 api_type = load ssdb with dd:API-api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api_new1', 'Action': '@udf', '@udf': 'data_api_new1,api_type', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[33]原语 data_api_new1 = @udf data_api_new1,api_type by SP.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ssdb', 'with': 'dd:sensitive_label'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[34]原语 sens = load ssdb with dd:sensitive_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api_new1', 'Action': '@udf', '@udf': 'data_api_new1,sens', 'by': 'SP.tag2dict', 'with': 'sensitive_label'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[35]原语 data_api_new1 = @udf data_api_new1,sens by SP.tag2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[36]原语 active = load ssdb with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_api_new1', 'Action': '@udf', '@udf': 'data_api_new1,active', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[37]原语 data_api_new1 = @udf data_api_new1,active by SP.ta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_api_new1', 'Action': 'loc', 'loc': 'data_api_new1', 'by': 'id,url,visits_num,visits_flow,srcip_num,dstip_num,account_num,api_type,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[38]原语 data_api_new1 = loc data_api_new1 by id,url,visits... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_api_new1', 'as': "'id':'_id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[39]原语 rename data_api_new1 as ("id":"_id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_api_new1.visits_flow', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': 'x:round(x/1048576,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[40]原语 data_api_new1.visits_flow = lambda visits_flow by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_api_new11', 'Action': 'order', 'order': 'data_api_new1', 'by': 'visits_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[41]原语 data_api_new11 = order data_api_new1 by visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_api_new11', 'to': 'pq', 'by': 'dt_table/data_api_new.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[44]原语 store data_api_new11 to pq by dt_table/data_api_ne... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_api_new1', 'as': "'url':'接口','visits_num':'访问数量','visits_flow':'访问流量(M)','srcip_num':'访问终端数量','dstip_num':'部署数量','account_num':'访问账号数量','api_type':'接口类型','active':'活跃状态','sensitive_label':'敏感类型'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[45]原语 rename data_api_new1 as ("url":"接口","visits_num":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_api_new_1,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[47]原语 b = load ssdb by ssdb0 query qclear,data_api_new_1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_api_new11', 'Action': 'order', 'order': 'data_api_new1', 'by': '访问流量(M)', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[48]原语 data_api_new11 = order data_api_new1 by 访问流量(M) wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_api_new11', 'to': 'ssdb', 'with': 'data_api_new_1', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[49]原语 store data_api_new11 to ssdb with data_api_new_1 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_api_new_2,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[50]原语 b = load ssdb by ssdb0 query qclear,data_api_new_2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_api_new11', 'Action': 'order', 'order': 'data_api_new1', 'by': '访问账号数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[51]原语 data_api_new11 = order data_api_new1 by 访问账号数量 wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_api_new11', 'to': 'ssdb', 'with': 'data_api_new_2', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[52]原语 store data_api_new11 to ssdb with data_api_new_2 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_api_new_3,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[53]原语 b = load ssdb by ssdb0 query qclear,data_api_new_3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_api_new11', 'Action': 'order', 'order': 'data_api_new1', 'by': '访问终端数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[54]原语 data_api_new11 = order data_api_new1 by 访问终端数量 wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_api_new11', 'to': 'ssdb', 'with': 'data_api_new_3', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[55]原语 store data_api_new11 to ssdb with data_api_new_3 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_api_new11'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[56]原语 drop data_api_new11 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_api_new1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[57]原语 drop data_api_new1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value,icon,pageid,参数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[66]原语 api_count = @udf udf0.new_df with (name,value,icon... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'data_api_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[67]原语 num = eval data_api_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '接口数量,$num,F138,modeling:api_new,'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[68]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_0', 'Action': 'filter', 'filter': 'data_api_new', 'by': 'active == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[69]原语 active_0 = filter data_api_new by active == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num0', 'Action': 'eval', 'eval': 'active_0', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[70]原语 num0 = eval active_0 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '活跃接口数量,$num0,F159,modeling:api_new,@active=0'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[71]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_1', 'Action': 'filter', 'filter': 'data_api_new', 'by': 'active == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[72]原语 active_1 = filter data_api_new by active == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num1', 'Action': 'eval', 'eval': 'active_1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[73]原语 num1 = eval active_1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '失活接口数量,$num1,F156,modeling:api_new,@active=1'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[74]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_2', 'Action': 'filter', 'filter': 'data_api_new', 'by': 'active == 2'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[75]原语 active_2 = filter data_api_new by active == 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num2', 'Action': 'eval', 'eval': 'active_2', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[76]原语 num2 = eval active_2 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '复活接口数量,$num2,F362,modeling:api_new,@active=2'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[77]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_3', 'Action': 'filter', 'filter': 'data_api_new', 'by': 'active == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[78]原语 active_3 = filter data_api_new by active == 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num3', 'Action': 'eval', 'eval': 'active_3', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[79]原语 num3 = eval active_3 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '新增接口数量,$num3,F203,modeling:api_new,@active=3'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[80]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_api_new.sensitive_label', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[81]原语 alter data_api_new.sensitive_label as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sensitive_api', 'Action': 'group', 'group': 'data_api_new', 'by': 'sensitive_label', 'agg': 'sensitive_label:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[82]原语 sensitive_api = group data_api_new by sensitive_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sensitive_api1', 'Action': 'filter', 'filter': 'sensitive_api', 'by': 'index == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[83]原语 sensitive_api1 = filter sensitive_api by index == ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'sensitive_api1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[84]原语 aa_num = eval sensitive_api1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num == 0', 'with': 'sensitive_api1 = @udf sensitive_api1 by udf0.df_append with 0'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=85
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[85]原语 if $aa_num == 0 with sensitive_api1 = @udf sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive_api1', 'Action': 'eval', 'eval': 'sensitive_api1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[86]原语 sensitive_api1 = eval sensitive_api1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '高敏感接口数量,$sensitive_api1,F245,modeling:api_new,@sensitive_label=3'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[87]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[93]原语 store api_count to ssdb by ssdb0 with api:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[96]原语 api_count = @udf udf0.new_df with num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_num', 'Action': 'eval', 'eval': 'data_api_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[97]原语 api_num = eval data_api_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_count', 'Action': '@udf', '@udf': 'api_count', 'by': 'udf0.df_append', 'with': '$api_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[98]原语 api_count = @udf api_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api1:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[99]原语 store api_count to ssdb by ssdb0 with api1:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_data_type', 'Action': 'group', 'group': 'data_api_new', 'by': 'data_type', 'agg': 'data_type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[105]原语 api_data_type = group data_api_new by data_type ag... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_data_type', 'by': '"data_type_count":"类型数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[106]原语 rename api_data_type by ("data_type_count":"类型数量")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_data_type', 'Action': 'loc', 'loc': 'api_data_type', 'by': 'index', 'to': '详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[108]原语 api_data_type = loc api_data_type by index to 详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_data_type.aa', 'Action': 'lambda', 'lambda': '详情', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[109]原语 api_data_type.aa = lambda 详情 by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_data_type', 'Action': 'loc', 'loc': 'api_data_type', 'by': 'aa', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[110]原语 api_data_type = loc api_data_type by aa to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_data_type', 'Action': 'loc', 'loc': 'api_data_type', 'by': '类型数量,详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[111]原语 api_data_type = loc api_data_type by 类型数量,详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_data_type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_type:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[112]原语 store api_data_type to ssdb by ssdb0 with api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_api_type', 'Action': 'group', 'group': 'data_api_new', 'by': 'api_type', 'agg': 'api_type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[118]原语 api_api_type = group data_api_new by api_type agg ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_api_type', 'Action': 'loc', 'loc': 'api_api_type', 'by': 'index', 'to': 'api_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[119]原语 api_api_type = loc api_api_type by index to api_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_api_type.api_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[120]原语 alter api_api_type.api_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[121]原语 api_type = load ssdb with dd:API-api_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_api_type', 'Action': '@udf', '@udf': 'api_api_type,api_type', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[122]原语 api_api_type = @udf api_api_type,api_type by SP.ta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_api_type.详情', 'Action': 'lambda', 'lambda': 'api_type', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[123]原语 api_api_type.详情 = lambda api_type by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_api_type', 'Action': 'loc', 'loc': 'api_api_type', 'by': 'api_type', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[124]原语 api_api_type = loc api_api_type by api_type to ind... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_api_type', 'by': '"api_type_count":"类型数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[125]原语 rename api_api_type by ("api_type_count":"类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_api_type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_type_api:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[126]原语 store api_api_type to ssdb by ssdb0 with api_type_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'risk_level'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[130]原语 aa = @udf udf0.new_df with risk_level 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[131]原语 aa = @udf aa by udf0.df_append with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[132]原语 aa = @udf aa by udf0.df_append with 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_append', 'with': '2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[133]原语 aa = @udf aa by udf0.df_append with 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_risk_level', 'Action': 'group', 'group': 'data_api_new', 'by': 'risk_level', 'agg': 'risk_level:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[134]原语 api_risk_level = group data_api_new by risk_level ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk_level', 'Action': 'loc', 'loc': 'api_risk_level', 'by': 'index', 'to': 'risk_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[135]原语 api_risk_level = loc api_risk_level by index to ri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api_risk_level', 'Action': 'join', 'join': 'api_risk_level,aa', 'by': 'risk_level,risk_level', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[136]原语 api_risk_level = join api_risk_level,aa by risk_le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_risk_level', 'Action': '@udf', '@udf': 'api_risk_level', 'by': 'udf0.df_fillna_cols', 'with': 'risk_level_count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[137]原语 api_risk_level = @udf api_risk_level by udf0.df_fi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_risk_level', 'by': 'risk_level:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[138]原语 alter api_risk_level by risk_level:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'level', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-risk_level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[139]原语 level = load ssdb by ssdb0 with dd:API-risk_level 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_risk_level', 'Action': '@udf', '@udf': 'api_risk_level,level', 'by': 'SP.tag2dict', 'with': 'risk_level'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[140]原语 api_risk_level = @udf api_risk_level,level by SP.t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_risk_level.risk_level', 'Action': 'lambda', 'lambda': 'risk_level', 'by': "x:x+'风险'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[141]原语 api_risk_level.risk_level = lambda risk_level by (... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk_level', 'Action': 'loc', 'loc': 'api_risk_level', 'by': 'index', 'to': '详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[142]原语 api_risk_level = loc api_risk_level by index to 详情... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk_level', 'Action': 'loc', 'loc': 'api_risk_level', 'by': 'risk_level', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[143]原语 api_risk_level = loc api_risk_level by risk_level ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_risk_level', 'by': '"risk_level_count":"风险接口数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[144]原语 rename api_risk_level by ("risk_level_count":"风险接口... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_risk_level', 'Action': 'loc', 'loc': 'api_risk_level', 'by': '风险接口数量,详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[145]原语 api_risk_level = loc api_risk_level by 风险接口数量,详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_risk_level', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk_level:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[146]原语 store api_risk_level to ssdb by ssdb0 with risk_le... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sensitive_1', 'Action': 'filter', 'filter': 'data_api_new', 'by': 'sensitive_label != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[150]原语 sensitive_1 = filter data_api_new by sensitive_lab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sensitive_url', 'Action': 'loc', 'loc': 'sensitive_1', 'by': 'url,visits_num,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[154]原语 sensitive_url = loc sensitive_1 by url,visits_num,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sensitive_url', 'Action': 'filter', 'filter': 'sensitive_url', 'by': 'visits_num > 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[155]原语 sensitive_url = filter sensitive_url by visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sensitive_url_limit', 'Action': 'order', 'order': 'sensitive_url', 'by': 'visits_num', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[156]原语 sensitive_url_limit = order sensitive_url by visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_1', 'Action': 'loc', 'loc': 'sensitive_url_limit', 'by': 'url,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[157]原语 api_1 = loc sensitive_url_limit by url,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sensitive_url_limit', 'Action': 'loc', 'loc': 'sensitive_url_limit', 'by': 'url,visits_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[158]原语 sensitive_url_limit = loc sensitive_url_limit by u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sensitive_url_limit', 'by': '\'url\':\'接口\',"visits_num":"接口数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[159]原语 rename sensitive_url_limit by ("url":"接口","visits_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sensitive_url_limit', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive_url:bar'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[160]原语 store sensitive_url_limit to ssdb by ssdb0 with se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_flow_join', 'Action': 'loc', 'loc': 'sensitive_1', 'by': 'id,url,visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[164]原语 api_flow_join = loc sensitive_1 by id,url,visits_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api_flow_join', 'Action': 'filter', 'filter': 'api_flow_join', 'by': 'visits_flow > 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[165]原语 api_flow_join = filter api_flow_join by visits_flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_flow_join.流量(M)', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': 'x:round(x/1048576,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[166]原语 api_flow_join.流量(M) = lambda visits_flow by (x:rou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api_flow_join', 'Action': 'order', 'order': 'api_flow_join', 'by': '流量(M)', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[167]原语 api_flow_join = order api_flow_join by 流量(M) limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_2', 'Action': 'loc', 'loc': 'api_flow_join', 'by': 'id,url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[168]原语 api_2 = loc api_flow_join by id,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_flow_join', 'Action': 'loc', 'loc': 'api_flow_join', 'by': 'drop', 'drop': 'visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[169]原语 api_flow_join = loc api_flow_join by drop visits_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_flow_join', 'as': '\'id\':\'参数\',"url":"敏感接口"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[170]原语 rename api_flow_join as ("id":"参数","url":"敏感接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_flow_join', 'Action': 'loc', 'loc': 'api_flow_join', 'by': '敏感接口,流量(M),参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[171]原语 api_flow_join = loc api_flow_join by 敏感接口,流量(M),参数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_flow_join', 'by': '敏感接口:str,流量(M):str,参数:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[172]原语 alter api_flow_join by 敏感接口:str,流量(M):str,参数:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_flow_join', 'Action': '@udf', '@udf': 'api_flow_join', 'by': 'VL.set_col_width', 'with': '400,80,10'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[173]原语 api_flow_join = @udf api_flow_join by VL.set_col_w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_flow_join', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_flow:table'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[174]原语 store api_flow_join to ssdb by ssdb0 with api_flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dip_app', 'Action': 'loc', 'loc': 'sensitive_1', 'by': 'url,srcip_num,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[178]原语 dip_app = loc sensitive_1 by url,srcip_num,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dip_app', 'Action': 'filter', 'filter': 'dip_app', 'by': 'srcip_num > 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[179]原语 dip_app = filter dip_app by srcip_num > 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ip_app_order', 'Action': 'order', 'order': 'dip_app', 'by': 'srcip_num', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[180]原语 ip_app_order = order dip_app by srcip_num limit 10... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_3', 'Action': 'loc', 'loc': 'ip_app_order', 'by': 'id,url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[181]原语 api_3 = loc ip_app_order by id,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ip_app_order', 'as': "'id':'参数','url':'敏感接口','srcip_num':'终端数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[182]原语 rename ip_app_order as ("id":"参数","url":"敏感接口","sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_app_order', 'Action': 'loc', 'loc': 'ip_app_order', 'by': '敏感接口,终端数量,参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[183]原语 ip_app_order = loc ip_app_order by 敏感接口,终端数量,参数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ip_app_order', 'by': '敏感接口:str,终端数量:str,参数:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[184]原语 alter ip_app_order by 敏感接口:str,终端数量:str,参数:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_app_order', 'Action': '@udf', '@udf': 'ip_app_order', 'by': 'VL.set_col_width', 'with': '400,80,0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[185]原语 ip_app_order = @udf ip_app_order by VL.set_col_wid... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_app_order', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip_app:table'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[186]原语 store ip_app_order to ssdb by ssdb0 with ip_app:ta... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_account', 'Action': 'loc', 'loc': 'sensitive_1', 'by': 'url,account_num,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[189]原语 api_account = loc sensitive_1 by url,account_num,i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api_account', 'Action': 'filter', 'filter': 'api_account', 'by': 'account_num > 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[190]原语 api_account = filter api_account by account_num > ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api_account', 'Action': 'order', 'order': 'api_account', 'by': 'account_num', 'with': 'desc limit 5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[191]原语 api_account = order api_account by account_num wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_4', 'Action': 'loc', 'loc': 'api_account', 'by': 'url,id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[192]原语 api_4 = loc api_account by url,id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_account', 'by': "'url':'接口','account_num':'账号数量','id':'参数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[193]原语 rename api_account by ("url":"接口","account_num":"账... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_account', 'Action': 'loc', 'loc': 'api_account', 'by': '接口,账号数量,参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[194]原语 api_account = loc api_account by 接口,账号数量,参数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_account', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api_account:table'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[195]原语 store api_account to ssdb by ssdb0 with api_accoun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'api', 'Action': 'union', 'union': 'api_1,api_2,api_3,api_4'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[199]原语 api = union api_1,api_2,api_3,api_4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'api', 'Action': 'distinct', 'distinct': 'api', 'by': 'url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[200]原语 api = distinct api by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api', 'Action': 'loc', 'loc': 'api', 'by': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[201]原语 api = loc api by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'gl_api'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[202]原语 store api to ssdb by ssdb0 with gl_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,url from data_api_new where portrait_status = 0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[204]原语 aa = load db by mysql1 with select id,url from dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'id:int,url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[205]原语 alter aa by id:int,url:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api', 'Action': 'join', 'join': 'aa,api', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[206]原语 api = join aa,api by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_fillna_cols', 'with': 'id:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[207]原语 api = @udf api by udf0.df_fillna_cols with id:0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api', 'Action': 'filter', 'filter': 'api', 'by': 'id != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[208]原语 api = filter api by id != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'api.index.size > 0', 'with': '""\nalter api.id as int\napi = add portrait_status by (1)\nbbb = @sdf sys_now\napi = add portrait_time by (\'$bbb\')\napi = @udf api by udf0.df_set_index with id\nb = @udf api by CRUD.save_table with (mysql1,data_api_new)\napi = loc api by index to id\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=209
		ptree['funs']=block_if_209
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[209]原语 if api.index.size > 0 with "alter api.id as intapi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_api.fbi]执行第[220]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],222

#主函数结束,开始块函数

def block_if_209(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[210]原语 alter api.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'portrait_status', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[211]原语 api = add portrait_status by (1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bbb', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[212]原语 bbb = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api', 'Action': 'add', 'add': 'portrait_time', 'by': "'$bbb'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[213]原语 api = add portrait_time by ("$bbb") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'api', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[214]原语 api = @udf api by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'api', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[215]原语 b = @udf api by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api', 'Action': 'loc', 'loc': 'api', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第209行if语句中]执行第[216]原语 api = loc api by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_209

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



