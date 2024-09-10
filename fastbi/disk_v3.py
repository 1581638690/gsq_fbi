#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: disk
#datetime: 2024-08-30T16:10:54.660575
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
		add_the_error('[disk.fbi]执行第[1]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'disk', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[2]原语 disk = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip', 'Action': '@udf', '@udf': 'SH.network_cards2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[4]原语 ip = @udf SH.network_cards2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ip.address', 'Action': 'lambda', 'lambda': 'address', 'by': 'x:str(x).replace("\\\'","").replace("[","").replace("]","").split(\'/\')[0]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[5]原语 ip.address = lambda address by (x:str(x).replace("... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'eval', 'eval': 'ip', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[6]原语 ip = eval ip by iloc[0,1] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'disk', 'Action': 'eval', 'eval': 'disk', 'by': 'iloc[0,3]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[8]原语 disk = eval disk by iloc[0,3] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b,b1', 'Action': '@udf', '@udf': 'getHostInfo.sshComment', 'with': '$ip|22|df'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[9]原语 b,b1=@udf getHostInfo.sshComment with "$ip|22|df" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'b.total', 'Action': 'str', 'str': 'total', 'by': " replace('%','' ) "}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[10]原语 b.total = str total by ( replace("%","" ) ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'total', 'Action': 'eval', 'eval': 'b', 'by': "loc[0,'total']"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[11]原语 total = eval b by loc[0,"total"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'disk', 'Action': 'add', 'add': 'disk_new', 'by': "'$total'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[12]原语 disk = add disk_new by ("$total") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'disk', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'disk'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[13]原语 store disk to ssdb by ssdb0 with disk 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'pd', 'Action': '@sdf', '@sdf': 'sys_eval', 'with': '$total>=$disk or $total>80'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[disk.fbi]执行第[14]原语 pd = @sdf sys_eval with ($total>=$disk or $total>8... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'c', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$pd, """\ndate = @sdf sys_now\ndate = @sdf format_now with ($date,"%Y-%m-%d %H:%M:%S")\ndisk = @udf udf0.new_df with (date,nowrate,thresholdrate)\ndisk = @udf disk by udf0.df_append with ($date,$total,$disk)\nstore disk to es by es7 with disk.noid\n\ncurl = @udf getHostInfo.udc with $ip|22|curl -u elastic:HW3KWy2dK5EWMwNTftAY -H "Content-Type: application/json" -XPOST http://$ip:9200/_cache/clear|root\n#curl = @udf getHostInfo.udc with 192.168.1.175|22|curl -u elastic:HW3KWy2dK5EWMwNTftAY -H "Content-Type: application/json" -XDELETE http://127.0.0.1:9200/xie3|root\n"""'}
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
		add_the_error('[disk.fbi]执行第[15]原语 c = @sdf sys_if_run with ($pd, "date = @sdf sys_no... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('curl',ptree)", 'as': 'altert', 'to': '清理成功', 'with': '未达到所设阈值,暂不清理！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[disk.fbi]执行第[25]原语 assert find_df("curl",ptree) as altert to 清理成功 wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[disk.fbi]执行第[26]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],26

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



