#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: link_tupu
#datetime: 2024-08-30T16:10:55.998442
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
		add_the_error('[link_tupu.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'link_agent'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[18]原语 aa = load ssdb by ssdb0 with link_agent 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[20]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(time) as time from api_monitor'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=21
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[21]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[23]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(time) as time from api_monitor'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[25]原语 aa = load ckh by ckh with select max(time) as time... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[26]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app from api_monitor where time >= '$time1' and time < '$time2' limit 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[29]原语 ccc = load ckh by ckh with select app from api_mon... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接 或 无数据更新！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[link_tupu.fbi]执行第[30]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[30]原语 assert find_df_have_data("ccc",ptree) as exit with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_agent'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[32]原语 store aa to ssdb by ssdb0 with link_agent 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss6', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct src_ip,dest_ip,dest_port as O from dbms where timestamp >= '$time1' and timestamp < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[38]原语 ss6 = load ckh by ckh with select distinct src_ip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss6', 'by': 'src_ip:str,dest_ip:str,O:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[39]原语 alter ss6 by src_ip:str,dest_ip:str,O:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss6', 'Action': 'loc', 'loc': 'ss6', 'by': 'src_ip,dest_ip,O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[40]原语 ss6 = loc ss6 by src_ip,dest_ip,O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss6', 'Action': '@udf', '@udf': 'ss6', 'by': 'udf0.df_row_lambda', 'with': "x: x[0] if x[0] != '127.0.0.1' else x[1]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[41]原语 ss6 = @udf ss6 by udf0.df_row_lambda with (x: x[0]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss6', 'as': "'lambda1':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[42]原语 rename ss6 as ("lambda1":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss6', 'Action': 'add', 'add': 'O', 'by': "df['dest_ip']+':'+df['O']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[43]原语 ss6 = add O by (df["dest_ip"]+":"+df["O"]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss6', 'Action': 'add', 'add': 'P', 'by': "'link_sql'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[44]原语 ss6 = add P by ("link_sql") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss6.len1', 'Action': 'lambda', 'lambda': 'O', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[46]原语 ss6.len1 = lambda O by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss6', 'Action': 'filter', 'filter': 'ss6', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[47]原语 ss6 = filter ss6 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss6.len1', 'Action': 'lambda', 'lambda': 'S', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[48]原语 ss6.len1 = lambda S by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss6', 'Action': 'filter', 'filter': 'ss6', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[49]原语 ss6 = filter ss6 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss6', 'Action': 'loc', 'loc': 'ss6', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[51]原语 ss6 = loc ss6 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type7', 'Action': 'loc', 'loc': 'ss6', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[53]原语 type7 = loc ss6 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type7', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[54]原语 type7 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type8', 'Action': 'loc', 'loc': 'ss6', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[55]原语 type8 = loc ss6 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type8', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[56]原语 rename type8 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type8', 'Action': 'add', 'add': 'type', 'by': "'数据库'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[57]原语 type8 = add type by ("数据库") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss1', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct account as S,srcip,real_ip from api_monitor where account != '' and time >= '$time1' and time < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[61]原语 ss1 = load ckh by ckh with select distinct account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss1', 'by': 'S:str,srcip:str,real_ip:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[62]原语 alter ss1 by S:str,srcip:str,real_ip:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss1', 'Action': '@udf', '@udf': 'ss1', 'by': 'udf0.df_row_lambda', 'with': "x: x[1] if x[1] != '127.0.0.1' else x[2]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[63]原语 ss1 = @udf ss1 by udf0.df_row_lambda with (x: x[1]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss1', 'as': "'lambda1':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[64]原语 rename ss1 as ("lambda1":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss1', 'Action': 'filter', 'filter': 'ss1', 'by': "O != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[65]原语 ss1 = filter ss1 by O != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss1', 'Action': 'add', 'add': 'P', 'by': "'link_belong'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[66]原语 ss1 = add P by ("link_belong") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss1.len1', 'Action': 'lambda', 'lambda': 'S', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[68]原语 ss1.len1 = lambda S by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss1', 'Action': 'filter', 'filter': 'ss1', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[69]原语 ss1 = filter ss1 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss1.len1', 'Action': 'lambda', 'lambda': 'O', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[70]原语 ss1.len1 = lambda O by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss1', 'Action': 'filter', 'filter': 'ss1', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[71]原语 ss1 = filter ss1 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss1', 'Action': 'loc', 'loc': 'ss1', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[73]原语 ss1 = loc ss1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ss1', 'Action': 'distinct', 'distinct': 'ss1', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[74]原语 ss1 = distinct ss1 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type1', 'Action': 'loc', 'loc': 'ss1', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[76]原语 type1 = loc ss1 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type1', 'Action': 'add', 'add': 'type', 'by': "'应用账号'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[77]原语 type1 = add type by ("应用账号") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type2', 'Action': 'loc', 'loc': 'ss1', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[78]原语 type2 = loc ss1 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type2', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[79]原语 rename type2 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type2', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[80]原语 type2 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss2', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct srcip,real_ip,app from api_monitor where content_type not in ('XML','JSON','数据文件') and time >= '$time1' and time < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[83]原语 ss2 = load ckh by ckh with select distinct srcip,r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss2', 'by': 'srcip:str,real_ip:str,app:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[84]原语 alter ss2 by srcip:str,real_ip:str,app:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss2', 'Action': '@udf', '@udf': 'ss2', 'by': 'udf0.df_row_lambda', 'with': "x: x[0] if x[0] != '127.0.0.1' else x[1]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[85]原语 ss2 = @udf ss2 by udf0.df_row_lambda with (x: x[0]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss2', 'as': "'lambda1':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[86]原语 rename ss2 as ("lambda1":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss2', 'Action': 'filter', 'filter': 'ss2', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[87]原语 ss2 = filter ss2 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss2.app1', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[88]原语 ss2.app1 = lambda app by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss2', 'Action': '@udf', '@udf': 'ss2', 'by': 'udf0.df_l2cs', 'with': 'app1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[89]原语 ss2 = @udf ss2 by udf0.df_l2cs with app1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss2', 'Action': '@udf', '@udf': 'ss2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[90]原语 ss2 = @udf ss2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss2', 'as': "'n100':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[91]原语 rename ss2 as ("n100":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss2', 'Action': 'loc', 'loc': 'ss2', 'by': 'S,O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[92]原语 ss2 = loc ss2 by S,O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss2', 'Action': 'add', 'add': 'aa', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[94]原语 ss2 = add aa by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss2', 'Action': '@udf', '@udf': 'ss2', 'by': 'udf0.df_row_lambda', 'with': 'x: x[2] if x[0] != x[1] else 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[95]原语 ss2 = @udf ss2 by udf0.df_row_lambda with (x: x[2]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss2', 'Action': 'filter', 'filter': 'ss2', 'by': 'lambda1 != 1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[96]原语 ss2 = filter ss2 by lambda1 != 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss2', 'Action': 'add', 'add': 'P', 'by': "'link_http1'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[97]原语 ss2 = add P by ("link_http1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss2.len1', 'Action': 'lambda', 'lambda': 'S', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[99]原语 ss2.len1 = lambda S by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss2', 'Action': 'filter', 'filter': 'ss2', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[100]原语 ss2 = filter ss2 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss2.len1', 'Action': 'lambda', 'lambda': 'O', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[101]原语 ss2.len1 = lambda O by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss2', 'Action': 'filter', 'filter': 'ss2', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[102]原语 ss2 = filter ss2 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss2', 'Action': 'loc', 'loc': 'ss2', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[104]原语 ss2 = loc ss2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ss2', 'Action': 'distinct', 'distinct': 'ss2', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[105]原语 ss2 = distinct ss2 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type5', 'Action': 'loc', 'loc': 'ss2', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[107]原语 type5 = loc ss2 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type5', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[108]原语 type5 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type6', 'Action': 'loc', 'loc': 'ss2', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[109]原语 type6 = loc ss2 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type6', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[110]原语 rename type6 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type6', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[111]原语 type6 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss3', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct urld as url,app,api_type,http_method,risk_level from api_monitor where content_type in ('XML','JSON','数据文件') and time >= '$time1' and time < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[114]原语 ss3 = load ckh by ckh with select distinct urld as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss3', 'by': 'url:str,app:str,api_type:str,http_method:str,risk_level:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[115]原语 alter ss3 by url:str,app:str,api_type:str,http_met... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss3', 'Action': 'loc', 'loc': 'ss3', 'by': 'http_method,url,app,api_type,risk_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[117]原语 ss3 = loc ss3 by http_method,url,app,api_type,risk... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss3', 'Action': '@udf', '@udf': 'ss3', 'by': 'udf0.df_row_lambda', 'with': "x: '' if x[0] != 'OPTIONS' and x[0] != 'POST' and x[0] != 'GET' and x[0] != 'PUT' and x[0] != 'PATCH' and x[0] != 'DELETE' and x[0] != 'HEAD' and x[0] != 'CONNECT' else x[0] "}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[118]原语 ss3 = @udf ss3 by udf0.df_row_lambda with (x: "" i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss3', 'Action': 'loc', 'loc': 'ss3', 'drop': 'http_method'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[119]原语 ss3 = loc ss3 drop http_method 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss3_1', 'Action': 'filter', 'filter': 'ss3', 'by': "lambda1 == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[120]原语 ss3_1 = filter ss3 by lambda1 == "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss3_1', 'as': "'lambda1':'http_method'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[121]原语 rename ss3_1 as ("lambda1":"http_method") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss3_2', 'Action': 'filter', 'filter': 'ss3', 'by': "lambda1 != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[122]原语 ss3_2 = filter ss3 by lambda1 != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss3_2.lambda1', 'Action': 'lambda', 'lambda': 'lambda1', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[123]原语 ss3_2.lambda1 = lambda lambda1 by (x:x+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ss3_2', 'Action': 'group', 'group': 'ss3_2', 'by': 'url,app,api_type,risk_level', 'agg': 'lambda1:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[124]原语 ss3_2 = group ss3_2 by url,app,api_type,risk_level... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss3_2.http_method', 'Action': 'lambda', 'lambda': 'lambda1_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[125]原语 ss3_2.http_method = lambda lambda1_sum by (x:x[:-1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss3_2', 'Action': '@udf', '@udf': 'ss3_2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[126]原语 ss3_2 = @udf ss3_2 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss3_2', 'Action': 'loc', 'loc': 'ss3_2', 'drop': 'lambda1_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[127]原语 ss3_2 = loc ss3_2 drop lambda1_sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ss3', 'Action': 'union', 'union': 'ss3_1,ss3_2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[128]原语 ss3 = union ss3_1,ss3_2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'url', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select distinct url from data_api_new where data_type in ('XML','JSON','数据文件')"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[131]原语 url = load db by mysql1 with select distinct url f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'url', 'by': 'url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[132]原语 alter url by url:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ss3', 'Action': 'join', 'join': 'ss3,url', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[133]原语 ss3 = join ss3,url by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss3.app1', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[134]原语 ss3.app1 = lambda app by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss3', 'Action': '@udf', '@udf': 'ss3', 'by': 'udf0.df_l2cs', 'with': 'app1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[135]原语 ss3 = @udf ss3 by udf0.df_l2cs with app1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss3', 'Action': '@udf', '@udf': 'ss3', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[136]原语 ss3 = @udf ss3 by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss3', 'as': "'n100':'app2'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[137]原语 rename ss3 as ("n100":"app2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss3', 'Action': 'loc', 'loc': 'ss3', 'by': 'url,app,app2,api_type,http_method,risk_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[138]原语 ss3 = loc ss3 by url,app,app2,api_type,http_method... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_type', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'dd:API-api_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[139]原语 api_type = load ssdb by ssdb0 with dd:API-api_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss3', 'Action': '@udf', '@udf': 'ss3,api_type', 'by': 'SP.tag2dict', 'with': 'api_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[140]原语 ss3 = @udf ss3,api_type by SP.tag2dict with api_ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss3.app2', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[141]原语 alter ss3.app2 as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'ss3', 'by': 'app2'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[142]原语 app = loc ss3 by app2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app', 'Action': 'distinct', 'distinct': 'app', 'by': 'app2'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[143]原语 app = distinct app by app2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss4', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[144]原语 ss4 = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'app', 'with': 'app = $1', 'run': '""\ntt = filter ss3 by app2 == \'@app\'\ntt = @udf tt by udf0.df_reset_index\ntt = add url_name by (df["app2"]+"-"+df["api_type"]+"接口")\n#tt = add app2 by ("应用-"+df["app2"])\ntt = loc tt by url,app2,url_name,http_method,risk_level\nss4 = union ss4,tt\n""'}
	try:
		ptree['lineno']=145
		ptree['funs']=block_foreach_145
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[145]原语 foreach app run "tt = filter ss3 by app2 == "@app"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa1', 'Action': 'load', 'load': 'pq', 'by': 'link/url_name.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[154]原语 aa1 = load pq by link/url_name.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'ss4', 'by': 'url,url_name,http_method,risk_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[155]原语 a1 = loc ss4 by url,url_name,http_method,risk_leve... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'a1', 'Action': 'union', 'union': 'a1,aa1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[156]原语 a1 = union a1,aa1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'a1', 'Action': 'distinct', 'distinct': 'a1', 'by': 'url,url_name,http_method,risk_level'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[157]原语 a1 = distinct a1 by url,url_name,http_method,risk_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a1', 'to': 'pq', 'by': 'link/url_name.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[158]原语 store a1 to pq by link/url_name.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a1', 'Action': 'loc', 'loc': 'a1', 'by': 'url,url_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[159]原语 a1 = loc a1 by url,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss4', 'Action': 'loc', 'loc': 'ss4', 'by': 'app2,url_name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[161]原语 ss4 = loc ss4 by app2,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ss4', 'Action': 'distinct', 'distinct': 'ss4', 'by': 'app2,url_name'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[162]原语 ss4 = distinct ss4 by app2,url_name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss4', 'as': "'app2':'O','url_name':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[163]原语 rename ss4 as ("app2":"O","url_name":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss4', 'Action': 'add', 'add': 'P', 'by': "'link_belong1'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[164]原语 ss4 = add P by ("link_belong1") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss4.len1', 'Action': 'lambda', 'lambda': 'S', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[166]原语 ss4.len1 = lambda S by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss4', 'Action': 'filter', 'filter': 'ss4', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[167]原语 ss4 = filter ss4 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss4.len1', 'Action': 'lambda', 'lambda': 'O', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[168]原语 ss4.len1 = lambda O by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss4', 'Action': 'filter', 'filter': 'ss4', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[169]原语 ss4 = filter ss4 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss4', 'Action': 'loc', 'loc': 'ss4', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[171]原语 ss4 = loc ss4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ss4', 'Action': 'distinct', 'distinct': 'ss4', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[172]原语 ss4 = distinct ss4 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type3', 'Action': 'loc', 'loc': 'ss4', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[174]原语 type3 = loc ss4 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type3', 'Action': 'add', 'add': 'type', 'by': "'接口'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[175]原语 type3 = add type by ("接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type4', 'Action': 'loc', 'loc': 'ss4', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[176]原语 type4 = loc ss4 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type4', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[177]原语 rename type4 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type4', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[178]原语 type4 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss5', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct srcip,real_ip,urld as url from api_monitor where content_type in ('XML','JSON','数据文件') and time >= '$time1' and time < '$time2'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[182]原语 ss5 = load ckh by ckh with select distinct srcip,r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss5', 'by': 'srcip:str,real_ip:str,url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[183]原语 alter ss5 by srcip:str,real_ip:str,url:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ss5', 'Action': 'join', 'join': 'ss5,url', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[185]原语 ss5 = join ss5,url by url,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss5', 'Action': '@udf', '@udf': 'ss5', 'by': 'udf0.df_row_lambda', 'with': "x: x[0] if x[0] != '127.0.0.1' else x[1]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[186]原语 ss5 = @udf ss5 by udf0.df_row_lambda with (x: x[0]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss5', 'as': "'lambda1':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[187]原语 rename ss5 as ("lambda1":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss5', 'Action': 'filter', 'filter': 'ss5', 'by': "S != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[188]原语 ss5 = filter ss5 by S != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss5', 'Action': 'loc', 'loc': 'ss5', 'by': 'S,url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[189]原语 ss5 = loc ss5 by S,url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ss5', 'Action': 'join', 'join': 'ss5,a1', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[190]原语 ss5 = join ss5,a1 by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ss5', 'as': "'url_name':'O'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[191]原语 rename ss5 as ("url_name":"O") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ss5', 'Action': 'add', 'add': 'P', 'by': "'link_http'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[192]原语 ss5 = add P by ("link_http") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss5.len1', 'Action': 'lambda', 'lambda': 'S', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[194]原语 ss5.len1 = lambda S by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss5', 'Action': 'filter', 'filter': 'ss5', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[195]原语 ss5 = filter ss5 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ss5.len1', 'Action': 'lambda', 'lambda': 'O', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[196]原语 ss5.len1 = lambda O by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss5', 'Action': 'filter', 'filter': 'ss5', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[197]原语 ss5 = filter ss5 by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss5', 'Action': 'loc', 'loc': 'ss5', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[199]原语 ss5 = loc ss5 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ss5', 'Action': 'distinct', 'distinct': 'ss5', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[200]原语 ss5 = distinct ss5 by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type11', 'Action': 'loc', 'loc': 'ss5', 'by': 'S'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[202]原语 type11 = loc ss5 by S 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type11', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[203]原语 type11 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'type12', 'Action': 'loc', 'loc': 'ss5', 'by': 'O'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[204]原语 type12 = loc ss5 by O 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type12', 'as': "'O':'S'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[205]原语 rename type12 as ("O":"S") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'type12', 'Action': 'add', 'add': 'type', 'by': "'接口'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[206]原语 type12 = add type by ("接口") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ss', 'Action': 'union', 'union': 'ss1,ss2,ss4,ss5,ss6'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[211]原语 ss = union ss1,ss2,ss4,ss5,ss6 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct S,O,P from link_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[212]原语 data = load ckh by ckh with select distinct S,O,P ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'data', 'by': 'S:str,O:str,P:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[213]原语 alter data by S:str,O:str,P:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'data', 'Action': 'add', 'add': 'aa', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[214]原语 data = add aa by 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ss', 'Action': 'join', 'join': 'ss,data', 'by': '[S,O,P],[S,O,P]', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[215]原语 ss = join ss,data by [S,O,P],[S,O,P] with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_fillna_cols', 'with': 'aa:0'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[216]原语 ss = @udf ss by udf0.df_fillna_cols with aa:0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss', 'by': 'aa:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[217]原语 alter ss by aa:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ss', 'Action': 'filter', 'filter': 'ss', 'by': 'aa == 0'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[218]原语 ss = filter ss by aa == 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ss', 'Action': 'distinct', 'distinct': 'ss', 'by': 'S,O,P'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[219]原语 ss = distinct ss by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[220]原语 ss = @udf ss by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ss', 'Action': 'loc', 'loc': 'ss', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[221]原语 ss = loc ss by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'new_count', 'Action': 'eval', 'eval': 'ss', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[225]原语 new_count = eval ss by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[link_tupu.fbi]执行第[226]原语 add_count = @sdf sys_eval with (int($new_count/500... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'new_pd', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[228]原语 new_pd = @udf udf0.new_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'new_pd', 'Action': 'add', 'add': 'num', 'by': 'range(1,$add_count)'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[229]原语 new_pd = add num by (range(1,$add_count)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'new_pd', 'with': 'num = $1', 'run': '""\nadd1 = filter ss by index >= 5000 * (@num - 1) and index < 5000 * @num\nret = @udf add1 by GL.add_http_mkd\nret_pd = @sdf sys_lambda with ($ret,x: \'Successfully\' in x )\n#if $ret_pd == True with store add1 to ckh by ckh with link_data\n""'}
	try:
		ptree['lineno']=230
		ptree['funs']=block_foreach_230
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[230]原语 foreach new_pd run "add1 = filter ss by index >= 5... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'data', 'Action': 'loc', 'loc': 'ss', 'by': 'S,O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[238]原语 data = loc ss by S,O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data', 'to': 'ckh', 'by': 'ckh', 'with': 'link_data'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[239]原语 store data to ckh by ckh with link_data 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type_1', 'Action': 'union', 'union': 'type1,type2,type3,type4,type5,type6,type7,type8,type11,type12'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[243]原语 type_1 = union type1,type2,type3,type4,type5,type6... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'type_1', 'as': "'S':'id'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[244]原语 rename type_1 as ("S":"id") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'type', 'Action': 'load', 'load': 'pq', 'by': 'link/link_type.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[245]原语 type = load pq by link/link_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'type', 'Action': 'union', 'union': 'type_1,type'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[246]原语 type = union type_1,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select app from data_app_new'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[248]原语 app = load db by mysql1 with select app from data_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app', 'by': 'app:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[249]原语 alter app by app:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'app.app1', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[250]原语 app.app1 = lambda app by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_l2cs', 'with': 'app1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[251]原语 app = @udf app by udf0.df_l2cs with app1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app', 'as': "'n100':'app2'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[252]原语 rename app as ("n100":"app2") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'app2'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[253]原语 app = loc app by app2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app', 'Action': 'distinct', 'distinct': 'app', 'by': 'app2'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[254]原语 app = distinct app by app2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node1', 'Action': 'filter', 'filter': 'type', 'by': "type == '应用' or type == '业务终端' or type == '管理终端' or type == '数据终端' or type == '终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[255]原语 node1 = filter type by type == "应用" or type == "业务... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node1', 'Action': 'join', 'join': 'node1,app', 'by': 'id,app2', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[257]原语 node1 = join node1,app by id,app2 with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'node1', 'Action': '@udf', '@udf': 'node1', 'by': 'udf0.df_fillna_cols', 'with': "app2:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[258]原语 node1 = @udf node1 by udf0.df_fillna_cols with app... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node2', 'Action': 'filter', 'filter': 'node1', 'by': "app2 != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[260]原语 node2 = filter node1 by app2 != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node2', 'Action': 'loc', 'loc': 'node2', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[261]原语 node2 = loc node2 by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node2', 'Action': 'add', 'add': 'type', 'by': "'应用'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[262]原语 node2 = add type by ("应用") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node1', 'Action': 'filter', 'filter': 'node1', 'by': "app2 == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[264]原语 node1 = filter node1 by app2 == "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node1', 'Action': 'loc', 'loc': 'node1', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[265]原语 node1 = loc node1 by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node1', 'Action': 'add', 'add': 'type', 'by': "'终端'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[266]原语 node1 = add type by ("终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select distinct S,O,P from link_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[268]原语 ss = load ckh by ckh with select distinct S,O,P fr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ss', 'by': 'S:str,O:str,P:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[269]原语 alter ss by S:str,O:str,P:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt1', 'Action': 'loc', 'loc': 'ss', 'by': 'S,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[270]原语 tt1 = loc ss by S,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tt1', 'as': "'S':'jd','P':'pp'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[271]原语 rename tt1 as ("S":"jd","P":"pp") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt2', 'Action': 'loc', 'loc': 'ss', 'by': 'O,P'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[272]原语 tt2 = loc ss by O,P 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'tt2', 'as': "'O':'jd','P':'pp'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[273]原语 rename tt2 as ("O":"jd","P":"pp") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'tt', 'Action': 'union', 'union': 'tt1,tt2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[274]原语 tt = union tt1,tt2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'node4', 'Action': 'join', 'join': 'tt,node1', 'by': 'jd,id', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[275]原语 node4 = join tt,node1 by jd,id with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'node4', 'Action': '@udf', '@udf': 'node4', 'by': 'udf0.df_fillna_cols', 'with': "id:'',type:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[276]原语 node4 = @udf node4 by udf0.df_fillna_cols with id:... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'node4.pp', 'Action': 'str', 'str': 'pp', 'by': "replace('1','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[277]原语 node4.pp = str pp by replace("1","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node4', 'Action': 'filter', 'filter': 'node4', 'by': "id != '' and pp != 'link_belong'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[278]原语 node4 = filter node4 by id != "" and pp != "link_b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'node4', 'Action': 'distinct', 'distinct': 'node4', 'by': 'jd,pp'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[279]原语 node4 = distinct node4 by jd,pp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'node4', 'Action': 'order', 'order': 'node4', 'by': 'pp', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[280]原语 node4 = order node4 by pp with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node4.pp', 'Action': 'lambda', 'lambda': 'pp', 'by': "x:x+','"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[281]原语 node4.pp = lambda pp by (x:x+",") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'node4', 'Action': 'group', 'group': 'node4', 'by': 'id', 'agg': 'pp:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[282]原语 node4 = group node4 by id agg pp:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node4', 'Action': 'loc', 'loc': 'node4', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[283]原语 node4 = loc node4 by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'node4.pp', 'Action': 'lambda', 'lambda': 'pp_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[284]原语 node4.pp = lambda pp_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_sj', 'Action': 'filter', 'filter': 'node4', 'by': "pp == 'link_sql'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[286]原语 node_sj = filter node4 by pp == "link_sql" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node_sj', 'Action': 'loc', 'loc': 'node_sj', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[287]原语 node_sj = loc node_sj by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_sj', 'Action': 'add', 'add': 'type', 'by': '"数据终端"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[288]原语 node_sj = add type by ("数据终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_yw', 'Action': 'filter', 'filter': 'node4', 'by': "pp == 'link_http'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[290]原语 node_yw = filter node4 by pp == "link_http" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node_yw', 'Action': 'loc', 'loc': 'node_yw', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[291]原语 node_yw = loc node_yw by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_yw', 'Action': 'add', 'add': 'type', 'by': '"业务终端"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[292]原语 node_yw = add type by ("业务终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node_gl', 'Action': 'filter', 'filter': 'node4', 'by': "pp != 'link_http' and pp != 'link_sql'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[294]原语 node_gl = filter node4 by pp != "link_http" and pp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'node_gl', 'Action': 'loc', 'loc': 'node_gl', 'by': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[295]原语 node_gl = loc node_gl by id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'node_gl', 'Action': 'add', 'add': 'type', 'by': '"管理终端"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[296]原语 node_gl = add type by ("管理终端") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'node3', 'Action': 'filter', 'filter': 'type', 'by': "type != '应用' and type != '终端' and type != '业务终端' and type != '管理终端' and type != '数据终端'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[299]原语 node3 = filter type by type != "应用" and type != "终... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'node', 'Action': 'union', 'union': 'node2,node3,node_sj,node_yw,node_gl'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[300]原语 node = union node2,node3,node_sj,node_yw,node_gl 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'node', 'Action': 'distinct', 'distinct': 'node', 'by': 'id,type'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[301]原语 node = distinct node by id,type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'node', 'to': 'pq', 'by': 'link/link_type.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[302]原语 store node to pq by link/link_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct account,srcip,real_ip,dstip,urld as url from api_monitor where account != '' and content_type in ('XML','JSON','数据文件')"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[306]原语 ddd = load ckh by ckh with select distinct account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ddd', 'by': 'account:str,srcip:str,real_ip:str,dstip:str,url:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[307]原语 alter ddd by account:str,srcip:str,real_ip:str,dst... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_row_lambda', 'with': "x: x[1] if x[1] != '127.0.0.1' else x[2]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[308]原语 ddd = @udf ddd by udf0.df_row_lambda with (x: x[1]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ddd', 'as': "'lambda1':'zd'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[309]原语 rename ddd as ("lambda1":"zd") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': "zd != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[310]原语 ddd = filter ddd by zd != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'ddd', 'Action': 'join', 'join': 'ddd,a1', 'by': 'url,url', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[311]原语 ddd = join ddd,a1 by url,url with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_fillna_cols', 'with': "url_name:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[312]原语 ddd = @udf ddd by udf0.df_fillna_cols with url_nam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': "url_name != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[313]原语 ddd = filter ddd by url_name != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.len1', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[315]原语 ddd.len1 = lambda account by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[316]原语 ddd = filter ddd by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.len1', 'Action': 'lambda', 'lambda': 'zd', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[317]原语 ddd.len1 = lambda zd by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[318]原语 ddd = filter ddd by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'zd,url_name,account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[321]原语 ddd = loc ddd by zd,url_name,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ddd', 'Action': 'distinct', 'distinct': 'ddd', 'by': 'zd,url_name,account'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[322]原语 ddd = distinct ddd by zd,url_name,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.account', 'Action': 'lambda', 'lambda': 'account', 'by': "x:x+';'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[323]原语 ddd.account = lambda account by (x:x+";") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ddd', 'Action': 'group', 'group': 'ddd', 'by': 'zd,url_name', 'agg': 'account:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[324]原语 ddd = group ddd by zd,url_name agg account:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[325]原语 ddd = @udf ddd by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.account', 'Action': 'lambda', 'lambda': 'account_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[326]原语 ddd.account = lambda account_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'zd,url_name,account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[327]原语 ddd = loc ddd by zd,url_name,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ddd', 'Action': 'distinct', 'distinct': 'ddd', 'by': 'zd,url_name,account'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[328]原语 ddd = distinct ddd by zd,url_name,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_http_acc.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[329]原语 b = @udf ZFile.rm_file with link/link_http_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ddd', 'to': 'pq', 'by': 'link/link_http_acc.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[330]原语 store ddd to pq by link/link_http_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct srcip,real_ip,app,account from api_monitor where content_type not in ('XML','JSON','数据文件') and account != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[333]原语 ddd = load ckh by ckh with select distinct srcip,r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ddd', 'by': 'srcip:str,real_ip:str,app:str,account:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[334]原语 alter ddd by srcip:str,real_ip:str,app:str,account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_row_lambda', 'with': "x: x[0] if x[0] != '127.0.0.1' else x[1]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[335]原语 ddd = @udf ddd by udf0.df_row_lambda with (x: x[0]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ddd', 'as': "'lambda1':'zd'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[336]原语 rename ddd as ("lambda1":"zd") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': "zd != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[337]原语 ddd = filter ddd by zd != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.app1', 'Action': 'lambda', 'lambda': 'app', 'by': 'x:x.split(":")'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[338]原语 ddd.app1 = lambda app by (x:x.split(":")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_l2cs', 'with': 'app1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[339]原语 ddd = @udf ddd by udf0.df_l2cs with app1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[340]原语 ddd = @udf ddd by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'zd,n100,account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[341]原语 ddd = loc ddd by zd,n100,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ddd', 'as': "'n100':'app'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[342]原语 rename ddd as ("n100":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ddd', 'Action': 'add', 'add': 'aa', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[344]原语 ddd = add aa by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_row_lambda', 'with': 'x: x[3] if x[0] != x[1] else 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[345]原语 ddd = @udf ddd by udf0.df_row_lambda with (x: x[3]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.len1', 'Action': 'lambda', 'lambda': 'account', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[347]原语 ddd.len1 = lambda account by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[348]原语 ddd = filter ddd by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.len1', 'Action': 'lambda', 'lambda': 'zd', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[349]原语 ddd.len1 = lambda zd by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[350]原语 ddd = filter ddd by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'zd,app,account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[352]原语 ddd = loc ddd by zd,app,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ddd', 'Action': 'distinct', 'distinct': 'ddd', 'by': 'zd,app,account'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[353]原语 ddd = distinct ddd by zd,app,account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.account', 'Action': 'lambda', 'lambda': 'account', 'by': "x:x+';'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[354]原语 ddd.account = lambda account by (x:x+";") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ddd', 'Action': 'group', 'group': 'ddd', 'by': 'zd,app', 'agg': 'account:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[355]原语 ddd = group ddd by zd,app agg account:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[356]原语 ddd = @udf ddd by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.account1', 'Action': 'lambda', 'lambda': 'account_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[357]原语 ddd.account1 = lambda account_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'zd,app,account1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[358]原语 ddd = loc ddd by zd,app,account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ddd', 'Action': 'distinct', 'distinct': 'ddd', 'by': 'zd,app,account1'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[359]原语 ddd = distinct ddd by zd,app,account1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_http1_acc.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[360]原语 b = @udf ZFile.rm_file with link/link_http1_acc.pq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ddd', 'to': 'pq', 'by': 'link/link_http1_acc.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[361]原语 store ddd to pq by link/link_http1_acc.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ddd', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct src_ip,dest_ip,dest_port,user from dbms where user != ''"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[364]原语 ddd = load ckh by ckh with select distinct src_ip,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'ddd', 'by': 'src_ip:str,dest_ip:str,dest_port:str,user:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[365]原语 alter ddd by src_ip:str,dest_ip:str,dest_port:str,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_row_lambda', 'with': "x: x[0] if x[0] != '127.0.0.1' else x[1]"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[366]原语 ddd = @udf ddd by udf0.df_row_lambda with (x: x[0]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'ddd', 'as': "'lambda1':'app'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[367]原语 rename ddd as ("lambda1":"app") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'ddd', 'Action': 'add', 'add': 'db', 'by': "df['dest_ip']+':'+df['dest_port']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[368]原语 ddd = add db by (df["dest_ip"]+":"+df["dest_port"]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.len1', 'Action': 'lambda', 'lambda': 'user', 'by': 'x:len(x)'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[370]原语 ddd.len1 = lambda user by (x:len(x)) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'ddd', 'Action': 'filter', 'filter': 'ddd', 'by': 'len1 < 80'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[371]原语 ddd = filter ddd by len1 < 80 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'app,db,user'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[373]原语 ddd = loc ddd by app,db,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ddd', 'Action': 'distinct', 'distinct': 'ddd', 'by': 'app,db,user'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[374]原语 ddd = distinct ddd by app,db,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.user', 'Action': 'lambda', 'lambda': 'user', 'by': "x:x+';'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[375]原语 ddd.user = lambda user by (x:x+";") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'ddd', 'Action': 'group', 'group': 'ddd', 'by': 'app,db', 'agg': 'user:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[376]原语 ddd = group ddd by app,db agg user:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ddd', 'Action': '@udf', '@udf': 'ddd', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[377]原语 ddd = @udf ddd by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ddd.user', 'Action': 'lambda', 'lambda': 'user_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[378]原语 ddd.user = lambda user_sum by (x:x[:-1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ddd', 'Action': 'loc', 'loc': 'ddd', 'by': 'app,db,user'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[379]原语 ddd = loc ddd by app,db,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'ddd', 'Action': 'distinct', 'distinct': 'ddd', 'by': 'app,db,user'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[380]原语 ddd = distinct ddd by app,db,user 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_sql_user.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[381]原语 b = @udf ZFile.rm_file with link/link_sql_user.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ddd', 'to': 'pq', 'by': 'link/link_sql_user.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[382]原语 store ddd to pq by link/link_sql_user.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[link_tupu.fbi]执行第[384]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],384

#主函数结束,开始块函数

def block_foreach_145(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'tt', 'Action': 'filter', 'filter': 'ss3', 'by': "app2 == '@app'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第145行foreach语句中]执行第[146]原语 tt = filter ss3 by app2 == "@app" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'tt', 'Action': '@udf', '@udf': 'tt', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第145行foreach语句中]执行第[147]原语 tt = @udf tt by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'tt', 'Action': 'add', 'add': 'url_name', 'by': 'df["app2"]+"-"+df["api_type"]+"接口"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第145行foreach语句中]执行第[148]原语 tt = add url_name by (df["app2"]+"-"+df["api_type"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'tt', 'Action': 'loc', 'loc': 'tt', 'by': 'url,app2,url_name,http_method,risk_level'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第145行foreach语句中]执行第[150]原语 tt = loc tt by url,app2,url_name,http_method,risk_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'ss4', 'Action': 'union', 'union': 'ss4,tt'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第145行foreach语句中]执行第[151]原语 ss4 = union ss4,tt 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_145

def block_foreach_230(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'add1', 'Action': 'filter', 'filter': 'ss', 'by': 'index >= 5000 * (@num - 1) and index < 5000 * @num'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第230行foreach语句中]执行第[231]原语 add1 = filter ss by index >= 5000 * (@num - 1) and... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'add1', 'by': 'GL.add_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第230行foreach语句中]执行第[232]原语 ret = @udf add1 by GL.add_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[第230行foreach语句中]执行第[233]原语 ret_pd = @sdf sys_lambda with ($ret,x: "Successful... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_foreach_230

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



