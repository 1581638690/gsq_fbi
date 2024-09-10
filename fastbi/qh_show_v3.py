#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: qh_show
#datetime: 2024-08-30T16:10:56.105436
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
		add_the_error('[qh_show.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from api_httpdata limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[18]原语 ccc = load ckh by ckh with select app from api_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[qh_show.fbi]执行第[19]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[19]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'visit1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select sum(visit_num) as visit_count,sum(visit_flow) as flow,left(toString(min(time)),19) as time from api_visit_hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[23]原语 visit1 = load ckh by ckh with select sum(visit_num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'visit1.index.size == 0', 'with': 'visit1 = @udf visit1 by udf0.df_append with (0,0,)'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=24
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[24]原语 if visit1.index.size == 0 with visit1 = @udf visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'visit1', 'by': 'visit_count:int,flow:int,time:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[25]原语 alter visit1 by visit_count:int,flow:int,time:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit', 'Action': 'loc', 'loc': 'visit1', 'by': 'visit_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[26]原语 visit = loc visit1 by visit_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'visit.vi_count', 'Action': 'lambda', 'lambda': 'visit_count', 'by': 'x:round(x/10000,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[27]原语 visit.vi_count = lambda visit_count by (x:round(x/... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'visit', 'Action': 'loc', 'loc': 'visit', 'by': 'vi_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[28]原语 visit = loc visit by vi_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'visit', 'as': "'vi_count':'总访问量(万次)'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[29]原语 rename visit as ("vi_count":"总访问量(万次)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt', 'Action': 'eval', 'eval': 'visit1', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[30]原语 tt = eval visit1 by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'visit', 'Action': 'add', 'add': 'tips', 'by': '"自$tt以来的总访问次数(HTTP协议)"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[31]原语 visit = add tips by ("自$tt以来的总访问次数(HTTP协议)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'visit', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit:count'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[32]原语 store visit to ssdb by ssdb0 with visit:count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'flow', 'Action': 'loc', 'loc': 'visit1', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[38]原语 flow = loc visit1 by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_flow', 'Action': 'eval', 'eval': 'flow', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[39]原语 v_flow = eval flow by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '0 <= $v_flow < 1024', 'with': '""\n#大屏\naa = loc flow by flow\nalter aa by flows:str\naa.flow = lambda flow by (x:x+\'(B)\')\nstore aa to ssdb by ssdb0 with visit_days1:sum\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=40
		ptree['funs']=block_if_40
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[40]原语 if 0 <= $v_flow < 1024  with "#大屏aa = loc flow by ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1024 <= $v_flow < 1048576', 'with': '""\n#大屏\n#flow = add flows by flow.flow//1024\nflow.flows = lambda flow by (x:round(x/1024,2))\naa = loc flow by flows\nalter aa by flows:str\naa.flows = lambda flows by (x:x+\'(KB)\')\nstore aa to ssdb by ssdb0 with visit_days1:sum\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=48
		ptree['funs']=block_if_48
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[48]原语 if 1024 <= $v_flow < 1048576  with "#大屏#flow = add... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1048576 <= $v_flow < 1073741824', 'with': '""\n#大屏\n#flow = add flows by flow.flow//1048576\nflow.flows = lambda flow by (x:round(x/1048576,2))\naa = loc flow by flows\nalter aa by flows:str\naa.flows = lambda flows by (x:x+\'(M)\')\nstore aa to ssdb by ssdb0 with visit_days1:sum\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=58
		ptree['funs']=block_if_58
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[58]原语 if 1048576 <= $v_flow < 1073741824  with "#大屏#flow... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '1073741824 <= $v_flow', 'with': '""\n#大屏\n#flow = add flows by flow.flow//1073741824\nflow.flows = lambda flow by (x:round(x/1073741824,2))\naa = loc flow by flows\nalter aa by flows:str\naa.flows = lambda flows by (x:x+\'(G)\')\nstore aa to ssdb by ssdb0 with visit_days1:sum\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=68
		ptree['funs']=block_if_68
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[68]原语 if 1073741824 <= $v_flow   with "#大屏#flow = add fl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,risk_level,first_time,risk_label from data_api_new where risk_level != "0" order by first_time desc limit 500'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[98]原语 e = @udf RS.load_mysql_sql with (mysql1,select app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'e', 'by': 'app:str,risk_level:str,first_time:str,risk_label:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[99]原语 alter e by app:str,risk_level:str,first_time:str,r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'e', 'Action': 'distinct', 'distinct': 'e', 'by': 'app', 'with': 'first'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[100]原语 e = distinct e by app with first 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'e.first_time', 'Action': 'str', 'str': 'first_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[101]原语 e.first_time = str first_time by (replace("T"," ")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'e.first_time', 'Action': 'str', 'str': 'first_time', 'by': 'slice(0,19)'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[102]原语 e.first_time = str first_time by (slice(0,19)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select risk_label,risk_name from data_api_risk'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[103]原语 sens = load db by mysql1 with select risk_label,ri... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'risk_label:str,risk_name:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[104]原语 alter sens by risk_label:str,risk_name:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'risk_label', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[105]原语 sens = loc sens by risk_label to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'by': '"risk_name":"value"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[106]原语 rename sens by ("risk_name":"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'e,sens', 'by': 'SP.tag2dict', 'with': 'risk_label'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[107]原语 e = @udf e,sens by SP.tag2dict with risk_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'level', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-risk_level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[108]原语 level = load ssdb by ssdb0 with dd:API-risk_level 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'e,level', 'by': 'SP.tag2dict', 'with': 'risk_level'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[109]原语 e = @udf e,level by SP.tag2dict with risk_level 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'e.risk_level', 'Action': 'lambda', 'lambda': 'risk_level', 'by': "x:x+'风险'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[110]原语 e.risk_level = lambda risk_level by (x:x+"风险") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'e', 'Action': 'loc', 'loc': 'e', 'by': 'app,risk_level,first_time,risk_label'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[111]原语 e = loc e by app,risk_level,first_time,risk_label 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'e', 'by': 'VL.set_col_width', 'with': '250,80,200,220'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[112]原语 e= @udf e by VL.set_col_width with (250,80,200,220... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'e', 'Action': '@udf', '@udf': 'e', 'by': 'VL.set_col_color', 'with': '#fff,#fff,#fff,#f00'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[113]原语 e = @udf e by VL.set_col_color with (#fff,#fff,#ff... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'e', 'by': '"app":"风险应用","risk_level":"风险等级","first_time":"首次发现时间","risk_label":"风险内容"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[114]原语 rename e by ("app":"风险应用","risk_level":"风险等级","fir... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'e', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risk:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[115]原语 store e to ssdb by ssdb0 with risk:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'g', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select region,count(*) as 数量 from data_ip_new group by region order by 数量 desc limit 10 ;'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[118]原语 g = @udf RS.load_mysql_sql with (mysql1,select reg... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'g', 'Action': '@udf', '@udf': 'g', 'by': 'udf0.df_fillna_cols', 'with': "region:'',数量:0"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[119]原语 g = @udf g by udf0.df_fillna_cols with region:"",数... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'g', 'Action': 'filter', 'filter': 'g', 'by': "region != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[120]原语 g = filter g by region != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'g', 'Action': 'order', 'order': 'g', 'by': '数量', 'with': 'desc limit 5'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[121]原语 g = order g by 数量 with desc limit 5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'g.详情', 'Action': 'lambda', 'lambda': 'region', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[122]原语 g.详情 = lambda region by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'g', 'Action': 'loc', 'loc': 'g', 'by': 'region', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[123]原语 g = loc g by region to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= rename', 'Ta': 'g', 'Action': 'rename', 'rename': 'g', 'by': '"count(*)":"数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[124]原语 g = rename g by ("count(*)":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'g', 'to': 'ssdb', 'with': 'ppregion:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[125]原语 store g to ssdb with ppregion:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'h', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select srcip,visit_num from data_ip_new order by visit_num desc limit 5'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[128]原语 h = load db by mysql1 with select srcip,visit_num ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'h', 'by': 'srcip:str,visit_num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[129]原语 alter h by srcip:str,visit_num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'h', 'by': '"srcip":"终端IP","maxcount":"数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[130]原语 rename h by ("srcip":"终端IP","maxcount":"数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'h', 'to': 'ssdb', 'with': 'riskipcount:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[131]原语 store h to ssdb with riskipcount:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'risk_level'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[145]原语 a = @udf udf0.new_df with risk_level 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[146]原语 a = @udf a by udf0.df_append with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[147]原语 a = @udf a by udf0.df_append with 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_append', 'with': '2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[148]原语 a = @udf a by udf0.df_append with 2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'a', 'by': 'risk_level:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[149]原语 alter a by risk_level:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select risk_level,count(url) as num from data_api_new group by risk_level'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[150]原语 aa = load db by mysql1 with select risk_level,coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'risk_level:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[151]原语 alter aa by risk_level:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'aa', 'Action': 'join', 'join': 'a,aa', 'by': 'risk_level,risk_level', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[152]原语 aa = join a,aa by risk_level,risk_level with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'aa', 'by': 'udf0.df_fillna_cols', 'with': 'num:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[153]原语 aa = @udf aa by udf0.df_fillna_cols with num:0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'di', 'Action': 'filter', 'filter': 'aa', 'by': "risk_level == '0'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[155]原语 di = filter aa by risk_level == "0" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'di', 'Action': 'loc', 'loc': 'di', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[156]原语 di = loc di by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'di', 'by': "'num':'低风险'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[157]原语 rename di by ("num":"低风险") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'di', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risklevel1:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[158]原语 store di to ssdb by ssdb0 with risklevel1:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'zhong', 'Action': 'filter', 'filter': 'aa', 'by': "risk_level == '1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[160]原语 zhong = filter aa by risk_level == "1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'zhong', 'Action': 'loc', 'loc': 'zhong', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[161]原语 zhong = loc zhong by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'zhong', 'as': "'num':'中风险'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[162]原语 rename zhong as ("num":"中风险") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'zhong', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risklevel2:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[163]原语 store zhong to ssdb by ssdb0 with risklevel2:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'gao', 'Action': 'filter', 'filter': 'aa', 'by': "risk_level == '2'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[165]原语 gao = filter aa by risk_level == "2" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'gao', 'Action': 'loc', 'loc': 'gao', 'by': 'num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[166]原语 gao = loc gao by num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'gao', 'as': "'num':'高风险'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[167]原语 rename gao as ("num":"高风险") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'gao', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'risklevel3:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[168]原语 store gao to ssdb by ssdb0 with risklevel3:data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_risk', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select b.type1,count(a.api) as num from api19_risk a left join api19_type b on a.type = b.type group by b.type1 order by num desc limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[171]原语 api19_risk = load db by mysql1 with select b.type1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'api19_risk', 'by': 'type1:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[172]原语 alter api19_risk by type1:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'api19_risk.弱点类型', 'Action': 'lambda', 'lambda': 'type1', 'by': 'x:x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[173]原语 api19_risk.弱点类型 = lambda type1 by (x:x) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api19_risk', 'Action': 'loc', 'loc': 'api19_risk', 'by': 'type1', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[174]原语 api19_risk = loc api19_risk by type1 to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'api19_risk', 'Action': 'order', 'order': 'api19_risk', 'by': 'num', 'with': 'asc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[175]原语 api19_risk = order api19_risk by num with asc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'api19_risk', 'as': "'num':'类型数量'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[176]原语 rename api19_risk as ("num":"类型数量") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'api19_risk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'api19_risk:data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[177]原语 store api19_risk to ssdb by ssdb0 with api19_risk:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[qh_show.fbi]执行第[180]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],180

#主函数结束,开始块函数

def block_if_40(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'flow', 'by': 'flow'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[42]原语 aa = loc flow by flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'flows:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[43]原语 alter aa by flows:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'aa.flow', 'Action': 'lambda', 'lambda': 'flow', 'by': "x:x+'(B)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[44]原语 aa.flow = lambda flow by (x:x+"(B)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days1:sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第40行if语句中]执行第[45]原语 store aa to ssdb by ssdb0 with visit_days1:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_40

def block_if_48(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'flow.flows', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1024,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第48行if语句中]执行第[51]原语 flow.flows = lambda flow by (x:round(x/1024,2)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'flow', 'by': 'flows'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第48行if语句中]执行第[52]原语 aa = loc flow by flows 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'flows:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第48行if语句中]执行第[53]原语 alter aa by flows:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'aa.flows', 'Action': 'lambda', 'lambda': 'flows', 'by': "x:x+'(KB)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第48行if语句中]执行第[54]原语 aa.flows = lambda flows by (x:x+"(KB)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days1:sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第48行if语句中]执行第[55]原语 store aa to ssdb by ssdb0 with visit_days1:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_48

def block_if_58(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'flow.flows', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1048576,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[61]原语 flow.flows = lambda flow by (x:round(x/1048576,2))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'flow', 'by': 'flows'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[62]原语 aa = loc flow by flows 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'flows:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[63]原语 alter aa by flows:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'aa.flows', 'Action': 'lambda', 'lambda': 'flows', 'by': "x:x+'(M)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[64]原语 aa.flows = lambda flows by (x:x+"(M)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days1:sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[65]原语 store aa to ssdb by ssdb0 with visit_days1:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_58

def block_if_68(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'flow.flows', 'Action': 'lambda', 'lambda': 'flow', 'by': 'x:round(x/1073741824,2)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[71]原语 flow.flows = lambda flow by (x:round(x/1073741824,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'flow', 'by': 'flows'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[72]原语 aa = loc flow by flows 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'aa', 'by': 'flows:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[73]原语 alter aa by flows:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'aa.flows', 'Action': 'lambda', 'lambda': 'flows', 'by': "x:x+'(G)'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[74]原语 aa.flows = lambda flows by (x:x+"(G)") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'visit_days1:sum'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第68行if语句中]执行第[75]原语 store aa to ssdb by ssdb0 with visit_days1:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_68

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



