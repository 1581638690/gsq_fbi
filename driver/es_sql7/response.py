class Response:
    def __init__(self, text, aggfields, sfields, cfields, group, return_rows=False):

        # 聚合字段
        self.aggfields = aggfields

        # sfields 表示 hit['_source'] 中的字段
        self.sfields = sfields

        # cfields 表示 (_index、_type、_id) 字段
        self.cfields = cfields

        # aggregations结果解析的时候需要根据group字段递归
        self.group = group

        # return_rows 只针对 count(distinct xxx) 这种语法！！
        self.return_rows = return_rows

        self.text = text

    def success(self):
        return self.total_shards == self.successful_shards

    @property
    def total_shards(self):
        return self.text['_shards']['total']

    @property
    def successful_shards(self):
        return self.text['_shards']['successful']

    def query_result(self):
        if 'aggregations' in self.text:
            agg = Aggregations(self.aggfields, self.sfields, self.group)
            agg.put_bucket(self.text['aggregations'])
            if self.return_rows:
                return [{'count': len(agg.buckets)}]
            return agg.buckets

        if 'hits' in self.text:
            return Hits(self.text['hits']['hits']).source(self.sfields, self.cfields)


class Aggregations:
    def __init__(self, aggfields, fields, group):
        self.aggfields = [aggfield.bpname for aggfield in aggfields]
        self.fields = fields
        self.group = group

        self.buckets = []

    def put_bucket(self, buckets=None, g=None, idx=-1):
        if isinstance(buckets, list):
            for bucket in buckets:
                self.put_bucket(bucket, g, idx)
        else:
            if idx > -1:
                if self.group[idx] in self.fields:
                    g = {**g, self.group[idx]: buckets['key']}
                else:
                    g = {**g}
            else:
                g = dict()

            idx += 1

            if idx < len(self.group):
                c = self.group[idx]
                v = buckets[c]
                if 'buckets' in v:
                    self.put_bucket(v['buckets'], g, idx)
            else:
                for f in self.aggfields:
                    if f in buckets:
                        g[f] = buckets[f]['value']
                self.buckets.append(g)


class Hits:
    def __init__(self, hits):
        self.hits = hits

    def source(self, sfields, cfields):
        res = []
        for hit in self.hits:
            # 如果不指定其他字段（非 _index/_type/_id 字段）那么hit['_source']中的内容就不需要了
            if not sfields:
                sour = {}
            else:
                sour = hit['_source']
            for f in cfields:
                sour[f] = hit[f]
            res.append(sour)

        return res

    def iter_source(self, sfields, cfields, size):
        offset = 0
        for data in self.hits:

            offset += 1

            if size != -1 and offset > size:
                break

            if not sfields:
                sour = {}
            else:
                sour = data['_source']
            for f in cfields:
                sour[f] = data[f]

            yield sour


class MappingRes:
    @staticmethod
    def to_result(text, index):
        result = []

        prop = text[index]['mappings']['properties']
        for field, opts in prop.items():

            field_type = opts['type']

            if 'fields' in opts:
                field_type = 'keyword/text'

            d = {
                'index': index,
                'column': field,
                'type': field_type
            }

            result.append(d)
        return result

