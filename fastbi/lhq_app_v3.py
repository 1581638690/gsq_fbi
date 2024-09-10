#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_app
#datetime: 2024-08-30T16:10:54.742921
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
		add_the_error('[lhq_app.fbi]执行第[19]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_app_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,app_type,sx,sensitive_label from data_app_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[22]原语 data_app_new = load db by mysql1 with select app,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_app_new', 'by': 'app:str,app_type:int,sx:int,sensitive_label:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[23]原语 alter data_app_new by app:str,app_type:int,sx:int,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,value,icon,pageid,参数'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[25]原语 app_count = @udf udf0.new_df with (name,value,icon... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_num', 'Action': 'eval', 'eval': 'data_app_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[26]原语 app_num = eval data_app_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '应用总数,$app_num,F147,modeling:app_new,'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[27]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'local_app', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'app_type == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[28]原语 local_app = filter data_app_new by app_type == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'local_app', 'Action': 'eval', 'eval': 'local_app', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[29]原语 local_app = eval local_app by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '内部应用数量,$local_app,F147,modeling:app_new_1,@app_type=1'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[30]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'internet_app', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'app_type == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[31]原语 internet_app = filter data_app_new by app_type == ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'internet_app', 'Action': 'eval', 'eval': 'internet_app', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[32]原语 internet_app = eval internet_app by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '外部应用数量,$internet_app,F147,modeling:app_new_0,@app_type=0'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[33]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'yy', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'sx != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[35]原语 yy = filter data_app_new by sx != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'yy_num', 'Action': 'eval', 'eval': 'yy', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[36]原语 yy_num = eval yy by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$yy_num == 0', 'with': 'yy = @udf yy by udf0.df_append with (,,,)'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=37
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[37]原语 if $yy_num == 0 with yy = @udf yy by udf0.df_appen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'yy', 'Action': 'loc', 'loc': 'yy', 'by': 'sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[38]原语 yy = loc yy by sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'yy', 'Action': 'distinct', 'distinct': 'yy', 'by': 'sx'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[39]原语 yy = distinct yy by sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'yy', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[40]原语 yy = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'yy.sx', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[41]原语 alter yy.sx as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'yy.sx', 'Action': 'lambda', 'lambda': 'sx', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[42]原语 yy.sx = lambda sx by (x:x+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'yy', 'Action': 'group', 'group': 'yy', 'by': 'aa', 'agg': 'sx:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[43]原语 yy = group yy by aa agg sx:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'yy.sx_sum', 'Action': 'lambda', 'lambda': 'sx_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[44]原语 yy.sx_sum = lambda sx_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sx_num', 'Action': 'eval', 'eval': 'yy', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[45]原语 sx_num = eval yy by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '已纳管应用数量,$yy_num,F143,modeling:app_new,@sx='}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[46]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_count.参数', 'Action': 'lambda', 'lambda': '参数', 'by': "x:x+'$sx_num' if x == '@sx=' else x"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[47]原语 app_count.参数 = lambda 参数 by (x:x+"$sx_num" if x ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ww', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'sx == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[49]原语 ww = filter data_app_new by sx == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ww_num', 'Action': 'eval', 'eval': 'ww', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[50]原语 ww_num = eval ww by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '未纳管应用数量,$ww_num,F144,modeling:app_new,@sx=0'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[51]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_app_new.sensitive_label', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[53]原语 alter data_app_new.sensitive_label as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sensitive_app', 'Action': 'group', 'group': 'data_app_new', 'by': 'sensitive_label', 'agg': 'sensitive_label:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[54]原语 sensitive_app = group data_app_new by sensitive_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sensitive_app1', 'Action': 'filter', 'filter': 'sensitive_app', 'by': 'index == 3'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[55]原语 sensitive_app1 = filter sensitive_app by index == ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa_num', 'Action': 'eval', 'eval': 'sensitive_app1', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[57]原语 aa_num = eval sensitive_app1 by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num == 0', 'with': 'sensitive_app1 = @udf sensitive_app1 by udf0.df_append with 0'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=58
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[58]原语 if $aa_num == 0 with sensitive_app1 = @udf sensiti... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive_app1', 'Action': 'eval', 'eval': 'sensitive_app1', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[60]原语 sensitive_app1 = eval sensitive_app1 by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '高敏感应用数量,$sensitive_app1,F245,modeling:app_new,@sensitive_label=3'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[61]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[66]原语 store app_count to ssdb by ssdb0 with app:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'num'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[69]原语 app_count = @udf udf0.new_df with num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_num', 'Action': 'eval', 'eval': 'data_app_new', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[70]原语 app_num = eval data_app_new by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_count', 'Action': '@udf', '@udf': 'app_count', 'by': 'udf0.df_append', 'with': '$app_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[71]原语 app_count = @udf app_count by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_count', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app1:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[72]原语 store app_count to ssdb by ssdb0 with app1:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data_app_new', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app,visits_num,visits_flow,api_num,account_num,srcip_num,dstip_num,app_type,name,sx,id from data_app_new where merge_state != 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[76]原语 data_app_new = load db by mysql1 with select app,v... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app_new', 'Action': '@udf', '@udf': 'data_app_new', 'by': 'udf0.df_fillna_cols', 'with': "visits_num:0,visits_flow:0,api_num:0,account_num:0,srcip_num:0,dstip_num:0,app_type:0,name:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[77]原语 data_app_new = @udf data_app_new by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_app_new', 'by': 'visits_num:int,visits_flow:int,api_num:int,account_num:int,srcip_num:int,dstip_num:int,app_type:int,name:str,sx:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[78]原语 alter data_app_new by visits_num:int,visits_flow:i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app_sx', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:app_sx'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[79]原语 app_sx = load ssdb by ssdb0 with dd:app_sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_sx', 'Action': 'loc', 'loc': 'app_sx', 'by': 'index', 'to': 'sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[80]原语 app_sx = loc app_sx by index to sx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_sx.sx', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[81]原语 alter app_sx.sx as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_sx', 'Action': 'loc', 'loc': 'app_sx', 'by': 'sx', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[82]原语 app_sx = loc app_sx by sx to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_sx', 'as': "'sysname':'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[83]原语 rename app_sx as ("sysname":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app_new', 'Action': '@udf', '@udf': 'data_app_new,app_sx', 'by': 'SP.tag2dict', 'with': 'sx'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[84]原语 data_app_new = @udf data_app_new,app_sx by SP.tag2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app_new', 'Action': '@udf', '@udf': 'data_app_new', 'by': 'udf0.df_fillna_cols', 'with': "app:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[86]原语 data_app_new = @udf data_app_new by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_app_new', 'Action': 'filter', 'filter': 'data_app_new', 'by': "app != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[87]原语 data_app_new = filter data_app_new by app != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_app_new1', 'Action': 'loc', 'loc': 'data_app_new', 'by': 'id,app,name,sx,visits_num,visits_flow,api_num,srcip_num,account_num,dstip_num,app_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[90]原语 data_app_new1 = loc data_app_new by id,app,name,sx... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_app_new1', 'Action': 'filter', 'filter': 'data_app_new1', 'by': 'app_type == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[91]原语 data_app_new1 = filter data_app_new1 by app_type =... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_app_new1', 'as': "'id':'_id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[92]原语 rename data_app_new1 as ("id":"_id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data_app_new1.app_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[93]原语 alter data_app_new1.app_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'data_app_new1.app_type', 'Action': 'str', 'str': 'app_type', 'by': "replace('1','内部')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[94]原语 data_app_new1.app_type = str app_type by (replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'data_app_new1.app_type', 'Action': 'str', 'str': 'app_type', 'by': "replace('0','外部')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[95]原语 data_app_new1.app_type = str app_type by (replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'data_app_new1.visits_flow', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': 'x:round(x/1048576,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[96]原语 data_app_new1.visits_flow = lambda visits_flow by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': 'visits_num', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[97]原语 data_app_new11 = order data_app_new1 by visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'pq', 'by': 'dt_table/data_app_new.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[98]原语 store data_app_new11 to pq by dt_table/data_app_ne... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_app_new1', 'as': "'app':'应用IP/域名','name':'应用名称','sx':'关联应用','visits_num':'访问数量','visits_flow':'访问流量(M)','api_num':'接口数量','srcip_num':'访问IP数量','account_num':'访问账号数量','dstip_num':'部署数量','app_type':'应用类型'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[100]原语 rename data_app_new1 as ("app":"应用IP/域名","name":"应... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_app_new_1,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[101]原语 b = load ssdb by ssdb0 query qclear,data_app_new_1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': '访问数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[102]原语 data_app_new11 = order data_app_new1 by 访问数量 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'ssdb', 'with': 'data_app_new_1', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[103]原语 store data_app_new11 to ssdb with data_app_new_1 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_app_new_2,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[104]原语 b = load ssdb by ssdb0 query qclear,data_app_new_2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': '访问流量(M)', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[105]原语 data_app_new11 = order data_app_new1 by 访问流量(M) wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'ssdb', 'with': 'data_app_new_2', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[106]原语 store data_app_new11 to ssdb with data_app_new_2 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_app_new_3,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[107]原语 b = load ssdb by ssdb0 query qclear,data_app_new_3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': '接口数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[108]原语 data_app_new11 = order data_app_new1 by 接口数量 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'ssdb', 'with': 'data_app_new_3', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[109]原语 store data_app_new11 to ssdb with data_app_new_3 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_app_new_4,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[110]原语 b = load ssdb by ssdb0 query qclear,data_app_new_4... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': '访问IP数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[111]原语 data_app_new11 = order data_app_new1 by 访问IP数量 wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'ssdb', 'with': 'data_app_new_4', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[112]原语 store data_app_new11 to ssdb with data_app_new_4 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_app_new_5,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[113]原语 b = load ssdb by ssdb0 query qclear,data_app_new_5... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': '访问账号数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[114]原语 data_app_new11 = order data_app_new1 by 访问账号数量 wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'ssdb', 'with': 'data_app_new_5', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[115]原语 store data_app_new11 to ssdb with data_app_new_5 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,data_app_new_6,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[116]原语 b = load ssdb by ssdb0 query qclear,data_app_new_6... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'data_app_new11', 'Action': 'order', 'order': 'data_app_new1', 'by': '部署数量', 'with': 'desc limit 1000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[117]原语 data_app_new11 = order data_app_new1 by 部署数量 with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data_app_new11', 'to': 'ssdb', 'with': 'data_app_new_6', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[118]原语 store data_app_new11 to ssdb with data_app_new_6 a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_app_new1'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[119]原语 drop data_app_new1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'drop', 'drop': 'data_app_new11'}
	try:
		drop_table(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[120]原语 drop data_app_new11 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_app_new', 'Action': 'loc', 'loc': 'data_app_new', 'by': 'app,visits_num,visits_flow,api_num,account_num,srcip_num,dstip_num,app_type,name,sx'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[122]原语 data_app_new = loc data_app_new by app,visits_num,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app_new', 'Action': '@udf', '@udf': 'data_app_new', 'by': 'udf0.df_replace', 'with': '无,'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[130]原语 data_app_new = @udf data_app_new by udf0.df_replac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app_new', 'Action': '@udf', '@udf': 'data_app_new', 'by': 'udf0.df_row_lambda', 'with': "x: x[8] if x[8] != '' else x[9] "}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[131]原语 data_app_new = @udf data_app_new by udf0.df_row_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'data_app_new', 'Action': '@udf', '@udf': 'data_app_new', 'by': 'udf0.df_row_lambda', 'with': "x: x[10] if x[10] != '' else x[0] "}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[132]原语 data_app_new = @udf data_app_new by udf0.df_row_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data_app_new', 'Action': 'loc', 'loc': 'data_app_new', 'by': 'app,visits_num,visits_flow,api_num,account_num,srcip_num,dstip_num,app_type,lambda1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[133]原语 data_app_new = loc data_app_new by app,visits_num,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data_app_new', 'as': "'lambda1':'name'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[134]原语 rename data_app_new as ("lambda1":"name") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_type_1', 'Action': 'filter', 'filter': 'data_app_new', 'by': 'app_type == 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[138]原语 app_type_1 = filter data_app_new by app_type == 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_join_order', 'Action': 'loc', 'loc': 'app_type_1', 'by': 'app,visits_num,name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[139]原语 app_join_order = loc app_type_1 by app,visits_num,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_join_order', 'Action': 'order', 'order': 'app_join_order', 'by': 'visits_num', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[140]原语 app_join_order = order app_join_order by visits_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_1', 'Action': 'loc', 'loc': 'app_join_order', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[141]原语 app_1 = loc app_join_order by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'num', 'Action': 'eval', 'eval': 'app_join_order', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[142]原语 num = eval app_join_order by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num != 0', 'with': 'aa_num = eval app_join_order by iloc[$num-1,1]'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ptree['lineno']=143
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[143]原语 if $num != 0 with aa_num = eval app_join_order by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num == 0', 'with': 'aa_num = eval app_join_order by index.size'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=144
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[144]原语 if $num == 0 with aa_num = eval app_join_order by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$num != 0 and $aa_num >= 10000', 'with': 'app_join_order.visits_num = lambda visits_num by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=145
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[145]原语 if $num != 0 and $aa_num >= 10000 with app_join_or... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_join_order.visits_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[146]原语 alter app_join_order.visits_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_join_order.visits_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[147]原语 alter app_join_order.visits_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num >= 10000', 'with': "app_join_order.visits_num = lambda visits_num by (x:x+'(万次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=148
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[148]原语 if $aa_num >= 10000 with app_join_order.visits_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa_num < 10000', 'with': "app_join_order.visits_num = lambda visits_num by (x:x+'(次)')"}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=149
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[149]原语 if $aa_num < 10000 with app_join_order.visits_num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_join_order', 'by': '\'name\':\'局域网应用\',\'app\':\'参数\',"visits_num":"应用访问数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[150]原语 rename app_join_order by ("name":"局域网应用","app":"参数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_join_order', 'Action': 'loc', 'loc': 'app_join_order', 'by': '局域网应用,应用访问数量,参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[151]原语 app_join_order = loc app_join_order by 局域网应用,应用访问数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_join_order', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_app:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[152]原语 store app_join_order to ssdb by ssdb0 with visit_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_flow_join', 'Action': 'loc', 'loc': 'app_type_1', 'by': 'app,visits_flow,name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[155]原语 app_flow_join = loc app_type_1 by app,visits_flow,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_flow_join1', 'Action': 'order', 'order': 'app_flow_join', 'by': 'visits_flow', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[156]原语 app_flow_join1 = order app_flow_join by visits_flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_flow_join', 'Action': 'order', 'order': 'app_flow_join', 'by': 'visits_flow', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[157]原语 app_flow_join = order app_flow_join by visits_flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_2', 'Action': 'loc', 'loc': 'app_flow_join', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[158]原语 app_2 = loc app_flow_join by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_flow_join', 'Action': 'order', 'order': 'app_flow_join', 'by': 'visits_flow', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[159]原语 app_flow_join = order app_flow_join by visits_flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_flow_join.访问流量(M)', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': 'x:round(x/1024/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[160]原语 app_flow_join.访问流量(M) = lambda visits_flow by (x:r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_flow_join', 'Action': 'filter', 'filter': 'app_flow_join', 'by': 'visits_flow != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[161]原语 app_flow_join = filter app_flow_join by visits_flo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_flow_join', 'Action': 'loc', 'loc': 'app_flow_join', 'by': 'drop', 'drop': 'visits_flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[162]原语 app_flow_join = loc app_flow_join by drop visits_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_flow_join.访问流量(M)', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[163]原语 alter app_flow_join.访问流量(M) as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_flow_join.访问流量(M)', 'Action': 'lambda', 'lambda': '访问流量(M)', 'by': "x:x+'(M)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[164]原语 app_flow_join.访问流量(M) = lambda 访问流量(M) by (x:x+"(M... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_flow_join', 'Action': 'loc', 'loc': 'app_flow_join', 'by': 'name,访问流量(M),app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[165]原语 app_flow_join = loc app_flow_join by name,访问流量(M),... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_flow_join', 'as': "'name':'局域网应用','app':'参数'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[166]原语 rename app_flow_join as ("name":"局域网应用","app":"参数"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_flow_join', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'flow_app:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[167]原语 store app_flow_join to ssdb by ssdb0 with flow_app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_flow_join1', 'Action': 'loc', 'loc': 'app_flow_join1', 'by': 'drop', 'drop': 'name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[170]原语 app_flow_join1 = loc app_flow_join1 by drop name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_flow_join1', 'Action': 'order', 'order': 'app_flow_join1', 'by': 'visits_flow', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[171]原语 app_flow_join1 = order app_flow_join1 by visits_fl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_flow_join1.visits_flow', 'Action': 'lambda', 'lambda': 'visits_flow', 'by': 'x:round(x/1024/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[172]原语 app_flow_join1.visits_flow = lambda visits_flow by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_flow_join1.详情', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[173]原语 app_flow_join1.详情 = lambda app by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_flow_join1', 'Action': 'loc', 'loc': 'app_flow_join1', 'by': 'app', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[174]原语 app_flow_join1 = loc app_flow_join1 by app to inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_flow_join1', 'by': '"visits_flow":"访问流量(M)"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[175]原语 rename app_flow_join1 by ("visits_flow":"访问流量(M)")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_flow_join1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'flow_app1:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[176]原语 store app_flow_join1 to ssdb by ssdb0 with flow_ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_join', 'Action': 'loc', 'loc': 'app_type_1', 'by': 'name,api_num,app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[180]原语 visit_join = loc app_type_1 by name,api_num,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_join_limit', 'Action': 'order', 'order': 'visit_join', 'by': 'api_num', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[181]原语 visit_join_limit = order visit_join by api_num lim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'visit_join_limit', 'Action': 'filter', 'filter': 'visit_join_limit', 'by': 'api_num != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[182]原语 visit_join_limit = filter visit_join_limit by api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_3', 'Action': 'loc', 'loc': 'visit_join_limit', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[183]原语 app_3 = loc visit_join_limit by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_join_limit', 'Action': 'loc', 'loc': 'visit_join_limit', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[186]原语 visit_join_limit = loc visit_join_limit by name to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_join_limit', 'by': '"app":"参数","api_num":"接口数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[187]原语 rename visit_join_limit by ("app":"参数","api_num":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_join_limit', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'max_api_app:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[188]原语 store visit_join_limit to ssdb by ssdb0 with max_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'vi_srcip_join', 'Action': 'loc', 'loc': 'app_type_1', 'by': 'name,srcip_num,app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[192]原语 vi_srcip_join = loc app_type_1 by name,srcip_num,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'vi_srcip_group', 'Action': 'order', 'order': 'vi_srcip_join', 'by': 'srcip_num', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[193]原语 vi_srcip_group = order vi_srcip_join by srcip_num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'vi_srcip_group', 'Action': 'filter', 'filter': 'vi_srcip_group', 'by': 'srcip_num != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[194]原语 vi_srcip_group = filter vi_srcip_group by srcip_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_4', 'Action': 'loc', 'loc': 'vi_srcip_group', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[195]原语 app_4 = loc vi_srcip_group by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'vi_srcip_group', 'by': '"app":"参数","srcip_num":"访问IP数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[196]原语 rename vi_srcip_group by ("app":"参数","srcip_num":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'vi_srcip_group', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'max_srcip:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[197]原语 store vi_srcip_group to ssdb by ssdb0 with max_src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_join', 'Action': 'loc', 'loc': 'app_type_1', 'by': 'name,dstip_num,app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[200]原语 visit_join = loc app_type_1 by name,dstip_num,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_top10_ip', 'Action': 'order', 'order': 'visit_join', 'by': 'dstip_num', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[201]原语 visit_top10_ip = order visit_join by dstip_num lim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'visit_top10_ip', 'Action': 'filter', 'filter': 'visit_top10_ip', 'by': 'dstip_num != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[202]原语 visit_top10_ip = filter visit_top10_ip by dstip_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_5', 'Action': 'loc', 'loc': 'visit_top10_ip', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[203]原语 app_5 = loc visit_top10_ip by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_top10_ip', 'Action': 'order', 'order': 'visit_top10_ip', 'by': 'dstip_num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[204]原语 visit_top10_ip = order visit_top10_ip by dstip_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit_top10_ip', 'by': "'name':'局域网应用','app':'参数','dstip_num':'部署数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[206]原语 rename visit_top10_ip by ("name":"局域网应用","app":"参数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit_top10_ip', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'max_ip_app:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[207]原语 store visit_top10_ip to ssdb by ssdb0 with max_ip_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit_account', 'Action': 'loc', 'loc': 'app_type_1', 'by': 'name,account_num,app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[211]原语 visit_account = loc app_type_1 by name,account_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'visit_account', 'Action': 'order', 'order': 'visit_account', 'by': 'account_num', 'limit': '5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[212]原语 visit_account = order visit_account by account_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'visit_account', 'Action': 'filter', 'filter': 'visit_account', 'by': 'account_num != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[213]原语 visit_account = filter visit_account by account_nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_6', 'Action': 'loc', 'loc': 'visit_account', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[214]原语 app_6 = loc visit_account by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'max_a_app', 'Action': 'loc', 'loc': 'visit_account', 'by': 'name', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[217]原语 max_a_app = loc visit_account by name to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'max_a_app', 'by': '\'name\':\'局域网应用访问账号Top10\',"app":"参数","account_num":"账号数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[218]原语 rename max_a_app by ("name":"局域网应用访问账号Top10","app"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'max_a_app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'max_a_app:top10'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[219]原语 store max_a_app to ssdb by ssdb0 with max_a_app:to... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_l', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[223]原语 api_l = load pq by sensitive/sens_data.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api_l', 'by': 'app:str,url:str,src_ip:str,account:str,key:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[224]原语 alter api_l by app:str,url:str,src_ip:str,account:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'api_l', 'Action': 'group', 'group': 'api_l', 'by': 'key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[225]原语 api_l = group api_l by key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api_l', 'Action': '@udf', '@udf': 'api_l', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[226]原语 api_l = @udf api_l by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api_l', 'as': "'num_sum':'标签数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[227]原语 rename api_l as ("num_sum":"标签数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_l_1', 'Action': 'loc', 'loc': 'api_l', 'by': '标签数量,key'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[229]原语 api_l_1 = loc api_l by 标签数量,key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api_l_1', 'Action': 'order', 'order': 'api_l_1', 'by': '标签数量', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[230]原语 api_l_1 = order api_l_1 by 标签数量 limit 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_l_1.详情', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[231]原语 api_l_1.详情 = lambda key by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_l_1.key', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x.replace("纳税人名称或公司名称","纳税人名称")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[232]原语 api_l_1.key = lambda key by (x:x.replace("纳税人名称或公司... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api_l_1.key', 'Action': 'lambda', 'lambda': 'key', 'by': 'x:x.replace("纳税人识别号或社会统一信用代码","纳税人识别号")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[233]原语 api_l_1.key = lambda key by (x:x.replace("纳税人识别号或社... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'aa', 'Action': 'order', 'order': 'api_l_1', 'by': '标签数量', 'with': 'asc limit 1'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[234]原语 aa = order api_l_1 by 标签数量 with asc limit 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[235]原语 aa = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa > 10000', 'with': 'api_l_1.标签数量 = lambda 标签数量 by (x:round(x/10000,2))'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=236
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[236]原语 if $aa > 10000 with api_l_1.标签数量 = lambda 标签数量 by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa > 10000', 'with': 'rename api_l_1 as ("标签数量":"标签数量(万)")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=237
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[237]原语 if $aa > 10000 with rename api_l_1 as ("标签数量":"标签数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa <= 10000', 'with': 'rename api_l_1 as ("标签数量":"标签数量")'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=238
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[238]原语 if $aa <= 10000 with rename api_l_1 as ("标签数量":"标签... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_l_1', 'Action': 'loc', 'loc': 'api_l_1', 'by': 'key', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[239]原语 api_l_1 = loc api_l_1 by key to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api_l_1', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'label:pie'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[240]原语 store api_l_1 to ssdb by ssdb0 with label:pie 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'api_l.key', 'Action': 'str', 'str': 'key', 'by': 'slice(0,4)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[242]原语 api_l.key = str key by (slice(0,4)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api_l', 'Action': 'loc', 'loc': 'api_l', 'by': 'key', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[243]原语 api_l = loc api_l by key to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'label_num', 'Action': 'eval', 'eval': 'api_l', 'by': 'iloc[:,0].sum()'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[244]原语 label_num = eval api_l by (iloc[:,0].sum()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_label', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '标签数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[245]原语 app_label = @udf udf0.new_df with (标签数量) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_label', 'Action': '@udf', '@udf': 'app_label', 'by': 'udf0.df_append', 'with': '$label_num'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[246]原语 app_label = @udf app_label by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_label', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_label:num'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[247]原语 store app_label to ssdb by ssdb0 with app_label:nu... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_label_group', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': '网段数量'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[250]原语 app_label_group = @udf udf0.new_df with 网段数量 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_label', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select distinct app from data_api_new where app != ''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[251]原语 app_label = @udf RS.load_mysql_sql with (mysql1,se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_label', 'by': 'app:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[252]原语 alter app_label by app:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'wd', 'Action': 'loc', 'loc': 'data_app_new', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[253]原语 wd = loc data_app_new by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app_label', 'Action': 'join', 'join': 'wd,app_label', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[254]原语 app_label = join wd,app_label by app,app with left... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_label.app', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[255]原语 app_label.app = lambda app by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_label', 'Action': '@udf', '@udf': 'app_label', 'by': 'udf0.df_l2cs', 'with': 'app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[256]原语 app_label = @udf app_label by udf0.df_l2cs with ap... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_label', 'Action': 'loc', 'loc': 'app_label', 'by': 'n100'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[257]原语 app_label = loc app_label by n100 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_label', 'as': "'n100':'app'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[258]原语 rename app_label as ("n100":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'app_label.n', 'Action': 'str', 'str': 'app', 'by': 'slice(-1,)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[259]原语 app_label.n = str app by (slice(-1,)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_label', 'Action': 'filter', 'filter': 'app_label', 'by': "n == '0' or n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[260]原语 app_label = filter app_label by n == "0" or n == "... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'app_label.app', 'Action': 'str', 'str': 'app', 'by': "findall('(.*\\.)')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[261]原语 app_label.app = str app by (findall("(.*\.)")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_label.app', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[262]原语 alter app_label.app as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app_label', 'Action': 'filter', 'filter': 'app_label', 'by': "app != '[]'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[263]原语 app_label = filter app_label by app != "[]" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_label.app', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x[2:-2]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[264]原语 app_label.app = lambda app by (x:x[2:-2]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_label.app', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x+"*"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[265]原语 app_label.app = lambda app by (x:x+"*") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'app_label_group', 'Action': 'group', 'group': 'app_label', 'by': 'app', 'agg': 'app:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[266]原语 app_label_group = group app_label by app agg app:c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app_label_group', 'Action': 'order', 'order': 'app_label_group', 'by': 'app_count', 'limit': '10'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[267]原语 app_label_group = order app_label_group by app_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_label_group', 'by': '"app_count":"网段数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[268]原语 rename app_label_group by ("app_count":"网段数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_label_group', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_label:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[269]原语 store app_label_group to ssdb by ssdb0 with app_la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'n', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'setting as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[274]原语 n = load ssdb by ssdb0 with setting as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'sn', 'Action': 'jaas', 'jaas': 'n', 'by': "n['setting']['fbi_num']['server_num']", 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[275]原语 sn = jaas n by n["setting"]["fbi_num"]["server_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'sn', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'int($sn)-0'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[276]原语 sn = @sdf sys_eval with (int($sn)-0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app_server', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select server,count(server) as a from data_app_new where server !='' group by server order by a desc limit $sn"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[277]原语 app_server = @udf RS.load_mysql_sql with (mysql1,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app_server', 'by': 'server:str,a:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[278]原语 alter app_server by server:str,a:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app_server', 'by': '"a":"服务类型数量","server":"服务类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[279]原语 rename app_server by ("a":"服务类型数量","server":"服务类型"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app_server.详情', 'Action': 'lambda', 'lambda': '服务类型', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[280]原语 app_server.详情 = lambda 服务类型 by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app_server', 'Action': 'loc', 'loc': 'app_server', 'by': '服务类型', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[281]原语 app_server = loc app_server by 服务类型 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app_server', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'app_server:trend'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[282]原语 store app_server to ssdb by ssdb0 with app_server:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'app', 'Action': 'union', 'union': 'app_1,app_2,app_3,app_4,app_5,app_6'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[286]原语 app = union app_1,app_2,app_3,app_4,app_5,app_6 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app', 'Action': 'distinct', 'distinct': 'app', 'by': 'app'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[287]原语 app = distinct app by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'gl_app'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[288]原语 store app to ssdb by ssdb0 with gl_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,app from data_app_new where portrait_status = 0'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[290]原语 aa = load db by mysql1 with select id,app from dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'id:int,app:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[291]原语 alter aa by id:int,app:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app', 'Action': 'join', 'join': 'aa,app', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[292]原语 app = join aa,app by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_fillna_cols', 'with': 'id:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[293]原语 app = @udf app by udf0.df_fillna_cols with id:0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app', 'Action': 'filter', 'filter': 'app', 'by': 'id != 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[294]原语 app = filter app by id != 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'app.index.size > 0', 'with': '""\nalter app.id as int\napp = add portrait_status by (1)\nbbb = @sdf sys_now\napp = add portrait_time by (\'$bbb\')\napp = @udf app by udf0.df_set_index with id\nb = @udf app by CRUD.save_table with (mysql1,data_app_new)\napp = loc app by index to id\n\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=295
		ptree['funs']=block_if_295
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[295]原语 if app.index.size > 0 with "alter app.id as intapp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_app.fbi]执行第[307]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],307

#主函数结束,开始块函数

def block_if_295(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app.id', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[296]原语 alter app.id as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'portrait_status', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[297]原语 app = add portrait_status by (1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bbb', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[298]原语 bbb = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'app', 'Action': 'add', 'add': 'portrait_time', 'by': "'$bbb'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[299]原语 app = add portrait_time by ("$bbb") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[300]原语 app = @udf app by udf0.df_set_index with id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'app', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[301]原语 b = @udf app by CRUD.save_table with (mysql1,data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第295行if语句中]执行第[302]原语 app = loc app by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_295

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



