'''
各类shell操作函数
'''

from email.headerregistry import Address
import os
import psutil
import shutil
import zipfile
import pandas as pd
import paramiko
import stat


import avenger.fsys
import sys
sys.path.append("/opt/openfbi/pylibs/")
import yaml
#import scipy
def mv(df):
	'''
	@author： yy
	@date: 2020/11/08
	@函数：mv
	@参数：df =>
			src             dest
		1   /opt/a.txt      /opt/aa/a.txt
		2   /opt/bb         /opt/aa/
	@描述：批量移动文件/目录(函数可自行创建不存在的路径)
	@返回：df表
	@示例：a=@udf df by SH.mv
	'''
	result = []
	for _, row in df.iterrows():
		src = row['src']
		dest = row['dest']
		if not os.path.exists(src):
			result.append('文件/路径<{}>不存在!'.format(src))
			continue
		if not (os.path.exists(dest) and os.path.isdir(dest)):
			destpath = os.path.split(dest)[0]
			if not os.path.exists(destpath):
				os.makedirs(destpath)
		shutil.move(src, dest)
		result.append('文件/路径<{}>移动成功!'.format(src))
	return pd.DataFrame(result, columns=['result'])


def cp(df):
	'''
	@author： yy
	@date: 2020/11/08
	@函数：cp
	@参数：df =>
			src             dest
		1   /opt/a.txt      /opt/aa/a.txt
		2   /opt/bb         /opt/aa/cc
	@描述：批量copy文件/目录(函数可自行创建不存在的路径)
	@返回：df表
	@示例：a=@udf df by SH.cp
	'''
	result = []
	for _, row in df.iterrows():
		src = row['src']
		dest = row['dest']
		if not os.path.exists(src):
			result.append('文件/目录<{}>不存在!'.format(src))
			continue
		if not (os.path.exists(dest) and os.path.isdir(dest)):
			destpath = os.path.split(dest)[0]
			if not os.path.exists(destpath):
				os.makedirs(destpath)
		if os.path.isdir(src):
			shutil.copytree(src, dest)
		else:
			shutil.copy(src, dest)
		result.append('文件/目录<{}>拷贝成功!'.format(src))
	return pd.DataFrame(result, columns=['result'])


def unzip(df):
	'''
	@author： yy
	@date: 2020/11/08
	@函数：unzip
	@参数：df =>
			src             dest        password
		1   /opt/a.zip      /opt/aa/    123
		2   /opt/b.zip      /opt/aa/    456
	@描述：批量解压zip包(支持加密解压)
	@返回：df表
	@示例：a=@udf df by SH.unzip
	'''
	result = []
	for _, row in df.iterrows():
		src = row['src']
		dest = row['dest']
		password = row.get('password')
		if not os.path.exists(src):
			result.append('文件<{}>不存在!'.format(src))
			continue
		if not os.path.exists(dest):
			os.makedirs(dest)
		try:
			with zipfile.ZipFile(src) as zf:
				if password:
					password = password.encode()
				zf.extractall(path=dest, pwd=password)
			result.append('文件<{}>解压成功!'.format(src))
		except Exception as e:
			result.append('文件<{}>解压失败,{}!'.format(src, str(e)))
	return pd.DataFrame(result, columns=['result'])


def network_cards(df):
	'''
	@author： yy
	@date: 2020/09/20
	@函数：network_cards
	@参数：无
	@描述：获取本机所有网卡信息
	@返回：df表
	@示例：a=@udf SH.network_cards
	'''
	result = []

	names = list(psutil.net_if_addrs().keys())
	for name in names:
		if name != 'lo':
			info = {
				'name': name,
				'address': '',
				'netmask': '',
				'gateway': '',
				'dns': ''
			}
			script_path = '/etc/sysconfig/network-scripts/ifcfg-{}'.format(name)
			with open(script_path, 'r') as f:
				lines = f.readlines()
				for line in lines:
					if line.startswith('IPADDR'):
						info['address'] = line.strip('\n').split('=')[-1]
					if line.startswith('NETMASK'):
						info['netmask'] = line.strip('\n').split('=')[-1]
					if line.startswith('GATEWAY'):
						info['gateway'] = line.strip('\n').split('=')[-1]
					if line.startswith('DNS1'):
						info['dns'] = line.strip('\n').split('=')[-1]
			result.append(info)

	return pd.DataFrame(result)
	
