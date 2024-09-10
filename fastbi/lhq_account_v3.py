#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_account
#datetime: 2024-08-30T16:10:55.236021
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
		add_the_error('[lhq_account.fbi]执行第[17]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_account_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,account,dept,active,type,visit_num,visit_flow,api_num,app_num,ip_num from data_account_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[19]原语 data_account_new = load db by mysql1 with select i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_account_new', 'Action': '@udf', '@udf': 'data_account_new', 'by': 'udf0.df_fillna_cols', 'with': "dept:'',active:0,type:'',visit_num:0,visit_flow:0,api_num:0,app_num:0,ip_num:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[20]原语 data_account_new = @udf data_account_new by udf0.d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_account_new', 'by': 'id:int,account:str,dept:str,active:int,type:str,visit_num:int,visit_flow:int,api_num:int,app_num:int,ip_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[21]原语 alter data_account_new by id:int,account:str,dept:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_account_new1', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'id,account,visit_num,visit_flow,app_num,api_num,ip_num,type,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[24]原语 data_account_new1 = loc data_account_new by id,acc... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_account_new1.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[25]原语 alter data_account_new1.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[26]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_account_new1', 'Action': '@udf', '@udf': 'data_account_new1,active', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[27]原语 data_account_new1 = @udf data_account_new1,active ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_account_new1.visit_flow', 'Action': 'lambda', 'lambda': 'visit_flow', 'by': 'x:round(x/1048576,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[28]原语 data_account_new1.visit_flow = lambda visit_flow b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_account_new1', 'as': "'id':'_id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[29]原语 rename data_account_new1 as ("id":"_id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_account_new11', 'Action': 'order', 'order': 'data_account_new1', 'by': 'visit_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[30]原语 data_account_new11 = order data_account_new1 by vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_account_new11', 'to': 'pq', 'by': 'dt_table/data_account_new.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[32]原语 store data_account_new11 to pq by dt_table/data_ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_account_new1', 'as': "'account':'账号','visit_num':'访问次数','visit_flow':'访问流量(M)','app_num':'访问应用数量','api_num':'访问接口数量','ip_num':'访问终端数量','dept':'部门','type':'类型','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[33]原语 rename data_account_new1 as ("account":"账号","visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_account_new_1,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[35]原语 b = load ssdb by ssdb0 query qclear,data_account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_account_new11', 'Action': 'order', 'order': 'data_account_new1', 'by': '访问接口数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[36]原语 data_account_new11 = order data_account_new1 by 访问... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_account_new11', 'to': 'ssdb', 'with': 'data_account_new_1', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[37]原语 store data_account_new11 to ssdb with data_account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_account_new_2,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[38]原语 b = load ssdb by ssdb0 query qclear,data_account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_account_new11', 'Action': 'order', 'order': 'data_account_new1', 'by': '访问流量(M)', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[39]原语 data_account_new11 = order data_account_new1 by 访问... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_account_new11', 'to': 'ssdb', 'with': 'data_account_new_2', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[40]原语 store data_account_new11 to ssdb with data_account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_account_new_3,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[41]原语 b = load ssdb by ssdb0 query qclear,data_account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_account_new11', 'Action': 'order', 'order': 'data_account_new1', 'by': '访问应用数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[42]原语 data_account_new11 = order data_account_new1 by 访问... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_account_new11', 'to': 'ssdb', 'with': 'data_account_new_3', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[43]原语 store data_account_new11 to ssdb with data_account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_account_new_4,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[44]原语 b = load ssdb by ssdb0 query qclear,data_account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_account_new11', 'Action': 'order', 'order': 'data_account_new1', 'by': '访问终端数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[45]原语 data_account_new11 = order data_account_new1 by 访问... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_account_new11', 'to': 'ssdb', 'with': 'data_account_new_4', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[46]原语 store data_account_new11 to ssdb with data_account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_account_new_5,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[47]原语 b = load ssdb by ssdb0 query qclear,data_account_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_account_new11', 'Action': 'order', 'order': 'data_account_new1', 'by': '访问次数', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[48]原语 data_account_new11 = order data_account_new1 by 访问... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_account_new11', 'to': 'ssdb', 'with': 'data_account_new_5', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[49]原语 store data_account_new11 to ssdb with data_account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_account_new11'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[50]原语 drop data_account_new11 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_account_new1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[51]原语 drop data_account_new1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[61]原语 account_count = @udf udf0.new_df with num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account_num', 'Action': 'eval', 'eval': 'data_account_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[62]原语 account_num = eval data_account_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_count', 'Action': '@udf', '@udf': 'account_count', 'by': 'udf0.df_append', 'with': '$account_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[63]原语 account_count = @udf account_count by udf0.df_appe... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account1:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[64]原语 store account_count to ssdb by ssdb0 with account1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value,icon'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[67]原语 account_num = @udf udf0.new_df with name,value,ico... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'data_account_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[70]原语 num = eval data_account_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'account_num', 'by': 'udf0.df_append', 'with': '账号数量,$num,F363'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[71]原语 account_num = @udf account_num by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_2', 'Action': 'filter', 'filter': 'data_account_new', 'by': 'active == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[74]原语 active_2 = filter data_account_new by active == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num2', 'Action': 'eval', 'eval': 'active_2', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[75]原语 num2 = eval active_2 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'account_num', 'by': 'udf0.df_append', 'with': '活跃账号数,$num2,F216'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[76]原语 account_num = @udf account_num by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_1', 'Action': 'filter', 'filter': 'data_account_new', 'by': 'active == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[79]原语 active_1 = filter data_account_new by active == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num1', 'Action': 'eval', 'eval': 'active_1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[80]原语 num1 = eval active_1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'account_num', 'by': 'udf0.df_append', 'with': '失活账号数,$num1,F280'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[81]原语 account_num = @udf account_num by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_2', 'Action': 'filter', 'filter': 'data_account_new', 'by': 'active == 2'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[84]原语 active_2 = filter data_account_new by active == 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num2', 'Action': 'eval', 'eval': 'active_2', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[85]原语 num2 = eval active_2 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'account_num', 'by': 'udf0.df_append', 'with': '复活账号数,$num2,F022'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[86]原语 account_num = @udf account_num by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_3', 'Action': 'filter', 'filter': 'data_account_new', 'by': 'active == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[89]原语 active_3 = filter data_account_new by active == 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num3', 'Action': 'eval', 'eval': 'active_3', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[90]原语 num3 = eval active_3 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'account_num', 'by': 'udf0.df_append', 'with': '新增账号数,$num3,F368'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[91]原语 account_num = @udf account_num by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_type', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[94]原语 account_type = loc data_account_new by type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'account_type', 'Action': 'distinct', 'distinct': 'account_type', 'by': 'type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[95]原语 account_type = distinct account_type by type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num1', 'Action': 'eval', 'eval': 'account_type', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[96]原语 num1 = eval account_type by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account_num', 'Action': '@udf', '@udf': 'account_num', 'by': 'udf0.df_append', 'with': '账号类型数,$num1,F362'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[97]原语 account_num = @udf account_num by udf0.df_append w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account_num', 'Action': 'add', 'add': 'pageid', 'by': "'modeling:account_new','modeling:account_new','modeling:account_new','modeling:account_new','modeling:account_new',''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[98]原语 account_num = add pageid by ("modeling:account_new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account_num', 'Action': 'add', 'add': '参数', 'by': "'','@active=0','@active=1','@active=2','@active=3',''"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[99]原语 account_num = add 参数 by ("","@active=0","@active=1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_type:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[100]原语 store account_num to ssdb by ssdb0 with account_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_trend', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'account,visit_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[104]原语 account_trend = loc data_account_new by account,vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'account_trend', 'Action': 'order', 'order': 'account_trend', 'by': 'visit_num', 'with': 'desc limit 5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[105]原语 account_trend = order account_trend by visit_num w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_1', 'Action': 'loc', 'loc': 'account_trend', 'by': 'account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[106]原语 account_1 = loc account_trend by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'account_trend.详情', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[107]原语 account_trend.详情 = lambda account by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account_trend', 'by': '"account":"账号","visit_num":"访问量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[108]原语 rename account_trend by ("account":"账号","visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account_trend', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_trend:table'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[109]原语 store account_trend to ssdb by ssdb0 with account_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_flow', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'account,visit_flow,dept'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[112]原语 account_flow = loc data_account_new by account,vis... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'account_flow', 'Action': 'order', 'order': 'account_flow', 'by': 'visit_flow', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[113]原语 account_flow = order account_flow by visit_flow li... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_2', 'Action': 'loc', 'loc': 'account_flow', 'by': 'account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[114]原语 account_2 = loc account_flow by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'account_flow.flow1', 'Action': 'lambda', 'lambda': 'visit_flow', 'by': 'x:round(x/1024/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[115]原语 account_flow.flow1 = lambda visit_flow by (x:round... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account_flow', 'Action': 'add', 'add': 'aa', 'by': '"(M)"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[116]原语 account_flow = add aa by ("(M)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'account_flow.flow1', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[117]原语 alter account_flow.flow1 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account_flow', 'Action': 'add', 'add': 'flow', 'by': 'account_flow["flow1"]+account_flow["aa"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[118]原语 account_flow = add flow by account_flow["flow1"]+a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_flow', 'Action': 'loc', 'loc': 'account_flow', 'by': 'account,flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[119]原语 account_flow = loc account_flow by account,flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'account_flow.详情', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[120]原语 account_flow.详情 = lambda account by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account_flow', 'by': '"account":"访问流量最多账号","flow":"访问流量(M)"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[121]原语 rename account_flow by ("account":"访问流量最多账号","flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account_flow', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_visit:table'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[122]原语 store account_flow to ssdb by ssdb0 with account_v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_aui', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'account,api_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[125]原语 ua_aui = loc data_account_new by account,api_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ua_aui', 'Action': 'order', 'order': 'ua_aui', 'by': 'api_num', 'with': 'desc limit 5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[126]原语 ua_aui = order ua_aui by api_num with desc limit 5... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_3', 'Action': 'loc', 'loc': 'ua_aui', 'by': 'account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[127]原语 account_3 = loc ua_aui by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ua_aui', 'Action': 'order', 'order': 'ua_aui', 'by': 'api_num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[128]原语 ua_aui = order ua_aui by api_num with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ua_aui.详情', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[129]原语 ua_aui.详情 = lambda account by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ua_aui', 'by': '"api_num":"接口数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[130]原语 rename ua_aui by ("api_num":"接口数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_aui', 'Action': 'loc', 'loc': 'ua_aui', 'by': 'account', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[131]原语 ua_aui = loc ua_aui by account to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ua_aui', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_api:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[132]原语 store ua_aui to ssdb by ssdb0 with account_api:pie... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_au', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'account,app_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[135]原语 ua_au = loc data_account_new by account,app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ua_au', 'Action': 'order', 'order': 'ua_au', 'by': 'app_num', 'with': 'desc limit 10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[136]原语 ua_au = order ua_au by app_num with desc limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_4', 'Action': 'loc', 'loc': 'ua_au', 'by': 'account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[137]原语 account_4 = loc ua_au by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ua_au', 'by': '"app_num":"应用数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[138]原语 rename ua_au by ("app_num":"应用数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ua_au.详情', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[139]原语 ua_au.详情 = lambda account by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_au', 'Action': 'loc', 'loc': 'ua_au', 'by': 'account', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[140]原语 ua_au = loc ua_au by account to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ua_au', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_app1:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[141]原语 store ua_au to ssdb by ssdb0 with account_app1:pie... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_au', 'Action': 'loc', 'loc': 'ua_au', 'by': 'drop', 'drop': '详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[142]原语 ua_au = loc ua_au by drop 详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_au', 'Action': 'loc', 'loc': 'ua_au', 'by': 'index', 'to': '账号名称'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[143]原语 ua_au = loc ua_au by index to 账号名称 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ua_au', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_app:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[144]原语 store ua_au to ssdb by ssdb0 with account_app:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ua_au', 'Action': 'loc', 'loc': 'data_account_new', 'by': 'account,ip_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[147]原语 ua_au = loc data_account_new by account,ip_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ua_au.详情', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[148]原语 ua_au.详情 = lambda account by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'account_ip', 'Action': 'order', 'order': 'ua_au', 'by': 'ip_num', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[149]原语 account_ip = order ua_au by ip_num limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_5', 'Action': 'loc', 'loc': 'account_ip', 'by': 'account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[150]原语 account_5 = loc account_ip by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account_ip', 'by': '"ip_num":"终端数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[151]原语 rename account_ip by ("ip_num":"终端数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_ip', 'Action': 'loc', 'loc': 'account_ip', 'by': 'account', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[152]原语 account_ip = loc account_ip by account to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account_ip', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_ip:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[153]原语 store account_ip to ssdb by ssdb0 with account_ip:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_au', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select srcip,account_num as 账号数量 from data_ip_new order by account_num desc limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[158]原语 aa_au = load db by mysql1 with select srcip,accoun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa_au', 'by': 'srcip:str,账号数量:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[159]原语 alter aa_au by srcip:str,账号数量:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'aa_au.详情', 'Action': 'lambda', 'lambda': 'srcip', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[160]原语 aa_au.详情 = lambda srcip by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa_au', 'Action': 'loc', 'loc': 'aa_au', 'by': 'srcip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[161]原语 aa_au = loc aa_au by srcip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa_au', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'srcip:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[162]原语 store aa_au to ssdb by ssdb0 with srcip:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'account', 'Action': 'union', 'union': 'account_1,account_2,account_3,account_4,account_5'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[166]原语 account = union account_1,account_2,account_3,acco... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'account', 'Action': 'distinct', 'distinct': 'account', 'by': 'account'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[167]原语 account = distinct account by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'gl_account'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[168]原语 store account to ssdb by ssdb0 with gl_account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,account from data_account_new where portrait_status = 0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[170]原语 aa = load db by mysql1 with select id,account from... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'id:int,account:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[171]原语 alter aa by id:int,account:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'account', 'Action': 'join', 'join': 'aa,account', 'by': 'account,account', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[172]原语 account = join aa,account by account,account with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_fillna_cols', 'with': 'id:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[173]原语 account = @udf account by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'account', 'Action': 'filter', 'filter': 'account', 'by': 'id != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[174]原语 account = filter account by id != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'account.index.size > 0', 'with': '""\nalter account.id as int\naccount = add portrait_status by (1)\nbbb = @sdf sys_now\naccount = add portrait_time by (\'$bbb\')\naccount = @udf account by udf0.df_set_index with id\nb = @udf account by CRUD.save_table with (mysql1,data_account_new)\naccount = loc account by index to id\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=175
		ptree['funs']=block_if_175
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[175]原语 if account.index.size > 0 with "alter account.id a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_account.fbi]执行第[186]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],186

#主函数结束,开始块函数

def block_if_175(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'account.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[176]原语 alter account.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account', 'Action': 'add', 'add': 'portrait_status', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[177]原语 account = add portrait_status by (1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bbb', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[178]原语 bbb = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'account', 'Action': 'add', 'add': 'portrait_time', 'by': "'$bbb'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[179]原语 account = add portrait_time by ("$bbb") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'account', 'Action': '@udf', '@udf': 'account', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[180]原语 account = @udf account by udf0.df_set_index with i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'account', 'by': 'CRUD.save_table', 'with': 'mysql1,data_account_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[181]原语 b = @udf account by CRUD.save_table with (mysql1,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account', 'Action': 'loc', 'loc': 'account', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第175行if语句中]执行第[182]原语 account = loc account by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_175

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



