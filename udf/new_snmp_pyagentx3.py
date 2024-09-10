#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import sys
# sys.path.insert(0,'..')
# --------------------------------------------
import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logger = logging.getLogger('pyagentx3.main')
logger.addHandler(NullHandler())
# --------------------------------------------


import datetime
import sys

sys.path.append("./lib")
sys.path.append("../lib")
sys.path.append("../driver")
sys.path.append("./udf")
sys.path.append("/opt/openfbi/pylibs")
sys.path.append("/opt/fbi-base/lib/python3.11/site-packages")

# import pymysql
import pyagentx3
from clickhouse_driver import Client
import psutil
import json
import pandas as pd
import time
import ZNSM

__workSpace = "../workspace/"

ip = [[y.address for y in x if y.netmask == '255.255.255.0'] for x in list(psutil.net_if_addrs().values())]
ip = [x[0] for x in ip if x != []]
ip = ip[0]
st = datetime.datetime.now()


def str_to_oid(data):
    length = len(data)
    oid_int = [str(ord(i)) for i in data]
    return str(length) + '.' + '.'.join(oid_int)


class TestData():

    def __init__(self):
        self.dic = {'prRuntime': 0,
                    'reCPUIndex': 0,
                    'reCPUUser': '0',
                    'reCPUSystem': '0',
                    'reCPUPercent': '0',
                    'reMemTotalReal': 0,
                    'reMemTotalFree': 0,
                    'reMemPercent': '0',
                    'reDiskIndex': '0',
                    'reDiskTotal': 0,
                    'reDiskAvail': 0,
                    'reDiskPercent': 0,
                    'tmReceiveSize': 0,
                    'tmAccessTime': 0,
                    'rmTotalHTTP': 0,
                    'rmTotalFTP': 0,
                    'rmTotalSMB': 0,
                    'rmTotalSMTP': 0,
                    'rmTotalIMAP': 0,
                    'rmTotalPOP3': 0,
                    'rmTotalDNS': 0,
                    'rmSendHTTP': 0,
                    'rmSendFTP': 0,
                    'rmSendSMB': 0,
                    'rmSendSMTP': 0,
                    'rmSendIMAP': 0,
                    'rmSendPOP3': 0,
                    'rmSendDNS': 0,
                    'LastFlow': 0,
                    'LastFlowTime': 0
                    }
        self.prName = "云安数据安全访问控制系统".encode(encoding='utf-8')
        # self.prName = "YZXA"
        self.prVersion = "V1.0"
        # prSupplier = quote("郑州云智信安安全技术有限公司".encode('gb2312'))
        self.prSupplier = "郑州云智信安安全技术有限公司".encode(encoding='utf-8')
        # self.prSupplier = "YZXA"
        self.prContact = "4006866653"
        # prLinkman = quote("郑州云智信安安全技术有限公司".encode('gb2312'))
        self.prLinkman = "郑州云智信安安全技术有限公司".encode(encoding='utf-8')
        # self.prLinkman = "YZXA"

        self.df = pd.DataFrame({'p': [1]}, index=[0])

        self.sample_int = 9000
        self.sample_counter = 0
        self.boot_ts = datetime.datetime.now().timestamp()
        self.amTotalCount = 0
        self.amSendCount = 0
        self.conn = Client(host='localhost', port=19000, database='default', user='default', password='client')

        self.sample_int = 0


