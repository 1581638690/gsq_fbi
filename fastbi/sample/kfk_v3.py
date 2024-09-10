#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/kfk
#datetime: 2024-08-30T16:10:57.122098
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
	
	
	ptree={'runtime': runtime, 'Action': 'define', 'define': 'kfk252', 'as': '192.168.1.251:9092'}
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[7]原语 define kfk252 as 192.168.1.251:9092 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'k', 'Action': '@udf', '@udf': 'KFK.df_link', 'with': 'kfk252'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[10]原语 k = @udf KFK.df_link with kfk252 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'topic', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_topics'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[13]原语 topic = @udf k by KFK.show_topics 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_brokers'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[16]原语 b = @udf k by KFK.show_brokers 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_version'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[19]原语 b = @udf k by KFK.show_version 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'o', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_offset', 'with': 'api_urls'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[22]原语 o = @udf k by KFK.show_offset with api_urls 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'o', 'Action': '@udf', '@udf': 'k,topic', 'by': 'KFK.show_muli_offset'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[25]原语 o = @udf k,topic by KFK.show_muli_offset 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'o', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_muli_offset', 'with': 'api_urls,api_flow,api_alert,api_user,api_ip,api_visit,api_app'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[28]原语 o = @udf k by KFK.show_muli_offset with api_urls,a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.describe', 'with': 'suricata'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[31]原语 d = @udf k by KFK.describe with suricata 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.show_partitions', 'with': 'test'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[33]原语 d = @udf k by KFK.show_partitions with test 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.create_topics', 'with': 'zichan_330001,2,1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[37]原语 c = @udf k by KFK.create_topics with zichan_330001... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'd', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.delete_topics', 'with': 'api_urls,api_flow,api_alert,api_user,api_ips,api_visit'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[41]原语 d = @udf k by KFK.delete_topics with api_urls,api_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'p', 'Action': '@udf', '@udf': 'topic', 'by': 'KFK.store', 'with': 'kfk,zichan_330001'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[44]原语 p = @udf topic by KFK.store with kfk,zichan_330001... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.fetch', 'with': 'test,g5,3000,3,True'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[47]原语 q = @udf k by KFK.fetch with test,g5,3000,3,True 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'q', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.load', 'with': 'api_urls,g5,3000,3,True'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[49]原语 q = @udf k by KFK.load with api_urls,g5,3000,3,Tru... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'c', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.list_all_cgs'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[53]原语 c = @udf k by KFK.list_all_cgs 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.get_offset_by_name', 'with': 'mq4'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[56]原语 a = @udf k by KFK.get_offset_by_name with mq4 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.desc_cgs', 'with': 'aa2'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[59]原语 b = @udf k by KFK.desc_cgs with aa2 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'k', 'by': 'KFK.fast_load', 'with': 'test,g5,3,3,True'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[64]原语 a = @udf k by KFK.fast_load with test,g5,3,3,True 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'q', 'by': 'KFK.fast_store', 'with': 'kfk2,zichan_3'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/kfk.fbi]执行第[66]原语 a=@udf q by  by KFK.fast_store with kfk2,zichan_3 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],69

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



