#!/opt/fbi-base/bin/python3
# -*- coding: utf-8 -*-


import sys
sys.path.append("/opt/openfbi/fbi-bin/lib")
sys.path.append("/opt/openfbi/fbi-bin/driver")
sys.path.append("/opt/openfbi/pylibs")

import os
from avenger.fbicommand import run_script
from avenger.fbiparser import fbi_parser
from avenger.fglobals import fbi_global
from avenger.fst import log_ST
from avenger.fsys import deal_fbi_script_sign
from avenger.fssdb import put_timer_lastrun
from driver.pyssdb import Client


#时间到秒的长度
T=19

"""
在子进程中运行脚本
"""
def run_script_by_timer(name,dnow):
	
	from datetime import datetime	
	costed = 0
	err_cnt = 0 
	try:
		ssdb0 = fbi_global.get_ssdb0()
		prmtv = ssdb0.get("sys:timer:%s"%(name))
		if prmtv ==None or prmtv=="":
			now = datetime.now()
			msg = '<font color="red">[{}][{}] 调度异常，没有找到正确的脚本名和参数 </font>'.format(dnow,now.isoformat()[0:T])
			put_timer_lastrun(name,msg)
			log_ST(name,"",prmtv,msg,state="错误",ssdb0=ssdb0)
			return 1
		runtime = fbi_global.get_runtime()
		ptree = fbi_parser.do_parse("public",prmtv)
		ptree["run"] = deal_fbi_script_sign(ptree["run"])
		ptree["runtime"] = runtime
		lines=[]
		ssdb0.close()
		costed,err_cnt,err_info =  run_script("public",ptree,lines,ptree["run"])
		#put_timer_lastrun(name,'<font color="green"> 调度完成,耗时:{} 秒,错误数: {} </font>'.format(costed,err_cnt))

		#记录运行后的信息
		ssdb0 = fbi_global.get_ssdb0()		
		now = datetime.now()
		msg = '<font color="green">[{}][{}] 调度完成,耗时:{} 秒,错误数: {} </font>'.format(dnow,now.isoformat()[0:T],costed,err_cnt)
		put_timer_lastrun(name,msg)		
		log_ST(name,err_info[0:1024],prmtv,msg,state="完成",ssdb0=ssdb0)
		ssdb0.close()
	except Exception as e :
		ssdb0 = fbi_global.get_ssdb0()
		now = datetime.now()
		msg = '<font color="#b2d235">[{}][{}] 调度完成,耗时:{} 秒,错误数: {},运行中可能有异常也可忽略: {} </font>'.format(dnow,now.isoformat()[0:T],costed,err_cnt,e)
		put_timer_lastrun(name,msg)
		log_ST(name,"{}".format(e),prmtv,msg,state="错误",ssdb0=ssdb0)
		ssdb0.close()
	return 0
#end fun


#"/opt/fbi-base/bin/python fbi-fst.py fst={} {}".format(self.name,self.now)
if __name__ =="__main__":
	try:
		param1 = sys.argv[1]
		fst,name = param1.split("=")
		dnow = sys.argv[2]
	except:
		print("参数不正确: fst=定时器名称 调度时间")
		exit()
	#StartDaemon(run_script_by_timer,name,dnow)
	run_script_by_timer(name,dnow)
