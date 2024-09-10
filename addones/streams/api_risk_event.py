#!/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#xlink的py文件
#filename: api_risk_event.xlk
#datetime: 2024-08-30T16:10:58.208088
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

#LastModifyDate:　2024-01-09T11:41:48    Author:   qh

#LastModifyDate:　2024-01-09T10:18:27    Author:   rzc

#LastModifyDate:　2024-01-09T09:13:31    Author:   superFBI

#LastModifyDate:　2024-01-08T19:40:10    Author:   superFBI

#LastModifyDate:　2024-01-08T18:46:39    Author:   superFBI

#LastModifyDate:　2024-01-08T09:37:46    Author:   superFBI

#LastModifyDate:　2024-01-06T16:21:20    Author:   superFBI

#LastModifyDate:　2024-01-06T15:42:20    Author:   superFBI

#LastModifyDate:　2024-01-06T13:59:50    Author:   superFBI

#LastModifyDate:　2023-12-28T09:33:23.395661    Author:   superFBI

#LastModifyDate:　2023-12-27T15:19:42.992824    Author:   superFBI

#初始化函数
def Inits():
	try:
		fbi_global.runtime.use_ws("xlink")
	except:
		pass
	
	# 消费kfk 
	stream["meta_name"] = "超频告警处理进程"
	stream["meta_desc"] = "从api_visit主题中消费数据，分析超频告警，风险事件数据存入ckh数据库api_risk表"
	a = load_ssdb_kv("setting")
	stream["redis_link"] = a["kfk"]["redis"]["addr_r"]
	stream["link"] = a["kfk"]["origin"]["link"]
	stream["topic"] = a["kfk"]["origin"]["topic"]
	stream["reset"] = a["kfk"]["origin"]["reset"]
	# stream["number"] = int(load_ssdb_kv("setting")["setting"]["warn"]["times"])
	
	#stream["source"]= {"link":stream["redis_link"]+":6382","topic":"api_visit1","redis":"pubsub"}
	#stream["source"] = {"unix_udp":"/tmp/risk_event"}
	stream["source"] = {"shm_name":"httpub","count":8}
	stream["max_mem"] = 6
#	stream["source"]= {"link":"192.168.1.190:9092","topic":"api_visit","group":"x7","start-0":True}

	stream["stw"]["stw_flow"]={"times":60,"fun":"flow,flow1"}
	#stream["stw"]["stw_flow1"]={"times":60,"fun":"flow1"}
	stream["st"]["st_60s"]={"times":60,"fun":"send60"}
	
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	c = load_ssdb_kv("model_config")
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_event" in a:
		set_param("api_event","1")
	else:
		set_param("api_event","0")
	set_param("link",stream["link"])
	if "api_model" in a:
		set_param("model_send","1")
	else:
		set_param("model_send","0")
#end 

#事件处理函数
def Events(o,topic=''):
	#if o.get('app') in stream["warn"]:
	k = iso_to_timestamp(o["timestamp"])
	temp = {
		'srcip': o.get('src_ip'),
		'srcport': o.get('src_port'),
		'dstip': o.get('dest_ip'),
		'dstport': o.get('dest_port'),
		'timestamp': iso_to_datetime(o.get('timestamp')),
		'app': o.get('app'),
		'url_a': o.get('url')
	}
	#没有必要搞成两个数据窗口
	#push_stw("stw_flow1",k,temp)
	#下面模型用
	if stream["all_combo"] or o.get("url_c") in stream["monitor_url"]:
		temp['account'] = o.get('account')
		temp['url'] = o.get('url_c')
		temp['real_ip'] = o.get('realip')
		temp['id'] = xlink_uuid(0)
		temp['suid'] = o.get('id')
		temp['type'] = 10
		temp['desc'] = "访问频次出现异常行为"
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
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'model_config', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'model_config as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[81]原语 model_config = load ssdb ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'on', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["switch"]["model10"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[82]原语 on = jaas model_config by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"$on" == "true"', 'with': '""\n#df = join src_model,df by srcip,srcip\ndf = limit df by 1000000\n"', 'else': '"\ndf = @udf udf0.new_df\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['else'] = replace_ps(ptree['else'],runtime)
	try:
		ptree['lineno']=83
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[83]原语 if "$on" == "true" with "... 出错,原因:'+e.__str__())

