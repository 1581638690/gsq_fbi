import json
import random
import re
import subprocess
import sys
import os
import time

import psutil

sys.path.append("./")
sys.path.append("./lib")
sys.path.append("../lib")
sys.path.append("./driver")
sys.path.append("/opt/openfbi/pylibs")

import pandas as pd
import numpy as np
from pysnmp.entity.engine import SnmpEngine
from pysnmp.entity.rfc3413.oneliner import cmdgen
# from pysnmp.entity.rfc3413.oneliner.cmdgen import CommandGenerator
from pysnmp.hlapi import *
from pysnmp.proto import rfc1902
from pysnmp.proto.rfc1902 import ObjectName
from pysnmp.smi.rfc1902 import NotificationType, ObjectIdentity
import subprocess


# usmHMACMD5AuthProtocol - MD5 hashing
#
# usmHMACSHAAuthProtocol - SHA hashing
#
# usmNoAuthProtocol - no authentication
#
# usmDESPrivProtocol - DES encryption
#
# usm3DESEDEPrivProtocol - triple-DES encryption
#
# usmAesCfb128Protocol - AES encryption, 128-bit
#
# usmAesCfb192Protocol - AES encryption, 192-bit
#
# usmAesCfb256Protocol - AES encryption, 256-bit
#
# usmNoPrivProtocol - no encryption


def get(df, p=''):
    ip, oid = p.strip().split(",")
    ip = ip.strip()
    oid = oid.strip()
    # if oid[0] != '.':
    #     oid = '.'+oid
    list1 = []
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
        cmdgen.CommunityData('myagent', 'public', 1),
        # cmdgen.UdpTransportTarget(('172.23.248.132', 161)),
        cmdgen.UdpTransportTarget((ip, 161)),
        oid.strip()
    )
    if errorStatus == 0:
        # print(errorIndication, errorStatus, errorIndex, varBinds)
        tmp = varBinds[0][1]
        list1.append(str(tmp))
        # df1.columns = ['Result']
        # return df1
    else:
        list1.append(f'Error,{errorIndication}')
        # df1.columns = ['Result']
        # return df1
    df1 = pd.DataFrame([list1])
    df1 = df1.T
    df1.columns = ['Result']
    return df1


def walk(df, p=''):
    ip, oid = p.strip().split(",")
    ip = ip.strip()
    oid = oid.strip()
    if oid[0] != '.':
        oid = '.' + oid
    errorIndication, errorStatus, errorIndex, varBindsTable = cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('myagent', 'public'),
        # cmdgen.UdpTransportTarget(('172.23.248.132', 161)),
        cmdgen.UdpTransportTarget((ip, 161)),
        oid.strip(),
    )
    # print(type(errorStatus))
    if str(errorStatus) == "noError":
        list1 = []
        for varBindsRow in varBindsTable:
            for item in varBindsRow:
                # print(item[1])
                list1.append(str(item[1]))
        df1 = pd.DataFrame(list1)
        df1.columns = ['Result']
        return df1
    else:
        return pd.DataFrame([f'Error,{errorStatus}'])


def send(df, p=''):
    ip, oid, = p.strip().split(",")
    ip = ip.strip()
    oid = oid.strip()
    g = sendNotification(
        SnmpEngine(),
        CommunityData('myagent', 'public', 1),
        UdpTransportTarget((ip, 162)),
        ContextData(),
        'trap test',
        # (ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), rfc1902.OctetString("testest"))
        NotificationType(ObjectIdentity(ObjectName(oid)), "testest"),
        # NotificationType(ObjectIdentity('SNMPv2-MIB', 'sysDescr'), "testest")
    )
    res = next(g)
    return 0


