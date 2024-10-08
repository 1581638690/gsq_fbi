#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: lhq_sec_sql
#datetime: 2024-08-30T16:10:55.202196
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
		add_the_error('[lhq_sec_sql.fbi]执行第[15]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select url,risk_level,api_type,name,data_type from data_api_new where api_status = 1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_sec_sql.fbi]执行第[17]原语 api =  @udf RS.load_mysql_sql with (mysql1,select ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df', 'Action': '@udf', '@udf': 'api', 'by': 'mondic.mon_dic_api'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_sec_sql.fbi]执行第[18]原语 df=@udf api by mondic.mon_dic_api 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'app', 'Action': '@udf', '@udf': 'RS.load_mysql_sql', 'with': 'mysql1,select app,name from data_app_new where app_status = "1"'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_sec_sql.fbi]执行第[30]原语 app = @udf RS.load_mysql_sql with (mysql1,select a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'df1', 'Action': '@udf', '@udf': 'app', 'by': 'mondic.mon_dic_app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[lhq_sec_sql.fbi]执行第[31]原语 df1=@udf app by mondic.mon_dic_app 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[lhq_sec_sql.fbi]执行第[38]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],39

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



