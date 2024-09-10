#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_ip
#datetime: 2024-08-30T16:10:56.252552
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
		add_the_error('[lhq_ip.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_ip_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,srcip,region,type,visit_num,visit_flow,app_num,account_num,api_num,active from data_ip_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[19]原语 data_ip_new = load db by mysql1 with select id,src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_ip_new', 'Action': '@udf', '@udf': 'data_ip_new', 'by': 'udf0.df_fillna_cols', 'with': "region:'',type:'',visit_num:0,visit_flow:0,app_num:0,account_num:0,api_num:0,active:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[20]原语 data_ip_new = @udf data_ip_new by udf0.df_fillna_c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_ip_new', 'by': 'region:str,type:str,visit_num:int,visit_flow:int,app_num:int,account_num:int,api_num:int,active:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[21]原语 alter data_ip_new by region:str,type:str,visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_ip_new1', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'id,srcip,visit_num,visit_flow,app_num,api_num,account_num,type,active'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[24]原语 data_ip_new1 = loc data_ip_new by id,srcip,visit_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_ip_new1.active', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[25]原语 alter data_ip_new1.active as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'active', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:api_active'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[26]原语 active = load ssdb by ssdb0 with dd:api_active 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_ip_new1', 'Action': '@udf', '@udf': 'data_ip_new1,active', 'by': 'SP.tag2dict', 'with': 'active'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[27]原语 data_ip_new1 = @udf data_ip_new1,active by SP.tag2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_ip_new1.visit_flow', 'Action': 'lambda', 'lambda': 'visit_flow', 'by': 'x:round(x/1048576,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[28]原语 data_ip_new1.visit_flow = lambda visit_flow by (x:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_ip_new1', 'as': "'id':'_id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[29]原语 rename data_ip_new1 as ("id":"_id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_ip_new11', 'Action': 'order', 'order': 'data_ip_new1', 'by': 'visit_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[30]原语 data_ip_new11 = order data_ip_new1 by visit_num wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_ip_new11', 'to': 'pq', 'by': 'dt_table/data_ip_new.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[32]原语 store data_ip_new11 to pq by dt_table/data_ip_new.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_ip_new1', 'as': "'srcip':'终端IP','visit_num':'访问次数','visit_flow':'访问流量(M)','app_num':'访问应用数量','api_num':'访问接口数量','account_num':'访问账号数量','region':'地域','type':'终端类型','active':'活跃状态'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[33]原语 rename data_ip_new1 as ("srcip":"终端IP","visit_num"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_ip_new_1,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[35]原语 b = load ssdb by ssdb0 query qclear,data_ip_new_1,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_ip_new11', 'Action': 'order', 'order': 'data_ip_new1', 'by': '访问流量(M)', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[36]原语 data_ip_new11 = order data_ip_new1 by 访问流量(M) with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_ip_new11', 'to': 'ssdb', 'with': 'data_ip_new_1', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[37]原语 store data_ip_new11 to ssdb with data_ip_new_1 as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_ip_new_2,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[38]原语 b = load ssdb by ssdb0 query qclear,data_ip_new_2,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_ip_new11', 'Action': 'order', 'order': 'data_ip_new1', 'by': '访问应用数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[39]原语 data_ip_new11 = order data_ip_new1 by 访问应用数量 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_ip_new11', 'to': 'ssdb', 'with': 'data_ip_new_2', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[40]原语 store data_ip_new11 to ssdb with data_ip_new_2 as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_ip_new_3,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[41]原语 b = load ssdb by ssdb0 query qclear,data_ip_new_3,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_ip_new11', 'Action': 'order', 'order': 'data_ip_new1', 'by': '访问账号数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[42]原语 data_ip_new11 = order data_ip_new1 by 访问账号数量 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_ip_new11', 'to': 'ssdb', 'with': 'data_ip_new_3', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[43]原语 store data_ip_new11 to ssdb with data_ip_new_3 as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_ip_new_4,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[44]原语 b = load ssdb by ssdb0 query qclear,data_ip_new_4,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_ip_new11', 'Action': 'order', 'order': 'data_ip_new1', 'by': '访问次数', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[45]原语 data_ip_new11 = order data_ip_new1 by 访问次数 with de... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_ip_new11', 'to': 'ssdb', 'with': 'data_ip_new_4', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[46]原语 store data_ip_new11 to ssdb with data_ip_new_4 as ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_ip_new11'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[47]原语 drop data_ip_new11 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_ip_new1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[48]原语 drop data_ip_new1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[67]原语 ip_count = @udf udf0.new_df with num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip_num', 'Action': 'eval', 'eval': 'data_ip_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[68]原语 ip_num = eval data_ip_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_count', 'Action': '@udf', '@udf': 'ip_count', 'by': 'udf0.df_append', 'with': '$ip_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[69]原语 ip_count = @udf ip_count by udf0.df_append with $i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip1:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[70]原语 store ip_count to ssdb by ssdb0 with ip1:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'data_ip_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[72]原语 num = eval data_ip_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_num', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value,icon'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[73]原语 ip_num = @udf udf0.new_df with name,value,icon 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_num', 'Action': '@udf', '@udf': 'ip_num', 'by': 'udf0.df_append', 'with': '终端总数,$num,F441'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[74]原语 ip_num = @udf ip_num by udf0.df_append with 终端总数,$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_2', 'Action': 'filter', 'filter': 'data_ip_new', 'by': 'active == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[77]原语 active_2 = filter data_ip_new by active == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num2', 'Action': 'eval', 'eval': 'active_2', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[78]原语 num2 = eval active_2 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_num', 'Action': '@udf', '@udf': 'ip_num', 'by': 'udf0.df_append', 'with': '活跃终端数,$num2,F140'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[79]原语 ip_num = @udf ip_num by udf0.df_append with 活跃终端数,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_1', 'Action': 'filter', 'filter': 'data_ip_new', 'by': 'active == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[82]原语 active_1 = filter data_ip_new by active == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num1', 'Action': 'eval', 'eval': 'active_1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[83]原语 num1 = eval active_1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_num', 'Action': '@udf', '@udf': 'ip_num', 'by': 'udf0.df_append', 'with': '失活终端数,$num1,F141'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[84]原语 ip_num = @udf ip_num by udf0.df_append with 失活终端数,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_2', 'Action': 'filter', 'filter': 'data_ip_new', 'by': 'active == 2'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[87]原语 active_2 = filter data_ip_new by active == 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num2', 'Action': 'eval', 'eval': 'active_2', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[88]原语 num2 = eval active_2 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_num', 'Action': '@udf', '@udf': 'ip_num', 'by': 'udf0.df_append', 'with': '复活终端数,$num2,F146'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[89]原语 ip_num = @udf ip_num by udf0.df_append with 复活终端数,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'active_3', 'Action': 'filter', 'filter': 'data_ip_new', 'by': 'active == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[92]原语 active_3 = filter data_ip_new by active == 3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num3', 'Action': 'eval', 'eval': 'active_3', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[93]原语 num3 = eval active_3 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_num', 'Action': '@udf', '@udf': 'ip_num', 'by': 'udf0.df_append', 'with': '新增终端数,$num3,F147'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[94]原语 ip_num = @udf ip_num by udf0.df_append with 新增终端数,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ip_num', 'Action': 'add', 'add': 'pageid', 'by': "'modeling:ip_new','modeling:ip_new','modeling:ip_new','modeling:ip_new','modeling:ip_new'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[96]原语 ip_num = add pageid by ("modeling:ip_new","modelin... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ip_num', 'Action': 'add', 'add': '参数', 'by': "'','@active=0','@active=1','@active=2','@active=3'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[97]原语 ip_num = add 参数 by ("","@active=0","@active=1","@a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_num', 'Action': 'loc', 'loc': 'ip_num', 'by': 'name,value,icon,pageid,参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[99]原语 ip_num = loc ip_num by name,value,icon,pageid,参数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_num', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zd:type'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[100]原语 store ip_num to ssdb by ssdb0 with zd:type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_network', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[111]原语 ip_network = loc data_ip_new by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'ip_network.srcip', 'Action': 'str', 'str': 'srcip', 'by': "findall('(.*\\.)')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[112]原语 ip_network.srcip = str srcip by (findall("(.*\.)")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ip_network.srcip', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[113]原语 alter ip_network.srcip as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ip_network', 'Action': 'filter', 'filter': 'ip_network', 'by': "srcip != '[]'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[114]原语 ip_network = filter ip_network by srcip != "[]" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ip_network.srcip', 'Action': 'lambda', 'lambda': 'srcip', 'by': "x:x[2:-2]+'*'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[115]原语 ip_network.srcip = lambda srcip by (x:x[2:-2]+"*")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ip_network_group', 'Action': 'group', 'group': 'ip_network', 'by': 'srcip', 'agg': 'srcip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[116]原语 ip_network_group = group ip_network by srcip agg s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'n', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'setting as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[117]原语 n = load ssdb by ssdb0 with setting as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'nn', 'Action': 'jaas', 'jaas': 'n', 'by': "n['setting']['fbi_num']['network_num']", 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[118]原语 nn = jaas n by n["setting"]["fbi_num"]["network_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'nn', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'int($nn)-0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[119]原语 nn = @sdf sys_eval with (int($nn)-0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ip_network_group', 'Action': 'order', 'order': 'ip_network_group', 'by': 'srcip_count', 'with': 'desc limit $nn'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[120]原语 ip_network_group = order ip_network_group by srcip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_network_group', 'Action': 'loc', 'loc': 'ip_network_group', 'by': 'index', 'to': 'ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[121]原语 ip_network_group = loc ip_network_group by index t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ip_network_group', 'by': '"srcip_count":"网段数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[122]原语 rename ip_network_group by ("srcip_count":"网段数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_network_group', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip_network:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[123]原语 store ip_network_group to ssdb by ssdb0 with ip_ne... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_region', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'region,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[128]原语 ip_region = loc data_ip_new by region,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ip_region', 'Action': 'filter', 'filter': 'ip_region', 'by': "region != '未知'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[129]原语 ip_region = filter ip_region by region != "未知" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ip_region_group', 'Action': 'group', 'group': 'ip_region', 'by': 'region', 'agg': 'region:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[130]原语 ip_region_group = group ip_region by region agg re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'an', 'Action': 'jaas', 'jaas': 'n', 'by': "n['setting']['fbi_num']['areal_num']", 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[132]原语 an = jaas n by n["setting"]["fbi_num"]["areal_num"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'an', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'int($an)-2'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[133]原语 an = @sdf sys_eval with (int($an)-2) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ip_region_group', 'Action': 'order', 'order': 'ip_region_group', 'by': 'region_count', 'with': 'desc limit $an'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[134]原语 ip_region_group = order ip_region_group by region_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_region_group1', 'Action': 'loc', 'loc': 'ip_region_group', 'by': 'index', 'to': 'name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[135]原语 ip_region_group1 = loc ip_region_group by index to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ip_region_group1', 'by': '"name":"地域",\'region_count\':\'数量\''}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[136]原语 rename ip_region_group1 by ("name":"地域","region_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_region_group1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip_region1:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[137]原语 store ip_region_group1 to ssdb by ssdb0 with ip_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_region_group', 'Action': 'loc', 'loc': 'ip_region_group', 'by': 'index', 'to': 'name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[139]原语 ip_region_group = loc ip_region_group by index to ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ip_region_group.详情', 'Action': 'lambda', 'lambda': 'name', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[140]原语 ip_region_group.详情 = lambda name by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_region_group', 'Action': 'loc', 'loc': 'ip_region_group', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[141]原语 ip_region_group = loc ip_region_group by name to i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ip_region_group', 'by': '"region_count":"数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[142]原语 rename ip_region_group by ("region_count":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_region_group', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip_region:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[143]原语 store ip_region_group to ssdb by ssdb0 with ip_reg... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:IP_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[152]原语 aa = load ssdb by ssdb0 with dd:IP_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'aa', 'as': "'value':'详情'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[153]原语 rename aa as ("value":"详情") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ip_type', 'Action': 'group', 'group': 'data_ip_new', 'by': 'type', 'agg': 'type:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[154]原语 ip_type = group data_ip_new by type agg type:count... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ip_type', 'Action': 'join', 'join': 'aa,ip_type', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[155]原语 ip_type = join aa,ip_type by index,index with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip_type', 'Action': '@udf', '@udf': 'ip_type', 'by': 'udf0.df_fillna_cols', 'with': 'type_count:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[156]原语 ip_type = @udf ip_type by udf0.df_fillna_cols with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_type', 'Action': 'loc', 'loc': 'ip_type', 'by': 'type_count,详情'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[157]原语 ip_type = loc ip_type by type_count,详情 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ip_type', 'as': "'type_count':'数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[158]原语 rename ip_type as ("type_count":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_type', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'zd:type_count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[159]原语 store ip_type to ssdb by ssdb0 with zd:type_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_top', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'srcip,visit_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[164]原语 ip_top = loc data_ip_new by srcip,visit_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ip_top', 'Action': 'order', 'order': 'ip_top', 'by': 'visit_num', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[165]原语 ip_top = order ip_top by visit_num limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ip_top.详情', 'Action': 'lambda', 'lambda': 'srcip', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[166]原语 ip_top.详情 = lambda srcip by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcip_1', 'Action': 'loc', 'loc': 'ip_top', 'by': 'srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[167]原语 srcip_1 = loc ip_top by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ip_top', 'Action': 'loc', 'loc': 'ip_top', 'by': 'srcip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[168]原语 ip_top = loc ip_top by srcip to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'ip_top', 'Action': 'order', 'order': 'ip_top', 'by': 'visit_num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[169]原语 ip_top = order ip_top by visit_num with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ip_top', 'by': '"visit_num":"终端访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[170]原语 rename ip_top by ("visit_num":"终端访问数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ip_top', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'ip_top:bar'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[171]原语 store ip_top to ssdb by ssdb0 with ip_top:bar 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_ip', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'srcip,visit_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[174]原语 flow_ip = loc data_ip_new by srcip,visit_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'flow_ip', 'Action': 'add', 'add': '访问流量', 'by': 'flow_ip.visit_flow//1048576'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[175]原语 flow_ip = add 访问流量 by flow_ip.visit_flow//1048576 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'flow_ip', 'Action': 'order', 'order': 'flow_ip', 'by': '访问流量', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[176]原语 flow_ip = order flow_ip by 访问流量 limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcip_2', 'Action': 'loc', 'loc': 'flow_ip', 'by': 'srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[177]原语 srcip_2 = loc flow_ip by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'flow_ip.访问流量', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[178]原语 alter flow_ip.访问流量 as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'flow_ip.访问流量', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[179]原语 alter flow_ip.访问流量 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'flow_ip.访问流量', 'Action': 'lambda', 'lambda': '访问流量', 'by': "x:x+'(M)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[180]原语 flow_ip.访问流量=lambda 访问流量 by x:x+"(M)" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow_ip', 'Action': 'loc', 'loc': 'flow_ip', 'by': 'drop', 'drop': 'visit_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[181]原语 flow_ip = loc flow_ip by drop visit_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'flow_ip', 'by': '"srcip":"终端"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[182]原语 rename flow_ip by ("srcip":"终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'flow_ip', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'flow_iptop:table'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[184]原语 store flow_ip to ssdb by ssdb0 with flow_iptop:tab... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_topip', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'srcip,app_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[188]原语 app_topip = loc data_ip_new by srcip,app_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_topip_order', 'Action': 'order', 'order': 'app_topip', 'by': 'app_num', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[189]原语 app_topip_order = order app_topip by app_num limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcip_3', 'Action': 'loc', 'loc': 'app_topip_order', 'by': 'srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[190]原语 srcip_3 = loc app_topip_order by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_topip_order', 'Action': 'order', 'order': 'app_topip_order', 'by': 'app_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[191]原语 app_topip_order = order app_topip_order by app_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_topip_order.详情', 'Action': 'lambda', 'lambda': 'srcip', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[192]原语 app_topip_order.详情 = lambda srcip by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_topip_order', 'Action': 'loc', 'loc': 'app_topip_order', 'by': 'srcip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[193]原语 app_topip_order  = loc app_topip_order by srcip to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_topip_order', 'by': '"index":"应用最多终端","app_num":"应用数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[194]原语 rename app_topip_order by ("index":"应用最多终端","app_n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_topip_order', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_topip:bar'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[195]原语 store app_topip_order to ssdb by ssdb0 with app_to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ao_oa', 'Action': 'loc', 'loc': 'data_ip_new', 'by': 'srcip,account_num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[198]原语 ao_oa = loc data_ip_new by srcip,account_num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'account_topip_order', 'Action': 'order', 'order': 'ao_oa', 'by': 'account_num', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[199]原语 account_topip_order = order ao_oa by account_num l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcip_4', 'Action': 'loc', 'loc': 'account_topip_order', 'by': 'srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[200]原语 srcip_4 = loc account_topip_order by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'account_topip_order', 'Action': 'order', 'order': 'account_topip_order', 'by': 'account_num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[201]原语 account_topip_order = order account_topip_order by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'account_topip_order.详情', 'Action': 'lambda', 'lambda': 'srcip', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[202]原语 account_topip_order.详情 = lambda srcip by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'account_topip_order', 'Action': 'loc', 'loc': 'account_topip_order', 'by': 'srcip', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[203]原语 account_topip_order = loc account_topip_order by s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'account_topip_order', 'by': '"account_num":"账号数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[204]原语 rename account_topip_order by ("account_num":"账号数量... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'account_topip_order', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'account_iptop:bar'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[205]原语 store account_topip_order to ssdb by ssdb0 with ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'srcip', 'Action': 'union', 'union': 'srcip_1,srcip_2,srcip_3,srcip_4'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[209]原语 srcip = union srcip_1,srcip_2,srcip_3,srcip_4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'srcip', 'Action': 'distinct', 'distinct': 'srcip', 'by': 'srcip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[210]原语 srcip = distinct srcip by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'srcip', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'gl_ip'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[211]原语 store srcip to ssdb by ssdb0 with gl_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,srcip from data_ip_new where portrait_status = 0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[213]原语 aa = load db by mysql1 with select id,srcip from d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'id:int,srcip:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[214]原语 alter aa by id:int,srcip:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'srcip', 'Action': 'join', 'join': 'aa,srcip', 'by': 'srcip,srcip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[215]原语 srcip = join aa,srcip by srcip,srcip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcip', 'Action': '@udf', '@udf': 'srcip', 'by': 'udf0.df_fillna_cols', 'with': 'id:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[216]原语 srcip = @udf srcip by udf0.df_fillna_cols with id:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'srcip', 'Action': 'filter', 'filter': 'srcip', 'by': 'id != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[217]原语 srcip = filter srcip by id != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'srcip.index.size > 0', 'with': '""\nalter srcip.id as int\nsrcip = add portrait_status by (1)\nbbb = @sdf sys_now\nsrcip = add portrait_time by (\'$bbb\')\nsrcip = @udf srcip by udf0.df_set_index with id\nb = @udf srcip by CRUD.save_table with (mysql1,data_ip_new)\nsrcip = loc srcip by index to id\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=218
		ptree['funs']=block_if_218
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[218]原语 if srcip.index.size > 0 with "alter srcip.id as in... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_ip.fbi]执行第[228]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],229

#主函数结束,开始块函数

def block_if_218(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'srcip.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[219]原语 alter srcip.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'srcip', 'Action': 'add', 'add': 'portrait_status', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[220]原语 srcip = add portrait_status by (1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bbb', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[221]原语 bbb = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'srcip', 'Action': 'add', 'add': 'portrait_time', 'by': "'$bbb'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[222]原语 srcip = add portrait_time by ("$bbb") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'srcip', 'Action': '@udf', '@udf': 'srcip', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[223]原语 srcip = @udf srcip by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'srcip', 'by': 'CRUD.save_table', 'with': 'mysql1,data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[224]原语 b = @udf srcip by CRUD.save_table with (mysql1,dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'srcip', 'Action': 'loc', 'loc': 'srcip', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第218行if语句中]执行第[225]原语 srcip = loc srcip by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_218

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



