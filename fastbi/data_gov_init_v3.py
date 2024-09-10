#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: data_gov_init
#datetime: 2024-08-30T16:10:53.443820
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
		add_the_error('[data_gov_init.fea]执行第[20]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= show', 'Ta': 'pk', 'Action': 'show', 'show': 'defines'}
	try:
		show_fun(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[24]原语 pk = show defines 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'data_key', 'Action': 'filter', 'filter': 'pk', 'by': 'key=="data_key"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[25]原语 data_key = filter pk by (key=="data_key") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'pk', 'Action': 'filter', 'filter': 'pk', 'by': 'key=="PK"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[26]原语 pk = filter pk by (key=="PK") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'pk', 'Action': 'loc', 'loc': 'pk', 'by': 'value'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[27]原语 pk = loc pk by value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'pk.value', 'Action': 'lambda', 'lambda': 'value', 'by': "x:x[:8]+''.join(random.sample('A!@#',4))+x[-4:]"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[28]原语 pk.value = lambda value by (x:x[:8]+"".join(random... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'pk', 'Action': '@udf', '@udf': 'pk', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[29]原语 pk = @udf pk by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pk_0', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'data_gov_data_key'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[31]原语 pk_0 = load ssdb by ssdb0 with data_gov_data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'pk', 'Action': 'union', 'union': 'pk_0,pk'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[32]原语 pk = union pk_0,pk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'pk', 'Action': '@udf', '@udf': 'pk', 'by': 'udf0.df_limit', 'with': '1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[33]原语 pk = @udf pk by udf0.df_limit with 1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'pk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_gov_data_key'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[34]原语 store pk to ssdb by ssdb0 with data_gov_data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pd_data_key', 'Action': 'eval', 'eval': 'data_key', 'by': 'index.size==0'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[36]原语 pd_data_key = eval data_key by (index.size==0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$pd_data_key== 1', 'with': '""\n#act_data_key = @sdf sys_if_run with ($pd_data_key,"""\ndata_key1 = eval pk by (iloc[0,0])\ndefine data_key as $data_key1\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=37
		ptree['funs']=block_if_37
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[37]原语 if $pd_data_key== 1 with "#act_data_key = @sdf sys... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'data_gov_init_1.fea'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[45]原语 run data_gov_init_1.fea 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'init_mkd.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[48]原语 run init_mkd.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 't', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[51]原语 t = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 't', 'Action': '@sdf', '@sdf': 'sys_str', 'by': '$t,[0:10]'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[52]原语 t = @sdf sys_str by $t,[0:10] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[53]原语 s = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_append', 'with': '$t'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[54]原语 s = @udf s by udf0.df_append with $t 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'count', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[55]原语 s = add count by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'ssdb', 'with': 'syslog_cz'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[56]原语 store s to ssdb with syslog_cz 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'qh_model.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[57]原语 run qh_model.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[data_gov_init.fea]执行第[60]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],60

#主函数结束,开始块函数

def block_if_37(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'data_key1', 'Action': 'eval', 'eval': 'pk', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第37行if语句中]执行第[39]原语 data_key1 = eval pk by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'data_key', 'as': '$data_key1'}
	ptree['as'] = deal_sdf(workspace,ptree['as'])
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[第37行if语句中]执行第[40]原语 define data_key as $data_key1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_37

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