def network_cards2(df):
	'''
	@author： gjw
	@date: 2020/09/20
	@函数：network_cards
	@参数：无
	@描述：获取本机所有网卡信息,针对ubuntu18.04以上的版本
	@返回：df表
	@示例：a=@udf SH.network_cards2
	'''
	result = []
	names = list(psutil.net_if_addrs().keys())
	ifaddrs = psutil.net_if_addrs()
	try:
		file = open("/etc/netplan/50-cloud-init.yaml", 'r', encoding="utf-8")
		file_data = file.read()
		file.close()
		ndata = yaml.load(file_data)
	except:
		ndata={}
	for name in names:
		if name != 'lo':
			if "network" in ndata and "ethernets" in ndata["network"] and name in ndata["network"]["ethernets"]:
				info={}
				info["name"]=name
				Address = ndata["network"]["ethernets"][name]["addresses"] if "addresses" in ndata["network"]["ethernets"][name] else ""
				if isinstance(Address,list) and len(Address) >=2:
					#0
					info["address"] = Address[0]
					info["address6"] = Address[1]
				else:
					info["address"] = Address
				info["netmask"] = "24"
				info["gateway"] = ndata["network"]["ethernets"][name]["gateway4"] if "gateway4" in ndata["network"]["ethernets"][name] else ""
				info["gateway6"] = ndata["network"]["ethernets"][name]["gateway6"] if "gateway6" in ndata["network"]["ethernets"][name] else ""
				info["dns"] = ndata["network"]["ethernets"][name]["nameservers"]["addresses"] \
					if "nameservers" in ndata["network"]["ethernets"][name] and  \
					"addresses" in ndata["network"]["ethernets"][name]["nameservers"] \
					else ""
				result.append(info)
			else: #没在配置文件里
				info={}
				info["name"]=name
				info["address"] = ""
				for card in ifaddrs[name]:
					if card[0]==2:
						info["address"] = card[1]					
				info["netmask"] = "24"
				info["gateway"] = ""
				info["dns"] = ""
				result.append(info)

	return pd.DataFrame(result)
	

def modify_ip(df, p=''):
	'''
	@author： yy
	@date: 2020/09/20
	@函数：modify_ip
	@参数：p->网卡name,新ip,子网掩码,网关ip,dns地址
	@描述：修改指定网卡ip信息
	@返回：df表
	@示例：a=@udf SH.modify_ip with eth0,10.68.120.88,255.255.255.0,10.68.120.252,1.1.1.1
	'''
	name, ip, mask, gateway, dns = p.strip().split(',')

	# 修改network-scripts下ip配置文件
	script_path = '/etc/sysconfig/network-scripts/ifcfg-{}'.format(name)
	with open(script_path, 'r') as f:
		lines = f.readlines()
	new_script = ''
	for line in lines:
		if line.startswith('IPADDR'):
			new_script += 'IPADDR={}\n'.format(ip)
		elif line.startswith('NETMASK'):
			new_script += 'NETMASK={}\n'.format(mask)
		elif line.startswith('GATEWAY'):
			new_script += 'GATEWAY={}\n'.format(gateway)
		elif line.startswith('DNS1'):
			new_script += 'DNS1={}\n'.format(dns)
		else:
			new_script += line
	with open(script_path, 'w') as f:
		f.writelines(new_script)

	# 重启network
	os.system('service network restart')


def modify_ip2(df, p=''):
	'''
	@author： gjw
	@date: 2022/10/21
	@函数：modify_ip
	@参数：p->网卡name,新ip/24,网关ip,dns地址
	@参数：p->网卡name,新ip/24,网关ip,ipv6/64,gateway6,dns地址
	@描述：修改指定网卡ip信息，针对ubuntu18.04以上的版本
	@返回：df表
	@示例：a=@udf SH.modify_ip2 with eth0,10.68.120.88/24,10.68.120.252,1.1.1.1
	@示例：a=@udf SH.modify_ip2 with eth0,192.168.1.87/24,192.168.1.1,fe80::6833:8ff:fe24:e81c/64,fe80::6833:8ff:fe24:1,1.1.1.1
	'''
	p = p.strip()
	ss = p.split(',')
	if len(ss) == 4:
		name, ip, gateway, dns = p.split(',')
		ipv6 =""
		gateway6 =""
	elif len(ss) ==6:
		name, ip, gateway, ipv6, gateway6, dns = p.split(',')
	else:
		raise Exception("参数传递错误!")

	name = name.strip()
	ip = ip.strip()
	gateway = gateway.strip()
	ipv6 = ipv6.strip()
	gateway6 = gateway6.strip()
	dns = dns.strip()
	file = open("/etc/netplan/50-cloud-init.yaml", 'r', encoding="utf-8")
	file_data = file.read()
	file.close()
	ndata = yaml.safe_load(file_data)
	names = list(psutil.net_if_addrs().keys())
	if name.strip() not in names:
		return
	if "network" not in ndata:
		ndata["network"] = {"version":2}
	if "ethernets" not in ndata["network"]:
		ndata["network"]["ethernets"]={}
	ndata["network"]["ethernets"][name] = {"addresses":[]}
	if ip !="":
		ndata["network"]["ethernets"][name]["addresses"].append(ip)
	if ipv6 !="":
		ndata["network"]["ethernets"][name]["addresses"].append(ipv6)

	if gateway !="":
		ndata["network"]["ethernets"][name]["gateway4"] = gateway
	if gateway6 !="":
		ndata["network"]["ethernets"][name]["gateway6"] = gateway6
	if dns !="":
		ndata["network"]["ethernets"][name]["nameservers"] = {"addresses":[dns]}
	with  open("/etc/netplan/50-cloud-init.yaml", 'w+', encoding="utf-8") as f:
		yaml_dump(ndata,f,0)
	# 重启network
	os.system('netplan apply')

