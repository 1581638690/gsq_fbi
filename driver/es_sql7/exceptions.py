class ESQLException(Exception):
    """
    esql异常父类
    """


class MethodNotSupportException(ESQLException):
    """
    不支持该查询类型异常
    """


class IndexException(ESQLException):
    """
    索引异常
    """


class FieldException(ESQLException):
    """
    字段异常
    """


class IndexAlreadyExistException(ESQLException):
    """
    索引不存在
    """

