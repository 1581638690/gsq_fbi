#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: link_XFF
#datetime: 2024-08-30T16:10:54.818321
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
		add_the_error('[link_XFF.fbi]执行第[13]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[16]原语 aa = load ssdb by ssdb0 with link_xff 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[18]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load db by mysql1 with select min(gmt_create) as time from ip_datalink'}
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
		add_the_error('[link_XFF.fbi]执行第[19]原语 if $a_num == 0 with aa = load db by mysql1 with se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[21]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select max(gmt_create) as time from ip_datalink'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[23]原语 aa = load db by mysql1 with select max(gmt_create)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[24]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select app from ip_datalink where gmt_create >= '$time1' and gmt_create < '$time2' limit 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[27]原语 ccc = load db by mysql1 with select app from ip_da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接 或 无数据更新！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[link_XFF.fbi]执行第[28]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[28]原语 assert find_df_have_data("ccc",ptree) as exit with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[30]原语 store aa to ssdb by ssdb0 with link_xff 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ff1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct account as S,ip as O from ip_datalink where account != '' and ip != '127.0.0.1' and gmt_create >= '$time1' and gmt_create < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[33]原语 ff1 = load db by mysql1 with select distinct accou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ff1', 'Action': 'add', 'add': 'P', 'by': '"acc_xff"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[34]原语 ff1 = add P by ("acc_xff") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type1', 'Action': 'loc', 'loc': 'ff1', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[36]原语 type1 = loc ff1 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type1', 'Action': 'add', 'add': 'type', 'by': "'应用账号'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[37]原语 type1 = add type by ("应用账号") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type2', 'Action': 'loc', 'loc': 'ff1', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[38]原语 type2 = loc ff1 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type2', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[39]原语 rename type2 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type2', 'Action': 'add', 'add': 'type', 'by': "'XFF'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[40]原语 type2 = add type by ("XFF") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'link', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct ip,ip_link,agent_ip from ip_datalink where gmt_create >= '$time1' and gmt_create < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[44]原语 link = load db by mysql1 with select distinct ip,i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'link.ip_link', 'Action': 'str', 'str': 'ip_link', 'by': 'replace("\'","")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[45]原语 link.ip_link = str ip_link by (replace(","")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'link.ip_link', 'Action': 'lambda', 'lambda': 'ip_link', 'by': 'x:x[1:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[46]原语 link.ip_link = lambda ip_link by (x:x[1:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'link.ip_link', 'Action': 'lambda', 'lambda': 'ip_link', 'by': 'x:x.split(", ")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[47]原语 link.ip_link = lambda ip_link by (x:x.split(", "))... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_l2cs', 'with': 'ip_link'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[49]原语 link = @udf link by udf0.df_l2cs with ip_link 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[50]原语 link = @udf link by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[51]原语 link = @udf link by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'drop': 'ip_link,index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[52]原语 link = loc link drop ip_link,index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nn', 'Action': 'loc', 'loc': 'link', 'by': 'ip,n100'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[54]原语 nn = loc link by ip,n100 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'nn', 'as': "'ip':'S','n100':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[55]原语 rename nn as ("ip":"S","n100":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type_xff', 'Action': 'loc', 'loc': 'nn', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[56]原语 type_xff = loc nn by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type_xff', 'Action': 'add', 'add': 'type', 'by': "'XFF'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[57]原语 type_xff = add type by ("XFF") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'by': 'n100,n101,n102,n103,n104,agent_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[59]原语 link = loc link by n100,n101,n102,n103,n104,agent_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'link', 'as': "'n100':'t1','n101':'t2','n102':'t3','n103':'t4','n104':'t5'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[60]原语 rename link as ("n100":"t1","n101":"t2","n102":"t3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_row_lambda', 'with': "x: x[5] if x[1] == '' else x[1]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[61]原语 link = @udf link by udf0.df_row_lambda with (x: x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'drop': 't2'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[62]原语 link = loc link drop t2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'link', 'as': "'lambda1':'t2'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[63]原语 rename link as ("lambda1":"t2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'by': 't1,t2,t3,t4,t5,agent_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[64]原语 link = loc link by t1,t2,t3,t4,t5,agent_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_row_lambda', 'with': "x: x[5] if x[2] == '' else x[2]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[65]原语 link = @udf link by udf0.df_row_lambda with (x: x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'drop': 't3'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[66]原语 link = loc link drop t3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'link', 'as': "'lambda1':'t3'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[67]原语 rename link as ("lambda1":"t3") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'by': 't1,t2,t3,t4,t5,agent_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[68]原语 link = loc link by t1,t2,t3,t4,t5,agent_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_row_lambda', 'with': "x: x[5] if x[3] == '' else x[3]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[69]原语 link = @udf link by udf0.df_row_lambda with (x: x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'drop': 't4'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[70]原语 link = loc link drop t4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'link', 'as': "'lambda1':'t4'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[71]原语 rename link as ("lambda1":"t4") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'by': 't1,t2,t3,t4,t5,agent_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[72]原语 link = loc link by t1,t2,t3,t4,t5,agent_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'link', 'Action': '@udf', '@udf': 'link', 'by': 'udf0.df_row_lambda', 'with': "x: x[5] if x[4] == '' else x[4]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[73]原语 link = @udf link by udf0.df_row_lambda with (x: x[... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'drop': 't5'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[74]原语 link = loc link drop t5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'link', 'as': "'lambda1':'t5'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[75]原语 rename link as ("lambda1":"t5") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link', 'Action': 'loc', 'loc': 'link', 'by': 't1,t2,t3,t4,t5,agent_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[76]原语 link = loc link by t1,t2,t3,t4,t5,agent_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nn1', 'Action': 'loc', 'loc': 'link', 'by': 't1,t2'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[77]原语 nn1 = loc link by t1,t2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'nn1', 'Action': 'distinct', 'distinct': 'nn1', 'by': 't1,t2'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[78]原语 nn1 = distinct nn1 by t1,t2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'nn1', 'as': "'t1':'S','t2':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[79]原语 rename nn1 as ("t1":"S","t2":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nn2', 'Action': 'loc', 'loc': 'link', 'by': 't2,t3'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[80]原语 nn2 = loc link by t2,t3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'nn2', 'Action': 'distinct', 'distinct': 'nn2', 'by': 't2,t3'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[81]原语 nn2 = distinct nn2 by t2,t3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'nn2', 'as': "'t2':'S','t3':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[82]原语 rename nn2 as ("t2":"S","t3":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nn3', 'Action': 'loc', 'loc': 'link', 'by': 't3,t4'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[83]原语 nn3 = loc link by t3,t4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'nn3', 'Action': 'distinct', 'distinct': 'nn3', 'by': 't3,t4'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[84]原语 nn3 = distinct nn3 by t3,t4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'nn3', 'as': "'t3':'S','t4':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[85]原语 rename nn3 as ("t3":"S","t4":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nn4', 'Action': 'loc', 'loc': 'link', 'by': 't4,t5'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[86]原语 nn4 = loc link by t4,t5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'nn4', 'Action': 'distinct', 'distinct': 'nn4', 'by': 't4,t5'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[87]原语 nn4 = distinct nn4 by t4,t5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'nn4', 'as': "'t4':'S','t5':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[88]原语 rename nn4 as ("t4":"S","t5":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ff2', 'Action': 'union', 'union': 'nn1,nn2,nn3,nn4,nn5'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[90]原语 ff2 = union nn1,nn2,nn3,nn4,nn5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ff2', 'Action': 'distinct', 'distinct': 'ff2', 'by': 'S,O'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[91]原语 ff2 = distinct ff2 by S,O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff2', 'Action': 'loc', 'loc': 'ff2', 'by': 'S,O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[92]原语 ff2 = loc ff2 by S,O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ff2', 'Action': 'union', 'union': 'ff2,nn'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[94]原语 ff2 = union ff2,nn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff2', 'Action': '@udf', '@udf': 'ff2', 'by': 'udf0.df_row_lambda', 'with': 'x: 0 if x[0] != x[1] else 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[95]原语 ff2 = @udf ff2 by udf0.df_row_lambda with (x: 0 if... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff2', 'Action': 'filter', 'filter': 'ff2', 'by': 'lambda1 == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[96]原语 ff2 = filter ff2 by lambda1 == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ff2', 'Action': 'add', 'add': 'P', 'by': '"link_xff"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[97]原语 ff2 = add P by ("link_xff") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff2', 'Action': 'filter', 'filter': 'ff2', 'by': "S != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[98]原语 ff2 = filter ff2 by S != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff2', 'Action': 'filter', 'filter': 'ff2', 'by': "O != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[99]原语 ff2 = filter ff2 by O != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff2', 'Action': 'loc', 'loc': 'ff2', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[100]原语 ff2 = loc ff2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type3', 'Action': 'loc', 'loc': 'ff2', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[102]原语 type3 = loc ff2 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type3', 'Action': 'add', 'add': 'type', 'by': "'代理'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[103]原语 type3 = add type by ("代理") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type4', 'Action': 'loc', 'loc': 'ff2', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[104]原语 type4 = loc ff2 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type4', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[105]原语 rename type4 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type4', 'Action': 'add', 'add': 'type', 'by': "'代理'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[106]原语 type4 = add type by ("代理") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'nn8', 'Action': 'loc', 'loc': 'link', 'by': 't5,agent_ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[109]原语 nn8 = loc link by t5,agent_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ff3', 'Action': 'distinct', 'distinct': 'nn8', 'by': 't5,agent_ip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[110]原语 ff3 = distinct nn8 by t5,agent_ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff3', 'Action': 'filter', 'filter': 'ff3', 'by': "t5 != '' and agent_ip != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[111]原语 ff3 = filter ff3 by t5 != "" and agent_ip != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ff3', 'as': "'t5':'S','agent_ip':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[112]原语 rename ff3 as ("t5":"S","agent_ip":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff3', 'Action': '@udf', '@udf': 'ff3', 'by': 'udf0.df_row_lambda', 'with': 'x: 0 if x[0] != x[1] else 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[113]原语 ff3 = @udf ff3 by udf0.df_row_lambda with (x: 0 if... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff3', 'Action': 'filter', 'filter': 'ff3', 'by': 'lambda1 == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[114]原语 ff3 = filter ff3 by lambda1 == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ff3', 'Action': 'add', 'add': 'P', 'by': '"xff_ip"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[115]原语 ff3 = add P by ("xff_ip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff3', 'Action': 'filter', 'filter': 'ff3', 'by': "S != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[116]原语 ff3 = filter ff3 by S != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff3', 'Action': 'filter', 'filter': 'ff3', 'by': "O != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[117]原语 ff3 = filter ff3 by O != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff3', 'Action': 'loc', 'loc': 'ff3', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[118]原语 ff3 = loc ff3 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type5', 'Action': 'loc', 'loc': 'ff3', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[120]原语 type5 = loc ff3 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type5', 'Action': 'add', 'add': 'type', 'by': "'代理'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[121]原语 type5 = add type by ("代理") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type6', 'Action': 'loc', 'loc': 'ff3', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[122]原语 type6 = loc ff3 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type6', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[123]原语 rename type6 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type6', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[124]原语 type6 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'tt', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct agent_ip,app,url from ip_datalink where gmt_create >= '$time1' and gmt_create < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[127]原语 tt = load db by mysql1 with select distinct agent_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct url,data_type,api_type from data_api_new where data_type in ('XML','JSON','数据文件')"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[128]原语 api = load db by mysql1 with select distinct url,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ff', 'Action': 'join', 'join': 'tt,api', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[130]原语 ff = join tt,api by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff', 'Action': '@udf', '@udf': 'ff', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[132]原语 ff = @udf ff by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff', 'Action': '@udf', '@udf': 'ff', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[133]原语 ff = @udf ff by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff4', 'Action': 'loc', 'loc': 'ff', 'by': 'agent_ip,app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[135]原语 ff4 = loc ff by agent_ip,app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ff4', 'as': "'agent_ip':'S','app':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[136]原语 rename ff4 as ("agent_ip":"S","app":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff4', 'Action': '@udf', '@udf': 'ff4', 'by': 'udf0.df_row_lambda', 'with': 'x: 0 if x[0] != x[1] else 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[137]原语 ff4 = @udf ff4 by udf0.df_row_lambda with (x: 0 if... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff4', 'Action': 'filter', 'filter': 'ff4', 'by': 'lambda1 == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[138]原语 ff4 = filter ff4 by lambda1 == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ff4', 'Action': 'add', 'add': 'P', 'by': '"link_x_http"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[139]原语 ff4 = add P by ("link_x_http") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff4', 'Action': 'loc', 'loc': 'ff4', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[140]原语 ff4 = loc ff4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ff4', 'Action': 'distinct', 'distinct': 'ff4', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[141]原语 ff4 = distinct ff4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff4', 'Action': 'filter', 'filter': 'ff4', 'by': "S != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[142]原语 ff4 = filter ff4 by S != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff4', 'Action': 'filter', 'filter': 'ff4', 'by': "O != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[143]原语 ff4 = filter ff4 by O != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type7', 'Action': 'loc', 'loc': 'ff4', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[145]原语 type7 = loc ff4 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type7', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[146]原语 type7 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type8', 'Action': 'loc', 'loc': 'ff4', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[147]原语 type8 = loc ff4 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type8', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[148]原语 rename type8 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type8', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[149]原语 type8 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[152]原语 api_type = load ssdb by ssdb0 with dd:API-api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ff.api_type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[153]原语 alter ff.api_type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff', 'Action': '@udf', '@udf': 'ff,api_type', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[154]原语 ff = @udf ff,api_type by SP.tag2dict with api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'ff', 'by': 'app'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[155]原语 app = loc ff by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app', 'Action': 'distinct', 'distinct': 'app', 'by': 'app'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[156]原语 app = distinct app by app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff5', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[157]原语 ff5 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'app', 'with': 'app = $1', 'run': '""\ntt = filter ff by app == \'@app\'\ntt = @udf tt by udf0.df_reset_index\ntt = add url_name by (df["app"]+"-"+df["api_type"]+"接口")\ntt = loc tt by url,app,url_name\nff5 = union ff5,tt\n""'}
	try:
		ptree['lineno']=158
		ptree['funs']=block_foreach_158
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[158]原语 foreach app run "tt = filter ff by app == "@app"tt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa1', 'Action': 'load', 'load': 'pq', 'by': 'link/xff_url_name.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[166]原语 aa1 = load pq by link/xff_url_name.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'ff5', 'by': 'url,url_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[167]原语 a1 = loc ff5 by url,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'a1', 'Action': 'union', 'union': 'a1,aa1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[168]原语 a1 = union a1,aa1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'a1', 'Action': 'distinct', 'distinct': 'a1', 'by': 'url,url_name'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[169]原语 a1 = distinct a1 by url,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a1', 'to': 'pq', 'by': 'link/xff_url_name.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[170]原语 store a1 to pq by link/xff_url_name.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'link_url', 'Action': 'loc', 'loc': 'a1', 'by': 'url,url_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[171]原语 link_url = loc a1 by url,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff5', 'Action': 'loc', 'loc': 'ff5', 'by': 'app,url_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[173]原语 ff5 = loc ff5 by app,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ff5', 'Action': 'distinct', 'distinct': 'ff5', 'by': 'app,url_name'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[174]原语 ff5 = distinct ff5 by app,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ff5', 'as': "'app':'S','url_name':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[175]原语 rename ff5 as ("app":"S","url_name":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ff5', 'Action': 'add', 'add': 'P', 'by': '"app_url"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[176]原语 ff5 = add P by ("app_url") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff5', 'Action': 'loc', 'loc': 'ff5', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[177]原语 ff5 = loc ff5 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff5', 'Action': 'filter', 'filter': 'ff5', 'by': "S != '127.0.0.1'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[178]原语 ff5 = filter ff5 by S != "127.0.0.1" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type9', 'Action': 'loc', 'loc': 'ff5', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[180]原语 type9 = loc ff5 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type9', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[181]原语 type9 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type10', 'Action': 'loc', 'loc': 'ff5', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[182]原语 type10 = loc ff5 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type10', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[183]原语 rename type10 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type10', 'Action': 'add', 'add': 'type', 'by': "'接口'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[184]原语 type10 = add type by ("接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ff', 'Action': 'union', 'union': 'ff1,ff2,ff3,ff4,ff5'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[205]原语 ff = union ff1,ff2,ff3,ff4,ff5 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ff', 'Action': 'distinct', 'distinct': 'ff', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[206]原语 ff = distinct ff by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ff.P', 'Action': 'lambda', 'lambda': 'P', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[207]原语 ff.P = lambda P by (x:x+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ff', 'Action': 'group', 'group': 'ff', 'by': 'S,O', 'agg': 'P:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[208]原语 ff = group ff by S,O agg P:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff', 'Action': '@udf', '@udf': 'ff', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[209]原语 ff = @udf ff by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ff.P', 'Action': 'lambda', 'lambda': 'P_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[210]原语 ff.P = lambda P_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'ff.P', 'Action': 'str', 'str': 'P', 'by': "replace('link_xff,xff_ip','xff_ip')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[212]原语 ff.P = str P by (replace("link_xff,xff_ip","xff_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'ff.P', 'Action': 'str', 'str': 'P', 'by': "replace('xff_ip,link_xff','xff_ip')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[213]原语 ff.P = str P by (replace("xff_ip,link_xff","xff_ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff', 'Action': 'loc', 'loc': 'ff', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[214]原语 ff = loc ff by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct S,O,P from link_xff'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[215]原语 data = load ckh by ckh with select distinct S,O,P ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'data', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[216]原语 data = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ff', 'Action': 'join', 'join': 'ff,data', 'by': '[S,O,P],[S,O,P]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[217]原语 ff = join ff,data by [S,O,P],[S,O,P] with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff', 'Action': '@udf', '@udf': 'ff', 'by': 'udf0.df_fillna', 'with': '0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[218]原语 ff = @udf ff by udf0.df_fillna with 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ff.aa', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[219]原语 alter ff.aa as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ff', 'Action': 'filter', 'filter': 'ff', 'by': 'aa == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[220]原语 ff = filter ff by aa == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ff', 'Action': 'distinct', 'distinct': 'ff', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[221]原语 ff = distinct ff by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ff', 'Action': '@udf', '@udf': 'ff', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[222]原语 ff = @udf ff by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ff', 'Action': 'loc', 'loc': 'ff', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[223]原语 ff = loc ff by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'new_count', 'Action': 'eval', 'eval': 'ff', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[227]原语 new_count = eval ff by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'add_count', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': 'int($new_count/5000) + 2'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[228]原语 add_count = @sdf sys_eval with (int($new_count/500... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new_pd', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[230]原语 new_pd = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'new_pd', 'Action': 'add', 'add': 'num', 'by': 'range(1,$add_count)'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[231]原语 new_pd = add num by (range(1,$add_count)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'new_pd', 'with': 'num = $1', 'run': '""\nadd1 = filter ff by index >= 5000 * (@num -1) and index < 5000 * @num\nret = @udf add1 by GL.add_http_mkd\nret_pd = @sdf sys_lambda with ($ret,x: \'Successfully\' in x )\n#if $ret_pd == True with store add1 to ckh by ckh with link_xff\n""'}
	try:
		ptree['lineno']=233
		ptree['funs']=block_foreach_233
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[233]原语 foreach new_pd run "add1 = filter ff by index >= 5... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data', 'Action': 'loc', 'loc': 'ff', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[240]原语 data = loc ff by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data', 'to': 'ckh', 'by': 'ckh', 'with': 'link_xff'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[241]原语 store data to ckh by ckh with link_xff 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type_1', 'Action': 'union', 'union': 'type1,type2,type3,type4,type5,type6,type7,type8,type9,type10,type_xff'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[245]原语 type_1 = union type1,type2,type3,type4,type5,type6... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type_1', 'as': "'S':'id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[246]原语 rename type_1 as ("S":"id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'load', 'load': 'pq', 'by': 'link/ip_type.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[247]原语 type = load pq by link/ip_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type', 'Action': 'union', 'union': 'type_1,type'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[248]原语 type = union type_1,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'type', 'Action': 'distinct', 'distinct': 'type', 'by': 'id,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[249]原语 type = distinct type by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'type', 'by': 'id,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[251]原语 tt = loc type by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'tt', 'Action': 'distinct', 'distinct': 'tt', 'by': 'id,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[252]原语 tt = distinct tt by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'tt.type', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[253]原语 alter tt.type as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'tt.type', 'Action': 'lambda', 'lambda': 'type', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[254]原语 tt.type = lambda type by (x:x+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'tt', 'Action': 'group', 'group': 'tt', 'by': 'id', 'agg': 'type:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[255]原语 tt = group tt by id agg type:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tt', 'Action': '@udf', '@udf': 'tt', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[256]原语 tt = @udf tt by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'tt.type', 'Action': 'lambda', 'lambda': 'type_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[257]原语 tt.type = lambda type_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'tt.type', 'Action': 'str', 'str': 'type', 'by': "replace('XFF,代理','代理')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[258]原语 tt.type = str type by (replace("XFF,代理","代理")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'tt.type', 'Action': 'str', 'str': 'type', 'by': "replace('代理,XFF','代理')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[259]原语 tt.type = str type by (replace("代理,XFF","代理")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'tt.type', 'Action': 'str', 'str': 'type', 'by': "replace('终端,代理','终端')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[260]原语 tt.type = str type by (replace("终端,代理","终端")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'tt.type', 'Action': 'str', 'str': 'type', 'by': "replace('代理,终端','终端')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[261]原语 tt.type = str type by (replace("代理,终端","终端")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': 'id,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[262]原语 tt = loc tt by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select distinct app from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[266]原语 app = load db by mysql1 with select distinct app f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt1', 'Action': 'filter', 'filter': 'tt', 'by': "type == '终端,应用' or type == '应用,终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[267]原语 tt1 = filter tt by type == "终端,应用" or type == "应用,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'tt1', 'Action': 'join', 'join': 'tt1,app', 'by': 'id,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[268]原语 tt1 = join tt1,app by id,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tt1', 'Action': '@udf', '@udf': 'tt1', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[269]原语 tt1 = @udf tt1 by udf0.df_fillna with "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt2', 'Action': 'filter', 'filter': 'tt1', 'by': "app == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[270]原语 tt2 = filter tt1 by app == "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt2', 'Action': 'loc', 'loc': 'tt2', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[271]原语 tt2 = loc tt2 by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tt2', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[272]原语 tt2 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt1', 'Action': 'filter', 'filter': 'tt1', 'by': "app != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[273]原语 tt1 = filter tt1 by app != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt1', 'Action': 'loc', 'loc': 'tt1', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[274]原语 tt1 = loc tt1 by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tt1', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[275]原语 tt1 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt3', 'Action': 'filter', 'filter': 'tt', 'by': "type != '终端,应用' and type != '应用,终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[276]原语 tt3 = filter tt by type != "终端,应用" and type != "应用... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tt', 'Action': 'union', 'union': 'tt1,tt2,tt3'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[277]原语 tt = union tt1,tt2,tt3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node', 'Action': 'loc', 'loc': 'tt', 'by': 'id,type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[279]原语 node = loc tt by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'node', 'Action': 'distinct', 'distinct': 'node', 'by': 'id,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[280]原语 node = distinct node by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'pq', 'by': 'link/ip_type.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[281]原语 store node to pq by link/ip_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[link_XFF.fbi]执行第[286]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],286

#主函数结束,开始块函数

def block_foreach_158(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt', 'Action': 'filter', 'filter': 'ff', 'by': "app == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第158行foreach语句中]执行第[159]原语 tt = filter ff by app == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tt', 'Action': '@udf', '@udf': 'tt', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第158行foreach语句中]执行第[160]原语 tt = @udf tt by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tt', 'Action': 'add', 'add': 'url_name', 'by': 'df["app"]+"-"+df["api_type"]+"接口"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第158行foreach语句中]执行第[161]原语 tt = add url_name by (df["app"]+"-"+df["api_type"]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': 'url,app,url_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第158行foreach语句中]执行第[162]原语 tt = loc tt by url,app,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ff5', 'Action': 'union', 'union': 'ff5,tt'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第158行foreach语句中]执行第[163]原语 ff5 = union ff5,tt 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_158

def block_foreach_233(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'add1', 'Action': 'filter', 'filter': 'ff', 'by': 'index >= 5000 * (@num -1) and index < 5000 * @num'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第233行foreach语句中]执行第[234]原语 add1 = filter ff by index >= 5000 * (@num -1) and ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'add1', 'by': 'GL.add_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第233行foreach语句中]执行第[235]原语 ret = @udf add1 by GL.add_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'ret_pd', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': "$ret,x: 'Successfully' in x "}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第233行foreach语句中]执行第[236]原语 ret_pd = @sdf sys_lambda with ($ret,x: "Successful... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_233

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



