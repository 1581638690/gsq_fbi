#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: warn_rule_disk
#datetime: 2024-08-30T16:10:54.567144
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
		add_the_error('[warn_rule_disk.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'zts_sj2.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[17]原语 run zts_sj2.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'lhq_sec_sql.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[19]原语 run lhq_sec_sql.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip', 'Action': '@udf', '@udf': 'SH.network_cards2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[24]原语 ip = @udf SH.network_cards2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ips', 'Action': '@udf', '@udf': 'ip', 'by': 'udf0.df_limit', 'with': '0,1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[25]原语 ips = @udf ip by udf0.df_limit with (0,1) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ips.address', 'Action': 'lambda', 'lambda': 'address', 'by': 'x:str(x).replace("\\\'","").replace("[","").replace("]","").split(\'/\')[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[26]原语 ips.address = lambda address by (x:str(x).replace(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'eval', 'eval': 'ips', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[27]原语 ip = eval ips by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[29]原语 date = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'wd', 'Action': '@udf', '@udf': 'PS.disk_usage'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[30]原语 wd = @udf PS.disk_usage 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'wd', 'Action': 'add', 'add': 'disk', 'by': '(wd.Free*100)//wd.Total'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[31]原语 wd = add disk by (wd.Free*100)//wd.Total 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'disk', 'Action': 'eval', 'eval': 'wd', 'by': 'iloc[0,4]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[32]原语 disk = eval wd by iloc[0,4] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'diskf', 'Action': 'eval', 'eval': 'wd', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[33]原语 diskf = eval wd by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'disku', 'Action': 'eval', 'eval': 'wd', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[34]原语 disku = eval wd by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'diskt', 'Action': 'eval', 'eval': 'wd', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[35]原语 diskt = eval wd by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dsre', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select replace(threshod,"%","")/100 as threshod from disk_resource where sid =1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[36]原语 dsre = @udf RS.load_mysql_sql with (mysql1,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'dsre.threshod', 'as': 'float'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[37]原语 alter dsre.threshod as float 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'disk as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[38]原语 a = load ssdb by ssdb0 with disk as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'per', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["data"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[39]原语 per = jaas a by a["data"] as sdf 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'num', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$diskt * $per'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[40]原语 num = @sdf sys_eval with ($diskt * $per) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'not 100-$disk > int($per)', 'as': 'notice', 'with': '磁盘空间剩余$disk %'}
	ptree['assert'] = deal_sdf(workspace,ptree['assert'])
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[44]原语 assert not 100-$disk > int($per) as notice  with 磁... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'a', 'Action': 'if', 'if': '$disku> $num', 'with': '""\ndisk_table = @udf udf0.new_df with (id,timestamp,srcip,srcport,dstip,dstport,action,signature,category,severity,filename,proto,app_proto)\ndisk_table = @udf disk_table by udf0.df_append with ("0",$date,$ip,,,,,,系统告警,1,,系统,)\n#dsre = add result by \'$per\'\n#ips = add timestamp by (\'$date\')\ndisk_table.id = lambda id by x: str(uuid.uuid1())\ndisk_table = add signature by ("磁盘警告：剩余容量$diskf G,占比$disk %！")\nalter disk_table.timestamp as datetime64\n#disk_table = loc disk_table by id to index\nstore disk_table to ckh by ckh with api_alert\n#ecount = @sdf sys_eval with ($ecount +1)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=46
		ptree['funs']=block_if_46
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[46]原语 a = if $disku> $num with "disk_table = @udf udf0.n... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'df -h'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[59]原语 s = @udf FBI.local_cmd with df -h 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'memory', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select replace(threshod,"%","")/100 as threshod from disk_resource where sid =2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[64]原语 memory = @udf RS.load_mysql_sql with (mysql1,selec... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'set_num', 'Action': 'eval', 'eval': 'memory', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[65]原语 set_num = eval memory by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sys_info', 'Action': '@udf', '@udf': 'PS.sys_baseinfo'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[66]原语 sys_info = @udf PS.sys_baseinfo 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sys_status', 'Action': '@udf', '@udf': 'PS.sys_stats'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[67]原语 sys_status = @udf PS.sys_stats 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sys_cpu_t', 'Action': 'eval', 'eval': 'sys_info', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[69]原语 sys_cpu_t = eval sys_info by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sys_cpu_u', 'Action': 'eval', 'eval': 'sys_status', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[71]原语 sys_cpu_u = eval sys_status by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sys_mo', 'Action': 'eval', 'eval': 'sys_status', 'by': 'iloc[3,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[74]原语 sys_mo = eval sys_status by iloc[3,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mo_u', 'Action': 'eval', 'eval': 'sys_status', 'by': 'iloc[1,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[76]原语 mo_u  = eval sys_status by iloc[1,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mo_t', 'Action': 'eval', 'eval': 'sys_status', 'by': 'iloc[2,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[78]原语 mo_t = eval sys_status by iloc[2,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'mo_s', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$mo_t - $mo_u'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[79]原语 mo_s = @sdf sys_eval with ($mo_t - $mo_u) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'mo_bie', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$sys_mo, x:"%.2f"%float(x)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[80]原语 mo_bie = @sdf sys_lambda with ($sys_mo, x:"%.2f"%f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'mo_bies', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$mo_bie *100'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[81]原语 mo_bies = @sdf sys_eval with ($mo_bie *100) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$sys_mo >= $set_num', 'with': '""\nme_table = @udf udf0.new_df with (id,timestamp,srcip,srcport,dstip,dstport,action,signature,category,severity,filename,proto,app_proto)\nme_table = @udf me_table by udf0.df_append with ("0",$date,$ip,,,,,,系统告警,1,,系统,)\nme_table = add signature by ("内存警告：内存使用$mo_u G,占比$mo_bies %！")\nme_table.id = lambda id by x: str(uuid.uuid1())\nalter me_table.timestamp as datetime64\n#me_table = loc me_table by id to index\nstore me_table to ckh by ckh with api_alert\n#ecount = @sdf sys_eval with ($ecount +1)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=82
		ptree['funs']=block_if_82
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[82]原语 if $sys_mo >= $set_num with "me_table = @udf udf0.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cpu_bie', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$sys_cpu_u / $sys_cpu_t * 100'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[93]原语 cpu_bie = @sdf sys_eval with ($sys_cpu_u / $sys_cp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cpu_s', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$sys_cpu_t - $sys_cpu_u'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[94]原语 cpu_s = @sdf sys_eval with ($sys_cpu_t - $sys_cpu_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cpu_bies', 'Action': '@sdf', '@sdf': 'sys_lambda', 'with': '$cpu_bie, x:"%.2f"%float(x)'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[95]原语 cpu_bies = @sdf sys_lambda with ($cpu_bie, x:"%.2f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cpu_mo', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select replace(threshod,"%","")/100 as threshod from disk_resource where sid =3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[96]原语 cpu_mo = @udf RS.load_mysql_sql with (mysql1,selec... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'cpu_mo', 'Action': 'eval', 'eval': 'cpu_mo', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[97]原语 cpu_mo = eval cpu_mo by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'cpu_mo', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$cpu_mo * 100'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[98]原语 cpu_mo = @sdf sys_eval with ($cpu_mo * 100) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= if', 'Ta': 'ac', 'Action': 'if', 'if': '$cpu_bie >= $cpu_mo', 'with': '""\ncpu_table = @udf udf0.new_df with (id,timestamp,srcip,srcport,dstip,dstport,action,signature,category,severity,filename,proto,app_proto)\ncpu_table = @udf cpu_table by udf0.df_append with ("0",$date,$ip,,,,,,系统告警,1,,系统,)\ncpu_table = add signature by ("CPU警告：系统CPU共$sys_cpu_t个,现CPU使用率$cpu_bies %！")\ncpu_table.id = lambda id by x: str(uuid.uuid1())\nalter cpu_table.timestamp as datetime64\n#cpu_table = loc cpu_table by id to index\nstore cpu_table to ckh by ckh with api_alert\n#ecount = @sdf sys_eval with ($ecount +1)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=99
		ptree['funs']=block_if_99
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[99]原语 ac = if $cpu_bie >= $cpu_mo with "cpu_table = @udf... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[warn_rule_disk.fbi]执行第[113]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],113

#主函数结束,开始块函数

def block_if_46(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'disk_table', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,timestamp,srcip,srcport,dstip,dstport,action,signature,category,severity,filename,proto,app_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[47]原语 disk_table = @udf udf0.new_df with (id,timestamp,s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'disk_table', 'Action': '@udf', '@udf': 'disk_table', 'by': 'udf0.df_append', 'with': '"0",$date,$ip,,,,,,系统告警,1,,系统,'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[48]原语 disk_table = @udf disk_table by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'disk_table.id', 'Action': 'lambda', 'lambda': 'id', 'by': 'x: str(uuid.uuid1())'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[51]原语 disk_table.id = lambda id by x: str(uuid.uuid1()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'disk_table', 'Action': 'add', 'add': 'signature', 'by': '"磁盘警告：剩余容量$diskf G,占比$disk %！"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[52]原语 disk_table = add signature by ("磁盘警告：剩余容量$diskf G,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'disk_table.timestamp', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[53]原语 alter disk_table.timestamp as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'disk_table', 'to': 'ckh', 'by': 'ckh', 'with': 'api_alert'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第46行if语句中]执行第[55]原语 store disk_table to ckh by ckh with api_alert 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_46

def block_if_82(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'me_table', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,timestamp,srcip,srcport,dstip,dstport,action,signature,category,severity,filename,proto,app_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[83]原语 me_table = @udf udf0.new_df with (id,timestamp,src... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'me_table', 'Action': '@udf', '@udf': 'me_table', 'by': 'udf0.df_append', 'with': '"0",$date,$ip,,,,,,系统告警,1,,系统,'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[84]原语 me_table = @udf me_table by udf0.df_append with ("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'me_table', 'Action': 'add', 'add': 'signature', 'by': '"内存警告：内存使用$mo_u G,占比$mo_bies %！"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[85]原语 me_table = add signature by ("内存警告：内存使用$mo_u G,占比$... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'me_table.id', 'Action': 'lambda', 'lambda': 'id', 'by': 'x: str(uuid.uuid1())'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[86]原语 me_table.id = lambda id by x: str(uuid.uuid1()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'me_table.timestamp', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[87]原语 alter me_table.timestamp as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'me_table', 'to': 'ckh', 'by': 'ckh', 'with': 'api_alert'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第82行if语句中]执行第[89]原语 store me_table to ckh by ckh with api_alert 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_82

def block_if_99(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cpu_table', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,timestamp,srcip,srcport,dstip,dstport,action,signature,category,severity,filename,proto,app_proto'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第99行if语句中]执行第[100]原语 cpu_table = @udf udf0.new_df with (id,timestamp,sr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'cpu_table', 'Action': '@udf', '@udf': 'cpu_table', 'by': 'udf0.df_append', 'with': '"0",$date,$ip,,,,,,系统告警,1,,系统,'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第99行if语句中]执行第[101]原语 cpu_table = @udf cpu_table by udf0.df_append with ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'cpu_table', 'Action': 'add', 'add': 'signature', 'by': '"CPU警告：系统CPU共$sys_cpu_t个,现CPU使用率$cpu_bies %！"'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第99行if语句中]执行第[102]原语 cpu_table = add signature by ("CPU警告：系统CPU共$sys_cp... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'cpu_table.id', 'Action': 'lambda', 'lambda': 'id', 'by': 'x: str(uuid.uuid1())'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第99行if语句中]执行第[103]原语 cpu_table.id = lambda id by x: str(uuid.uuid1()) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'cpu_table.timestamp', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[第99行if语句中]执行第[104]原语 alter cpu_table.timestamp as datetime64 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'cpu_table', 'to': 'ckh', 'by': 'ckh', 'with': 'api_alert'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第99行if语句中]执行第[106]原语 store cpu_table to ckh by ckh with api_alert 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_99

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