def add_ip2(df, p=''):
	'''
	@author： yy
	@date: 2020/09/20
	@函数：modify_ip
	@参数：p->网卡name,新ip/24
	@描述：修改指定网卡ip信息，针对ubuntu18.04以上的版本
	@返回：df表
	@示例：a=@udf SH.modify_ip with eth0,10.68.120.88
	'''
	name, ip = p.strip().split(',')
	name = name.strip()
	ip = ip.strip()
	file = open("/etc/netplan/50-cloud-init.yaml", 'r', encoding="utf-8")
	file_data = file.read()
	file.close()
	ndata = yaml.safe_load(file_data)
	names = list(psutil.net_if_addrs().keys())
	if name.strip() not in names:
		return
	if "network" not in ndata:
		ndata["network"] = {"version":2}
	if "ethernets" not in ndata["network"]:
		ndata["network"]["ethernets"]={}
	if name not in ndata["network"]["ethernets"]:
		ndata["network"]["ethernets"][name] = {"addresses":[ip]}
	else:
		ndata["network"]["ethernets"][name]["addresses"].append(ip)
	with  open("/etc/netplan/50-cloud-init.yaml", 'w+', encoding="utf-8") as f:
		yaml_dump(ndata,f,0)
	# 重启network
	os.system('netplan apply')


def del_ip2(df, p=''):
	'''
	@author： yy
	@date: 2020/09/20
	@函数：modify_ip
	@参数：p->网卡name,新ip/24
	@描述：修改指定网卡ip信息，针对ubuntu18.04以上的版本
	@返回：df表
	@示例：a=@udf SH.modify_ip with eth0,10.68.120.88
	'''
	name, ip = p.strip().split(',')
	name = name.strip()
	ip = ip.strip()
	file = open("/etc/netplan/50-cloud-init.yaml", 'r', encoding="utf-8")
	file_data = file.read()
	file.close()
	ndata = yaml.safe_load(file_data)
	names = list(psutil.net_if_addrs().keys())
	if name.strip() not in names:
		return
	if "network" not in ndata:
		ndata["network"] = {"version":2}
	if "ethernets" not in ndata["network"]:
		ndata["network"]["ethernets"]={}
	if name not in ndata["network"]["ethernets"] or ip not in ndata["network"]["ethernets"][name]["addresses"]:
		return df
	else:
		ndata["network"]["ethernets"][name]["addresses"].remove(ip)
	with  open("/etc/netplan/50-cloud-init.yaml", 'w+', encoding="utf-8") as f:
		yaml_dump(ndata,f,0)
	# 重启network
	os.system('netplan apply')

def yaml_dump(data,f,i):
	for k,v in data.items():
		f.write("  "*i)
		f.write(k+":")
		if isinstance(v,dict):
			f.write("\n")
			yaml_dump(v,f,i+1)
		elif isinstance(v,list) or isinstance(v,tuple):
			f.write("\n")
			for a in v :
				f.write("  "*(i+1))
				f.write('- "%s"\n'%(a))
		else:
			f.write("  "*(i+1))
			f.write("%s\n"%(v))
			
		