def getv3(df, p=''):
    ip, oid, user, Apwd, Xpwd, aP, pP = p.strip().split(",")
    ip = ip.strip()
    oid = oid.strip()
    user = user.strip()
    Apwd = Apwd.strip()
    Xpwd = Xpwd.strip()
    aP = aP.strip()
    pP = pP.strip()
    auth_dict = {'MD5': usmHMACMD5AuthProtocol,
                 'SHA': usmHMACSHAAuthProtocol,
                 'no': usmNoAuthProtocol,
                 }
    protocol_dict = {'DES': usmDESPrivProtocol,
                     'triple-DES': usm3DESEDEPrivProtocol,
                     'AES128': usmAesCfb128Protocol,
                     'AES192': usmAesCfb192Protocol,
                     'AES256': usmAesCfb256Protocol,
                     'no': usmNoPrivProtocol}
    aP = auth_dict.get(aP)
    pP = protocol_dict.get(pP)

    if oid[0] != '.':
        oid = '.' + oid
    list1 = []
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
        UsmUserData(user, Apwd, Xpwd, authProtocol=aP, privProtocol=pP),
        # cmdgen.CommunityData('public', 1),
        # cmdgen.UdpTransportTarget(('172.23.248.132', 161)),
        cmdgen.UdpTransportTarget((ip, 161)),
        oid.strip()
    )
    if errorStatus == 0:
        # print(errorIndication, errorStatus, errorIndex, varBinds)
        tmp = varBinds[0][1]
        list1.append(str(tmp))
        # df1.columns = ['Result']
        # return df1
    else:
        list1.append(f'Error,{errorIndication}')
        # df1.columns = ['Result']
        # return df1
    df1 = pd.DataFrame([list1])
    df1 = df1.T
    df1.columns = ['Result']
    return df1


def walkv3(df, p=''):
    ip, oid, user, Apwd, Xpwd, aP, pP = p.strip().split(",")
    ip = ip.strip()
    oid = oid.strip()
    user = user.strip()
    Apwd = Apwd.strip()
    Xpwd = Xpwd.strip()
    aP = aP.strip()
    pP = pP.strip()
    auth_dict = {'MD5': usmHMACMD5AuthProtocol,
                 'SHA': usmHMACSHAAuthProtocol,
                 'no': usmNoAuthProtocol,
                 }
    protocol_dict = {'DES': usmDESPrivProtocol,
                     'triple-DES': usm3DESEDEPrivProtocol,
                     'AES128': usmAesCfb128Protocol,
                     'AES192': usmAesCfb192Protocol,
                     'AES256': usmAesCfb256Protocol,
                     'no': usmNoPrivProtocol}
    aP = auth_dict.get(aP)
    pP = protocol_dict.get(pP)
    if oid[0] != '.':
        oid = '.' + oid
    errorIndication, errorStatus, errorIndex, varBindsTable = cmdgen.CommandGenerator().nextCmd(
        UsmUserData(user, Apwd, Xpwd, authProtocol=aP, privProtocol=pP),
        cmdgen.CommunityData('myagent', 'public'),
        # cmdgen.UdpTransportTarget(('172.23.248.132', 161)),
        cmdgen.UdpTransportTarget((ip, 161)),
        oid.strip()
    )
    # print(type(errorStatus))
    if str(errorStatus) == "noError":
        list1 = []
        for varBindsRow in varBindsTable:
            for item in varBindsRow:
                # print(item[1])
                list1.append(str(item[1]))
        df1 = pd.DataFrame(list1)
        df1.columns = ['Result']
        return df1
    else:
        return pd.DataFrame([f'Error,{errorStatus}'])


#
# def send_v3(df,p=''):
#     p = p.strip()
#     ip, oid = p.split(',')
#     g = sendNotification(
#         SnmpEngine(),
#         CommunityData('myagent', 'public', 1),
#         UdpTransportTarget(('172.23.254.32', 162)),
#         ContextData(),
#         'trap',
#         NotificationType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), 'test')
#     )
#     return next(g)

