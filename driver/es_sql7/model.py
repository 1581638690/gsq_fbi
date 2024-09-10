import operator


# index
class Index:
    def __init__(self, name):
        if isinstance(name, str):
            name = [name]

        self.name = [n.split('.')[0] for n in name]


# doc_type
class DocType:
    def __init__(self, name):
        if isinstance(name, str):
            name = [name]

        doc_types = []
        for n in name:
            if '.' not in n:
                dt = 'base'
            else:
                dt = n.split('.')[1]
            doc_types.append(dt)

        self.name = doc_types


class Sort:

    def __init__(self, ordered):
        self.ordered = ordered

    def to_dict(self):
        st = {'sort': []}
        for s in self.ordered:
            st['sort'].append(s)
        return st


class Offset:

    def __init__(self, offset=None):
        if not offset:
            offset = 0
        self.offset = offset

    def to_dict(self):
        return {'from': self.offset}


class Size:

    def __init__(self, size=None):
        if not size:
            size = 10
        self.size = size

    def to_dict(self):
        return {'size': self.size}


# 普通字段
class Field:

    def __init__(self, name):
        # 多种形式id处理
        if name.lower() in ('id', '_id'):
            name = '_id'
        self.name = name

    # 小于等于
    def __le__(self, other):
        return {'range': {self.name: {'lte': other}}}

    # 大于等于
    def __ge__(self, other):
        return {'range': {self.name: {'gte': other}}}

    # 小于
    def __lt__(self, other):
        return {'range': {self.name: {'lt': other}}}

    # 大于
    def __gt__(self, other):
        return {'range': {self.name: {'gt': other}}}

    # 等于
    def __eq__(self, other):
        '''
        注：other本身不会被分词
        '''
        return {'term': {self.name: other}}

    __ne__ = __eq__

    # between
    def between(self, other):
        return {'range': {self.name: {'gte': other[0], 'lte': other[1]}}}

    # like
    def wildcard(self, other):
        '''
        注：仅作用于不分词字段
        dsl
        {
            "wildcard": { "user" : "ki*y" }
        }
        '''
        return {'wildcard': {self.name: other}}

    # in
    def terms(self, other):
        '''
        注：仅作用于不分词字段
        dsl
        {
            "terms": { "user" : ["one","two"] }
        }
        '''
        return {'terms': {self.name: other}}

    def exists(self):
        '''
        dsl
        {
            "exists": {"field": "tom"}
        }
        '''
        return {'exists': {'field': self.name}}


# 聚合字段
class AggField:

    def __init__(self, name, func):
        self.name = name
        self.func = func

        if self.name == '*':
            self.name = '_index'

    @property
    def bpname(self):
        return '{}_{}'.format(self.func.lower(), self.name.strip('_'))

    def __eq__(self, other):
        if isinstance(other, AggField):
            return (self.name == other.name) and (self.func == other.func)
        else:
            return False

    def __hash__(self):
        return hash(self.name + self.func)


class Bool:

    def __init__(self, must=None, should=None, must_not=None):
        self.must = must or []
        self.should = should or []
        self.must_not = must_not or []

    def __and__(self, other):
        q = self._new()

        q.must = [self.to_dict(), other.to_dict()]

        return q

    def __or__(self, other):
        q = self._new()

        q.should = [self.to_dict(), other.to_dict()]

        return q

    def to_dict(self):
        # 用filter而不用must是考虑filter不计算score，性能更好
        return {'bool': {'filter': self.must, 'should': self.should, 'must_not': self.must_not}}

    def _new(self):
        return self.__class__()