#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'monitor_url', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'monitor_url_xlk'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[89]原语 monitor_url = load ssdb b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'all_combo', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["switch"]["all_combo"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[90]原语 all_combo = jaas model_co... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"$all_combo" == "false"', 'with': '""\ndf = join monitor_url,df by url,url\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	try:
		ptree['lineno']=91
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[91]原语 if "$all_combo" == "false... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'wl', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model10"]["whitelist"]'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[94]原语 wl = jaas model_config by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wl', 'Action': '@udf', '@udf': 'wl', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[95]原语 wl = @udf wl by FBI.json2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wll', 'Action': '@udf', '@udf': 'wl', 'by': 'model.dropem'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[96]原语 wll = @udf wl by model.dr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wl', 'Action': '@udf', '@udf': 'wl', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[97]原语 wl = @udf wl by udf0.df_r... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'wls', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[98]原语 wls = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'wl', 'with': 'idx=$1', 'run': '""\nwl1 = filter wl by (index == @idx)\nwl1 = @udf wl1 by model.dropem\nwl1 = loc wl1 drop index\nwl2 = @udf wl1,df by model.join2\nwls = union (wls,wl2)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[99]原语 foreach wl run "wl1 = fil... 出错,原因:'+e.__str__())

#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': 'wll.iloc[0,:].size == 0', 'with': '""\nwls = limit df by 500000\n""'}
	try:
		ptree['lineno']=106
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[106]原语 if wll.iloc[0,:].size == ... 出错,原因:'+e.__str__())

