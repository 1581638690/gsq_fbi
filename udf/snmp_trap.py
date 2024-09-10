import sys
import time


sys.path.append("./")
sys.path.append("./lib")
sys.path.append("../lib")
sys.path.append("./driver")
sys.path.append("/opt/openfbi/pylibs")

from pysnmp.entity.engine import SnmpEngine
# from pysnmp.entity.rfc3413.oneliner.cmdgen import CommandGenerator
from pysnmp.hlapi import CommunityData, UdpTransportTarget, ContextData, sendNotification
from pysnmp.proto.rfc1902 import ObjectName
from pysnmp.smi.rfc1902 import NotificationType, ObjectIdentity

from pysnmp.proto.rfc1902 import OctetString
import psutil,os

trap_ip = sys.argv[1]
community = sys.argv[2]

# trap_ip = "172.24.26.128"
# community = "public"
trap_port = 162

# os.system("ps -ef | grep snmp_trap | grep -v grep | cut -c 9-15 |sudo xargs kill -s 9")

while True:
    reCPUPercent = psutil.cpu_percent(interval=1)
    reMemPercent = psutil.virtual_memory().percent
    reDiskPercent = psutil.disk_usage('/').percent

    # def send(df, p=''):
    if reCPUPercent > 80.0:
        g = sendNotification(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((trap_ip, trap_port)),
            ContextData(),
            'trap',
            # (ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), rfc1902.OctetString("testest"))
            NotificationType(ObjectIdentity(ObjectName('1.3.6.1.4.1.60003.2.1')), OctetString("CPU trap")),
            # NotificationType(ObjectIdentity('SNMPv2-MIB', 'sysDescr'), "testest")
        )
        res = next(g)
        # return 0
    elif reMemPercent > 80.0:
        g = sendNotification(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((trap_ip, trap_port)),
            ContextData(),
            'trap',
            # (ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), rfc1902.OctetString("testest"))
            NotificationType(ObjectIdentity(ObjectName('1.3.6.1.4.1.60003.2.2')), OctetString("Memory Trap")),
            # NotificationType(ObjectIdentity('SNMPv2-MIB', 'sysDescr'), "testest")
        )
        res = next(g)
    elif reDiskPercent > 80.0:
        g = sendNotification(
            SnmpEngine(),
            CommunityData(community),
            UdpTransportTarget((trap_ip, trap_port)),
            ContextData(),
            'trap',
            # (ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0), rfc1902.OctetString("testest"))
            NotificationType(ObjectIdentity(ObjectName('1.3.6.1.4.1.60003.2.3')), OctetString("Disk trap")),
            # NotificationType(ObjectIdentity('SNMPv2-MIB', 'sysDescr'), "testest")
        )
        res = next(g)
    time.sleep(60)