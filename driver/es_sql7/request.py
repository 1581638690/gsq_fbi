

import sys
sys.path.append("/opt/openfbi/fbi-bin/driver")
from elasticsearch7.helpers import scan, bulk

from .response import *
from .dsl import *
from .utils import error_handle


class Request:

    common_fields = ('_index', '_type', '_id')

    @staticmethod
    def sep_fileds(fields):
        sf = []
        cf = []
        for field in fields:
            if field in Request.common_fields:
                cf.append(field)
            else:
                sf.append(field)
        return sf, cf

    @staticmethod
    @error_handle
    def select(es, parsed):
        s = Select(parsed)

        fields, aggfields, group = s.fields()
        sf, cf = Request.sep_fileds(fields)
        source = {'_source': sf}
        dsl = {
            **source,
            **s.query(),
            **s.agg(aggfields),
            **s.sort(),
            **s.offset(),
            **s.size()
        }

        text = es.search(
            index=s.index,
            body=dsl
        )
        resp = Response(text, aggfields, sf, cf, group, s.return_rows)
        return resp.query_result()

    @staticmethod
    def scan(es, parsed):
        '''
        这里scan的处理参考elasticsearch-dsl中的实现，由调用方从生成器中迭代数据做处理。
        毕竟scan操作性能耗费比较大
        '''
        s = Scan(parsed)

        fields = s.fields()
        sf, cf = Request.sep_fileds(fields)
        source = {'_source': sf}
        size = s.size()
        sort = s.sort()
        if sort['sort']:
            dsl = {**source, **s.query(), **s.sort()}
            preserve_order = True
        else:
            dsl = {**source, **s.query()}
            preserve_order = False

        text = scan(
            es,
            query=dsl,
            index=s.index,
            preserve_order=preserve_order
        )

        resp = Hits(text)
        return resp.iter_source(sf, cf, size)

    @staticmethod
    @error_handle
    def insert(es, parsed):
        s = Insert(parsed)

        columns = s.fields()
        values = s.values()

        datas = [dict(zip(columns, value)) for value in values]

        def iteritem(items):
            for item in items:
                sour = {
                    '_index': s.index[0],
                }

                if '_id' in item:
                    sour['_id'] = item['_id']
                    del item['_id']

                sour['_source'] = item

                yield sour

        text = bulk(es, iteritem(datas))
        return text

    @staticmethod
    @error_handle
    def delete(es, parsed):
        s = Delete(parsed)

        text = es.delete_by_query(
            index=s.index,
            body=s.query()
        )
        return text

    @staticmethod
    @error_handle
    def update(es, parsed):
        # todo 支持update_by_query
        s = Update(parsed)

        text = es.update(
            index=s.index,
            id=s.id,
            body={'doc': s.reset_value()}
        )
        return text

    @staticmethod
    @error_handle
    def create(es, parsed):
        s = Create(parsed)

        index = s.index

        body = {
            'mappings': {
                'properties': s.fields()
            },
            'settings': {
                'number_of_shards': s.shards(),
                'number_of_replicas': s.replicas()
            }
        }
        text = es.indices.create(
            index=index,
            body=body
        )

        return text

    @staticmethod
    @error_handle
    def drop(es, parsed):
        s = Drop(parsed)

        text = es.indices.delete(
            index=s.index
        )

        return text

    @staticmethod
    @error_handle
    def desc(es, parsed):
        s = Desc(parsed)

        index = s.index

        text = es.indices.get_mapping(
            index=index,
        )
        return MappingRes.to_result(text, index[0])

    @staticmethod
    @error_handle
    def show(es, parsed):
        s = Show(parsed)

        opt = s.opt()
        reg = s.reg()

        if opt == 'tables':
            text = es.cat.indices(index=reg)
            if not text:
                return []
            cols = ['health', 'status',
                    'index', 'uuid',
                    'pri', 'rep',
                    'docs.count', 'docs.deleted',
                    'store.size', 'pri.store.size']
            datas = [d.split() for d in text.strip().split('\n')]
            return [dict(zip(cols, x)) for x in datas]


SQLCLASS = {
    'SELECT': Request.select,
    'SCAN': Request.scan,
    'INSERT': Request.insert,
    'DELETE': Request.delete,
    'UPDATE': Request.update,

    'CREATE': Request.create,
    'DROP': Request.drop,
    'DESC': Request.desc,

    'SHOW': Request.show
}