class YXZASnmpPart1(pyagentx3.Updater):

    def __init__(self, data_store=None):
        pyagentx3.Updater.__init__(self)
        self.data_store = data_store

    def update(self):
        try:
            tm2 = ZNSM.dpdk_stats(self.data_store.df)
            tmp2 = tm2.iloc[0, 1]

            time.sleep(0.5)

            tm = ZNSM.dpdk_stats(self.data_store.df)
            tmp = tm.iloc[0, 1]

            self.data_store.dic['reNetFlow'] = str(round((tmp - tmp2) / 1024 / 1024 / 0.5, 2))
        except Exception as e:
            self.data_store.dic['reNetFlow'] = str(0)

        self.data_store.dic['reCPUIndex'] = psutil.cpu_count(False)
        self.data_store.dic['reCPUUser'] = str(sum(psutil.cpu_percent(interval=1, percpu=True)[:7]))
        self.data_store.dic['reCPUSystem'] = str(sum(psutil.cpu_percent(interval=1, percpu=True)[8:]))
        self.data_store.dic['reCPUPercent'] = str(psutil.cpu_percent(interval=1))
        self.data_store.dic['reMemTotalReal'] = psutil.virtual_memory().total
        self.data_store.dic['reMemTotalFree'] = psutil.virtual_memory().available
        self.data_store.dic['reMemPercent'] = str(psutil.virtual_memory().percent)
        self.data_store.dic['reDiskIndex'] = json.dumps(psutil.disk_partitions()).replace('"', '')[:250]
        self.data_store.dic['reDiskTotal'] = psutil.disk_usage('/').total
        self.data_store.dic['reDiskAvail'] = psutil.disk_usage('/').free
        self.data_store.dic['reDiskPercent'] = str(psutil.disk_usage('/').percent)
        self.data_store.dic['prRuntime'] = (datetime.datetime.now() - st).microseconds

        # get new data
        # self.data_store.sample_counter += 1
        # now = datetime.datetime.now().timestamp()

        # Triggers a trap when counter is divisable by 5
        # send_trap = 1 if (self.data_store.sample_counter % 5) == 0 else 0

        # Updated SNMP objects
        self.set_OCTETSTRING('1.1', self.data_store.prName)
        self.set_OCTETSTRING('1.2', self.data_store.prVersion)
        self.set_OCTETSTRING('1.3', self.data_store.prSupplier)
        self.set_OCTETSTRING('1.4', self.data_store.prContact)
        self.set_OCTETSTRING('1.5', self.data_store.prLinkman)
        self.set_INTEGER('1.6', self.data_store.dic['prRuntime'])

        self.set_OCTETSTRING('2.1.1', self.data_store.dic['reCPUIndex'])
        self.set_OCTETSTRING('2.1.2', self.data_store.dic['reCPUUser'])
        self.set_OCTETSTRING('2.1.3', self.data_store.dic['reCPUSystem'])
        self.set_OCTETSTRING('2.1.4', self.data_store.dic['reCPUPercent'])
        self.set_COUNTER64('2.2.1', self.data_store.dic['reMemTotalReal'])
        self.set_COUNTER64('2.2.2', self.data_store.dic['reMemTotalFree'])
        self.set_OCTETSTRING('2.2.3', self.data_store.dic['reMemPercent'])
        self.set_OCTETSTRING('2.3.1', self.data_store.dic['reDiskIndex'])
        self.set_COUNTER64('2.3.2', self.data_store.dic['reDiskTotal'])
        self.set_COUNTER64('2.3.3', self.data_store.dic['reDiskAvail'])
        self.set_OCTETSTRING('2.3.4', self.data_store.dic['reDiskPercent'])
        self.set_OCTETSTRING('2.4.1', self.data_store.dic['reNetFlow'])




