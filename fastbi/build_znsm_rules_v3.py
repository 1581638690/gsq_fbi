#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: build_znsm_rules
#datetime: 2024-08-30T16:10:54.794379
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
		add_the_error('[build_znsm_rules.fbi]执行第[3]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_rules', 'Action': '@udf', '@udf': 'CRUD.load_s3_sql', 'with': 'rules.db, select * from a1 union all select * from c1 union all select * from f1 union all select * from m1 union all select * from n1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[5]原语 df_rules = @udf CRUD.load_s3_sql with rules.db, se... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_rules_mining', 'Action': '@udf', '@udf': 'CRUD.load_s3_sql', 'with': 'rules.db, select * from mining_info'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[6]原语 df_rules_mining = @udf CRUD.load_s3_sql with rules... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df_rules_mining1', 'Action': 'filter', 'filter': 'df_rules_mining', 'by': 'classtype=="矿池正则RUL"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[8]原语 df_rules_mining1 = filter df_rules_mining by class... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df_rules_mining1', 'Action': 'add', 'add': 'option', 'by': '\'pcre:"\'+df_rules_mining1[\'option\']+\'"; metadata:created_at \'+df_rules_mining1[\'created\']+\', updated_at \'+df_rules_mining1[\'modified\']+\';\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[9]原语 df_rules_mining1 = add option by ("pcre:""+df_rule... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_rules_mining1', 'Action': 'loc', 'loc': 'df_rules_mining1', 'by': 'drop', 'drop': 'created,modified'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[10]原语 df_rules_mining1 = loc df_rules_mining1 by drop cr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df_rules_mining2', 'Action': 'filter', 'filter': 'df_rules_mining', 'by': 'classtype=="矿池URL"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[12]原语 df_rules_mining2 = filter df_rules_mining by class... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'df_rules_mining2', 'Action': 'add', 'add': 'option', 'by': '\'content:"\'+df_rules_mining2[\'option\']+\'"; metadata:created_at \'+df_rules_mining2[\'created\']+\', updated_at \'+df_rules_mining2[\'modified\']+\';\''}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[13]原语 df_rules_mining2 = add option by ("content:""+df_r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_rules_mining2', 'Action': 'loc', 'loc': 'df_rules_mining2', 'by': 'drop', 'drop': 'created,modified'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[14]原语 df_rules_mining2 = loc df_rules_mining2 by drop cr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_rules', 'Action': 'union', 'union': 'df_rules,df_rules_mining1'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[16]原语 df_rules = union df_rules,df_rules_mining1 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'df_rules', 'Action': 'union', 'union': 'df_rules,df_rules_mining2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[17]原语 df_rules = union df_rules,df_rules_mining2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_rules', 'Action': '@udf', '@udf': 'df_rules', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[18]原语 df_rules = @udf df_rules by udf0.df_fillna with ()... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'df_classtype', 'Action': 'group', 'group': 'df_rules', 'by': 'classtype', 'agg': 'classtype:count'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[21]原语 df_classtype = group df_rules by classtype agg cla... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'df_classtype', 'Action': 'loc', 'loc': 'df_classtype', 'by': 'index', 'to': 'classtype'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[22]原语 df_classtype = loc df_classtype by index to classt... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_classtype', 'Action': '@udf', '@udf': 'df_classtype', 'by': 'udf0.df_fillna', 'with': ''}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[23]原语 df_classtype = @udf df_classtype by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df_classtype', 'Action': 'filter', 'filter': 'df_classtype', 'by': "classtype!=''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[24]原语 df_classtype = filter df_classtype by classtype!="... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx1', 'Action': '@udf', '@udf': 'ZNSM_dyllan.clear_file', 'with': '/opt/znsm/conf/cfg/classification.config'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[26]原语 xx1 = @udf ZNSM_dyllan.clear_file with /opt/znsm/c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx2', 'Action': '@udf', '@udf': 'df_classtype', 'by': 'ZNSM_dyllan.build_classType_file_v1', 'with': '/opt/znsm/conf/cfg/classification.config'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[28]原语 xx2 = @udf df_classtype by ZNSM_dyllan.build_class... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_rules', 'Action': '@udf', '@udf': 'df_rules', 'by': 'ZNSM_dyllan.change_column_to_md5', 'with': 'classtype'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[32]原语 df_rules = @udf df_rules by ZNSM_dyllan.change_col... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df_rules.classtype', 'Action': 'lambda', 'lambda': 'classtype', 'by': 'x:"zhcs"+x'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[33]原语 df_rules.classtype = lambda classtype by (x:"zhcs"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx3', 'Action': '@udf', '@udf': 'ZNSM_dyllan.clear_file', 'with': '/opt/znsm/rules/znsm.rules'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[36]原语 xx3 = @udf ZNSM_dyllan.clear_file with /opt/znsm/r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx4', 'Action': '@udf', '@udf': 'df_rules', 'by': 'ZNSM.build_rules_file_v1', 'with': '/opt/znsm/rules/znsm.rules'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[38]原语 xx4 = @udf df_rules by ZNSM.build_rules_file_v1 wi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df_rules_mining3', 'Action': 'filter', 'filter': 'df_rules_mining', 'by': 'classtype=="矿池IP"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[41]原语 df_rules_mining3 = filter df_rules_mining by class... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'df_rules_mining3.option', 'Action': 'lambda', 'lambda': 'option', 'by': 'x:str(x)+",2,80"'}
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[42]原语 df_rules_mining3.option = lambda option by (x:str(... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx', 'Action': '@udf', '@udf': 'ZNSM_dyllan.clear_file', 'with': '/opt/znsm/iprep/mining_ip.csv'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[43]原语 xx = @udf ZNSM_dyllan.clear_file with /opt/znsm/ip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx', 'Action': '@udf', '@udf': 'df_rules_mining3', 'by': 'ZNSM_dyllan.build_column_to_file', 'with': '/opt/znsm/iprep/mining_ip.csv,option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[44]原语 xx = @udf df_rules_mining3 by ZNSM_dyllan.build_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df_rules_mining4', 'Action': 'filter', 'filter': 'df_rules_mining', 'by': 'classtype=="矿池域名"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[47]原语 df_rules_mining4 = filter df_rules_mining by class... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df_rules_mining4', 'Action': '@udf', '@udf': 'df_rules_mining4', 'by': 'ZNSM_dyllan.change_column_to_md5', 'with': 'option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[48]原语 df_rules_mining4 = @udf df_rules_mining4 by ZNSM_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx', 'Action': '@udf', '@udf': 'ZNSM_dyllan.clear_file', 'with': '/opt/znsm/rules/mining_domain.list'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[49]原语 xx = @udf ZNSM_dyllan.clear_file with /opt/znsm/ru... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx', 'Action': '@udf', '@udf': 'df_rules_mining4', 'by': 'ZNSM_dyllan.build_column_to_file', 'with': '/opt/znsm/rules/mining_domain.list,option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[50]原语 xx = @udf df_rules_mining4 by ZNSM_dyllan.build_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'df_rules_mining5', 'Action': 'filter', 'filter': 'df_rules_mining', 'by': 'classtype=="挖矿文件"'}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[53]原语 df_rules_mining5 = filter df_rules_mining by class... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx', 'Action': '@udf', '@udf': 'ZNSM_dyllan.clear_file', 'with': '/opt/znsm/rules/md5_minerd.list'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[54]原语 xx = @udf ZNSM_dyllan.clear_file with /opt/znsm/ru... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'xx', 'Action': '@udf', '@udf': 'df_rules_mining5', 'by': 'ZNSM_dyllan.build_column_to_file', 'with': '/opt/znsm/rules/md5_minerd.list,option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[55]原语 xx = @udf df_rules_mining5 by ZNSM_dyllan.build_co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': '/opt/znsm/bin/reload_rule_live.sh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[59]原语 c = @udf FBI.local_cmd with /opt/znsm/bin/reload_r... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': 'c', 'by': 'df.index.size >=1', 'as': 'notice', 'to': '更新规则,重启成功！', 'with': '更新规则,重启失败！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[61]原语 assert c by df.index.size >=1 as notice  to 更新规则,重... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[build_znsm_rules.fbi]执行第[62]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],62

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



