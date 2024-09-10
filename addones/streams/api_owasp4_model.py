#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_owasp4_model.xlk
#datetime: 2024-08-30T16:10:58.490183
#copyright: OpenFBI

import sys 
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/pylibs")
sys.path.append("../")
import json
from . import *
import threading
try:
	import numpy as np 
	import  pandas as pd
	from avenger.fbiprocesser import *
	from avenger.fglobals import *

except:
	pass



#流和批共享的函数：

#数组到DF
def push_arrays_to_df(arrays,name=""):
	if len(arrays)==0:
		return 0
		
	try:
		#lockP.acquire()
		b  = arrays.copy()
		del arrays[0:len(b)]
		#arrays.clear()
		#lockP.release()

		df = pd.DataFrame(b)
		#设置index 为0
		df['seq19821221'] = 0
		df.set_index('seq19821221',inplace=True)
		if fbi_global.runtime.is_have(name):
			o = fbi_global.runtime.get(name)
			dfs=[o.df,df]
			dfz = pd.concat(dfs,sort=True)
			o.df = dfz
		else:
			o = FbiTable(name,df)
			fbi_global.runtime.put(o)
		if stream["pm_ssdb_printf"]:#用于调试
			o.df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_arrays_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
#end push_arrays_to_df

#字典到DF
def push_dict_to_df(d,name=""):
	try:
		dd = d.copy() #浅复制，保持不变
		df = pd.DataFrame(data=list(dd.values()),index=list(dd.keys()))
		o = FbiTable(name,df)
		fbi_global.runtime.put(o)
		if stream["pm_ssdb_printf"]:#用于调试
			df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_dict_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
#end push_dict_to_df


#mysql到DF
def mysql_to_df(a,cols,name=""):
	try:
		df = pd.DataFrame(data=a,columns=cols)
		if stream["pm_ssdb_printf"]:#用于调试
			df.to_feather("/dev/shm/xlink_df:{}:{}.fat".format(stream["name"],name))
	except Exception as e:
		add_error_to_log(stream['name'],'push_mysql_to_df执行出错','DF: %s,原因: %s'%(name,e.__str__()))
	return df
#end mysql_to_df

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

#LastModifyDate:　2024-01-09T11:34:52    Author:   qh

#LastModifyDate:　2024-01-09T11:27:20    Author:   qh

#LastModifyDate:　2024-01-09T11:24:09    Author:   qh

#LastModifyDate:　2024-01-09T10:18:55    Author:   rzc

#LastModifyDate:　2024-01-09T09:13:00    Author:   superFBI

#LastModifyDate:　2024-01-08T19:45:44    Author:   superFBI

#LastModifyDate:　2024-01-08T18:57:08    Author:   superFBI

#LastModifyDate:　2024-01-08T09:32:57    Author:   superFBI

#LastModifyDate:　2024-01-06T16:14:21    Author:   superFBI

#LastModifyDate:　2024-01-06T15:45:09    Author:   superFBI

#LastModifyDate:　2024-01-06T13:57:02    Author:   superFBI

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	
	# 消费kfk 
	stream["meta_name"] = "model处理进程"
	stream["meta_desc"] = "从api_visit主题中消费数据，分析高频次访问敏感，访问敏感接口频次过高存入ckh数据库api_model表"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"]= {"unix_udp":"/tmp/owp_model"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["max_mem"] = 6
	stream["stw"]["stw_flow"]={"times":60,"fun":"flow"}
	stream["st"]["st_10s"]={"times":10,"fun":"print10"}
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_model" in a:
		set_param("model_syslog","1")
	else:
		set_param("model_syslog","0")
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	c = load_ssdb_kv("model_config")
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
#end 

