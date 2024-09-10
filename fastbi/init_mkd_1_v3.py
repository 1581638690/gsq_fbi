#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: init_mkd_1
#datetime: 2024-08-30T16:10:55.470384
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
	
	
	ptree={'runtime': runtime, 'Action': 'cleartimer', 'cleartimer': '图谱'}
	try:
		clear_timer(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[7]原语 cleartimer 图谱 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo rm -rf /data/mkd.db/'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[10]原语 a = @udf FBI.local_cmd with sudo rm -rf /data/mkd.... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'FBI.local_cmd', 'with': 'sudo /home/zhds/alds/bin/init_mkd.sh'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[14]原语 a = @udf FBI.local_cmd with sudo /home/zhds/alds/b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'a', 'Action': '@udf', '@udf': 'GL.init_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[17]原语 a = @udf GL.init_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'ret', 'Action': '@udf', '@udf': 'GL.start_http_mkd'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[20]原语 ret = @udf GL.start_http_mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[22]原语 aa = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_agent'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[25]原语 store aa to ssdb by ssdb0 with link_agent 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'link_data', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate link_data'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[28]原语 link_data = load ckh by ckh with truncate link_dat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/url_name.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[30]原语 bb = @udf ZFile.rm_file with link/url_name.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_type.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[32]原语 bb = @udf ZFile.rm_file with link/link_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_http_acc.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[34]原语 bb = @udf ZFile.rm_file with link/link_http_acc.pq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_http1_acc.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[36]原语 bb = @udf ZFile.rm_file with link/link_http1_acc.p... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/link_sql_user.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[38]原语 bb = @udf ZFile.rm_file with link/link_sql_user.pq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/S_O_count.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[40]原语 bb = @udf ZFile.rm_file with link/S_O_count.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'time'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[42]原语 aa = @udf udf0.new_df with time 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'link_xff'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[43]原语 store aa to ssdb by ssdb0 with link_xff 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'link_xff', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate link_xff'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[45]原语 link_xff = load ckh by ckh with truncate link_xff 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/ip_type.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[47]原语 bb = @udf ZFile.rm_file with link/ip_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/S_O_xff_count.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[49]原语 bb = @udf ZFile.rm_file with link/S_O_xff_count.pq... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ldgz', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate ldgz'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[52]原语 ldgz = load ckh by ckh with truncate ldgz 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'mkd', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'truncate mkd'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[53]原语 mkd = load ckh by ckh with truncate mkd 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'ZFile.rm_file', 'with': 'link/ldgz_type.pq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[55]原语 bb = @udf ZFile.rm_file with link/ldgz_type.pq 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'run', 'run': 'ldgz/zc_gx_pic_other.fbi'}
	try:
		from avenger.fbicommand import run_script_prmtv 
		run_name,e_cnt,e_err = run_script_prmtv(ptree,'run {}'.format(ptree['run']))
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[57]原语 run ldgz/zc_gx_pic_other.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'settimer', 'settimer': '图谱', 'by': '0 */10 * * * *', 'run': 'tupu.fbi'}
	try:
		set_timer(ptree)
	except Exception as e:
		add_the_error('[init_mkd_1.fbi]执行第[60]原语 settimer 图谱 by "0 */10 * * * *" run tupu.fbi 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],60

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



