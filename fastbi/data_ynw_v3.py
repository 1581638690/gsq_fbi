#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: data_ynw
#datetime: 2024-08-30T16:10:54.628509
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
		add_the_error('[data_ynw.fbi]执行第[12]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c0', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,dstip ip from data_app_new where dstip !=''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[19]原语 c0 = @udf RS.load_mysql_sql with (mysql1,select id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'c0', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[20]原语 ynw = @udf c0 by ip24.repeat  with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.app_type', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[21]原语 ynw.app_type = lambda yn by (x:1 if x==1 else 0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c0', 'Action': 'loc', 'loc': 'ynw', 'by': 'id,ip,app_type'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[23]原语 c0 = loc ynw by id,ip,app_type 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c0', 'Action': 'loc', 'loc': 'c0', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[24]原语 c0 = loc c0 by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'c0', 'as': "'ip':'dstip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[25]原语 rename c0 as ("ip":"dstip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c0', 'Action': '@udf', '@udf': 'c0', 'by': 'CRUD.save_table', 'with': 'mysql1,data_app_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[26]原语 c0 = @udf c0 by CRUD.save_table with mysql1,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynw', 'Action': 'loc', 'loc': 'ynw', 'by': 'drop', 'drop': 'app_type,yn,wd'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[27]原语 ynw = loc ynw by drop app_type,yn,wd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ynw', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_app_ynw'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[28]原语 store ynw to ssdb by ssdb0 with data_app_ynw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c0', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,dstip ip from data_api_new where dstip !=''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[30]原语 c0 = @udf RS.load_mysql_sql with (mysql1,select id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'c0', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[31]原语 ynw = @udf c0 by ip24.repeat  with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.api_yuw', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[32]原语 ynw.api_yuw = lambda yn by (x:1 if x==1 else 0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c0', 'Action': 'loc', 'loc': 'ynw', 'by': 'id,api_yuw'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[34]原语 c0 = loc ynw by id,api_yuw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c0', 'Action': 'loc', 'loc': 'c0', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[35]原语 c0 = loc c0 by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'c0', 'as': "'ip':'dstip'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[36]原语 rename c0 as ("ip":"dstip") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c0', 'Action': '@udf', '@udf': 'c0', 'by': 'CRUD.save_table', 'with': 'mysql1,data_api_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[37]原语 c0 = @udf c0 by CRUD.save_table with mysql1,data_a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c0', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': "mysql1,select id,dstip ip from data_file_server where dstip !=''"}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[39]原语 c0 = @udf RS.load_mysql_sql with (mysql1,select id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynw', 'Action': '@udf', '@udf': 'c0', 'by': 'ip24.repeat', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[40]原语 ynw = @udf c0 by ip24.repeat  with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynw.file_yuw', 'Action': 'lambda', 'lambda': 'yn', 'by': 'x:1 if x==1 else 0'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[41]原语 ynw.file_yuw = lambda yn by (x:1 if x==1 else 0) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c0', 'Action': 'loc', 'loc': 'ynw', 'by': 'id,file_yuw'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[43]原语 c0 = loc ynw by id,file_yuw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'c0', 'Action': 'loc', 'loc': 'c0', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[44]原语 c0 = loc c0 by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c0', 'Action': '@udf', '@udf': 'c0', 'by': 'CRUD.save_table', 'with': 'mysql1,data_file_server'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[45]原语 c0 = @udf c0 by CRUD.save_table with mysql1,data_f... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select a.id,b.app_type from data_api_new a join data_app_new b where a.app=b.name'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[47]原语 api= @udf RS.load_mysql_sql with (mysql1,select a.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'api', 'Action': 'loc', 'loc': 'api', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[48]原语 api = loc api by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'aa', 'Action': 'eval', 'eval': 'api', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[49]原语 aa = eval api by index.size 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$aa != 0', 'with': 'api = @udf api by CRUD.save_table with mysql1,data_api_new'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=50
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[50]原语 if $aa != 0 with "api = @udf api by CRUD.save_tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'pp', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select id,srcip ip from data_ip_new '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[52]原语 pp = @udf RS.load_mysql_sql with (mysql1,select id... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'pp', 'Action': '@udf', '@udf': 'pp', 'by': 'LBS.regionDatx', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[53]原语 pp = @udf pp by LBS.regionDatx with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'pp', 'Action': 'add', 'add': 'country', 'by': 'pp.country+pp.city'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[54]原语 pp = add country by pp.country+pp.city 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'pp', 'Action': 'loc', 'loc': 'pp', 'by': 'id,ip,country'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[55]原语 pp = loc pp by id,ip,country 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'pp', 'as': "'country':'region'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[56]原语 rename pp as ("country":"region") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ynwip', 'Action': '@udf', '@udf': 'pp', 'by': 'ip24.net_area1', 'with': 'ip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[57]原语 ynwip = @udf pp by ip24.net_area1 with ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'ynwip.yn', 'Action': 'lambda', 'lambda': 'yn', 'by': "x:'域内' if x==1 else '域外'"}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[58]原语 ynwip.yn = lambda yn by (x:"域内" if x==1 else "域外")... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'pp', 'Action': 'join', 'join': 'pp,ynwip', 'by': 'ip,ip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[59]原语 pp = join pp,ynwip by ip,ip with left 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'pp', 'Action': 'loc', 'loc': 'pp', 'by': 'id,ip,region,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[60]原语 pp = loc pp by id,ip,region,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'pp', 'Action': '@udf', '@udf': 'pp', 'by': 'udf0.df_row_lambda', 'with': 'x: x[2] if x[2]!="局域网" else x[3] '}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[61]原语 pp = @udf pp by udf0.df_row_lambda with (x: x[2] i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'pp', 'Action': 'loc', 'loc': 'pp', 'drop': 'region,yn'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[62]原语 pp = loc pp drop region,yn 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'pp', 'Action': 'loc', 'loc': 'pp', 'by': 'id', 'to': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[63]原语 pp = loc pp by id to index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'pp', 'as': "'ip':'srcip','lambda1':'region'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[64]原语 rename pp as ("ip":"srcip","lambda1":"region") 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'pp', 'Action': '@udf', '@udf': 'pp', 'by': 'CRUD.save_table', 'with': 'mysql1,data_ip_new'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[65]原语 pp = @udf pp by CRUD.save_table with mysql1,data_i... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'ynwip', 'Action': 'loc', 'loc': 'ynwip', 'by': 'drop', 'drop': 'yn,wd'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[66]原语 ynwip = loc ynwip by drop yn,wd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ynwip', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'data_ip_ynw'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[67]原语 store ynwip to ssdb by ssdb0 with data_ip_ynw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[data_ynw.fbi]执行第[68]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],68

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