#事件处理函数
def Events(o,topic=''):
	if o.get('url_c') in stream["monitor_url"] or stream["all_combo"]:
		k = iso_to_timestamp(o["timestamp"])
		temp = {
			'srcip': o.get('src_ip'),
			'dest_ip': o.get('dest_ip'),
			'dest_port': int(o.get('dest_port')),
			'first_time': iso_to_datetime(o.get('timestamp')),
			'last_time': iso_to_datetime(o.get('timestamp')),
			'app': o.get('app'),
			'api': o.get('url_c'),
			'method': o.get("http").get('method'),
			'length': o.get("http").get('length', 0),
			'age': o.get("http").get('age'),
			'state': "待确认",
			'srcport': o.get('src_port'),
			'url_a': o.get('url'),
			'account': o.get('account'),
			'real_ip': o.get('realip'),
			'id': xlink_uuid(0),
			'suid': o.get('id')
		}
		push_stw("stw_flow",k,temp)
#end 

#窗口函数，使用FBI的原语

#窗口函数，使用FBI语句块 
def flow(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'src_model', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'srcip_model_xlk'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[66]原语 src_model = load ssdb by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'model_config', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'model_config as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[67]原语 model_config = load ssdb ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'on', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["switch"]["model2"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[68]原语 on = jaas model_config by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"$on" == "true"', 'with': '""\ndf2 = join src_model,df by srcip,srcip\n"', 'else': '"\ndf2 = @udf udf0.new_df\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=69
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[69]原语 if "$on" == "true" with "... 出错,原因:'+e.__str__())

#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'monitor_url', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'monitor_url_xlk'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[74]原语 monitor_url = load ssdb b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'monitor_url', 'as': '"url":"api"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[75]原语 rename monitor_url as ("u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'all_combo', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["switch"]["all_combo"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[78]原语 all_combo = jaas model_co... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"$all_combo" == "false"', 'with': '""\ndf2 = join monitor_url,df2 by api,api\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=79
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[79]原语 if "$all_combo" == "false... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'wl', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model2"]["whitelist"]'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[82]原语 wl = jaas model_config by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wl', 'Action': '@udf', '@udf': 'wl', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[83]原语 wl = @udf wl by FBI.json2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wll', 'Action': '@udf', '@udf': 'wl', 'by': 'model.dropem'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[84]原语 wll = @udf wl by model.dr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wl', 'Action': '@udf', '@udf': 'wl', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[85]原语 wl = @udf wl by udf0.df_r... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'wl', 'as': '"dstip":"dest_ip","dstport":"dest_port","url":"api"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[86]原语 rename wl as ("dstip":"de... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wls', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[87]原语 wls = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'wl', 'with': 'idx=$1', 'run': '""\nwl1 = filter wl by (index == @idx)\nwl1 = @udf wl1 by model.dropem\nwl1 = loc wl1 drop index\nwl2 = @udf wl1,df2 by model.join2\nwls = union (wls,wl2)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[88]原语 foreach wl run "wl1 = fil... 出错,原因:'+e.__str__())

