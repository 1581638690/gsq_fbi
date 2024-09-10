#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/mkd
#datetime: 2024-08-30T16:10:57.186457
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
	
	
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'GL.init_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[12]原语 a = @udf GL.init_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'csv', 'by': 'ldgz.csv'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[16]原语 data = load csv by ldgz.csv 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'data', 'as': '{"A":"S","B":"O","C":"P"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[19]原语 rename data as {"A":"S","B":"O","C":"P"} 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'count', 'Action': '@udf', '@udf': 'data', 'by': 'GL.load_to_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[22]原语 count = @udf data by  GL.load_to_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'GL.start_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[29]原语 ret = @udf GL.start_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'all', 'Action': '@udf', '@udf': 'GL.query_http_mkd', 'with': 'g.M().Out("192.168.1.86")'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[32]原语 all = @udf GL.query_http_mkd with g.M().Out("192.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'all', 'Action': '@udf', '@udf': 'GL.query_http_mkd', 'with': 'g.V("192.168.1.86").Out().All()'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[35]原语 all = @udf GL.query_http_mkd with g.V("192.168.1.8... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @sdf', 'Ta': 'link', 'Action': '@sdf', '@sdf': 'sys_define', 'with': 'http:// 192.168.90.103:2345'}
	try:
		ret = sdf_func(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[39]原语 link = @sdf sys_define with http:// 192.168.90.103... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'server', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'host'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[40]原语 server = @udf  udf0.new_df with host 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'server', 'Action': '@udf', '@udf': 'server', 'by': 'udf0.df_append', 'with': '192.168.90.103:2345'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[41]原语 server= @udf server by udf0.df_append with 192.168... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'server', 'by': 'GL.start_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[42]原语 ret = @udf server by  GL.start_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'all', 'Action': '@udf', '@udf': 'server', 'by': 'GL.query_http_mkd', 'with': 'g.M().Out("192.168.1.86")'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[45]原语 all = @udf server by GL.query_http_mkd with g.M().... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'all', 'Action': '@udf', '@udf': 'server', 'by': 'GL.query_http_mkd', 'with': 'g.V("192.168.1.86").Out().All()'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[48]原语 all = @udf server by GL.query_http_mkd with g.V("1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd2', 'Action': 'limit', 'limit': 'data', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[53]原语 d2 = limit data by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'd2', 'by': 'GL.add_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[54]原语 ret = @udf d2 by  GL.add_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'd2', 'by': 'GL.add_http_mkd', 'with': 'http://192.168.90.103:2345'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[55]原语 ret = @udf d2 by  GL.add_http_mkd  with http://192... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'd2', 'Action': 'limit', 'limit': 'data', 'by': '10'}
	try:
		limit_fun(ptree)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[58]原语 d2 = limit data by 10 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'd2', 'by': 'GL.del_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[59]原语 ret = @udf d2 by  GL.del_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'd2', 'by': 'GL.del_http_mkd', 'with': '$link'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/mkd.fbi]执行第[60]原语 ret = @udf d2 by  GL.del_http_mkd  with $link 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],63

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



