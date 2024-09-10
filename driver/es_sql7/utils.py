from functools import wraps
import json


import sys
sys.path.append("/opt/openfbi/fbi-bin/driver")

from elasticsearch7.exceptions import RequestError, NotFoundError


def getkv(d):
    return list(d.items())[0]


def error_handle(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            result = func(*args, **kwargs)

            if 'deleted' in result and result['total'] == result['deleted']:
                return {'status_code': 200}

            if 'acknowledged' in result or '_id' in result:
                return {'status_code': 200}

            # bulk
            if isinstance(result, tuple):
                if not result[1]:
                    return {'status_code': 200}
                else:
                    return {'error_msg': result[1]}

            return result
        except (RequestError, NotFoundError) as e:
            raise
            error_msg = e.error
            error_code = e.status_code

            try:
                # 处理根据id删除文档错误
                error_msg = json.loads(error_msg)
                if not error_msg['found'] and '_id' in error_msg:
                    error_msg = 'document_missing_exception'
            except:
                pass

            return {'status_code': error_code, 'error_msg': error_msg}
        except:
            raise

    return wrapped
