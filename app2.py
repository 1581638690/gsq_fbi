#!/opt/fbi-base/bin/python3
# -*- coding: utf-8 -*- 


"""
app.py 

导入应用
#=========================
"""

import datetime
import sys
import os

import json
sys.path.append("./lib")
sys.path.append("../")
from avenger.fssdb import put_timer,put_key2
from avenger.fastbi import fbi_compile_all

from avenger.fglobals import fbi_global


def ssdb_conn(server="127.0.0.1", port=8888):
	conn = fbi_global.get_ssdb0()
	return conn

# 读的时候采用unicode
def db_conn():
	import sqlite3
	conn = sqlite3.connect("db/kv.db")
	conn.text_factory = str
	return conn


import zipfile
import shutil
import re
import traceback



def load_app(p=''):
	"""
	@author: gjw
	@date: 2020/09/23
	@函数：load_app
	@参数: 文件名
	@描述：导入应用程序所有数据
	@返回：DF表
	@示例：a=@udf scan.load_app with p
	"""
	p = p.strip()

	conn = ssdb_conn()
	
	#zip_path = os.path.join(__workSpace, p)
	zip_path = p
	# 判断zip存在性
	if not os.path.exists(zip_path):
		raise Exception('{}不存在!'.format(zip_path))

	workSpace="/opt/openfbi/workspace/apps"
	# 解压
	pp = p.split("/")
	unpack_dir_name = pp[-1].strip('.zip')
	unpack_dir_path = os.path.join(workSpace, unpack_dir_name)
	shutil.unpack_archive(zip_path, unpack_dir_path)

	image_dir_path = os.path.join(unpack_dir_path, 'images')
	db_dir_path = os.path.join(unpack_dir_path, 'db')
	fea_dir_path = os.path.join(unpack_dir_path, 'scripts')
	word_dir_path = os.path.join(unpack_dir_path, 'temp_word')
	json_path = os.path.join(unpack_dir_path, 'app.json')
	login_json = os.path.join(unpack_dir_path, 'login.json')
	ds_json = os.path.join(unpack_dir_path, 'ds.json')
	st_json = os.path.join(unpack_dir_path, 'st.json')

	# 写入ssdb
	with open(json_path) as f:
		app_data = json.load(f)
		for key, value in app_data.items():
			if key=="Version:Build:System":
				#add by gjw on 2022-0308 导入版本编译信息
				VBS_str = conn.get("Version:Build:System")
				if VBS_str=="" or VBS_str==None:
					VBS = {}
				else:
					try:
						VBS = json.loads(VBS_str)
					except:
						VBS = {}
				vbs = json.loads(value)
				VBS[vbs[0]] = vbs[1]
				conn.set("Version:Build:System",json.dumps(VBS))
			else:
				conn.set(key, value)
	conn.close()

	#定时器
	try:
		with open(st_json) as f:
			data = json.load(f)
			for r in data:
				try:
					#add by gjw on 20121219 导入的定时器，带有启用信息
					rule,addones=r[1].split(":")
					put_timer(r[0],rule,r[2],addones)
				except:
					put_timer(r[0],r[1],r[2])
	except:
		pass
	
	try:
		with open(ds_json) as f:
			data = json.load(f)
			for r in data:
				if r[0] not in ["PK","SN"]:
					put_key2(r[0],r[1],r[2],r[3])
	except:
		pass

	def _copytree(sour, dest):
		for child in os.listdir(sour):
			sour_child = os.path.join(sour, child)
			dest_child = os.path.join(dest, child)
			if os.path.isdir(sour_child):
				if not os.path.exists(dest_child):
					shutil.copytree(sour_child, dest_child)
				else:
					_copytree(sour_child, dest_child)
			else:
				shutil.copy(sour_child, dest_child)
	try:
		shutil.copy(login_json, "../mPig/html/bi/")
	except:
		pass
	
	
	try:
		_copytree(fea_dir_path, 'script')
		_copytree(image_dir_path, '../mPig/html/images/logo/')
		_copytree(db_dir_path, '/opt/openfbi/fbi-bin/db/tables/')
		_copytree(word_dir_path, '/opt/openfbi/workspace/temp_word/')
	except:
		pass
	
	try:
		fbi_compile_all()
	except:
		pass
	
	return "OK!"

#导入需要的ssdb数据
def imp_keys(__dd_path):
	conn = ssdb_conn()
	try:
		f = open(__dd_path)
		data = json.load(f)
		f.close()
		for k_v in data:
			for k, v in k_v.items():
				conn.set(k, v)
	except Exception as e:
		print("导入数据出错: %s" %(e))
	conn.close()
	
#导入需要的ssdb数据
def imp_users(__dd_path):
	conn = ssdb_conn()
	try:
		f = open(__dd_path)
		data = json.load(f)
		f.close()
		for k_v in data:
			for k,v in k_v.items():
				print("导入用户...%s...Done!"%(k))
				conn.hset("user",k, v)
	except Exception as e:
		print("导入用户出错: %s" %(e))
	conn.close()
	

if __name__ == '__main__':
	if len(sys.argv)<2:
		print("用法1(导入应用)： app.py  xxxx.zip")
		print("用法2(导入数据)： app.py  --data xxxx.db")
		print("用法3(导入用户)： app.py  --user xxxx.db")
		__dd_path = "/opt/openfbi/fbi-bin/db/dd1.db"
		imp_keys(__dd_path)
		exit()
	if "--data" in sys.argv:
		if len(sys.argv) <3 :
			print("用法2(导入数据)： app.py  --data xxxx.db")
			exit()
		__dd_path = sys.argv[2]
		imp_keys(__dd_path)
	elif  "--user" in sys.argv:
		if len(sys.argv) <3 :
			print("用法3(导入用户)： app.py  --user xxxx.db")
			exit()
		user_path = sys.argv[2]
		imp_users(user_path)
	else:#应用
		ret = load_app(sys.argv[1])
		print("%s 安装 %s"%(sys.argv[1],ret))