# -------------------------------------------------------------------------------------------- #
# ---------------------------------这边开始是对远程主机进行的操作--------------------------------- #
# -------------------------------------------------------------------------------------------- #
def scp_from(df, p=''):
	'''
	@author： yy
	@date: 2020/09/26
	@函数：scp_from
	@参数：df
			from            to
			/opt/aa.json    /data/aa.json
			/opt/test       /data/test
			/opt/bb.json    /data

		  p->主机ip,主机port,登陆账号,登陆密码
	@描述：从远程主机下载文件当本机
	@返回：df表
	@示例：a=@udf df by SH.scp_from with 10.68.120.88,22,xx,xx
	'''
	params = p.strip().split(',')
	if len(params) == 1:
		host, port, username, password = get_key(params[0]).split(',')
	elif len(params) == 3:
		host, port, authkey = params
		authkey = get_key(authkey)
		username, password = authkey.split(',')
	else:
		host, port, username, password = params

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, int(port), username=username, password=password)
	ftp = client.open_sftp()

	def _download(frm, to, rec=-1):
		try:
			st_mode = ftp.stat(frm).st_mode
		except IOError:
			return
		if stat.S_ISDIR(st_mode):
			childs = ftp.listdir(frm)
			rec += 1
			for child in childs:
				child_path = os.path.join(frm, child)
				_download(child_path, to, rec)
		else:
			frm_path, frm_fn = os.path.split(frm)
			if rec >= 1:
				curdir = os.path.join(to, *frm_path.split('/')[-rec:])
				if not os.path.exists(curdir):
					os.makedirs(curdir, exist_ok=True)
				to = os.path.join(curdir, frm_fn)
			elif os.path.isdir(to):
				to = os.path.join(to, frm_fn)
			ftp.get(frm, to)

	for _, row in df.iterrows():
		frm = row['from']
		to = row['to']
		_download(frm, to)

	ftp.close()
	client.close()


def scp_to(df, p=''):
	'''
	@author： yy
	@date: 2020/09/26
	@函数：scp_to
	@参数：df
			from            to
			/opt/aa.json    /data/aa.json
			/opt/test       /data/test
			/opt/bb.json    /data

		  p->主机ip,主机port,登陆账号,登陆密码
	@描述：将本机文件上传到远程服务器
	@返回：df表
	@示例：a=@udf df by SH.scp_to with 10.68.120.88,22,xx,xx
	'''
	params = p.strip().split(',')
	if len(params) == 1:
		host, port, username, password = get_key(params[0]).split(',')
	elif len(params) == 3:
		host, port, authkey = params
		authkey = get_key(authkey)
		username, password = authkey.split(',')
	else:
		host, port, username, password = params

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, int(port), username=username, password=password)
	ftp = client.open_sftp()

	def _upload(frm, to, rec=-1):
		if not os.path.exists(frm):
			return
		if os.path.isdir(frm):
			childs = os.listdir(frm)
			rec += 1
			for child in childs:
				child_path = os.path.join(frm, child)
				_upload(child_path, to, rec)
		else:
			frm_path, frm_fn = os.path.split(frm)
			if rec >= 1:
				curdir = os.path.join(to, *frm_path.split('/')[-rec:])
				try:
					ftp.stat(curdir)
				except IOError:
					# exec_command需要时间执行
					client.exec_command('mkdir -p {}'.format(curdir))
					while True:
						try:
							ftp.stat(curdir)
						except IOError:
							continue
						else:
							break
				to = os.path.join(curdir, frm_fn)
			elif stat.S_ISDIR(ftp.stat(to).st_mode):
				to = os.path.join(to, frm_fn)
			ftp.put(frm, to)

	for _, row in df.iterrows():
		frm = row['from']
		to = row['to']
		_upload(frm, to)

	ftp.close()
	client.close()


def sls(df, p=''):
	'''
	@author： yy
	@date: 2020/09/27
	@函数：sls
	@参数：p->主机ip,主机port,登陆账号,登陆密码,远程路径
	@描述：查看远程主机上的指定路径下的内容
	@返回：df表
	@示例：a=@udf SH.sls with 10.68.120.88,22,xx,xx,/opt
	'''
	params = p.strip().split(',')
	if len(params) == 2:
		loginkey, path = params
		host, port, username, password = get_key(loginkey).split(',')
	elif len(params) == 4:
		host, port, authkey, path = params
		authkey = get_key(authkey)
		username, password = authkey.split(',')
	else:
		host, port, username, password, path = params

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(host, int(port), username=username, password=password)
	ftp = client.open_sftp()
	result = ftp.listdir(path)
	ftp.close()
	client.close()

	return pd.DataFrame(result, columns=['result'])















