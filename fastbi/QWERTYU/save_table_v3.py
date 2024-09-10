#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: QWERTYU/save_table
#datetime: 2024-08-30T16:10:57.469330
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
		add_the_error('[QWERTYU/save_table.fea]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': '@data_key'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[12]原语 a = load ssdb by ssdb0 with @data_key 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'ABC.low'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[13]原语 a=@udf a by ABC.low 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'SJGL'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[14]原语 b=load ssdb by ssdb0 with SJGL 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'classtype', 'Action': 'eval', 'eval': 'a', 'by': "get_value(0,'classtype')"}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[15]原语 classtype= eval a by (get_value(0,"classtype")) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'b', 'Action': 'filter', 'filter': 'b', 'by': "classtype=='$classtype'"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[16]原语 b=filter b by classtype=="$classtype" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'c', 'Action': 'union', 'union': 'a,b'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[18]原语 c=union (a,b) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[19]原语 c=@udf c by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'c', 'by': 'ABC.judge'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[20]原语 c=@udf c by ABC.judge 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('c',ptree)", 'as': 'exit', 'with': '新增失败，已有重复规则'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[QWERTYU/save_table.fea]执行第[21]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[21]原语 assert find_df_have_data("c",ptree) as exit with 新... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sid', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': '@link,select sid +1 as sid from eventManagement order by sid desc limit 1'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[22]原语 sid = @udf RS.load_mysql_sql with (@link,select si... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'pd', 'Action': 'eval', 'eval': 'sid', 'by': 'index.size>0'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[23]原语 pd = eval sid by index.size>0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'temp2', 'Action': '@sdf', '@sdf': 'sys_if_run', 'with': '$pd,"""\nsid= eval sid by (get_value(0,\'sid\'))\n"""'}
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
		add_the_error('[QWERTYU/save_table.fea]执行第[24]原语 temp2 = @sdf sys_if_run with ($pd,"sid= eval sid b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'temp1', 'Action': '@sdf', '@sdf': 'sys_unif_run', 'with': '$pd,"""\nsid= @udf sid by udf0.df_append with (1.0)\nsid= eval sid by (get_value(0,\'sid\'))\n"""'}
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
		add_the_error('[QWERTYU/save_table.fea]执行第[27]原语 temp1= @sdf sys_unif_run with ($pd,"sid= @udf sid ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'Sid.sid', 'with': '$sid'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[31]原语 a=@udf a by Sid.sid with $sid 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'a', 'by': 'CRUD.save_table', 'with': '@link,@table'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[37]原语 b = @udf a by CRUD.save_table with (@link,@table) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('b',ptree)", 'as': 'alert', 'to': '保存成功！', 'with': '保存失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[38]原语 assert find_df("b",ptree) as  alert  to 保存成功！ with... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'id', 'Action': 'eval', 'eval': 'b', 'by': 'index[0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[41]原语 id = eval b by index[0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'CRUD.get_object_table', 'with': '@link,@table,$id'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[42]原语 d = @udf CRUD.get_object_table with (@link,@table,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'd', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[44]原语 push d as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "@link,select * from eventManagement where enable!='0'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[46]原语 b = @udf RS.load_mysql_sql with (@link,select * fr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'temp', 'Action': 'loc', 'loc': 'b', 'by': 'sid,source,destination,sport,dport,priority,gmt_modified,enable,classtype'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[47]原语 temp=loc b by sid,source,destination,sport,dport,p... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp', 'to': 'csv', 'by': 'sjgl.csv'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[48]原语 store temp to csv by sjgl.csv 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': '/opt/openfbi/fbi-bin/kill_pname.sh znsm/eve'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[50]原语 s = @udf FBI.local_cmd with /opt/openfbi/fbi-bin/k... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'znsm:logger:config'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[53]原语 a = load ssdb by ssdb0 with znsm:logger:config 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'with': 'znsm:logger:config'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[54]原语 store a to ssdb with znsm:logger:config 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'temp', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'SJGL'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[55]原语 store temp to ssdb by ssdb0 with SJGL 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.kfkconfig', 'Action': 'lambda', 'lambda': 'row', 'by': 'x: "kfk={} topic={}".format(x["kfk_addr"],x["kfk_topic"]) if x["kfk_addr"]!="" and x["kfk_topic"]!="" else ""'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[58]原语 a.kfkconfig = lambda row by  x: "kfk={} topic={}".... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.esconfig', 'Action': 'lambda', 'lambda': 'row', 'by': 'x: "es={} table={}".format(x["es_addr"],x["es_index"]) if x["es_addr"]!="" and x["es_index"]!="" else ""'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[59]原语 a.esconfig = lambda row by  x: "es={} table={}".fo... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'a.syslogconfig', 'Action': 'lambda', 'lambda': 'row', 'by': 'x: "{}={}".format(x["syslog_type"],x["syslog_addr"]) if x["syslog_addr"]!="" and x["syslog_type"]!="0" else ""'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[60]原语 a.syslogconfig = lambda row by  x: "{}={}".format(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'kfk_config', 'Action': 'eval', 'eval': 'a', 'by': 'loc[0,"kfkconfig"]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[64]原语 kfk_config = eval a by loc[0,"kfkconfig"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'es_config', 'Action': 'eval', 'eval': 'a', 'by': 'loc[0,"esconfig"]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[65]原语 es_config = eval a by loc[0,"esconfig"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'syslog_config', 'Action': 'eval', 'eval': 'a', 'by': 'loc[0,"syslogconfig"]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[66]原语 syslog_config = eval a by loc[0,"syslogconfig"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': '/opt/openfbi/fbi-bin/addones/json_out.py files=/data/znsm/eve* $kfk_config $es_config $syslog_config -D'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[68]原语 s = @udf FBI.local_cmd with /opt/openfbi/fbi-bin/a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('s',ptree)", 'as': 'altert', 'to': '保存成功', 'with': '保存失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[71]原语 assert find_df("s",ptree) as altert to 保存成功 with 保... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[QWERTYU/save_table.fea]执行第[73]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],73

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



