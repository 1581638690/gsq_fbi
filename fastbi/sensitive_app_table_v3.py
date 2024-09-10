#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sensitive_app_table
#datetime: 2024-08-30T16:10:55.182882
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
		add_the_error('[sensitive_app_table.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select app from sen_http_count limit 1'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[14]原语 ccc = load ckh by ckh with select app from sen_htt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[sensitive_app_table.fbi]执行第[15]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[15]原语 assert find_df("ccc",ptree) as exit with 数据库未连接！ 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'app', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,count(*) url_count from (select app,url from sen_http_count where app != '' group by app,url) group by app"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[21]原语 app = load ckh by ckh with select app,count(*) url... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'app', 'by': 'app:str,url_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[22]原语 alter app by app:str,url_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'srcip', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,count(*) srcip_count from (select app,src_ip from sen_http_count where app != '' and src_ip != '' group by app,src_ip) group by app"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[24]原语 srcip = load ckh by ckh with select app,count(*) s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'srcip', 'by': 'app:str,srcip_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[25]原语 alter srcip by app:str,srcip_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'account', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,count(*) account_count from (select app,account from sen_http_count where app != '' and account != '' group by app,account) group by app"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[27]原语 account = load ckh by ckh with select app,count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'account', 'by': 'app:str,account_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[28]原语 alter account by app:str,account_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_data.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[32]原语 sens = load pq by sensitive/sens_data.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'app:str,url:str,src_ip:str,account:str,key:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[34]原语 alter sens by app:str,url:str,src_ip:str,account:s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'app,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[35]原语 sens = loc sens by app,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens', 'Action': 'group', 'group': 'sens', 'by': 'app,key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[36]原语 sens = group sens by app,key agg num:sum 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[37]原语 sens = @udf sens by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': "'num_sum':'num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[38]原语 rename sens as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sensitive', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select app,count(*) as sensitive_count from sen_http_count where app != '' group by app"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[40]原语 sensitive = load ckh by ckh with select app,count(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive', 'by': 'app:str,sensitive_count:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[41]原语 alter sensitive by app:str,sensitive_count:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sensitive2', 'Action': 'loc', 'loc': 'sens', 'by': 'app,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[46]原语 sensitive2 = loc sens by app,key,num 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'sensitive2', 'Action': 'order', 'order': 'sensitive2', 'by': 'num', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[47]原语 sensitive2 = order sensitive2 by num with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sensitive2', 'as': "'key':'sensitive_count','num':'s_num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[48]原语 rename sensitive2 as ("key":"sensitive_count","num... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sensitive2', 'by': 'app:str,sensitive_count:str,s_num:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[50]原语 alter sensitive2 by app:str,sensitive_count:str,s_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sensitive2', 'Action': 'add', 'add': 's_num', 'by': 'df[\'sensitive_count\'] +"("+ df[\'s_num\'] + ")"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[51]原语 sensitive2 = add s_num by  df["sensitive_count"] +... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sensitive2.s_num', 'Action': 'lambda', 'lambda': 's_num', 'by': "x: x+'，'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[52]原语 sensitive2.s_num = lambda s_num by (x: x+"，") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sensitive2', 'Action': 'group', 'group': 'sensitive2', 'by': 'app', 'agg': 's_num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[53]原语 sensitive2 = group sensitive2 by app agg s_num:sum... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sensitive2', 'Action': '@udf', '@udf': 'sensitive2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[54]原语 sensitive2 = @udf sensitive2 by udf0.df_reset_inde... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'sensitive2.s_num_sum', 'Action': 'lambda', 'lambda': 's_num_sum', 'by': 'x:x[:-1]'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[55]原语 sensitive2.s_num_sum = lambda s_num_sum by x:x[:-1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app', 'Action': 'join', 'join': 'app,srcip', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[56]原语 app = join app,srcip by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app', 'Action': 'join', 'join': 'app,account', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[58]原语 app = join app,account by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app', 'Action': 'join', 'join': 'app,sensitive', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[60]原语 app = join app,sensitive by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'app', 'Action': 'join', 'join': 'app,sensitive2', 'by': 'app,app', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[62]原语 app = join app,sensitive2 by app,app with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'app', 'by': 'udf0.df_fillna_cols', 'with': "url_count:0,srcip_count:0,account_count:0,sensitive_count:0,s_num_sum:''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[63]原语 app = @udf app by udf0.df_fillna_cols with url_cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app', 'Action': 'order', 'order': 'app', 'by': 'sensitive_count', 'with': 'desc'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[64]原语 app = order app by sensitive_count with desc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'app', 'Action': 'filter', 'filter': 'app', 'by': "s_num_sum != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[65]原语 app = filter app by s_num_sum != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'app', 'Action': 'distinct', 'distinct': 'app', 'by': 'app,url_count,srcip_count,account_count,sensitive_count,s_num_sum'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[66]原语 app = distinct app by app,url_count,srcip_count,ac... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'app', 'Action': 'loc', 'loc': 'app', 'by': 'app,url_count,srcip_count,account_count,sensitive_count,s_num_sum'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[67]原语 app = loc app by app,url_count,srcip_count,account... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'pq', 'by': 'sensitive/sensitive_app.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[70]原语 store app to pq by sensitive/sensitive_app.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'app', 'Action': 'order', 'order': 'app', 'by': 'sensitive_count', 'with': 'desc limit 10000'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[71]原语 app = order app by sensitive_count with desc limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'app', 'as': '"app":"应用","url_count":"接口数量","srcip_count":"终端数量","account_count":"账号数量","sensitive_count":"敏感数据数量","s_num_sum":"敏感数据分类数量"'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[73]原语 rename app as ("app":"应用","url_count":"接口数量","srci... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'query': 'qclear,sensitive_app,-,-'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[75]原语 b = load ssdb by ssdb0 query qclear,sensitive_app,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'app', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sensitive_app', 'as': 'Q'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[77]原语 store app to ssdb by ssdb0 with sensitive_app as Q... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[sensitive_app_table.fbi]执行第[81]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],81

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



