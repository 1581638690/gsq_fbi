#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: sample/load_db
#datetime: 2024-08-30T16:10:57.131108
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
	
	
	ptree={'runtime': runtime, '': '=', 'Ta': 'b', 'Action': 'load', 'load': 'sqlite', 'by': 'zx1129-1.db', 'query': 'SELECT name FROM sqlite_master'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[6]原语 b = load sqlite by zx1129-1.db query SELECT name F... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'b2', 'Action': 'load', 'load': 'sqlite', 'by': 'zx1129-1.db', 'with': '执行案件信息'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[7]原语 b2 =  load sqlite by zx1129-1.db with 执行案件信息 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'my', 'as': 'mysql+mysqlconnector://yy:a123456@127.0.0.1:3306/yy'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[10]原语 define my as mysql+mysqlconnector://yy:a123456@127... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'my', 'with': 'show tables;'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[11]原语 ss = load db by my with show tables; 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'my2', 'as': 'mysql+pymysql://test:dcap123@192.168.1.116:3306/test'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[15]原语 define my2 as mysql+pymysql://test:dcap123@192.168... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'my2', 'with': 'show tables;'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[16]原语 ss = load db by my2 with show tables; 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'my2', 'with': 'select count(*) from zxaj;'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[17]原语 ss = load db by my2 with select count(*) from zxaj... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'b2', 'to': 'db', 'by': 'my2', 'with': 'zxaj'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[18]原语 store b2 to db by my2 with zxaj 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'pg', 'as': 'postgresql+pg8000://postgres:postgres@192.168.1.132/postgres'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[21]原语 define pg as postgresql+pg8000://postgres:postgres... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'pg', 'with': "select * from pg_tables where schemaname = 'public';"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[22]原语 ss = load db by pg with select * from pg_tables wh... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data', 'to': 'db', 'by': 'pg', 'with': 'tcpflow'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[23]原语 store data to db by pg with tcpflow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'pg2', 'as': 'postgresql+psycopg2://postgres:postgre22s@192.168.1.132/postgres'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[26]原语 define pg2 as postgresql+psycopg2://postgres:postg... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'pg211', 'as': 'postgresql+psycopg2://postgres:@192.168.1.132/postgres'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[27]原语 define pg211 as postgresql+psycopg2://postgres:@19... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'pg211', 'with': "select * from pg_tables where schemaname = 'public';"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[30]原语 ss = load db by pg211 with select * from pg_tables... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'pg3', 'as': 'postgresql://postgres:postgres@192.168.1.132/postgres'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[32]原语 define pg3 as postgresql://postgres:postgres@192.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'pg3', 'with': "select * from pg_tables where schemaname = 'public';"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[33]原语 ss = load db by pg3 with select * from pg_tables w... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'ss', 'to': 'db', 'by': 'pg3', 'with': 'tt'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[34]原语 store ss to db by pg3 with tt 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sd', 'Action': 'load', 'load': 'db', 'by': 'pg3', 'with': "SELECT tablename,obj_description(relfilenode,'pg_class') FROM pg_tables a, pg_class b WHERE a.tablename = b.relname ORDER BY a.tablename;"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[37]原语 sd = load db by pg3 with  SELECT   tablename,obj_d... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sl', 'Action': 'load', 'load': 'db', 'by': 'pg3', 'with': "SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull FROM pg_class as c,pg_attribute as a where c.relname = 'tcpflow' and a.attrelid = c.oid and a.attnum>0"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[45]原语 sl = load db by pg3 with  SELECT col_description(a... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'ms', 'as': 'mssql+pymssql://SA:Fhcs2019@192.168.1.132/test?charset=utf8'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[53]原语 define ms as mssql+pymssql://SA:Fhcs2019@192.168.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss2', 'Action': 'load', 'load': 'db', 'by': 'ms', 'with': 'select * from sysdatabases'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[55]原语 ss2 = load db by ms with select * from sysdatabase... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'st2', 'Action': 'load', 'load': 'db', 'by': 'ms', 'with': "SELECT * FROM SysObjects where xtype='U'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[57]原语 st2 = load db by ms with SELECT * FROM SysObjects ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'st2', 'Action': 'load', 'load': 'db', 'by': 'ms', 'with': "SELECT * FROM SysColumns WHERE id=Object_Id('db')"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[59]原语 st2 = load db by ms with SELECT * FROM SysColumns ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 'data', 'to': 'db', 'by': 'ms', 'with': 'tcpflow'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[61]原语 store data to db by ms with tcpflow 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'o131', 'as': 'oracle://sys:123456@192.168.1.131:1521/orcl?mode=SYSDBA&events=true'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[64]原语 define o131 as oracle://sys:123456@192.168.1.131:1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss2', 'Action': 'load', 'load': 'db', 'by': 'o131', 'with': 'select * from user_tables'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[65]原语 ss2 = load db by o131 with select * from user_tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'o18s', 'as': 'oracle://test:test@192.168.1.131:1521/?service_name=XEPDB1'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[68]原语 define o18s as oracle://test:test@192.168.1.131:15... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sss', 'Action': 'load', 'load': 'db', 'by': 'o18s', 'with': 'select * from user_tables'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[69]原语 sss = load db by o18s with select * from user_tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'sss', 'Action': 'load', 'load': 'db', 'by': 'o18s', 'with': 'select * from user_tab_columns'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[70]原语 sss = load db by o18s with select * from user_tab_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'data', 'Action': 'load', 'load': 'db', 'by': 'ms', 'with': 'select count(*) from db'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[72]原语 data = load db by ms with select count(*) from db 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 's', 'Action': '@udf', '@udf': 'ZFile.list_dir', 'with': 'fmtcsv-db'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[73]原语 s = @udf ZFile.list_dir with fmtcsv-db 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'store', 'store': 's', 'to': 'db', 'by': 'pg2', 'with': 'files'}
	try:
		store_to(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[74]原语 store s to db by pg2  with files 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'define', 'define': 'db2', 'as': 'db2+ibm_db://db2inst1:fhcs2019@192.168.1.133/mydata'}
	ptree['as'] = replace_ps(ptree['as'],runtime)
	try:
		define_fun(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[78]原语 define db2 as db2+ibm_db://db2inst1:fhcs2019@192.1... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'db2', 'with': 'select * from sysibm.sysschemata'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[80]原语 ss = load db by db2 with select * from sysibm.syss... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'db2', 'with': 'select * from syscat.tables'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[83]原语 ss = load db by db2 with select * from syscat.tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'db2', 'with': "select * from syscat.tables where tabschema='FIRST'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[86]原语 ss = load db by db2 with select * from syscat.tabl... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'ss', 'Action': 'load', 'load': 'db', 'by': 'db2', 'with': "SELECT * FROM SYSCAT.COLUMNS AS C where c.TABNAME = 'PERSONS' and c.TABSCHEMA = 'FIRST'"}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[sample/load_db.fbi]执行第[89]原语 ss = load db by db2 with  SELECT * FROM SYSCAT.COL... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],100

#主函数结束,开始块函数

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



