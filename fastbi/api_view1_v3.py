#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_view1
#datetime: 2024-08-30T16:10:55.288433
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
		add_the_error('[api_view1.fbi]执行第[9]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'add_ip', 'Action': 'load', 'load': 'ckh', 'by': 'ckh', 'with': 'select srcip,dstip,count(*) as num from api_abroad group by srcip,dstip'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[11]原语 add_ip = load ckh by ckh with select srcip,dstip,c... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'add_ip', 'by': 'srcip:str,dstip:str,num:int'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[12]原语 alter add_ip by srcip:str,dstip:str,num:int 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': 'add_ip.index.size == 0', 'with': '""\naa = @udf udf0.new_df with world,longitude,dimension,value,china1,longitude1,dimension1\nstore aa to ssdb by ssdb0 with add_ip:view\n""'}
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=13
		ptree['funs']=block_if_13
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[13]原语 if add_ip.index.size == 0 with "aa = @udf udf0.new... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'assert', 'assert': "find_df_have_data('add_ip',ptree)", 'as': 'exit', 'with': '境外访问告警未开启！'}
	try:
		ret,err = assert_fun(ptree,errors,True)
		if ret==False: 
			add_the_error('[api_view1.fbi]执行第[17]原语 assert find_df_have_data(... 断言失败, '+err)

			return errors,-1
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[17]原语 assert find_df_have_data("add_ip",ptree) as exit w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'src_ip', 'Action': 'loc', 'loc': 'add_ip', 'by': 'srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[20]原语 src_ip = loc add_ip by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'src_ip', 'Action': 'distinct', 'distinct': 'src_ip', 'by': 'srcip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[21]原语 src_ip = distinct src_ip by srcip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'src_country', 'Action': '@udf', '@udf': 'src_ip', 'by': 'LBS.regionDatx', 'with': 'srcip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[22]原语 src_country = @udf src_ip by LBS.regionDatx with s... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'src_country', 'Action': 'filter', 'filter': 'src_country', 'by': "latitude != '' and longitude != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[23]原语 src_country = filter src_country by latitude != ""... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'src_country', 'Action': 'loc', 'loc': 'src_country', 'by': 'srcip,country,latitude,longitude'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[24]原语 src_country = loc src_country by srcip,country,lat... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'src_country', 'as': "'country':'world','latitude':'dimension','longitude':'longitude'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[25]原语 rename src_country as ("country":"world","latitude... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dst_ip', 'Action': 'loc', 'loc': 'add_ip', 'by': 'dstip'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[27]原语 dst_ip = loc add_ip by dstip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= distinct', 'Ta': 'dst_ip', 'Action': 'distinct', 'distinct': 'dst_ip', 'by': 'dstip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[28]原语 dst_ip = distinct dst_ip by dstip 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dst_country', 'Action': '@udf', '@udf': 'dst_ip', 'by': 'LBS.regionDatx', 'with': 'dstip'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[29]原语 dst_country = @udf dst_ip by LBS.regionDatx with d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dst_country', 'Action': 'loc', 'loc': 'dst_country', 'by': 'dstip,country,province,city,latitude,longitude'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[30]原语 dst_country = loc dst_country by dstip,country,pro... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dst_country', 'Action': 'loc', 'loc': 'dst_country', 'by': 'index', 'to': 'id'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[31]原语 dst_country = loc dst_country by index to id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dst1_country', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'id,dstip,country,province,city,latitude,longitude'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[32]原语 dst1_country = @udf udf0.new_df with id,dstip,coun... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'foreach', 'foreach': 'dst_country', 'with': 'id = $1', 'run': '""\naa = filter dst_country by id == @id\naa = loc aa by id,dstip,country,province,city,latitude,longitude\nprov = eval aa by iloc[0,2]\naa.province = lambda province by (x:x if x != \'$prov\' else \'\')\ndst1_country = union dst1_country,aa\n""'}
	try:
		ptree['lineno']=34
		ptree['funs']=block_foreach_34
		foreach_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			del global_tasks[t.ident]['Break']
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[34]原语 foreach dst_country run "aa = filter dst_country b... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'cc'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[42]原语 bb = @udf udf0.new_df with cc 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'udf0.df_append', 'with': '中国浙江杭州'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[43]原语 bb = @udf bb by udf0.df_append with 中国浙江杭州 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'bb', 'Action': '@udf', '@udf': 'bb', 'by': 'LBS.geocoder', 'with': 'cc,cc'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[44]原语 bb = @udf bb by LBS.geocoder with (cc,cc) 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dst1_country_1', 'Action': 'filter', 'filter': 'dst1_country', 'by': "country == '局域网'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[45]原语 dst1_country_1 = filter dst1_country by country ==... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'dst1_country_1', 'Action': '@udf', '@udf': 'dst1_country_1', 'by': 'udf0.df_replace', 'with': '局域网,中国浙江杭州'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[46]原语 dst1_country_1 = @udf dst1_country_1 by udf0.df_re... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'dst1_country_1', 'Action': 'join', 'join': 'dst1_country_1,bb', 'by': 'country,城市', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[47]原语 dst1_country_1 = join dst1_country_1,bb by country... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dst1_country_1', 'Action': 'loc', 'loc': 'dst1_country_1', 'by': 'country,dstip,longitude,latitude'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[48]原语 dst1_country_1 = loc dst1_country_1 by country,dst... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dst1_country_1', 'as': "'country':'china1','longitude':'longitude1','latitude':'dimension1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[49]原语 rename dst1_country_1 as ("country":"china1","long... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'dst1_country_2', 'Action': 'filter', 'filter': 'dst1_country', 'by': "country != '局域网'"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[50]原语 dst1_country_2 = filter dst1_country by country !=... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'dst1_country_2', 'Action': 'add', 'add': 'china1', 'by': "dst1_country_2['country']+dst1_country_2['province']+dst1_country_2['city']"}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[51]原语 dst1_country_2 = add china1 by dst1_country_2["cou... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'dst1_country_2', 'Action': 'loc', 'loc': 'dst1_country_2', 'by': 'dstip,china1,latitude,longitude'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[52]原语 dst1_country_2 = loc dst1_country_2 by dstip,china... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'rename', 'rename': 'dst1_country_2', 'as': "'longitude':'longitude1','latitude':'dimension1'"}
	try:
		rename_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[53]原语 rename dst1_country_2 as ("longitude":"longitude1"... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'dst1_country', 'Action': 'union', 'union': 'dst1_country_1,dst1_country_2'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[54]原语 dst1_country = union dst1_country_1,dst1_country_2... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'add_ip_sd', 'Action': 'join', 'join': 'add_ip,src_country', 'by': 'srcip,srcip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[56]原语 add_ip_sd = join add_ip,src_country by srcip,srcip... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'add_ip_sd', 'Action': 'join', 'join': 'add_ip_sd,dst1_country', 'by': 'dstip,dstip', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[57]原语 add_ip_sd = join add_ip_sd,dst1_country by dstip,d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'add_ip_sd', 'Action': 'loc', 'loc': 'add_ip_sd', 'by': 'world,longitude,dimension,num,china1,longitude1,dimension1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[58]原语 add_ip_sd = loc add_ip_sd by world,longitude,dimen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'add_ip_sd', 'by': 'longitude:str,dimension:str,longitude1:str,dimension1:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[59]原语 alter add_ip_sd by longitude:str,dimension:str,lon... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= group', 'Ta': 'add_ip_sd', 'Action': 'group', 'group': 'add_ip_sd', 'by': 'world,longitude,dimension,china1,longitude1,dimension1', 'agg': 'num:sum'}
	try:
		group_by(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[60]原语 add_ip_sd = group add_ip_sd by world,longitude,dim... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'add_ip_sd', 'Action': '@udf', '@udf': 'add_ip_sd', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[61]原语 add_ip_sd = @udf add_ip_sd by udf0.df_reset_index 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'add_ip_sd', 'Action': 'filter', 'filter': 'add_ip_sd', 'by': "longitude != '' and longitude1 != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[62]原语 add_ip_sd = filter add_ip_sd by longitude != "" an... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= order', 'Ta': 'add_ip_sd', 'Action': 'order', 'order': 'add_ip_sd', 'by': 'num_sum', 'with': 'desc limit 200'}
	try:
		order_by(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[63]原语 add_ip_sd = order add_ip_sd by num_sum with desc l... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'alter', 'alter': 'add_ip_sd', 'by': 'num_sum:str'}
	try:
		alter_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[64]原语 alter add_ip_sd by num_sum:str 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'add_ip_sd', 'Action': 'add', 'add': 'value', 'by': 'add_ip_sd[\'world\']+"访问"+add_ip_sd[\'china1\']+add_ip_sd["num_sum"]+"次"'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[65]原语 add_ip_sd = add value by (add_ip_sd["world"]+"访问"+... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'add_ip_sd', 'Action': 'loc', 'loc': 'add_ip_sd', 'by': 'world,longitude,dimension,value,china1,longitude1,dimension1'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[66]原语 add_ip_sd = loc add_ip_sd by world,longitude,dimen... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'add_ip_sd', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'add_ip:view'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[67]原语 store add_ip_sd to ssdb by ssdb0 with add_ip:view 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_view1.fbi]执行第[70]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],70

#主函数结束,开始块函数

def block_if_13(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'aa', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'world,longitude,dimension,value,china1,longitude1,dimension1'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第13行if语句中]执行第[14]原语 aa = @udf udf0.new_df with world,longitude,dimensi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'aa', 'to': 'ssdb', 'by': 'ssdb0', 'with': 'add_ip:view'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[第13行if语句中]执行第[15]原语 store aa to ssdb by ssdb0 with add_ip:view 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_if_13

def block_foreach_34(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= filter', 'Ta': 'aa', 'Action': 'filter', 'filter': 'dst_country', 'by': 'id == @id'}
	ptree['by'] = replace_ps(ptree['by'],runtime)
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第34行foreach语句中]执行第[35]原语 aa = filter dst_country by id == @id 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= loc', 'Ta': 'aa', 'Action': 'loc', 'loc': 'aa', 'by': 'id,dstip,country,province,city,latitude,longitude'}
	try:
		loc_data(ptree)
	except Exception as e:
		add_the_error('[第34行foreach语句中]执行第[36]原语 aa = loc aa by id,dstip,country,province,city,lati... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'prov', 'Action': 'eval', 'eval': 'aa', 'by': 'iloc[0,2]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[第34行foreach语句中]执行第[37]原语 prov = eval aa by iloc[0,2] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= lambda', 'Ta': 'aa.province', 'Action': 'lambda', 'lambda': 'province', 'by': "x:x if x != '$prov' else ''"}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		lambda_col(ptree)
	except Exception as e:
		add_the_error('[第34行foreach语句中]执行第[38]原语 aa.province = lambda province by (x:x if x != "$pr... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'dst1_country', 'Action': 'union', 'union': 'dst1_country,aa'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第34行foreach语句中]执行第[39]原语 dst1_country = union dst1_country,aa 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

#end block_foreach_34

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