class Query:

    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

        self.not_equal = False

        self.must = []
        self.should = []
        self.must_not = []

    def bool(self):
        cx = self.to_dict()

        if self.not_equal:
            self.must_not.append(cx)
        else:
            self.must.append(cx)

        return Bool(self.must, self.should, self.must_not)

    @property
    def range(self):
        return {
            '=': operator.eq,
            '>': operator.gt,
            '>=': operator.ge,
            '<': operator.lt,
            '=<': operator.le,
            '!=': operator.ne,
            '<>': operator.ne
        }

    def to_dict(self):
        if self.operator in self.range.keys():
            if self.operator in ('!=', '<>'):
                self.not_equal = True
            d = self.range[self.operator](self.field, self.value)
        elif self.operator == 'BETWEEN':
            d = self.field.between(self.value)
        elif self.operator == 'LIKE':
            d = self.field.wildcard(self.value)
        elif self.operator == 'IN':
            d = self.field.terms(self.value)
        elif self.operator == 'NOTIN':
            self.not_equal = True
            d = self.field.terms(self.value)
        elif self.operator == 'IS':
            self.not_equal = True
            d = self.field.exists()
        elif self.operator == 'ISNOT':
            d = self.field.exists()
        else:
            raise Exception('不支持该查询方法{}.'.format(self.operator))

        return d


class HBool:

    def __init__(self, bps=None, script=''):
        # buckets_path
        self.bps = bps
        self.script = script

    def __and__(self, other):
        q = self._new()

        q.bps = {**self.bps, **other.bps}
        q.script = '{} && {}'.format(self.script, other.script)

        return q

    def __or__(self, other):
        q = self._new()

        q.bps = {**self.bps, **other.bps}
        q.script = '{} || {}'.format(self.script, other.script)

        return q

    def to_dict(self):
        if not self.script:
            return {'having': {'bucket_selector': {'buckets_path': self.bps}}}
        return {'having': {'bucket_selector': {'buckets_path': self.bps, 'script': self.script}}}

    def _new(self):
        return self.__class__()


class HQuery:

    def __init__(self, aggfield, operator, value):
        self.aggfield = aggfield
        if operator == '=':
            self.operator = '=='
        else:
            self.operator = operator
        self.value = value

    def bool(self):
        bpname = self.aggfield.bpname

        bp = self.to_bp(bpname)
        script = self.to_script(bpname)

        return HBool(bp, script)

    def to_bp(self, bpname):
        return {bpname: bpname}

    def to_script(self, bpname):
        if self.operator == 'BETWEEN':
            return 'params.{} {} {} && params.{} {} {}'.format(
                bpname, '>=', self.value[0],
                bpname, '<=', self.value[1]
            )
        return 'params.{} {} {}'.format(bpname, self.operator, self.value)


class Agg:

    def __init__(self, name):
        self.name = name
        self.size = 4096

    def to_dict(self):
        return {self.name: {"terms": {"field": self.name, "size": self.size}}}


class Aggs:

    def __init__(self, aggs):
        self.aggs = aggs

    # 这边有点写复杂了，不过暂时先这样了
    def to_dict(self, hbool=None, bks=None):
        bks = bks or []

        inner = {}

        if not self.aggs and bks:
            for bk in bks:
                inner.update(bk)
            return {'aggs': inner}

        for idx, agg in enumerate(reversed(self.aggs)):
            if idx == 0:
                inner = agg.to_dict()
                inner[agg.name].update({'aggs': {}})
                if hbool:
                    inner[agg.name]['aggs'].update(hbool)
                for bk in bks:
                    inner[agg.name]['aggs'].update(bk)
            else:
                t = agg.to_dict()
                t[agg.name].update({'aggs': {**inner}})
                inner = {**t}

        return {'aggs': inner}


class Bucket:

    def __init__(self, aggfield):
        self.name = aggfield.name
        self.func = aggfield.func
        self.bpname = aggfield.bpname

    @property
    def aggfuncs(self):
        return {
            'COUNT': 'value_count',
            'MAX': 'max',
            'MIN': 'min',
            'AVG': 'avg',
            'SUM': 'sum'
        }

    def to_dict(self):
        return {
            self.bpname: {self.aggfuncs[self.func]: {'field': self.name}}
        }


class MappingMultiFields:

    @staticmethod
    def to_dict():
        return {'fields': {'raw': {'type': 'keyword'}}}


class MappingField:
    '''
    todo 支持更多的参数
    '''

    def __init__(self, name, type, analyzer='standard'):
        self.name = name
        self.type = type
        self.analyzer = analyzer

    def to_dict(self):
        if isinstance(self.type, list):
            mf = MappingMultiFields.to_dict()
            return {self.name: {'type': 'text', **mf}}
        else:
            return {self.name: {'type': self.type}}





