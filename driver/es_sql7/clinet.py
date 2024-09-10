
import sys
sys.path.append("/opt/openfbi/fbi-bin/driver")
from elasticsearch7 import Elasticsearch

from es_sqlparser import parse_handle
from .request import SQLCLASS


class Client:

    def __init__(self, hosts, **kwargs):
        self.es = Elasticsearch(hosts, **kwargs)

    def sql_format(self, sql):
        if not sql.endswith(';'):
            sql = sql + ';'
        return sql

    def parse(self, sql):
        return parse_handle(sql)
        
    #add by gjw on 2020-0429 关闭链接
    def close(self):
        self.es.transport.close()
        
    def execute(self, sql):
        sql = self.sql_format(sql)
        parsed = self.parse(sql)
        print(parsed)

        method = parsed['method']

        return SQLCLASS[method](self.es, parsed)





