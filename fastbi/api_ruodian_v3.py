#/opt/fbi-base/bin/python
# -*- coding: utf-8 -*- 
#FBI脚本的py文件
#filename: api_ruodian
#datetime: 2024-08-30T16:10:54.414852
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
		add_the_error('[api_ruodian.fbi]执行第[5]原语 use @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_num', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select count(*) as num from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[api_ruodian.fbi]执行第[7]原语 api19_num = load db by mysql1 with select count(*)... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api_num', 'Action': 'eval', 'eval': 'api19_num', 'by': 'iloc[0,0]'}
	try:
		eval_df(ptree)
	except Exception as e:
		add_the_error('[api_ruodian.fbi]执行第[8]原语 api_num = eval api19_num by iloc[0,0] 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'if', 'if': '$api_num == 0', 'with': '""\napi19_type = @udf udf0.new_df with type,type1,type2,level,weakness,possibility,influence,advise\napi19_type = @udf api19_type by udf0.df_append with (API19-1-1,参数可遍历,API19-1失效的对象认证,中,前后台交互通过改变链接中的参数值来控制API返回不同用户数据，但是因为没有完善的权限控制机制，导致了攻击者可以通过修改参数值来遍历用户数据，从而造成敏感信息泄漏。,在传输过程中进行拦截监听，容易被拦截者修改参数获取并恶意篡改用户数据，导致敏感信息泄露。,在传输过程中可以直接修改参数值来遍历用户所有数据。,1.基于用户策略和继承关系来实现适当的授权机制；2.不要依赖客户端发送的ID，改用存储在会话对象中的ID；3.检查每个客户端访问数据库的请求授权；4.使用无法猜测的随机参数。)\napi19_type = @udf api19_type by udf0.df_append with (API19-1-2,对象可猜测,API19-1失效的对象认证,中,前后台交互发送请求链接，攻击者识别拦截到并通过另一个端点获取到不同用户数据，从而造成敏感信息泄漏。,在在传输过程中攻击者识别进行拦截，通过其它端点修改url获取到用户数据，导致敏感信息泄露。,可直接识别到url获取到用户数据，敏感信息全部泄露。,1.基于用户策略和继承关系来实现适当的授权机制；2.不要依赖客户端发送的ID，改用存储在会话对象中的ID；3.检查每个客户端访问数据库的请求授权；4.使用无法猜测的随机参数。)\napi19_type = @udf api19_type by udf0.df_append with (API19-2-1,Basic认证,API19-2失效的用户认证,中,BASIC 认证虽然采用 Base64 密码方式，但这不是加密处理。不需要任何附加信息即可对其进行解码。,信息传输过程中容易被攻击者窃听，密码无加密且容易被盗取。,信息传输过程中获取到用户认证信息，所有数据全部暴漏。,可通过HTTPS协议和密码加密来保证信息传输的安全。)\napi19_type = @udf api19_type by udf0.df_append with (API19-2-2,明文密码认证,API19-2失效的用户认证,中,容易被攻击者得到用户的密码冒充身份得到认证获取用户信息并进行恶意篡改。同时传输过程中被会被恶意拦截到从而让攻击者获取到真实密码。,信息传输过程中容易被攻击者恶意拦截获取密码，用户信息容易被盗取。,信息传输过程中攻击者获取真实密码，得到所有用户权限。,BASE64、AES常用算法进行明文密码加密。)\napi19_type = @udf api19_type by udf0.df_append with (API19-2-3,数据接口无认证,API19-2失效的用户认证,中,较弱的API身份验证允许攻击者冒充其他用户的身份。,信息传输过程中易被攻击者获取到真实用户凭据，导致用户信息泄露。,信息传输过程中攻击者获取到真实用户凭据，获取查看用户信息。,检查所有可能的方式来对所有API进行身份验证· 使用标准身份验证、令牌生成、密码存储和多因素身份验证 (MFA)· 使用短期访问令牌· 验证您的应用程序对身份验证使用更严格的速率限制，并实施锁定策略和弱密码检查。)\napi19_type = @udf api19_type by udf0.df_append with (API19-3-1,单次返回数据量过大,API19-3过度的数据暴露,中,接收的数据量过于巨大，完整接收将导致内存溢出；其次数据过多存在敏感数据导致信息泄露。,信息传输过程中易被攻击者获取到用户真实敏感数据，导致用户大量敏感信息泄露。,攻击者拦截获取到用户真实敏感数据，敏感数据泄露。,数据分批次获取并进行整合并做删减处理，对相应的字段进行扩大处理。)\napi19_type = @udf api19_type by udf0.df_append with (API19-3-2,单次返回数据类型过多,API19-3过度的数据暴露,中,信息传输过程中易被攻击者获取到用户真实敏感数据，导致用户大量敏感信息泄露。,信息传输过程中数据类型过多特别容易被攻击者识别出API，并进行用户数据收集，导致太多数据被暴露。,信息传输过程中被攻击者恶意拦截监听，识别出API，并进行用户数据收集。,内容范围限制关键数据的传输，并使数据结构未知。)\napi19_type = @udf api19_type by udf0.df_append with (API19-3-3,返回数据量可修改,API19-3过度的数据暴露,中,信息传输过程中易被攻击者获取到大量用户真实敏感数据，导致用户大量敏感信息泄露，并产生合规风险。,信息传输过程中容易被攻击者获取用户额外数据，对用户数据进行收集，产生泄露风险。,信息传输过程中被攻击者识别出API直接获取用户额外数据并及进行收集，敏感数据大量泄露。,内容范围限制为必需内容。)\napi19_type = @udf api19_type by udf0.df_append with (API19-3-4,返回数据波动过大,API19-3过度的数据暴露,中,容易造成个人信息的过度收集和敏感信息的暴露。,信息传输过程中容易被攻击者获取用户敏感数据，容易对用户数据进行收集产生泄露风险。,信息传输过程中被攻击者识别出api请求，并获取用户敏感数据并收集，用户信息泄露。,对Web服务器的API请求应尽可能地被混淆和控制，限制API被调用的次数上限，与“时长”配合使用。)\napi19_type = @udf api19_type by udf0.df_append with (API19-4-1,单个接口访问频率过高,API19-4资源缺乏或速率限制,中,API对用户可以请求的资源的大小或数量没有任何限制。这不仅会影响API服务器的性能，导致拒绝服务，而且还为暴力等验证缺陷敞开大门。,导致API将无法响应该客户端的其他请求，或其他客户端的请求。,频繁发送请求会导致出现性能问题，形成DoS。,对用户调用API的频率执行明确的时间窗口限制，在突破限制时通知客户，并提供限制数量及限制重置的时间。)\napi19_type = @udf api19_type by udf0.df_append with (API19-4-2,单个IP访问频率过高,API19-4资源缺乏或速率限制,中,用户访问请求没有任何限制容易产生数据泄露。,API将无法响应用户请求，缓存溢出报错。,出现溢出报错，导致用户无法请求获取数据，被攻击者恶意识别导致信息暴漏。,限制客户端在定义的时间范围内调用API的频率。)\napi19_type = @udf api19_type by udf0.df_append with (API19-4-3,响应时间波动过大,API19-4资源缺乏或速率限制,中,接口请求响应时间波动过大容易请求阻塞。,在传输过程中可能出现阻塞容易被攻击。,会导致用户数据被盗。,限制有效载荷大小。)\napi19_type = @udf api19_type by udf0.df_append with (API19-7-1,跨域访问,API19-7安全配置不当,中,无法读取同源网页的cookies、LocalStorage和IndexedDB；无法解除非同源网页的DOM；无法向非同源网页发送AJAX请求。,可以获取到用户的cookie信息或者劫持用户跳转到其它的网站。,获取到用户的个人信息进行请求访问，导致信息泄露。,确定API只能被特定HTTP方法访问，其他的HTTP方法访问都应该被禁止，API应该实现正确的CORS（跨域资源共享）策略。)\napi19_type = @udf api19_type by udf0.df_append with (API19-7-2,cookie中保存密码,API19-7安全配置不当,中,会轻易从这个cookie里获得用户是否登录的信息，从而达到记录状态，导致用户登陆密码泄露。,传输过程中进行监听拦截直接获取真实密码，被利用性极高。,传输过程中通过真实密码登录拥有用户所有权限，获取用户信息导致泄露。,可以使用https协议进行传输。)\n#api19_type = @udf api19_type by udf0.df_append with (API19-7-3,公网暴露,API19-7安全配置不当,中,容易被恶意扫描和利用，安全风险性更高。,用户信息直接开放，泄露敏感数据风险极高。,服务器完全被控制，可直接调用用户信息。,使用HTTPS协议，增加安全补丁，严格检查所有与验证和权限有关的设定。)\napi19_type = @udf api19_type by udf0.df_append with (API19-7-3,Basic认证在公网暴露,API19-7安全配置不当,中,容易被恶意利用获取到更高的权限，安全风险性更高。,暴露存储或服务器管理面板，泄露权限风险极高。,服务器完全被控制，可直接获取权限。,禁用不必要的功能，自动化安装部署，在所有环境中自动监控和验证安全配置的有效性，实时解决安全问题。)\napi19_type = @udf api19_type by udf0.df_append with (API19-7-4,不安全的直接对象访问,API19-7安全配置不当,中,服务器上具体文件名、路径或数据库关键字等内部资源被暴露在URL或网页中。,攻击者可以此来尝试直接访问其他资源。,恶意访问到内部资源获取内部信息，所有信息全部暴漏。,避免在URL或网页中直接引用内部文件名或数据库关键字；可以使用自定义的映射名称来取代直接对象名；锁定网站服务器上的所有目录和文件夹，设置访问权限；验证用户输入的URL请求，拒绝包含./或.//的请求。)\napi19_type = @udf api19_type by udf0.df_append with (API19-7-5,敏感数据公网暴露,API19-7安全配置不当,中,容易被恶意扫描和利用，安全风险性更高。,用户信息直接开放，泄露敏感数据风险极高。,客户端完全被控制，可直接调用所有敏感信息。,使用HTTPS协议，增加安全补丁，不显示过多的敏感信息的详细错误消息，严格检查所有与验证和权限有关的设定。)\napi19_type = @udf api19_type by udf0.df_append with (API19-8-1,SQL查询接口,API19-8注入,中,web应用程序对用户输入数据的合法性没有判断或过滤不严，攻击者可以在web应用程序中事先定义好的查询语句的结尾上添加额外的SQL语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意查询，从而进一步得到相应的数据信息。,数据传输过程中易被攻击者非授权的恶意查询从而得到用户信息导致信息泄露。,数据传输过程中，攻击者可以恶意查询用户信息，导致信息泄露。,对SQL语法的深度解析，检测SQL语句会造成数据安全威胁的异常情况。)\napi19_type = @udf api19_type by udf0.df_append with (API19-8-2,SQL执行接口,API19-8注入,中,web应用程序对用户输入数据的合法性没有判断或过滤不严，攻击者可以在web应用程序中事先定义好的执行语句的结尾上添加额外的SQL语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意操作数据，从而修改用户相应的数据信息。,数据传输过程中易被攻击者非授权的恶意修改用户信息导致信息篡改及泄露。,攻击者可以恶意修改用户信息或者获取用户数据之后进行恶意删除。,对SQL语法的深度解析，检测SQL语句会造成数据安全威胁的异常情况。)\napi19_type_1 = load db by mysql1 with select id,type from api19_type\napi19_type_0 = join api19_type_1,api19_type by type,type with right\n##筛除id为空时，数据新增 id不为空时，数据更新\napi19_type_0 = @udf api19_type_0 by udf0.df_fillna\napi19_type_new = filter api19_type_0 by id == \'\'\napi19_type_new = add id by 0\napi19_type = filter api19_type_0 by id != \'\'\napi19_type = union api19_type,api19_type_new\napi19_type = @udf api19_type by udf0.df_set_index with id\napi19_type_2 = @udf api19_type by CRUD.save_table with (mysql1,api19_type)\n""'}
	ptree['if'] = deal_sdf(workspace,ptree['if'])
	ptree['with'] = replace_ps(ptree['with'],runtime)
	try:
		ptree['lineno']=9
		ptree['funs']=block_if_9
		if_fun(ptree)
		if t.ident in global_tasks and 'Exit' in global_tasks[t.ident]: 
			add_the_error('Exit终止运行!')
			return errors,-1
		if t.ident in global_tasks and 'Break' in global_tasks[t.ident]: 
			return errors,-1
	except Exception as e:
		add_the_error('[api_ruodian.fbi]执行第[9]原语 if $api_num == 0 with "api19_type = @udf udf0.new_... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, 'Action': 'clear', 'clear': '@FID'}
	ptree['clear'] = replace_ps(ptree['clear'],runtime)
	try:
		clear_fun(ptree)
	except Exception as e:
		add_the_error('[api_ruodian.fbi]执行第[49]原语 clear @FID 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	return global_tasks[t.ident]['errors'],49

#主函数结束,开始块函数

def block_if_9(ptree):

	if "runtime" not in ptree:
		runtime = FbiRunTime("fastbi")
		fbi_global.put_runtime(runtime)
	else:
		runtime = ptree["runtime"]

	workspace=''
	t = threading.current_thread()
	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'udf0.new_df', 'with': 'type,type1,type2,level,weakness,possibility,influence,advise'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[10]原语 api19_type = @udf udf0.new_df with type,type1,type... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-1-1,参数可遍历,API19-1失效的对象认证,中,前后台交互通过改变链接中的参数值来控制API返回不同用户数据，但是因为没有完善的权限控制机制，导致了攻击者可以通过修改参数值来遍历用户数据，从而造成敏感信息泄漏。,在传输过程中进行拦截监听，容易被拦截者修改参数获取并恶意篡改用户数据，导致敏感信息泄露。,在传输过程中可以直接修改参数值来遍历用户所有数据。,1.基于用户策略和继承关系来实现适当的授权机制；2.不要依赖客户端发送的ID，改用存储在会话对象中的ID；3.检查每个客户端访问数据库的请求授权；4.使用无法猜测的随机参数。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[11]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-1-2,对象可猜测,API19-1失效的对象认证,中,前后台交互发送请求链接，攻击者识别拦截到并通过另一个端点获取到不同用户数据，从而造成敏感信息泄漏。,在在传输过程中攻击者识别进行拦截，通过其它端点修改url获取到用户数据，导致敏感信息泄露。,可直接识别到url获取到用户数据，敏感信息全部泄露。,1.基于用户策略和继承关系来实现适当的授权机制；2.不要依赖客户端发送的ID，改用存储在会话对象中的ID；3.检查每个客户端访问数据库的请求授权；4.使用无法猜测的随机参数。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[12]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-2-1,Basic认证,API19-2失效的用户认证,中,BASIC 认证虽然采用 Base64 密码方式，但这不是加密处理。不需要任何附加信息即可对其进行解码。,信息传输过程中容易被攻击者窃听，密码无加密且容易被盗取。,信息传输过程中获取到用户认证信息，所有数据全部暴漏。,可通过HTTPS协议和密码加密来保证信息传输的安全。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[13]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-2-2,明文密码认证,API19-2失效的用户认证,中,容易被攻击者得到用户的密码冒充身份得到认证获取用户信息并进行恶意篡改。同时传输过程中被会被恶意拦截到从而让攻击者获取到真实密码。,信息传输过程中容易被攻击者恶意拦截获取密码，用户信息容易被盗取。,信息传输过程中攻击者获取真实密码，得到所有用户权限。,BASE64、AES常用算法进行明文密码加密。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[14]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-2-3,数据接口无认证,API19-2失效的用户认证,中,较弱的API身份验证允许攻击者冒充其他用户的身份。,信息传输过程中易被攻击者获取到真实用户凭据，导致用户信息泄露。,信息传输过程中攻击者获取到真实用户凭据，获取查看用户信息。,检查所有可能的方式来对所有API进行身份验证· 使用标准身份验证、令牌生成、密码存储和多因素身份验证 (MFA)· 使用短期访问令牌· 验证您的应用程序对身份验证使用更严格的速率限制，并实施锁定策略和弱密码检查。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[15]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-3-1,单次返回数据量过大,API19-3过度的数据暴露,中,接收的数据量过于巨大，完整接收将导致内存溢出；其次数据过多存在敏感数据导致信息泄露。,信息传输过程中易被攻击者获取到用户真实敏感数据，导致用户大量敏感信息泄露。,攻击者拦截获取到用户真实敏感数据，敏感数据泄露。,数据分批次获取并进行整合并做删减处理，对相应的字段进行扩大处理。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[16]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-3-2,单次返回数据类型过多,API19-3过度的数据暴露,中,信息传输过程中易被攻击者获取到用户真实敏感数据，导致用户大量敏感信息泄露。,信息传输过程中数据类型过多特别容易被攻击者识别出API，并进行用户数据收集，导致太多数据被暴露。,信息传输过程中被攻击者恶意拦截监听，识别出API，并进行用户数据收集。,内容范围限制关键数据的传输，并使数据结构未知。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[17]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-3-3,返回数据量可修改,API19-3过度的数据暴露,中,信息传输过程中易被攻击者获取到大量用户真实敏感数据，导致用户大量敏感信息泄露，并产生合规风险。,信息传输过程中容易被攻击者获取用户额外数据，对用户数据进行收集，产生泄露风险。,信息传输过程中被攻击者识别出API直接获取用户额外数据并及进行收集，敏感数据大量泄露。,内容范围限制为必需内容。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[18]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-3-4,返回数据波动过大,API19-3过度的数据暴露,中,容易造成个人信息的过度收集和敏感信息的暴露。,信息传输过程中容易被攻击者获取用户敏感数据，容易对用户数据进行收集产生泄露风险。,信息传输过程中被攻击者识别出api请求，并获取用户敏感数据并收集，用户信息泄露。,对Web服务器的API请求应尽可能地被混淆和控制，限制API被调用的次数上限，与“时长”配合使用。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[19]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-4-1,单个接口访问频率过高,API19-4资源缺乏或速率限制,中,API对用户可以请求的资源的大小或数量没有任何限制。这不仅会影响API服务器的性能，导致拒绝服务，而且还为暴力等验证缺陷敞开大门。,导致API将无法响应该客户端的其他请求，或其他客户端的请求。,频繁发送请求会导致出现性能问题，形成DoS。,对用户调用API的频率执行明确的时间窗口限制，在突破限制时通知客户，并提供限制数量及限制重置的时间。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[20]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-4-2,单个IP访问频率过高,API19-4资源缺乏或速率限制,中,用户访问请求没有任何限制容易产生数据泄露。,API将无法响应用户请求，缓存溢出报错。,出现溢出报错，导致用户无法请求获取数据，被攻击者恶意识别导致信息暴漏。,限制客户端在定义的时间范围内调用API的频率。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[21]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-4-3,响应时间波动过大,API19-4资源缺乏或速率限制,中,接口请求响应时间波动过大容易请求阻塞。,在传输过程中可能出现阻塞容易被攻击。,会导致用户数据被盗。,限制有效载荷大小。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[22]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-7-1,跨域访问,API19-7安全配置不当,中,无法读取同源网页的cookies、LocalStorage和IndexedDB；无法解除非同源网页的DOM；无法向非同源网页发送AJAX请求。,可以获取到用户的cookie信息或者劫持用户跳转到其它的网站。,获取到用户的个人信息进行请求访问，导致信息泄露。,确定API只能被特定HTTP方法访问，其他的HTTP方法访问都应该被禁止，API应该实现正确的CORS（跨域资源共享）策略。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[23]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-7-2,cookie中保存密码,API19-7安全配置不当,中,会轻易从这个cookie里获得用户是否登录的信息，从而达到记录状态，导致用户登陆密码泄露。,传输过程中进行监听拦截直接获取真实密码，被利用性极高。,传输过程中通过真实密码登录拥有用户所有权限，获取用户信息导致泄露。,可以使用https协议进行传输。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[24]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-7-3,Basic认证在公网暴露,API19-7安全配置不当,中,容易被恶意利用获取到更高的权限，安全风险性更高。,暴露存储或服务器管理面板，泄露权限风险极高。,服务器完全被控制，可直接获取权限。,禁用不必要的功能，自动化安装部署，在所有环境中自动监控和验证安全配置的有效性，实时解决安全问题。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[26]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-7-4,不安全的直接对象访问,API19-7安全配置不当,中,服务器上具体文件名、路径或数据库关键字等内部资源被暴露在URL或网页中。,攻击者可以此来尝试直接访问其他资源。,恶意访问到内部资源获取内部信息，所有信息全部暴漏。,避免在URL或网页中直接引用内部文件名或数据库关键字；可以使用自定义的映射名称来取代直接对象名；锁定网站服务器上的所有目录和文件夹，设置访问权限；验证用户输入的URL请求，拒绝包含./或.//的请求。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[27]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-7-5,敏感数据公网暴露,API19-7安全配置不当,中,容易被恶意扫描和利用，安全风险性更高。,用户信息直接开放，泄露敏感数据风险极高。,客户端完全被控制，可直接调用所有敏感信息。,使用HTTPS协议，增加安全补丁，不显示过多的敏感信息的详细错误消息，严格检查所有与验证和权限有关的设定。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[28]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-8-1,SQL查询接口,API19-8注入,中,web应用程序对用户输入数据的合法性没有判断或过滤不严，攻击者可以在web应用程序中事先定义好的查询语句的结尾上添加额外的SQL语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意查询，从而进一步得到相应的数据信息。,数据传输过程中易被攻击者非授权的恶意查询从而得到用户信息导致信息泄露。,数据传输过程中，攻击者可以恶意查询用户信息，导致信息泄露。,对SQL语法的深度解析，检测SQL语句会造成数据安全威胁的异常情况。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[29]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_append', 'with': 'API19-8-2,SQL执行接口,API19-8注入,中,web应用程序对用户输入数据的合法性没有判断或过滤不严，攻击者可以在web应用程序中事先定义好的执行语句的结尾上添加额外的SQL语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意操作数据，从而修改用户相应的数据信息。,数据传输过程中易被攻击者非授权的恶意修改用户信息导致信息篡改及泄露。,攻击者可以恶意修改用户信息或者获取用户数据之后进行恶意删除。,对SQL语法的深度解析，检测SQL语句会造成数据安全威胁的异常情况。'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[30]原语 api19_type = @udf api19_type by udf0.df_append wit... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '=', 'Ta': 'api19_type_1', 'Action': 'load', 'load': 'db', 'by': 'mysql1', 'with': 'select id,type from api19_type'}
	try:
		load_data(ptree)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[31]原语 api19_type_1 = load db by mysql1 with select id,ty... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= join', 'Ta': 'api19_type_0', 'Action': 'join', 'join': 'api19_type_1,api19_type', 'by': 'type,type', 'with': 'right'}
	try:
		join_by(ptree)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[32]原语 api19_type_0 = join api19_type_1,api19_type by typ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type_0', 'Action': '@udf', '@udf': 'api19_type_0', 'by': 'udf0.df_fillna'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[34]原语 api19_type_0 = @udf api19_type_0 by udf0.df_fillna... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_type_new', 'Action': 'filter', 'filter': 'api19_type_0', 'by': "id == ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[35]原语 api19_type_new = filter api19_type_0 by id == "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= add', 'Ta': 'api19_type_new', 'Action': 'add', 'add': 'id', 'by': '0'}
	try:
		add_col(ptree)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[36]原语 api19_type_new = add id by 0 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= filter', 'Ta': 'api19_type', 'Action': 'filter', 'filter': 'api19_type_0', 'by': "id != ''"}
	try:
		filter_query(ptree)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[37]原语 api19_type = filter api19_type_0 by id != "" 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= union', 'Ta': 'api19_type', 'Action': 'union', 'union': 'api19_type,api19_type_new'}
	try:
		union(ptree)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[38]原语 api19_type = union api19_type,api19_type_new 出错, 原因: <font color="#FF9900">'+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type', 'Action': '@udf', '@udf': 'api19_type', 'by': 'udf0.df_set_index', 'with': 'id'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[39]原语 api19_type = @udf api19_type by udf0.df_set_index ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

	ptree={'runtime': runtime, '': '= @udf', 'Ta': 'api19_type_2', 'Action': '@udf', '@udf': 'api19_type', 'by': 'CRUD.save_table', 'with': 'mysql1,api19_type'}
	try:
		ret = udf_func(ptree,2)
	except Exception as e:
		add_the_error('[第9行if语句中]执行第[40]原语 api19_type_2 = @udf api19_type by CRUD.save_table ... 出错, 原因: <font color="#FF9900"> '+e.__str__()+'</font>')

#end block_if_9

if __name__ =="__main__":
	b=time.time()
	errors,count =fbi_main({"work_space":"public"})
	print("原语数量: %s"%(count))
	print("耗时(秒): %s"%(time.time()-b))
	print("ERROR: %s"%(len(errors)))
	for e in errors:
		print(e)



