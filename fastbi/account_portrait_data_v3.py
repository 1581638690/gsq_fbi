#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: account_portrait_data
#datetime: 2024-08-30T16:10:54.939804
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
		add_the_error('[account_portrait_data.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select visit_num,visit_flow,api_num,ip_num,app_num,flag,firsttime,portrait_time from data_account_new where account = '@account'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[14]原语 s = load db by mysql1 with select visit_num,visit_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 's', 'Action': 'filter', 'filter': 's', 'by': "flag == '@account'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[15]原语 s = filter s by flag == "@account" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[16]原语 s = @udf s by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.firsttime', 'Action': 'str', 'str': 'firsttime', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[17]原语 s.firsttime = str firsttime by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.firsttime', 'Action': 'str', 'str': 'firsttime', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[18]原语 s.firsttime = str firsttime by (replace("T"," ")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.portrait_time', 'Action': 'str', 'str': 'portrait_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[19]原语 s.portrait_time = str portrait_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.portrait_time', 'Action': 'str', 'str': 'portrait_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[20]原语 s.portrait_time = str portrait_time by (replace("T... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'visit_num,visit_flow,api_num,ip_num,app_num,flag,firsttime,portrait_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[21]原语 s = loc s by visit_num,visit_flow,api_num,ip_num,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_flow', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[23]原语 v_flow = eval s by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '0 <= $v_flow < 1024'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[24]原语 aa = @sdf sys_eval with 0 <= $v_flow < 1024 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bb', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '1024 <= $v_flow < 1048576'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[25]原语 bb = @sdf sys_eval with 1024 <= $v_flow < 1048576 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cc', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '1048576 <= $v_flow < 1073741824'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[26]原语 cc = @sdf sys_eval with 1048576 <= $v_flow < 10737... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '1073741824 <= $v_flow'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[27]原语 dd = @sdf sys_eval with 1073741824 <= $v_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'aa', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$aa,"s = add 1 by (\'(B)\')"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[28]原语 aa = @sdf sys_if_run with ($aa,"s = add 1 by ("(B)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bb', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$bb,"s.visit_flow = lambda visit_flow by (x:round(x/1024,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[29]原语 bb = @sdf sys_if_run with ($bb,"s.visit_flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bb', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$bb,"s = add 1 by (\'(KB)\')"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[30]原语 bb = @sdf sys_if_run with ($bb,"s = add 1 by ("(KB... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cc', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$cc,"s.visit_flow = lambda visit_flow by (x:round(x/1024/1024,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[31]原语 cc = @sdf sys_if_run with ($cc,"s.visit_flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cc', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$cc,"s = add 1 by (\'(M)\')"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[32]原语 cc = @sdf sys_if_run with ($cc,"s = add 1 by ("(M)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$dd,"s.visit_flow = lambda visit_flow by (x:round(x/1024/1024/1024,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[33]原语 dd = @sdf sys_if_run with ($dd,"s.visit_flow = lam... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$dd,"s = add 1 by (\'(G)\')"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[34]原语 dd = @sdf sys_if_run with ($dd,"s = add 1 by ("(G)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visit_flow', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[36]原语 alter s.visit_flow as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'visit_flow', 'by': 's["visit_flow"]+s["1"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[37]原语 s = add visit_flow by s["visit_flow"]+s["1"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'drop': '1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[38]原语 s = loc s drop 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.flag', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[39]原语 alter s.flag as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.flag', 'Action': 'str', 'str': 'flag', 'by': 'replace("None","无")'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[40]原语 s.flag = str flag by (replace("None","无")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visit_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[41]原语 alter s.visit_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.api_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[42]原语 alter s.api_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.ip_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[43]原语 alter s.ip_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.app_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[44]原语 alter s.app_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 's', 'by': '"visit_num":"访问量","visit_flow":"访问流量","api_num":"接口数量","ip_num":"访问IP数量","app_num":"访问应用数量","flag":"标签","portrait_time":"画像访问时间","firsttime":"首次发现时间"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[45]原语 rename s by ("visit_num":"访问量","visit_flow":"访问流量"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[53]原语 s = @udf s by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'index', 'to': 'name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[54]原语 s = loc s by index to name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 's', 'as': "0:'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[56]原语 rename s as (0:"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'icon', 'by': "'F396','F352','F307','F146','F019','F298','F306','F150'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[57]原语 s = add icon by ("F396","F352","F307","F146","F019... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'name,value,icon'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[59]原语 s = loc s by name,value,icon 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'acc:@account:profile'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[60]原语 store s to ssdb with acc:@account:profile 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select account from data_account_new where account = '@account'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[63]原语 t = load db by mysql1 with select account from dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'name', 'Action': 'loc', 'loc': 't', 'by': 'account'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[64]原语 name = loc t by account 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'name', 'as': '"account":"账号名"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[65]原语 rename name as ("account":"账号名") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'name', 'to': 'ssdb', 'with': 'acc:@account:name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[66]原语 store name to ssdb with acc:@account:name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[account_portrait_data.fbi]执行第[68]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],68

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