#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'wls', 'Action': 'distinct', 'distinct': 'wls', 'by': 'id'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[109]原语 wls = distinct wls by id... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'bcount', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model10"]["count"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[110]原语 bcount = jaas model_confi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'ccount', 'Action': 'jaas', 'jaas': 'model_config', 'by': 'model_config["setting"]["model10"]["url_count"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[111]原语 ccount = jaas model_confi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df2', 'Action': 'filter', 'filter': 'wls', 'by': "real_ip == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[112]原语 df2 = filter wls by (real... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df22', 'Action': 'filter', 'filter': 'wls', 'by': "real_ip != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[113]原语 df22 = filter wls by (rea... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'model', 'Action': 'group', 'group': 'df2', 'by': 'srcip,url', 'agg': 'srcip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[114]原语 model = group df2 by srci... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'model', 'Action': '@udf', '@udf': 'model', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[115]原语 model = @udf model by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'model', 'Action': 'filter', 'filter': 'model', 'by': 'srcip_count > $bcount'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[116]原语 model = filter model by s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'model10', 'Action': 'join', 'join': 'model,df2', 'by': '[srcip,url],[srcip,url]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[117]原语 model10 = join model,df2 ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'model10', 'Action': 'distinct', 'distinct': 'model10', 'by': 'srcip,url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[118]原语 model10 = distinct model1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'modell', 'Action': 'group', 'group': 'model10', 'by': 'srcip,app', 'agg': 'url:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[119]原语 modell = group model10 by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'modell', 'Action': '@udf', '@udf': 'modell', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[120]原语 modell = @udf modell by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'modell', 'Action': 'filter', 'filter': 'modell', 'by': 'url_count > $ccount'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[121]原语 modell = filter modell by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell', 'Action': 'join', 'join': 'modell,model10', 'by': '[srcip,app],[srcip,app]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[122]原语 modell = join modell,mode... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'modell', 'Action': 'distinct', 'distinct': 'modell', 'by': 'srcip,app'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[123]原语 modell = distinct modell ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'url', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[124]原语 url = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[125]原语 proof = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[126]原语 proofs = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'model10.srcip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[127]原语 alter model10.srcip_count... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'bcount', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$bcount,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[129]原语 bcount = @sdf sys_str wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'ccount', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$ccount,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[130]原语 ccount = @sdf sys_str wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'modell', 'Action': 'loc', 'loc': 'modell', 'by': 'srcip,app,url,url_count,dstip,dstport,srcport,timestamp,url_a,account,real_ip,id,type,desc,suid,srcip_count'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[131]原语 modell = loc modell by (s... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'modell', 'with': 'srcip=$1,app=$2,url=$3', 'run': '""\nf = filter model10 by (srcip == "@srcip" and app == "@app")\naa = loc f by url,srcip_count\naa = distinct aa by url\naa = add a by (\'访问接口\' + aa.url + \'达\' + aa.srcip_count + \'次\')\naa = loc aa by a\naa = @udf aa by udf0.df_T\naa = @udf aa by udf0.df_cs2l\nurl = union (url,aa)\nbb = loc f by suid\nbb= @udf bb by udf0.df_T\nbb = @udf bb by udf0.df_cs2l\nproof = union (proof,bb)\nf = loc f by timestamp,suid\nd = @udf f by model.proof10 with @srcip,@url,$bcount,$ccount\nproofs = union (proofs,d)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[132]原语 foreach modell run "f = f... 出错,原因:'+e.__str__())

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
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'url', 'Action': '@udf', '@udf': 'url', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[149]原语 url = @udf url by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'url', 'Action': 'loc', 'loc': 'url', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[150]原语 url = loc url drop index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'proof', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[151]原语 proof = @udf proof by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proof', 'Action': 'loc', 'loc': 'proof', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[152]原语 proof = loc proof drop in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'modell', 'Action': '@udf', '@udf': 'modell', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[153]原语 modell = @udf modell by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'modell', 'Action': '@udf', '@udf': 'modell', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[154]原语 modell = @udf modell by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'modell', 'Action': 'loc', 'loc': 'modell', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[155]原语 modell = loc modell drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell', 'Action': 'join', 'join': 'modell,url', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[156]原语 modell = join modell,url ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell.srcip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[157]原语 alter modell.srcip_count ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell.url_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[158]原语 alter modell.url_count as... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell.s0', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[159]原语 alter modell.s0 as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'modell', 'Action': 'add', 'add': 'message', 'by': "'终端“' + modell.srcip + '”疑似出现机器访问行为，超频访问接口' + modell.url_count + '个，一分钟内:' + modell.s0"}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[160]原语 modell = add message by (... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'modell', 'Action': 'loc', 'loc': 'modell', 'drop': 'srcip_count,url_count,s0,suid'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[161]原语 modell = loc modell drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell', 'Action': 'join', 'join': 'modell,proof', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[162]原语 modell = join modell,proo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'proofs', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[163]原语 proofs = @udf proofs by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proofs', 'Action': 'loc', 'loc': 'proofs', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[164]原语 proofs = loc proofs drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell', 'Action': 'join', 'join': 'modell,proofs', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[165]原语 modell = join modell,proo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'model', 'Action': 'group', 'group': 'df22', 'by': 'real_ip,url', 'agg': 'real_ip:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[167]原语 model = group df22 by rea... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'model', 'Action': '@udf', '@udf': 'model', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[168]原语 model = @udf model by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'model', 'Action': 'filter', 'filter': 'model', 'by': 'real_ip_count > $bcount'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[169]原语 model = filter model by r... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'model10', 'Action': 'join', 'join': 'model,df22', 'by': '[real_ip,url],[real_ip,url]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[170]原语 model10 = join model,df22... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'model10', 'Action': 'distinct', 'distinct': 'model10', 'by': 'real_ip,url'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[171]原语 model10 = distinct model1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'modell2', 'Action': 'group', 'group': 'model10', 'by': 'real_ip,app', 'agg': 'url:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[172]原语 modell2 = group model10 b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'modell2', 'Action': '@udf', '@udf': 'modell2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[173]原语 modell2 = @udf modell2 by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'modell2', 'Action': 'filter', 'filter': 'modell2', 'by': 'url_count > $ccount'}
	ptree['by'] = deal_sdf(workspace,ptree['by'])
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[174]原语 modell2 = filter modell2 ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell2', 'Action': 'join', 'join': 'modell2,model10', 'by': '[real_ip,app],[real_ip,app]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[175]原语 modell2 = join modell2,mo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'modell2', 'Action': 'distinct', 'distinct': 'modell2', 'by': 'real_ip,app'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[176]原语 modell2 = distinct modell... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'url', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[177]原语 url = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[178]原语 proof = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'udf0.new_df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[179]原语 proofs = @udf udf0.new_df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'model10.real_ip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[180]原语 alter model10.real_ip_cou... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'bcount', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$bcount,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[181]原语 bcount = @sdf sys_str wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 'ccount', 'Action': '@sdf', '@sdf': 'sys_str', 'with': '$ccount,strip()'}
	ptree['with'] = deal_sdf(workspace,ptree['with'])
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[182]原语 ccount = @sdf sys_str wit... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'foreach', 'foreach': 'modell2', 'with': 'real_ip=$1,app=$2,url=$10', 'run': '""\nf = filter model10 by (real_ip == "@real_ip" and app == "@app")\naa = loc f by url,real_ip_count\naa = distinct aa by url\naa = add a by (\'访问接口\' + aa.url + \'达\' + aa.real_ip_count + \'次\')\naa = loc aa by a\naa = @udf aa by udf0.df_T\naa = @udf aa by udf0.df_cs2l\nurl = union (url,aa)\nbb = loc f by suid\nbb= @udf bb by udf0.df_T\nbb = @udf bb by udf0.df_cs2l\nproof = union (proof,bb)\nf = loc f by timestamp,suid\nd = @udf f by model.proof10 with @real_ip,@url,$bcount,$ccount\nproofs = union (proofs,d)\n""'}
	try:
		foreach_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[183]原语 foreach modell2 run "f = ... 出错,原因:'+e.__str__())

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
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'url', 'Action': '@udf', '@udf': 'url', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[200]原语 url = @udf url by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'url', 'Action': 'loc', 'loc': 'url', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[201]原语 url = loc url drop index... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proof', 'Action': '@udf', '@udf': 'proof', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[202]原语 proof = @udf proof by udf... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proof', 'Action': 'loc', 'loc': 'proof', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[203]原语 proof = loc proof drop in... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'modell2', 'Action': '@udf', '@udf': 'modell2', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[204]原语 modell2 = @udf modell2 by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'modell2', 'Action': '@udf', '@udf': 'modell2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[205]原语 modell2 = @udf modell2 by... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'modell2', 'Action': 'loc', 'loc': 'modell2', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[206]原语 modell2 = loc modell2 dro... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell2', 'Action': 'join', 'join': 'modell2,url', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[207]原语 modell2 = join modell2,ur... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell2.real_ip_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[208]原语 alter modell2.real_ip_cou... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell2.url_count', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[209]原语 alter modell2.url_count a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell2.s0', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[210]原语 alter modell2.s0 as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'modell2', 'Action': 'add', 'add': 'message', 'by': "'终端“' + modell2.real_ip + '”疑似出现机器访问行为，超频访问接口' + modell2.url_count + '个，一分钟内:' + modell2.s0"}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[211]原语 modell2 = add message by ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'modell2', 'Action': 'loc', 'loc': 'modell2', 'drop': 'real_ip_count,url_count,s0,suid'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[212]原语 modell2 = loc modell2 dro... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell2', 'Action': 'join', 'join': 'modell2,proof', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[213]原语 modell2 = join modell2,pr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'proofs', 'Action': '@udf', '@udf': 'proofs', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[214]原语 proofs = @udf proofs by u... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'proofs', 'Action': 'loc', 'loc': 'proofs', 'drop': 'index'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[215]原语 proofs = loc proofs drop ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'modell2', 'Action': 'join', 'join': 'modell2,proofs', 'by': 'index,index', 'with': 'left'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[216]原语 modell2 = join modell2,pr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= union', 'Ta': 'modell', 'Action': 'union', 'union': 'modell,modell2'}
	try:
		union(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[217]原语 modell = union (modell,mo... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'modell', 'Action': 'distinct', 'distinct': 'modell', 'by': 'id'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[218]原语 modell = distinct modell ... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'modell', 'by': '"s0":"proof"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[219]原语 rename modell by ("s0":"p... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'modell.proof', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[220]原语 alter modell.proof as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'modell', 'Action': 'add', 'add': 'level', 'by': '1'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[221]原语 modell = add level by (1)... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'modell', 'to': 'ckh', 'by': 'ckh', 'with': 'api_model'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[222]原语 store modell to ckh by ck... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'define', 'define': 'kfka', 'as': '@link'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[223]原语 define kfka as "@link"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'k', 'Action': '@udf', '@udf': 'KFK.df_link', 'with': 'kfka'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[224]原语 k = @udf KFK.df_link with... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"@model_send" == "1" and modell.iloc[0,:].size == 17', 'with': '""\nalter modell.timestamp as str\nmodell = add event_type by ("model")\na = @udf modell by KFK.fast_store with kfka,api_send\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=225
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[225]原语 if "@model_send" == "1" a... 出错,原因:'+e.__str__())

#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, '': '= @sdf', 'Ta': 't2', 'Action': '@sdf', '@sdf': 'sys_now'}
	try:
		ret = sdf_func(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[230]原语 t2 = @sdf sys_now... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 't1', 'Action': 'eval', 'eval': 'af', 'by': 'index.size'}
	try:
		eval_df(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[231]原语 t1 = eval af by index.siz... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'model10'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[234]原语 drop model10... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'modell'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[235]原语 drop modell... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'modell2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[236]原语 drop modell2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[237]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'af'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[238]原语 drop af... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[239]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[240]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#窗口函数，使用FBI语句块 
def flow1(k,df):
	errors=[]
	workspace='xlink'
	runtime = fbi_global.runtime
	runtime.ps['@k']=k
	runtime.keys= runtime.ps.keys()
	o = FbiTable('df',df)
	fbi_global.runtime.put(o)
	ptree={'runtime': runtime,'work_space': workspace, '': '=', 'Ta': 'a', 'Action': 'load', 'load': 'ssdb', 'by': 'ssdb0', 'with': 'alarm as json'}
	try:
		load_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[244]原语 a = load ssdb by ssdb0 wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= jaas', 'Ta': 'b', 'Action': 'jaas', 'jaas': 'a', 'by': 'a["setting"]["warn"]["warn"]', 'as': 'sdf'}
	try:
		jaas_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[245]原语 b = jaas a by a["setting"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'b', 'Action': '@udf', '@udf': 'b', 'by': 'FBI.json2df'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[246]原语 b = @udf b by FBI.json2df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df1', 'Action': 'loc', 'loc': 'df', 'by': 'srcip,srcport,dstip,dstport,timestamp,app,url_a'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[248]原语 df1 = loc df by (srcip,sr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= group', 'Ta': 'df2', 'Action': 'group', 'group': 'df1', 'by': 'app,srcip', 'agg': 'app:count'}
	try:
		group_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[249]原语 df2 = group df1 by app,sr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'df2', 'Action': '@udf', '@udf': 'df2', 'by': 'udf0.df_reset_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[250]原语 df2 = @udf df2 by udf0.df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'new', 'Action': 'join', 'join': 'b,df2', 'by': 'app,app'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[252]原语 new = join b,df2 by app,a... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'new.times', 'as': 'int'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[254]原语 alter new.times as int... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= filter', 'Ta': 'df2', 'Action': 'filter', 'filter': 'new', 'by': ' app_count >= times '}
	try:
		filter_query(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[255]原语 df2 = filter new by ( app... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= loc', 'Ta': 'df2', 'Action': 'loc', 'loc': 'df2', 'by': 'app,app_count,srcip'}
	try:
		loc_data(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[256]原语 df2 = loc df2 by (app,app... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= join', 'Ta': 'df3', 'Action': 'join', 'join': 'df1,df2', 'by': '[srcip,app],[srcip,app]'}
	try:
		join_by(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[258]原语 df3 = join df1,df2 by [sr... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= distinct', 'Ta': 'df3', 'Action': 'distinct', 'distinct': 'df3', 'by': 'app'}
	try:
		distinct_dup(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[259]原语 df3 = distinct df3 by app... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'rename', 'rename': 'df3', 'by': '"app_count":"risk_sign","timestamp":"first_time","url_a":"url"'}
	try:
		rename_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[260]原语 rename df3 by ("app_count... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'df3.risk_sign', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[261]原语 alter df3.risk_sign as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'risk_sign', 'by': "'访问频次:' + df3.risk_sign"}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[262]原语 df3 = add risk_sign by ("... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'risk_level', 'by': '3'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[263]原语 df3 = add risk_level by 3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'risk_label', 'by': '"超频告警"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[264]原语 df3 = add risk_label by (... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'content', 'by': '"None"'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[265]原语 df3 = add content by ("No... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'last_time', 'by': 'df3.first_time'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[266]原语 df3 = add last_time by df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= add', 'Ta': 'df3', 'Action': 'add', 'add': 'is_verify', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[267]原语 df3 = add is_verify by 0... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'af', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[268]原语 af = @udf af by udf0.df_f... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'af', 'Action': '@udf', '@udf': 'df3', 'by': 'udf0.df_zero_index'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[269]原语 af = @udf df3 by udf0.df_... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.is_verify', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[270]原语 alter af.is_verify as str... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.risk_level', 'as': 'str'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[271]原语 alter af.risk_level as st... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.last_time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[272]原语 alter af.last_time as dat... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'alter', 'alter': 'af.first_time', 'as': 'datetime64'}
	try:
		alter_col(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[273]原语 alter af.first_time as da... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'store', 'store': 'af', 'to': 'ckh', 'by': 'ckh', 'with': 'api_risk'}
	try:
		store_to(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[274]原语 store af to ckh by ckh wi... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'define', 'define': 'kfka', 'as': '@link'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[275]原语 define kfka as "@link"... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, '': '= @udf', 'Ta': 'k', 'Action': '@udf', '@udf': 'KFK.df_link', 'with': 'kfka'}
	try:
		ret = udf_func(ptree,p=2)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[276]原语 k = @udf KFK.df_link with... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'if', 'if': '"@api_event" == "1"', 'with': '""\n#define kfka as "@link"\n#k = @udf KFK.df_link with kfka\nalter af.first_time as str\nalter af.last_time as str\naf = add event_type by ("overclock")\na = @udf af by KFK.fast_store with kfka,api_send\n""'}
	ptree['if'] = replace_ps(ptree['if'],runtime)
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=277
		if_fun(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[277]原语 if "@api_event" == "1" wi... 出错,原因:'+e.__str__())

#
#
#
#
#
#
#
	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'new'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[285]原语 drop new... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'b'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[286]原语 drop b... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df1'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[287]原语 drop df1... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df2'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[288]原语 drop df2... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df3'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[289]原语 drop df3... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'af'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[290]原语 drop af... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[291]原语 drop df... 出错,原因:'+e.__str__())

	ptree={'runtime': runtime,'work_space': workspace, 'Action': 'drop', 'drop': 'df'}
	try:
		drop_table(ptree)
	except Exception as e:
		errors.append('[api_risk_event.xlk]执行第[292]原语 drop df... 出错,原因:'+e.__str__())

	return errors 
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
	return str(time.time_ns())
#end 

#系统定时函数，st为时间戳 
def send60(st):
	c = load_ssdb_kv("model_config")
	stream["all_combo"] = c["setting"]["switch"]["all_combo"]
	s = load_ssdb_kv("monitor_url_xlk")["data"]
	stream["monitor_url"] = []
	for item in s:
		stream["monitor_url"].append(item[0])
	a = load_ssdb_kv("qh_send")["sends"].split(',')
	if "api_event" in a:
		set_param("api_event","1")
	else:
		set_param("api_event","0")
	if "api_model" in a:
		set_param("model_send","1")
	else:
		set_param("model_send","0")
#end 

#自定义python函数，必须有参数,可以在初始化函数，事件处理函数，和定时函数中使用
def xlink_uuid(x):
 return "%d-%7f-%3f" % (x,time.time(), random.random())
#end 

#udf

#end 