class YXZASnmpPart2(pyagentx3.Updater):

    def __init__(self, data_store=None):
        pyagentx3.Updater.__init__(self)
        self.data_store = data_store

    def update(self):
        # Implement netSnmpIETFWGTable from NET-SNMP-EXAMPLES-MIB.txt
        # Number of entries in table is random to show that MIB is reset
        # on every update
        try:
            tm = ZNSM.dpdk_stats(self.data_store.df, p='')
            tmp = int(tm.iloc[0, 1])
        except Exception as e:
            tmp = 0

        self.data_store.dic['tmReceiveSize'] = tmp
        self.data_store.dic['tmAccessTime'] = self.data_store.conn.execute("select count(*) count from api_visit")[0][0]

        self.data_store.dic['rmTotalHTTP'] = self.data_store.conn.execute("select count(*) count from api_visit")[0][0]
        self.data_store.dic['rmTotalFTP'] = self.data_store.conn.execute("select count(*) count from api_ftp")[0][0]
        self.data_store.dic['rmTotalSMB'] = self.data_store.conn.execute("select count(*) count from api_smb")[0][0]
        self.data_store.dic['rmTotalSMTP'] = self.data_store.conn.execute("select count(*) count from api_smtp")[0][0]
        self.data_store.dic['rmTotalIMAP'] = self.data_store.conn.execute("select count(*) count from api_imap")[0][0]
        self.data_store.dic['rmTotalPOP3'] = self.data_store.conn.execute("select count(*) count from api_pop3")[0][0]
        self.data_store.dic['rmTotalDNS'] = self.data_store.conn.execute("select count(*) count from api_dns")[0][0]
        self.data_store.dic['rmSendHTTP'] = \
            self.data_store.conn.execute("select count(*) count from api_visit where srcip='" + ip + "'")[0][0]
        self.data_store.dic['rmSendFTP'] = \
            self.data_store.conn.execute("select count(*) count from api_ftp where srcip='" + ip + "'")[0][0]
        self.data_store.dic['rmSendSMB'] = \
            self.data_store.conn.execute("select count(*) count from api_smb where srcip='" + ip + "'")[0][0]
        self.data_store.dic['rmSendSMTP'] = \
            self.data_store.conn.execute("select count(*) count from api_smtp where srcip='" + ip + "'")[0][0]
        self.data_store.dic['rmSendIMAP'] = \
            self.data_store.conn.execute("select count(*) count from api_imap where srcip='" + ip + "'")[0][0]
        self.data_store.dic['rmSendPOP3'] = \
            self.data_store.conn.execute("select count(*) count from api_pop3 where srcip='" + ip + "'")[0][0]
        self.data_store.dic['rmSendDNS'] = \
            self.data_store.conn.execute("select count(*) count from api_dns where srcip='" + ip + "'")[0][0]

        # 196测试用
        # dic['rmTotalHTTP'] = conn.execute("select count(*) count from flow2")[0][0]
        # dic['rmTotalFTP'] = conn.execute("select count(*) count from event_ftp")[0][0]
        # dic['rmSendHTTP'] = conn.execute(f"select count(*) count from flow2 where src_ip='{ip}'")[0][0]

        c1 = self.data_store.conn.execute(f"select count(*) count from api_abroad")[0][0]
        c2 = self.data_store.conn.execute(f"select count(*) count from api_delay")[0][0]
        c3 = self.data_store.conn.execute(f"select count(*) count from api_risk")[0][0]
        c4 = self.data_store.conn.execute(f"select count(*) count from datafilter_alarm")[0][0]
        c5 = self.data_store.conn.execute(f"select count(*) count from sensitive_data_alarm")[0][0]
        c6 = self.data_store.conn.execute(f"select count(*) count from r_req_alm")[0][0]
        c7 = self.data_store.conn.execute(f"select count(*) count from stat_req_alm")[0][0]

        self.data_store.dic['amTotalCount'] = c1 + c2 + c3 + c4 + c5 + c6 + c7

        self.set_COUNTER64('1.1.1', self.data_store.dic['tmReceiveSize'])
        self.set_COUNTER64('1.1.2', self.data_store.dic['tmAccessTime'])
        self.set_COUNTER64('2.1.1', self.data_store.dic['rmTotalHTTP'])
        self.set_COUNTER64('2.1.2', self.data_store.dic['rmTotalFTP'])
        self.set_COUNTER64('2.1.3', self.data_store.dic['rmTotalSMB'])
        self.set_COUNTER64('2.1.4', self.data_store.dic['rmTotalSMTP'])
        self.set_COUNTER64('2.1.5', self.data_store.dic['rmTotalIMAP'])
        self.set_COUNTER64('2.1.6', self.data_store.dic['rmTotalPOP3'])
        self.set_COUNTER64('2.1.7', self.data_store.dic['rmTotalDNS'])
        self.set_COUNTER64('2.2.2', self.data_store.dic['rmSendHTTP'])
        self.set_COUNTER64('2.2.2', self.data_store.dic['rmSendFTP'])
        self.set_COUNTER64('2.2.3', self.data_store.dic['rmSendSMB'])
        self.set_COUNTER64('2.2.4', self.data_store.dic['rmSendSMTP'])
        self.set_COUNTER64('2.2.5', self.data_store.dic['rmSendIMAP'])
        self.set_COUNTER64('2.2.6', self.data_store.dic['rmSendPOP3'])
        self.set_COUNTER64('2.2.7', self.data_store.dic['rmSendDNS'])
        self.set_COUNTER64('3.1', self.data_store.dic['amTotalCount'])
        self.set_COUNTER64('3.2', self.data_store.amSendCount)



        # for i in range(random.randint(3, 5)):
        #     idx = str_to_oid('group%s' % (i + 1))
        #     self.set_OCTETSTRING('1.1.2.' + idx, 'member 1')
        #     self.set_OCTETSTRING('1.1.3.' + idx, 'member 2')


class NetSnmpIntegerSet(pyagentx3.SetHandler):

    def test(self, oid, data):
        if int(data) > 100:
            raise pyagentx3.SetHandlerError()

    def commit(self, oid, data):
        print("COMMIT CALLED: %s = %s" % (oid, data))
        self.data_store.sample_int = data


class SampleAgent(pyagentx3.Agent):

    def __init__(self, agent_id='SampleAgent', socket_path=None):
        super().__init__(agent_id, socket_path)

    def setup(self):
        data = TestData()

        self.register('1.3.6.1.4.1.60003.200',
                      YXZASnmpPart1, freq=10, data_store=data)

        # self.register('1.3.6.1.4.1.60003.200',
        #     NetSnmpTestMibTable, freq=5, data_store=data)

        self.register('1.3.6.1.4.1.60003.1',
                      YXZASnmpPart2, freq=20, data_store=data)

        self.register_set('1.3.6.1.4.1.8072.2.1.1.0',
                          NetSnmpIntegerSet, data_store=data)


def main():
    pyagentx3.setup_logging(debug=False)

    try:
        agt = SampleAgent()
        agt.start()
    except Exception as ex:
        print("Unhandled exception: %s" % ex)
        agt.stop()
    except KeyboardInterrupt:
        agt.stop()


if __name__ == "__main__":
    main()
