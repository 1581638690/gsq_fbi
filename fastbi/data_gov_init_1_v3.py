#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: data_gov_init_1
#datetime: 2024-08-30T16:10:56.225521
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
		add_the_error('[data_gov_init_1.fea]执行第[10]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[13]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'admin,系统管理员,N,9009,use:APP-DLP-SW'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[14]原语 user = @udf user by udf0.df_append with (admin,系统管... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'SSDB2.del_option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[15]原语 @udf user by SSDB2.del_option 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[16]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[17]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'auditAdm,审计管理员,N,9008,use:APP-DLP-SWsj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[18]原语 user = @udf user by udf0.df_append with (auditAdm,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[19]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[20]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'secAdm,安全管理员,N,9007,use:APP-DLP-SWaq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[21]原语 user = @udf user by udf0.df_append with (secAdm,安全... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[22]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[23]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'operateAdm,操作管理员,N,9006,use:APP-DLP-SWcz'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[24]原语 user = @udf user by udf0.df_append with (operateAd... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[25]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[27]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'dsaw,系统管理员,N,9005,use:APP-DLP-SE'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[28]原语 user = @udf user by udf0.df_append with (dsaw,系统管理... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'SSDB2.del_option'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[29]原语 @udf user by SSDB2.del_option 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[30]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[31]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'auditadm,审计管理员,N,9004,use:APP-DLP-SEsj'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[32]原语 user = @udf user by udf0.df_append with (auditadm,... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[33]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[34]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'secadm,安全管理员,N,9003,use:APP-DLP-SEaq'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[35]原语 user = @udf user by udf0.df_append with (secadm,安全... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[36]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'name,realname,isadmin,pot,nav'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[37]原语 user = @udf udf0.new_df with (name,realname,isadmi... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'user', 'Action': '@udf', '@udf': 'user', 'by': 'udf0.df_append', 'with': 'operateadm,操作管理员,N,9002,use:APP-DLP-SEcz'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[38]原语 user = @udf user by udf0.df_append with (operatead... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': '@udf', '@udf': 'user', 'by': 'udfA.imp_users'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[39]原语 @udf user by udfA.imp_users 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[data_gov_init_1.fea]执行第[42]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],42

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



