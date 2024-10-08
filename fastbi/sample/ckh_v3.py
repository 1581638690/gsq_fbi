#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/ckh
#datetime: 2024-08-30T16:10:57.145955
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
	
	
	ptree={'runtime': runtime, 'Action': 'define', 'define': 'ckh', 'as': '192.168.1.192:19000:default:client'}
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[5]原语 define ckh as 192.168.1.192:19000:default:client 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'CREATE TABLE flow (src_ip String, dest_ip String, src_port Int32, dest_port Int32, bytes_toserver Int64, bytes_toclient Int64, flow_start DateTime64(6), flow_end DateTime64(6) ) ENGINE = MergeTree() PARTITION BY toYYYYMMDD(flow_start) order by flow_start'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[7]原语 b = load ckh by ckh with   CREATE TABLE flow (src_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'show tables'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[20]原语 c = load ckh by ckh with show tables 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select * from flow2 limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[23]原语 c = load ckh by ckh with select * from flow2 limit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'c', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select src_ip,dest_ip, count(*) as links from flow2 group by src_ip,dest_ip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[25]原语 c = load ckh by ckh with select src_ip,dest_ip, co... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'h', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select toHour(flow_start) as hour,count(*) as links from flow2 group by hour'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[28]原语 h = load ckh by ckh with select toHour(flow_start)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'h30', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "select toHour(flow_start) as hour,count(*) as links from flow2 where toDate(flow_start)>toDate('2020-05-15') and toDate(flow_start) <toDate('2020-06-15') group by hour"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[31]原语 h30 = load ckh by ckh with select toHour(flow_star... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select toYYYYMMDD(flow_start), toDate(flow_start),toWeek(flow_start) from flow2 limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[34]原语 t = load ckh by ckh with select toYYYYMMDD(flow_st... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select toYYYYMMDD(flow_start), toDate(flow_start) from flow2 where toDate(flow_start)=toDate(now()) limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[37]原语 t = load ckh by ckh with select toYYYYMMDD(flow_st... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select toYYYYMMDD(flow_start), toDate(flow_start) from flow2 where toDate(flow_start)=toDate(now())-1 limit 10'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[40]原语 t = load ckh by ckh with select toYYYYMMDD(flow_st... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 't', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': "SELECT dateDiff('hour', toDateTime('2018-01-01 22:00:00'), toDateTime('2018-01-02 23:00:00'));"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[43]原语 t = load ckh by ckh with SELECT dateDiff("hour", t... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'c', 'as': '{"src_ip":"source","dest_ip":"target","links":"value"}'}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[sample/ckh.fbi]执行第[46]原语 rename c as {"src_ip":"source","dest_ip":"target",... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],49

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



