#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_portrait_data
#datetime: 2024-08-30T16:10:55.802056
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
		add_the_error('[api_portrait_data.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'apilist1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select id,url,visits_num,visits_flow,app,data_type,risk_level,method,first_time,portrait_time from data_api_new where id = '@id'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[18]原语 apilist1 = load db by mysql1 with select id,url,vi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'apilist1', 'Action': '@udf', '@udf': 'apilist1', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[19]原语 apilist1 = @udf apilist1 by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 'apilist1', 'by': 'visits_num,visits_flow,app,data_type,risk_level,method,first_time,portrait_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[21]原语 s = loc apilist1 by (visits_num,visits_flow,app,da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.first_time', 'Action': 'str', 'str': 'first_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[22]原语 s.first_time = str first_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.first_time', 'Action': 'str', 'str': 'first_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[23]原语 s.first_time = str first_time by (replace("T"," ")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.portrait_time', 'Action': 'str', 'str': 'portrait_time', 'by': '[0:19]'}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[24]原语 s.portrait_time = str portrait_time by [0:19] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.portrait_time', 'Action': 'str', 'str': 'portrait_time', 'by': "replace('T',' ')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[25]原语 s.portrait_time = str portrait_time by (replace("T... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': "replace('0','低风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[27]原语 s.risk_level = str risk_level by (replace("0","低风险... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': "replace('1','中风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[28]原语 s.risk_level = str risk_level by (replace("1","中风险... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 's.risk_level', 'Action': 'str', 'str': 'risk_level', 'by': "replace('2','高风险')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[29]原语 s.risk_level = str risk_level by (replace("2","高风险... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'visits_num,visits_flow,app,data_type,risk_level,method,first_time,portrait_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[30]原语 s = loc s by (visits_num,visits_flow,app,data_type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'v_flow', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[32]原语 v_flow = eval s by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[33]原语 aa = @sdf sys_eval with 0 <= $v_flow < 1024 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[34]原语 bb = @sdf sys_eval with 1024 <= $v_flow < 1048576 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[35]原语 cc = @sdf sys_eval with 1048576 <= $v_flow < 10737... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[36]原语 dd = @sdf sys_eval with 1073741824 <= $v_flow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[37]原语 aa = @sdf sys_if_run with ($aa,"s = add 1 by ("(B)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'bb', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$bb,"s.visits_flow = lambda visits_flow by (x:round(x/1024,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[38]原语 bb = @sdf sys_if_run with ($bb,"s.visits_flow = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[39]原语 bb = @sdf sys_if_run with ($bb,"s = add 1 by ("(KB... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cc', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$cc,"s.visits_flow = lambda visits_flow by (x:round(x/1024/1024,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[40]原语 cc = @sdf sys_if_run with ($cc,"s.visits_flow = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[41]原语 cc = @sdf sys_if_run with ($cc,"s = add 1 by ("(M)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'dd', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$dd,"s.visits_flow = lambda visits_flow by (x:round(x/1024/1024/1024,2))"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[42]原语 dd = @sdf sys_if_run with ($dd,"s.visits_flow = la... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

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
		add_the_error('[api_portrait_data.fbi]执行第[43]原语 dd = @sdf sys_if_run with ($dd,"s = add 1 by ("(G)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visits_flow', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[45]原语 alter s.visits_flow as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'visits_flow', 'by': 's["visits_flow"]+s["1"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[46]原语 s = add visits_flow by s["visits_flow"]+s["1"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'drop': '1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[48]原语 s = loc s drop 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visits_num', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[49]原语 alter s.visits_num as str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.visits_num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[50]原语 alter s.visits_num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'qh_api_if.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[51]原语 run qh_api_if.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 's', 'by': '"visits_num":"访问量","visits_flow":"访问流量","app":"所属应用","data_type":"资源类型","risk_level":"风险等级","portrait_time":"画像开启时间","first_time":"首次发现时间","method":"请求类型"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[52]原语 rename s by ("visits_num":"访问量","visits_flow":"访问流... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_T'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[53]原语 s = @udf s by udf0.df_T 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'index', 'to': 'name'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[54]原语 s = loc s by index to name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'icon', 'by': "'F396','F352','F307','F146','F019','F298','F306','F150'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[57]原语 s = add icon by ("F396","F352","F307","F146","F019... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 's', 'as': "0:'value'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[58]原语 rename s as (0:"value") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'pageid', 'by': "'','','modeling:app_new_1','','','','',''"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[59]原语 s = add pageid by ("","","modeling:app_new_1","","... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'eval', 'eval': 's', 'by': 'iloc[2,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[60]原语 app = eval s by iloc[2,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': '参数', 'by': "'','','@app=$app','','','','',''"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[61]原语 s = add 参数 by ("","","@app=$app","","","","","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'by': 'name,value,icon,pageid,参数'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[63]原语 s = loc s by name,value,icon,pageid,参数 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'z:@id:profile'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[64]原语 store s to ssdb with z:@id:profile 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'name', 'Action': 'loc', 'loc': 'apilist1', 'by': 'url'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[68]原语 name = loc apilist1 by url 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'name', 'as': '"api":"接口名"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[69]原语 rename name as ("api":"接口名") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'name', 'to': 'ssdb', 'with': 'z:@id:name'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[70]原语 store name to ssdb with z:@id:name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_portrait_data.fbi]执行第[72]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],72

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



