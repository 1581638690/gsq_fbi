#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: data_zdip_lable
#datetime: 2024-08-30T16:10:55.415782
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
		add_the_error('[data_zdip_lable.fbi]执行第[3]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sx', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': "select flag,dep,dep_zrr,safearea,job,zdtype,country,province,city from data_ip_new where srcip='@ip'"}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[5]原语 sx = load db by mysql1 with select flag,dep,dep_zr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ynw', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'data_ip_ynw'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[7]原语 ynw=load ssdb by ssdb0 with data_ip_ynw 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'sx1', 'Action': 'filter', 'filter': 'ynw', 'by': "ip =='@ip'"}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[8]原语 sx1 = filter ynw by ip =="@ip" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sx1', 'Action': '@udf', '@udf': 'sx1', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[9]原语 sx1 = @udf sx1 by udf0.df_zero_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'sx', 'Action': 'join', 'join': 'sx,sx1', 'by': 'index', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[10]原语 sx = join sx,sx1 by index with right 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'sx', 'as': "'flag':'标签备注','dep':'部门','dep_zrr':'责任人','job':'岗位','zdtype':'终端类型','country':'所属国家','province':'所属省份','city':'所属城市','safearea':'安全域','net1':'一类网用途','net2':'二类网用途','net3':'三类网用途'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[11]原语 rename sx as ("flag":"标签备注","dep":"部门","dep_zrr":"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'sx', 'Action': 'loc', 'loc': 'sx', 'by': 'drop', 'drop': 'ip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[12]原语 sx = loc sx by drop ip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'sx', 'Action': '@udf', '@udf': 'sx', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[13]原语 sx = @udf sx by udf0.df_fillna 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'push', 'push': 'sx', 'as': 'table'}
	try:
		push_fun(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[14]原语 push sx as table 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[data_zdip_lable.fbi]执行第[19]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],22

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



