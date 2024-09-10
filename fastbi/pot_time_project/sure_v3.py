#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: pot_time_project/sure
#datetime: 2024-08-30T16:10:57.579509
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
		add_the_error('[pot_time_project/sure.fea]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[7]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.pd', 'Action': 'lambda', 'lambda': 'updata_time', 'by': "x:True if x!='' else False"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[8]原语 a.pd = lambda updata_time by (x:True if x!="" else... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_new', 'Action': 'loc', 'loc': 'a', 'by': 'ntp'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[12]原语 df_new = loc a by ntp 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'df_old', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'key:pot_time_project_ntp'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[13]原语 df_old = load ssdb by ssdb0 with key:pot_time_proj... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'df_new', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'key:pot_time_project_ntp'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[14]原语 store df_new to ssdb by ssdb0 with key:pot_time_pr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'df', 'Action': 'join', 'join': 'df_new,df_old', 'by': 'index,index'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[15]原语 df = join df_new,df_old by index,index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'df.ntp_x.ntp_y', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[16]原语 alter df.ntp_x.ntp_y as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df', 'Action': 'add', 'add': 'is_change', 'by': 'df["ntp_x"]-df["ntp_y"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[17]原语 df = add is_change by (df["ntp_x"]-df["ntp_y"]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df.pd2', 'Action': 'lambda', 'lambda': 'is_change', 'by': 'x:True if x!=0 else False'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[18]原语 df.pd2 = lambda is_change by (x:True if x!=0 else ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pd2', 'Action': 'eval', 'eval': 'df', 'by': "get_value(0,'pd2')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[19]原语 pd2 = eval df by (get_value(0,"pd2")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'NTP', 'Action': 'eval', 'eval': 'a', 'by': "get_value(0,'ntp')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[22]原语 NTP =eval a by (get_value(0,"ntp")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pd', 'Action': 'eval', 'eval': 'a', 'by': "get_value(0,'pd')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[24]原语 pd = eval a by (get_value(0,"pd")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'if_run', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$NTP,\xa0"""\nif_run2 = @sdf sys_if_run with ($pd2,\xa0"cmd1 = @udf df0@sys by NSM.exe_os_cmd with (timedatectl set-ntp true)")\n"""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ss = ptree['with'].split('\n')
	ss0 = deal_sdf(workspace,ss[0])
	ss1 = deal_sdf(workspace,ss[-1])
	ptree['with'] = '%s\n%s\n%s\n'%(ss0,'\n'.join(ss[1:-1]),ss1)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[26]原语 if_run = @sdf sys_if_run with ($NTP, "if_run2 = @s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'unif_run', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$NTP,\xa0 """\nif_run3 = @sdf sys_if_run with ($pd2,\xa0"cmd2= @udf df0@sys by NSM.exe_os_cmd with (timedatectl set-ntp false)")\na.updata_time = lambda updata_time by (x:\'"\' + x + \'"\')\nupdata_time = eval a by (get_value(0,\'updata_time\'))\nis_pd_true = @sdf sys_if_run with ($pd,"cmd3= @udf df0@sys by NSM.exe_os_cmd with (date -s $updata_time)")\n"""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ss = ptree['with'].split('\n')
	ss0 = deal_sdf(workspace,ss[0])
	ss1 = deal_sdf(workspace,ss[-1])
	ptree['with'] = '%s\n%s\n%s\n'%(ss0,'\n'.join(ss[1:-1]),ss1)
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[30]原语 unif_run = @sdf sys_unif_run with ($NTP,  "if_run3... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not_have_error()', 'as': 'altert', 'to': '时间修改成功!', 'with': '修改失败!'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[36]原语 assert not_have_error() as altert to 时间修改成功! with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[pot_time_project/sure.fea]执行第[37]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],37

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



