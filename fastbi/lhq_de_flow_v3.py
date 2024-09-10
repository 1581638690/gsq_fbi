#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_de_flow
#datetime: 2024-08-30T16:10:54.328824
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
		add_the_error('[lhq_de_flow.fbi]执行第[16]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'clear_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT partition,formatDateTime(toDate(partition), '%Y-%m-%d') as partition2 FROM system.parts WHERE (database = 'default') and (table = 'api_monitor') GROUP BY partition order by partition desc"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[28]原语 clear_ckh = load ckh by ckh with  SELECT partition... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'clear_ckh.partition', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[42]原语 alter clear_ckh.partition as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'date', 'Action': 'eval', 'eval': 'clear_ckh', 'by': 'index.max()'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[45]原语 date = eval clear_ckh by index.max() 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'date', 'Action': 'filter', 'filter': 'clear_ckh', 'by': 'index == $date'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[46]原语 date = filter clear_ckh by index == $date 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'date1', 'Action': 'eval', 'eval': 'date', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[47]原语 date1 = eval date by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'date2', 'Action': 'eval', 'eval': 'date', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[48]原语 date2 = eval date by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'df -h'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[49]原语 s = @udf FBI.local_cmd with df -h 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: str(x)[:-3]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[50]原语 s.stdout = lambda stdout by x: str(x)[:-3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.x', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: len(x.split("/data"))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[51]原语 s.x = lambda stdout by x: len(x.split("/data")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 's', 'Action': 'filter', 'filter': 's', 'by': 'x ==2'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[52]原语 s = filter s by x ==2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x.split("/data")[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[53]原语 s.stdout = lambda stdout by x: x.split("/data")[0]... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x.strip()'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[54]原语 s.stdout = lambda stdout by x: x.strip() 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': "x: x[x.rfind(' '):]"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[55]原语 s.stdout = lambda stdout by x: x[x.rfind(" "):] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x.strip()'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[56]原语 s.stdout = lambda stdout by x: x.strip() 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x.split("%")[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[57]原语 s.stdout = lambda stdout by x: x.split("%")[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 's.index.size==0', 'with': '""\ns = @udf FBI.local_cmd with df -h\ns.stdout = lambda stdout by x: str(x)[:-3]\ns.x = lambda stdout by x: len(x.split("T"))\ns = filter s by x >1\ns.stdout = lambda stdout by x: x.split("%")[0]\ns.stdout = lambda stdout by x: x[-3:]\ns.stdout = lambda stdout by x: x.strip()\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
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
		add_the_error('[lhq_de_flow.fbi]执行第[58]原语 if s.index.size==0 with "s = @udf FBI.local_cmd wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 's.stdout', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[67]原语 alter s.stdout as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 's', 'Action': 'eval', 'eval': 's', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[68]原语 s = eval s by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'del_ckh', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'setting as json'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[69]原语 del_ckh = load ssdb by ssdb0 with setting as json 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= jaas', 'Ta': 'del_ckh', 'Action': 'jaas', 'jaas': 'del_ckh', 'by': 'del_ckh["setting"]["delete_date"]["del_ckh"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[70]原语 del_ckh = jaas del_ckh by del_ckh["setting"]["dele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$s >= $del_ckh', 'with': '""\nd_ckh = load ckh by ckh with alter table api_bussiness drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_abroad drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_dns drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_ftp drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_http drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_imap drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_model drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_monitor drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_pop3 drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_smb drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_smtp drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_tftp drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table datafilter_alarm drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table merge_urls drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table sen_http_count drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table sensitive_data drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table sensitive_data_alarm drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table stat_req_alm drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_delay drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table agent_datalink drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_link_data drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_modsecurity drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table ip_link_data drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table ip_link drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_fileinfo drop partition \'$date1\'\na = load ckh by ckh with select distinct file_path filename from api_fileinfo where formatDateTime(toDate(timestamp), \'%Y-%m-%d\') = \'$date2\' and file_path != \'\'\na.filename = lambda filename by x: \'../workspace/znsm/\' + x\nb = @udf a by ZFile.rm\n### 断点取值，重新计算\naa = @udf udf0.new_df with time\n###接口敏感信息\nstore aa to ssdb by ssdb0 with sensitive_tab\n#bb = @udf ZFile.rm_file with sensitive/sens_data.pq\nbb = @udf FBI.local_cmd with sudo rm -rf /data/workspace/sensitive\nrun sensitive_tab.fbi\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=71
		ptree['funs']=block_if_71
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[71]原语 if $s >= $del_ckh with "d_ckh = load ckh by ckh wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'clear_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT partition FROM system.parts WHERE (database = 'default') and (table = 'api_visit_day') GROUP BY partition order by partition desc"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[111]原语 clear_ckh = load ckh by ckh with  SELECT partition... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'clear_ckh.partition', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[125]原语 alter clear_ckh.partition as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'date', 'Action': 'eval', 'eval': 'clear_ckh', 'by': 'index.max()'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[126]原语 date = eval clear_ckh by index.max() 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'date', 'Action': 'filter', 'filter': 'clear_ckh', 'by': 'index == $date1'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[127]原语 date = filter clear_ckh by index == $date1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'date', 'Action': 'eval', 'eval': 'date', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[128]原语 date = eval date by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date0', 'Action': '@sdf', '@sdf': 'sys_now', 'with': '-1m'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[129]原语 date0 = @sdf sys_now with -1m 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date0', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$date10,"%Y%m%d"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[130]原语 date0= @sdf format_now with ($date10,"%Y%m%d") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': "'$date1' == '$date10'", 'with': '""\nd_ckh = load ckh by ckh with alter table api_visit_hour drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_visit_day drop partition \'$date1\'\nd_ckh = load ckh by ckh with alter table api_hx drop partition \'$date1\'\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=131
		ptree['funs']=block_if_131
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[131]原语 if "$date1" == "$date10" with "d_ckh = load ckh by... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_de_flow.fbi]执行第[137]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],137

#主函数结束,开始块函数

def block_if_58(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'df -h'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[59]原语 s = @udf FBI.local_cmd with df -h 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: str(x)[:-3]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[60]原语 s.stdout = lambda stdout by x: str(x)[:-3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.x', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: len(x.split("T"))'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[61]原语 s.x = lambda stdout by x: len(x.split("T")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 's', 'Action': 'filter', 'filter': 's', 'by': 'x >1'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[62]原语 s = filter s by x >1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x.split("%")[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[63]原语 s.stdout = lambda stdout by x: x.split("%")[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x[-3:]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[64]原语 s.stdout = lambda stdout by x: x[-3:] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 's.stdout', 'Action': 'lambda', 'lambda': 'stdout', 'by': 'x: x.strip()'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第58行if语句中]执行第[65]原语 s.stdout = lambda stdout by x: x.strip() 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_58

def block_if_71(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_bussiness drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[72]原语 d_ckh = load ckh by ckh with alter table api_bussi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_abroad drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[73]原语 d_ckh = load ckh by ckh with alter table api_abroa... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_dns drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[74]原语 d_ckh = load ckh by ckh with alter table api_dns d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_ftp drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[75]原语 d_ckh = load ckh by ckh with alter table api_ftp d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_http drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[76]原语 d_ckh = load ckh by ckh with alter table api_http ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_imap drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[77]原语 d_ckh = load ckh by ckh with alter table api_imap ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_model drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[78]原语 d_ckh = load ckh by ckh with alter table api_model... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_monitor drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[79]原语 d_ckh = load ckh by ckh with alter table api_monit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_pop3 drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[80]原语 d_ckh = load ckh by ckh with alter table api_pop3 ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_smb drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[81]原语 d_ckh = load ckh by ckh with alter table api_smb d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_smtp drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[82]原语 d_ckh = load ckh by ckh with alter table api_smtp ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_tftp drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[83]原语 d_ckh = load ckh by ckh with alter table api_tftp ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table datafilter_alarm drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[84]原语 d_ckh = load ckh by ckh with alter table datafilte... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table merge_urls drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[85]原语 d_ckh = load ckh by ckh with alter table merge_url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table sen_http_count drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[86]原语 d_ckh = load ckh by ckh with alter table sen_http_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table sensitive_data drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[87]原语 d_ckh = load ckh by ckh with alter table sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table sensitive_data_alarm drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[88]原语 d_ckh = load ckh by ckh with alter table sensitive... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table stat_req_alm drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[89]原语 d_ckh = load ckh by ckh with alter table stat_req_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_delay drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[90]原语 d_ckh = load ckh by ckh with alter table api_delay... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table agent_datalink drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[91]原语 d_ckh = load ckh by ckh with alter table agent_dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_link_data drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[92]原语 d_ckh = load ckh by ckh with alter table api_link_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_modsecurity drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[93]原语 d_ckh = load ckh by ckh with alter table api_modse... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table ip_link_data drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[94]原语 d_ckh = load ckh by ckh with alter table ip_link_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table ip_link drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[95]原语 d_ckh = load ckh by ckh with alter table ip_link d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_fileinfo drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[96]原语 d_ckh = load ckh by ckh with alter table api_filei... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select distinct file_path filename from api_fileinfo where formatDateTime(toDate(timestamp), '%Y-%m-%d') = '$date2' and file_path != ''"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[97]原语 a = load ckh by ckh with select distinct file_path... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.filename', 'Action': 'lambda', 'lambda': 'filename', 'by': "x: '../workspace/znsm/' + x"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[98]原语 a.filename = lambda filename by x: "../workspace/z... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'ZFile.rm'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[99]原语 b = @udf a by ZFile.rm 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[101]原语 aa = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive_tab'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[103]原语 store aa to ssdb by ssdb0 with sensitive_tab 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/workspace/sensitive'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[105]原语 bb = @udf FBI.local_cmd with sudo rm -rf /data/wor... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'sensitive_tab.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[第71行if语句中]执行第[106]原语 run sensitive_tab.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_71

def block_if_131(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_visit_hour drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第131行if语句中]执行第[132]原语 d_ckh = load ckh by ckh with alter table api_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_visit_day drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第131行if语句中]执行第[133]原语 d_ckh = load ckh by ckh with alter table api_visit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd_ckh', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "alter table api_hx drop partition '$date1'"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第131行if语句中]执行第[134]原语 d_ckh = load ckh by ckh with alter table api_hx dr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_131

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