#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'wls', 'Action': 'distinct', 'distinct': 'wls', 'by': 'id'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[95]原语 wls = distinct wls by id... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': 'wll.iloc[0,:].size == 0', 'with': '""\nwls = limit df2 by 500000\n""'}
	try:
		ptree['lineno']=96
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[96]原语 if wll.iloc[0,:].size == ... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df22', 'Action': 'filter', 'filter': 'wls', 'by': "real_ip == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[99]原语 df22 = filter wls by (rea... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df222', 'Action': 'filter', 'filter': 'wls', 'by': "real_ip != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[100]原语 df222 = filter wls by (re... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model2"]["count"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[102]原语 b = jaas model_config by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df3', 'Action': 'group', 'group': 'df22', 'by': 'srcip', 'agg': 'srcip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[103]原语 df3 = group df22 by srcip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[104]原语 df3 = @udf df3 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df3', 'Action': 'filter', 'filter': 'df3', 'by': 'srcip_count > $b'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[105]原语 df3 = filter df3 by srcip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df3,wls', 'by': 'srcip,srcip'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[106]原语 df3 = join df3,wls by src... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df3', 'Action': 'distinct', 'distinct': 'df3', 'by': 'srcip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[107]原语 df3 = distinct df3 by src... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'model2', 'Action': 'loc', 'loc': 'df3', 'drop': 'state,method,length,age,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[108]原语 model2 = loc df3 drop (st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'rux', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'risk_url_xlk'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[110]原语 rux = load ssdb by ssdb0 ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'model2', 'by': '"api":"url","dest_ip":"dstip","dest_port":"dstport","first_time":"timestamp"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[111]原语 rename model2 by ("api":"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 's', 'Action': 'join', 'join': 'rux,model2', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[112]原语 s = join rux,model2 by ur... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[113]原语 proof = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[114]原语 proofs = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'b', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$b,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[115]原语 b = @sdf sys_str with ($b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 's', 'with': 'url=$1,srcip=$2,srcip_count=$3', 'run': '""\nf = filter df22 by (srcip == "@srcip" and api == "@url")\nbb = loc f by suid\nbb= @udf bb by udf0.df_T\nbb = @udf bb by udf0.df_cs2l\nproof = union (proof,bb)\nc = loc f by first_time,suid\nrename c as ("first_time":"timestamp")\nd = @udf c by model.proof2 with @srcip,@url,$b,@srcip_count\nproofs = union (proofs,d)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[116]原语 foreach s run "f = filter... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'proof', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[127]原语 proof = @udf proof by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proof', 'Action': 'loc', 'loc': 'proof', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[128]原语 proof = loc proof drop in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[129]原语 s = @udf s by udf0.df_fil... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 's', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[130]原语 s = @udf s by udf0.df_res... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[131]原语 s = loc s drop index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 's', 'Action': 'join', 'join': 's,proof', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[132]原语 s = join s,proof by index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 's', 'by': '"s0":"proof"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[133]原语 rename s by ("s0":"proof"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 's.srcip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[134]原语 alter s.srcip_count as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'message', 'with': '\'终端“\' + s["srcip"] + \'”访问敏感接口频次过高，一分钟内访问\' + s["srcip_count"] + \'次\''}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[135]原语 s = add message with ("终端... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'proofs', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[136]原语 proofs = @udf proofs by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proofs', 'Action': 'loc', 'loc': 'proofs', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[137]原语 proofs = loc proofs drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 's', 'Action': 'join', 'join': 's,proofs', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[138]原语 s = join s,proofs by inde... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df3', 'Action': 'group', 'group': 'df222', 'by': 'real_ip', 'agg': 'real_ip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[139]原语 df3 = group df222 by real... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df3', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[140]原语 df3 = @udf df3 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df3', 'Action': 'filter', 'filter': 'df3', 'by': 'real_ip_count > $b'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[141]原语 df3 = filter df3 by real_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df3,wls', 'by': 'real_ip,real_ip'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[142]原语 df3 = join df3,wls by rea... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df3', 'Action': 'distinct', 'distinct': 'df3', 'by': 'real_ip'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[143]原语 df3 = distinct df3 by rea... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'model2', 'Action': 'loc', 'loc': 'df3', 'drop': 'state,method,length,age,last_time'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[144]原语 model2 = loc df3 drop (st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'model2', 'by': '"api":"url","dest_ip":"dstip","dest_port":"dstport","first_time":"timestamp"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[145]原语 rename model2 by ("api":"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'ss', 'Action': 'join', 'join': 'rux,model2', 'by': 'url,url'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[146]原语 ss = join rux,model2 by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[147]原语 proof = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[148]原语 proofs = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'b', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$b,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[149]原语 b = @sdf sys_str with ($b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'ss', 'with': 'url=$1,real_ip=$2,real_ip_count=$3', 'run': '""\nf = filter df222 by (real_ip == "@real_ip" and api == "@url")\nbb = loc f by suid\nbb= @udf bb by udf0.df_T\nbb = @udf bb by udf0.df_cs2l\nproof = union (proof,bb)\nc = loc f by first_time,suid\nrename c as ("first_time":"timestamp")\nd = @udf c by model.proof2 with @real_ip,@url,$b,@real_ip_count\nproofs = union (proofs,d)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[150]原语 foreach ss run "f = filte... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'proof', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[161]原语 proof = @udf proof by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proof', 'Action': 'loc', 'loc': 'proof', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[162]原语 proof = loc proof drop in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[163]原语 ss = @udf ss by udf0.df_f... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'ss', 'Action': '@udf', '@udf': 'ss', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[164]原语 ss = @udf ss by udf0.df_r... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'ss', 'Action': 'loc', 'loc': 'ss', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[165]原语 ss = loc ss drop index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'ss', 'Action': 'join', 'join': 'ss,proof', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[166]原语 ss = join ss,proof by ind... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'ss', 'by': '"s0":"proof"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[167]原语 rename ss by ("s0":"proof... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'ss.real_ip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[168]原语 alter ss.real_ip_count as... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'ss', 'Action': 'add', 'add': 'message', 'with': '\'终端“\' + ss["real_ip"] + \'”访问敏感接口频次过高，一分钟内访问\' + ss["real_ip_count"] + \'次\''}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[169]原语 ss = add message with ("终... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'proofs', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[170]原语 proofs = @udf proofs by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proofs', 'Action': 'loc', 'loc': 'proofs', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[171]原语 proofs = loc proofs drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'ss', 'Action': 'join', 'join': 'ss,proofs', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[172]原语 ss = join ss,proofs by in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 's', 'Action': 'loc', 'loc': 's', 'drop': 'srcip_count,suid'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[173]原语 s = loc s drop (srcip_cou... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'ss', 'Action': 'loc', 'loc': 'ss', 'drop': 'real_ip_count,suid'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[174]原语 ss = loc ss drop (real_ip... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= union', 'Ta': 's', 'Action': 'union', 'union': 's,ss'}
	try:
		union(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[175]原语 s = union (s,ss)... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 's.proof', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[176]原语 alter s.proof as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'type', 'with': '2'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[177]原语 s = add type with (2)... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'level', 'with': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[178]原语 s = add level with (1)... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 's', 'Action': 'add', 'add': 'desc', 'with': '"同一终端或同一账号高频次访问敏感接口"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[179]原语 s = add desc with ("同一终端或... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 's', 'to': 'ckh', 'by': 'ckh', 'with': 'api_model'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[181]原语 store s to ckh by ckh wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"@model_syslog" == "1" and s.iloc[0,:].size == 17', 'with': '""\n#define kfka as "@link"\n#k = @udf KFK.df_link with kfka\nalter s.timestamp as str\ns = add event_type by ("model")\n#a = @udf s by KFK.fast_store with kfka,api_send\na = @udf s by df2jsonfile.pushf\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=182
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[182]原语 if "@model_syslog" == "1"... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[190]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'model2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[191]原语 drop model2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 's'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[192]原语 drop s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'ss'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[193]原语 drop ss... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[194]原语 drop df2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df22'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[195]原语 drop df22... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df222'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[196]原语 drop df222... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[197]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'wls'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[198]原语 drop wls... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'rux'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[199]原语 drop rux... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'proof'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[200]原语 drop proof... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'proofs'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[201]原语 drop proofs... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_owasp4_model.xlk]执行第[202]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#系统定时函数，st为时间戳 
def print10(st):
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	#set_param("link",stream["link"])
	if "api_model" in a:
		set_param("model_syslog","1")
	else:
		set_param("model_syslog","0")
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	b = []
	for item in s:
		b.append(item[0])
	stream["monitor_url"] = b
	c = load_ssdb_kv("model_config")
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#udf

#end 