def config_save(dic, p=''):
    p = p.strip()

    # os.system("ps -ef | grep new_snmp_pyagentx3 | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9")
    res = subprocess.call("ps -ef | grep new_snmp_pyagentx3 | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9",
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # pids = [(x, psutil.Process(x).cmdline()) for x in psutil.pids() if psutil.pid_exists(x)]
    # for pid, cmdline in pids:
    #     # p = psutil.Process(pid)
    #     if 'udf/new_snmp_pyagentx3.py' in cmdline or 'udf/snmp_trap.py' in cmdline:
    #         res = subprocess.Popen(["kill", "-9", f"{pid}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #         output = res.stdout

    dicv2 = dic['snmp']['snmp_service_v2']
    dicv3 = dic['snmp']['snmp_service_v3']
    res = subprocess.call("sudo systemctl stop snmpd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # result = res.stdout
    # time.sleep(1)
    group = dicv2['snmp_group']
    try:
        # with open(r"/etc/snmp/snmpd.conf", 'a+') as f:
        #     f.write(f"\n\rrocommunity {group} default -V systemonly\n")
        #     f.close()
        # os.system("sudo chmod 777 /etc/snmp/snmpd.conf")
        res = subprocess.call("sudo chmod 777 /etc/snmp/snmpd.conf", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        # result = res.stdout
        f = open('/etc/snmp/snmpd.conf', 'r')
        lines = f.readlines()
        f.close()
        f = open('/etc/snmp/snmpd.conf', 'w')
        for line in lines:
            a = re.sub(r'rocommunity .* default -V systemonly', f'rocommunity {group} default -V systemonly', line)
            f.writelines(a)
        f.close()
    except Exception as e:
        return pd.DataFrame({'res': [e]}, index=[0])
    # return True
    # elif version == 'v3':
    # time.sleep(2)
    user = dicv3['snmp_v3_user']
    a = dicv3['authentication_mode']
    A = dicv3['authentication_pwd']
    x = dicv3['privacy_mod']
    X = dicv3['privacy_pwd']
    try:
        # result = os.system(r"sudo rm -rf /var/lib/snmp/snmpd.conf")
        res = subprocess.call("sudo rm -rf /var/lib/snmp/snmpd.conf", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        # result = os.system(f"sudo net-snmp-config --create-snmpv3-user -ro -a {a} -A {A} -x {x} -X {X} {user}")
        res = subprocess.call(
            f"sudo net-snmp-config --create-snmpv3-user -ro -a {a} -A {A} -x {x} -X {X} {user}", shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    except Exception as e:
        return pd.DataFrame({'res': [e]}, index=[0])
    # result = os.system("nohup sudo /opt/fbi-base/bin/python3 udf/snmp_start.py > /dev/null 2>&1 &")
    # time.sleep(5)
    # if not result:
    #     return False

    # os.system("sudo systemctl start snmpd")
    res = subprocess.call("sudo systemctl start snmpd", shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    # time.sleep(1)
    # os.system("nohup sudo /opt/fbi-base/bin/python3.11 udf/new_snmp_pyagentx3.py > /dev/null 2>&1 &")
    res = subprocess.call(
        ["nohup", "sudo", "/opt/fbi-base/bin/python3.11", "udf/new_snmp_pyagentx3.py", ">", "/dev/null", "/dev/null",
         "2>&1", "&"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    dictrap = dic['snmp']['snmp_trap']
    trap_c = dictrap['snmp_trap_group']
    trap_ip = dictrap['ip']

    # res = os.system(f"nohup sudo /opt/fbi-base/bin/python3 udf/snmp_trap.py {trap_ip} {trap_c} > /dev/null 2>&1 &")
    res = subprocess.call(
        ["nohup", "sudo", "/opt/fbi-base/bin/python3.11", "udf/snmp_trap.py", f"{trap_ip}", f"{trap_c}" ">",
         "/dev/null", "/dev/null",
         "2>&1", "&"], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    # result = res.stdout
    return pd.DataFrame({'res': [True]}, index=[0])


def config_save2(dic, p=''):
    # import signal
    p = p.strip()
    dicv2 = dic['snmp']['snmp_service_v2']
    # dicv3 = dic['snmp']['snmp_service_v3']
    # os.system("ps -ef | grep snmp_start | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9")
    pids = [(x, psutil.Process(x).cmdline()) for x in psutil.pids() if psutil.pid_exists(x)]
    for pid, cmdline in pids:
        # p = psutil.Process(pid)
        if 'udf/snmp_start.py' in cmdline or 'udf/snmp_trap.py' in cmdline:
            res = os.system(f"kill -9 {pid}")

    time.sleep(1)
    group = dicv2['snmp_group']
    # try:
    #     # with open(r"/etc/snmp/snmpd.conf", 'a+') as f:
    #     #     f.write(f"\n\rrocommunity {group} default -V systemonly\n")
    #     #     f.close()
    #     # os.system("sudo chmod 777 /etc/snmp/snmpd.conf")
    #     f = open('/opt/openfbi/fbi-bin/udf/snmp_start.py', 'r')
    #     lines = f.readlines()
    #     f.close()
    #     f = open('/opt/openfbi/fbi-bin/udf/snmp_start.py', 'w')
    #     for line in lines:
    #         a = re.sub(r'community = "[a-zA-Z0-9]+"', f'community = "{group}"', line)
    #         f.writelines(a)
    #     f.close()
    # except Exception as e:
    #     return e
    res = os.system(f"nohup sudo /opt/fbi-base/bin/python3 udf/snmp_start.py {group} > /dev/null 2>&1 &")
    #
    dictrap = dic['snmp']['snmp_trap']
    trap_c = dictrap['snmp_trap_group']
    trap_ip = dictrap['ip']

    # os.system("ps -ef | grep snmp_trap | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9")

    # try:
    #     # with open(r"/etc/snmp/snmpd.conf", 'a+') as f:
    #     #     f.write(f"\n\rrocommunity {group} default -V systemonly\n")
    #     #     f.close()
    #     # os.system("sudo chmod 777 /etc/snmp/snmpd.conf")
    #     f = open('/opt/openfbi/fbi-bin/udf/snmp_trap.py', 'r')
    #     lines = f.readlines()
    #     f.close()
    #     f = open('/opt/openfbi/fbi-bin/udf/snmp_trap.py', 'w')
    #     for line in lines:
    #         a = re.sub(r'community = "[a-zA-Z0-9]+"', f'community = "{trap_c}"', line)
    #         a = re.sub(r'trap_ip = "[0-9.]*"', f'trap_ip = "{trap_ip}"', a)
    #         f.writelines(a)
    #     f.close()
    # except Exception as e:
    #     return e

    res = os.system(f"nohup sudo /opt/fbi-base/bin/python3 udf/snmp_trap.py {trap_ip} {trap_c} > /dev/null 2>&1 &")

    return pd.DataFrame({'res': [True]}, index=[0])


def config_save_t(dic, p=''):
    import threading
    t = threading.Thread(target=config_save, args=(dic, ''))
    t.start()

    return pd.DataFrame({'res': [True]}, index=[0])


def config_save_part1(dic, p=''):
    p = p.strip()
    res = subprocess.call("ps -ef | grep new_snmp_pyagentx3 | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9",
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = subprocess.call("ps -ef | grep snmp_trap | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9",
                          shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # res = subprocess.call("sudo systemctl stop snmpd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = subprocess.call("ps -ef | grep snmpd | grep -v grep | cut -c 9-16 |xargs sudo kill -9", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    return pd.DataFrame({'res': [True]}, index=[0])


def config_save_part2(dic, p=''):
    p = p.strip()
    dicv3 = dic['snmp']['snmp_service_v3']
    dicv2 = dic['snmp']['snmp_service_v2']
    group = dicv2['snmp_group']
    try:
        res = subprocess.call("sudo chmod 777 /etc/snmp/snmpd.conf", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        f = open('/etc/snmp/snmpd.conf', 'r')
        lines = f.readlines()
        f.close()
        f = open('/etc/snmp/snmpd.conf', 'w')
        for line in lines:
            a = re.sub(r'rocommunity .* default -V systemonly', f'rocommunity {group} default -V systemonly', line)
            f.writelines(a)
        f.close()
        return pd.DataFrame({'res': [True]}, index=[0])
    except Exception as e:
        return pd.DataFrame({'res': [e]}, index=[0])


def config_save_part3(dic, p=''):
    p = p.strip()
    dicv3 = dic['snmp']['snmp_service_v3']
    user = dicv3['snmp_v3_user']
    a = dicv3['authentication_mode']
    A = dicv3['authentication_pwd']
    x = dicv3['privacy_mod']
    X = dicv3['privacy_pwd']
    try:
        res = subprocess.call("sudo rm -rf /var/lib/snmp/snmpd.conf", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        res = subprocess.call(
            f"sudo net-snmp-config --create-snmpv3-user -ro -a {a} -A {A} -x {x} -X {X} {user}", shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return pd.DataFrame({'res': [True]}, index=[0])
    except Exception as e:
        return pd.DataFrame({'res': [e]}, index=[0])


def config_save_part4(dic, p=''):
    p = p.strip()
    dictrap = dic['snmp']['snmp_trap']
    trap_c = dictrap['snmp_trap_group']
    trap_ip = dictrap['ip']

    # res = subprocess.call("sudo systemctl start snmpd", shell=True, stdout=subprocess.PIPE,
    #                       stderr=subprocess.STDOUT)
    res = subprocess.call("sudo /usr/sbin/snmpd", shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT)

    time.sleep(1)

    res = subprocess.call(
        "nohup sudo /opt/fbi-base/bin/python3.11 udf/new_snmp_pyagentx3.py > /dev/null 2>&1 &", shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    res = subprocess.call(
        f"nohup sudo /opt/fbi-base/bin/python3.11 udf/snmp_trap.py {trap_ip} {trap_c} > /dev/null 2>&1 &",
        shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return pd.DataFrame({'res': [True]}, index=[0])

def walk_test(df, p=''):
    #ip, oid = p.strip().split(",")
    ip, port, oid, group = p.strip().split(",")
    ip = ip.strip()
    port=port.strip()
    port = int(port)
    oid = oid.strip()
    group = group.strip()
    if oid[0] != '.':
        oid = '.' + oid
    command = f"snmpwalk -v 2c -c {group} {ip} {oid}"
    try:
        tmp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        list1 = []
        for line in tmp.stdout.readlines():
            list1.append(line.strip().decode("gbk"))
        df1 = pd.DataFrame({'result': list1})
        # df1.columns = ['result']
    except Exception as e:
        return pd.DataFrame({'res': [e]}, index=[0])
    return df1

def walk_test2(df, p=''):
    #ip, oid = p.strip().split(",")
    ip, port, oid, group = p.strip().split(",")
    ip = ip.strip()
    port=port.strip()
    oid = oid.strip()
    group = group.strip()
    # if oid[0] != '.':
    #     oid = '.' + oid
    list1 = []
    depth = 1
    queue = [(oid, depth)]
    while queue:
        oid,depth = queue.pop(0)
        # if oid[0] != '.':
        #     oid = '.' + oid
        target_oid = ObjectIdentity(oid)
        snmp_params = (CommunityData(group),
                       UdpTransportTarget((ip, int(port))),
                       ContextData(),
                       ObjectType(target_oid))
        # while True:
        errorIndication, errorStatus, errorIndex, varBinds = next(nextCmd(SnmpEngine(),*snmp_params,lexicographicMode=False))
        # print(type(errorStatus))
        if errorIndication:
            print(f'Error,{errorStatus}')
            break
        elif errorStatus:
            if errorStatus != 2:
                break
        else:
            for varBind in varBinds:
                print(varBind)
                print(type(varBind))
                if str(varBind).endswith("No Such Instance currently exists at this OID"):
                    break
                list1.append(varBind)
                # for item in varBind:
                #     print(item)
                    # list1.append(str(item[1]))
                if isinstance(varBind, ObjectType):
                    child_oid_str = str(varBind[0])
                    # if depth == 0 or re.findall(child_oid_str, oid):
                    queue.append((child_oid_str, depth + 1))
                    break
            # if not varBinds[-1][0].isPrefixOf(target_oid):
            #     break
    df1 = pd.DataFrame(list1)
    df1.columns = ['Result']
    return df1



if __name__ == '__main__':
    # snmpget()
    # walk()
    df1 = pd.DataFrame({"snmp": {"snmp_service": {"snmp_version": "v3", "snmp_group": "test", "snmp_v3_user": "test", "authentication_mode": "MD5", "authentication_pwd": "123123123", "privacy_mod": "DES", "privacy_pwd": "321321321"}}}
    , index=[0])
    # df1 = {"snmp": {"snmp_service_v2": {"snmp_group": "abc"},
    #                 "snmp_service_v3": {"snmp_v3_user": "abc", "authentication_mode": "MD5",
    #                                     "authentication_pwd": "123123123", "privacy_mod": "DES",
    #                                     "privacy_pwd": "123123123"}}}
    # df2 = get(df1, '172.23.254.32,.1.3.6.1.2.1.1.6.0')
    # df3 = walk(df1, '127.0.0.1,.1.3.6.1.2.1.1')
    # df4 = send(df1, '172.23.254.32,1.3.6.1.2.1.1.1.0')
    # df5 = getv3(df1, '172.23.240.57,.1.3.6.1.2.1.1.1.0,snmpuser,12345678,12345678,MD5,DES')
    # df5 = config_save2(df1,
    #                    p="""{"snmp": {"snmp_service_v2": {"snmp_group": "ceshi"}, "snmp_service_v3": {"snmp_v3_user": "test111", "authentication_mode": "MD5", "authentication_pwd": "123123123", "privacy_mod": "DES", "privacy_pwd": "123123123"}, "snmp_trap": {"name": "traptest", "ip": "192.168.1.175", "snmp_trap_version": "", "snmp_trap_group": "", "snmp_trap_v3_user": "", "authentication_trap_mode": "", "authentication_trap_pwd": "", "privacy_trap_mod": "", "privacy_trap_pwd": ""}}}""")
    df2 = walk_test2(df1,"192.168.124.247,161,.1.3.6.1.4.1.2021.9.1.9,qwer")
    print(df2)