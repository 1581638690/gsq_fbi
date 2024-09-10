#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: archives
#datetime: 2024-08-30T16:10:54.213434
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
		add_the_error('[archives.fbi]执行第[4]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[archives.fbi]执行第[5]原语 date = @sdf sys_now 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'date', 'Action': '@sdf', '@sdf': 'format_now', 'with': '$date,"%Y-%m-%d %H:%M:%S"'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[archives.fbi]执行第[8]原语 date = @sdf format_now with ($date,"%Y-%m-%d %H:%M... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sql_df'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[10]原语 a = load ssdb by ssdb0 with sql_df 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.sql', 'Action': 'str', 'str': 'sql', 'by': " replace('select','scan' ) "}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[11]原语 a.sql = str sql by ( replace("select","scan" ) ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'a.sql', 'Action': 'str', 'str': 'sql', 'by': " replace('limit 100','' ) "}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[12]原语 a.sql = str sql by ( replace("limit 100","" ) ) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sql_str', 'Action': 'eval', 'eval': 'a', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[13]原语 sql_str= eval a by (iloc[0,0]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'es7', 'Action': 'load', 'load': 'es', 'by': 'es7', 'with': '$sql_str with size=20000000'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[14]原语 es7 = load es by es7 with ($sql_str with size=2000... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'es7', 'to': 'csv', 'by': '事件日志_$date.csv'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[15]原语 store es7 to csv by 事件日志_$date.csv 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'RS.mv_file', 'with': '事件日志_$date.csv,csv/事件日志_$date.csv'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[16]原语 @udf RS.mv_file with (事件日志_$date.csv,csv/事件日志_$dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ip', 'Action': '@udf', '@udf': 'SH.network_cards2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[17]原语 ip = @udf SH.network_cards2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ip', 'Action': 'eval', 'eval': 'ip', 'by': 'iloc[0,1]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[18]原语 ip= eval ip by (iloc[0,1]) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'getHostInfo.udc', 'with': "127.0.0.1|22|gzip /opt/openfbi/workspace/csv/'事件日志_$date.csv'|root"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[19]原语 b = @udf getHostInfo.udc with 127.0.0.1|22|gzip /o... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[20]原语 bb = @udf udf0.new_df with (file) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb1', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'file,gmt_create'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[21]原语 bb1 = @udf udf0.new_df with (file,gmt_create) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb1', 'Action': '@udf', '@udf': 'bb1', 'by': 'udf0.df_append', 'with': '事件日志_$date.csv.gz,$date'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[22]原语 bb1 = @udf bb1 by udf0.df_append with (事件日志_$date.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb1', 'Action': '@udf', '@udf': 'bb1', 'by': 'RS.store_mysql', 'with': 'mysql41,csv'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[23]原语 bb1 = @udf bb1 by RS.store_mysql with (mysql41,csv... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb2', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': 'csv/事件日志_$date.csv.gz'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[24]原语 bb2 = @udf bb by udf0.df_append with (csv/事件日志_$da... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'bb2', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'pot_bb3:@FPS', 'as': '600'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[26]原语 store bb2 to ssdb by ssdb0 with pot_bb3:@FPS as 60... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'RS.exec_mysql_sql', 'with': 'mysql41,select * from csv order by gmt_create desc'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[29]原语 a = @udf RS.exec_mysql_sql with (mysql41,select * ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'a', 'by': 'udf0.df_set_index', 'with': 'file'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[30]原语 a = @udf a by udf0.df_set_index with (file) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'a', 'Action': 'add', 'add': 'value', 'by': 'a.index'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[31]原语 a = add value by (a.index) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'a', 'Action': 'loc', 'loc': 'a', 'by': 'value'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[32]原语 a = loc a by value 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'a', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'dd:docx'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[33]原语 store a to ssdb by ssdb0 with dd:docx 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[archives.fbi]执行第[35]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],36

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



