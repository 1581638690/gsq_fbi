#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sens_dbms
#datetime: 2024-08-30T16:10:55.267729
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
		add_the_error('[sens_dbms.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'sens_dbms'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[12]原语 aa = load ssdb by ssdb0 with sens_dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'a_num', 'Action': 'eval', 'eval': 'aa', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[14]原语 a_num = eval aa by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$a_num == 0', 'with': 'aa = load ckh by ckh with select min(timestamp) as time from dbms_sendata'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=15
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[15]原语 if $a_num == 0 with aa = load ckh by ckh with sele... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time1', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[17]原语 time1 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select max(timestamp) as time from dbms_sendata'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[19]原语 aa = load ckh by ckh with select max(timestamp) as... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'time2', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[20]原语 time2 = eval aa by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ccc', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select dest_ip from dbms_sendata where timestamp >= '$time1' and timestamp < '$time2' limit 1"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[23]原语 ccc = load ckh by ckh with select dest_ip from dbm... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df('ccc',ptree)", 'as': 'exit', 'with': '无数据更新 或者 数据库未连接！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[sens_dbms.fbi]执行第[24]原语 assert find_df("ccc",ptre... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[24]原语 assert find_df("ccc",ptree) as exit with 无数据更新 或者 ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'sens_dbms'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[26]原语 store aa to ssdb by ssdb0 with sens_dbms 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select dest_ip,dest_port,db,db_type,user,res_count,count(*) num from dbms_sendata where timestamp >= '$time1' and timestamp < '$time2' group by dest_ip,dest_port,user,res_count,db,db_type"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[30]原语 sens = load ckh by ckh with select dest_ip,dest_po... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'dest_ip:str,dest_port:int,user:str,db:str,db_type:str,res_count:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[31]原语 alter sens by dest_ip:str,dest_port:int,user:str,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "res_count != '' and res_count != 'null' and res_count != '{}' and res_count != 'None'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[32]原语 sens = filter sens by res_count != "" and res_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens.res_count', 'Action': 'str', 'str': 'res_count', 'by': "replace(' ','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[33]原语 sens.res_count = str res_count by replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': 'res_count unlike name'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[34]原语 sens = filter sens by res_count unlike name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_d2df', 'with': 'res_count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[35]原语 sens = @udf sens by udf0.df_d2df with res_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'num:int,value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[36]原语 alter sens by num:int,value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'num', 'by': 'df["num"] * df["value"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[37]原语 sens = add num by df["num"] * df["value"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'total_type', 'by': "'Msg值'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[38]原语 sens = add total_type by ("Msg值") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens1', 'Action': 'loc', 'loc': 'sens', 'by': 'dest_ip,dest_port,db,db_type,user,total_type,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[39]原语 sens1 = loc sens by dest_ip,dest_port,db,db_type,u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sens', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select dest_ip,dest_port,db,db_type,user,req_count,count(*) num from dbms_sendata where timestamp >= '$time1' and timestamp < '$time2' group by dest_ip,dest_port,user,req_count,db,db_type"}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[41]原语 sens = load ckh by ckh with select dest_ip,dest_po... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'dest_ip:str,dest_port:int,user:str,db:str,db_type:str,req_count:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[42]原语 alter sens by dest_ip:str,dest_port:int,user:str,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': "req_count != '' and req_count != 'null' and req_count != '{}' and req_count != 'None'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[43]原语 sens = filter sens by req_count != "" and req_coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= str', 'Ta': 'sens.req_count', 'Action': 'str', 'str': 'req_count', 'by': "replace(' ','')"}
	try:
		str_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[44]原语 sens.req_count = str req_count by replace(" ","") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sens', 'Action': 'filter', 'filter': 'sens', 'by': 'req_count unlike name'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[45]原语 sens = filter sens by req_count unlike name 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_d2df', 'with': 'req_count'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[46]原语 sens = @udf sens by udf0.df_d2df with req_count 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sens', 'by': 'num:int,value:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[47]原语 alter sens by num:int,value:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'num', 'by': 'df["num"] * df["value"]'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[48]原语 sens = add num by df["num"] * df["value"] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'sens', 'Action': 'add', 'add': 'total_type', 'by': "'Sql语句'"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[49]原语 sens = add total_type by ("Sql语句") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens2', 'Action': 'loc', 'loc': 'sens', 'by': 'dest_ip,dest_port,db,db_type,user,total_type,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[50]原语 sens2 = loc sens by dest_ip,dest_port,db,db_type,u... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sens', 'Action': 'union', 'union': 'sens1,sens2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[52]原语 sens = union sens1,sens2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sss', 'Action': 'load', 'load': 'pq', 'by': 'sensitive/sens_dbms.pq'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[54]原语 sss = load pq by sensitive/sens_dbms.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'sss.num', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[55]原语 alter sss.num as int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'sens', 'Action': 'union', 'union': 'sens,sss'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[56]原语 sens = union sens,sss 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'sens', 'Action': 'group', 'group': 'sens', 'by': 'dest_ip,dest_port,db,db_type,user,total_type,key', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[57]原语 sens = group sens by dest_ip,dest_port,db,db_type,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sens', 'Action': '@udf', '@udf': 'sens', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[58]原语 sens = @udf sens by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sens', 'as': "'num_sum':'num'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[59]原语 rename sens as ("num_sum":"num") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sens', 'Action': 'loc', 'loc': 'sens', 'by': 'dest_ip,dest_port,db,db_type,user,total_type,key,num'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[60]原语 sens = loc sens by dest_ip,dest_port,db,db_type,us... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'sens', 'to': 'pq', 'by': 'sensitive/sens_dbms.pq'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[61]原语 store sens to pq by sensitive/sens_dbms.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[sens_dbms.fbi]执行第[65]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],65

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



