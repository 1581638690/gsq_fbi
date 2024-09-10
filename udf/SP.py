# /bin/python
# -!- coding: utf-8 -!-
"""
sql解析相关函数
author : shb

"""
import random
import re
import sys
import os
import time
import pandas as pd
import numpy as np

sys.path.append("../")
sys.path.append("./lib")
sys.path.append("../lib")


def find_table(sql, p=''):
    p = p.strip()
    sql_list = sql.replace("\n", ' ').replace("\t", ' ').replace(',', ' and ').split(" ")
    sql_list = [x for x in sql_list if x != '']
    sql_list = [x for x in sql_list if '"' != x]
    table_list = []
    loc = 1
    for i in range(len(sql_list)):
        if "create" == sql_list[i].lower() or 'drop' == sql_list[i].lower() or 'alter' == sql_list[
            i].lower() or 'insert' == sql_list[i].lower():
            if "if" == sql_list[i + 2].lower() and 'not' == sql_list[i + 3].lower():
                table_list.append(re.match(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                           sql_list[i + 5]).group(0))
            elif "if" == sql_list[i + 2].lower() and 'exists' == sql_list[i + 3].lower():
                table_list.append(re.match(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                           sql_list[i + 4]).group(0))
            else:
                table_list.append(re.match(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                           sql_list[i + 2]).group(0))
            if p == 'table':
                return ','.join(table_list)
            elif p == 'dict':
                return table_list

        if "from" == sql_list[i].lower() or "join" == sql_list[i].lower():
            if len(sql_list) > i + 2 and "select" not in sql_list[i + 2].lower() and "select" not in sql_list[
                i + 1].lower() and "select" not in sql_list[i].lower():
                if sql_list[i + 2].lower() == 'as':
                    table_list.append({sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 3].replace("(",
                                                                                                                  '').replace(
                        ")", '')})
                elif sql_list[i + 2].lower() in ['and', 'where', 'left', 'or', 'inner', 'right', 'full', 'union','order','group']:
                    table_list.append(sql_list[i + 1].replace("(", '').replace(")", ''))
                # elif sql_list[i + 3].lower() in ['and', 'where', 'left', 'or', 'inner', 'right', 'full', 'union']:
                #     table_list.append(sql_list[i + 1].replace("(", '').replace(")", ''))
                elif len(sql_list) > i + 5:
                    key = 1
                    while len(sql_list) > i + 5 and key == 1:
                        if sql_list[i + 3].lower() in ['and']:
                            table_list.append(
                                {sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 2].replace("(",
                                                                                                            '').replace(
                                    ")", '')})
                            i += 3
                        elif sql_list[i + 4].lower() in ['and'] and sql_list[i + 2].lower() in ['as']:
                            table_list.append(
                                {sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 3].replace("(",
                                                                                                            '').replace(
                                    ")", '')})
                            i += 4
                        else:
                            key = 0
                    else:
                        if len(sql_list) > i + 3 and sql_list[i + 3].lower() in ['on', 'and', 'where', 'left', 'or',
                                                                                 'inner', 'right', 'full', 'union']:
                            table_list.append(
                                {sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 2].replace("(",
                                                                                                            '').replace(
                                    ")", '')})
                        elif len(sql_list) > i + 4 and sql_list[i + 4].lower() in ['on', 'and', 'where', 'left', 'or',
                                                                                   'inner', 'right', 'full', 'union']:
                            table_list.append(
                                {sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 3].replace("(",
                                                                                                            '').replace(
                                    ")", '')})
                        elif len(sql_list) <= i + 3:
                            table_list.append(
                                {sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 2].replace("(",
                                                                                                            '').replace(
                                    ")", '')})

                        # if sql_list[i + 5].lower() not in ['and', 'where', 'left', 'or', 'inner', 'right', 'full', 'union']:
                        #     if sql_list[i + 5].lower() in ['as']:
                        #         table_list.append({sql_list[i + 4].replace("(", '').replace(")", ''): sql_list[i + 6].replace("(",
                        #                                                                                                       '').replace(
                        #             ")", '')})
                        #     else:
                        #         table_list.append(
                        #             {sql_list[i + 4].replace("(", '').replace(")", ''): sql_list[i + 5].replace("(",
                        #                                                                                         '').replace(
                        #                 ")", '')})
                else:
                    table_list.append({sql_list[i + 1].replace("(", '').replace(")", ''): sql_list[i + 2].replace("(",
                                                                                                                  '').replace(
                        ")", '')})
            elif len(sql_list) < i + 3 and len(sql_list) > i + 1:
                table_list.append(sql_list[i + 1].replace("(", '').replace(")", ''))
        elif 'update' == sql_list[i].lower():
            table_list.append(sql_list[i + 1])
        elif 'insert' == sql_list[i].lower():
            table_list.append(sql_list[i + 2])
    if p == 'table':
        table = [list(x.keys())[0] if type(x) is dict else x for x in table_list]
        table = list(set(table))
        table = table if type(table) is str else ','.join(table)
        return table
    elif p == 'dict':
        return table_list


def find_col(sql, p=''):
    p = p.strip()
    sql_list = sql.replace("\n", ' ').replace("\t", ' ').replace(",", ' , ').replace("(", '  ').replace(")",
                                                                                                        '  ').replace(
        "=", ' ').split(" ")
    sql_list = [x for x in sql_list if x != '']
    sql_list = [x for x in sql_list if '"' != x]
    sql_list1 = []
    col_list = []
    # loc = 1
    # for i in range(len(sql_list)):
    #     if sql_list[i] == "/*":
    #         loc = 0
    #     if sql_list[i] == "*/":
    #         loc = 1
    for i in range(len(sql_list)):
        if sql_list[i].lower() in ['update', 'delete', 'insert', 'alter', 'show']:
            if sql_list[i].lower() == 'insert':
                tmplist = [x.lower() for x in sql_list]
                if 'values' in tmplist:
                    tmplist = sql_list[i:tmplist.index('values')]
                if 'value' in tmplist:
                    tmplist = sql_list[i:tmplist.index('value')]
            elif sql_list[i].lower() == 'update':
                if 'where' in sql_list:
                    tmplist = [x.lower() for x in sql_list]
                    tmplist = sql_list[i:tmplist.index('where')]
                else:
                    tmplist = sql_list
            else:
                tmplist = sql_list
            tmplist.append(',')
            tmplist.append(',')
            tmplist.append(',')
            tmplist.append(',')
            tmplist.append(',')
            sql_list1.append(tmplist)
            break
        elif 'from' in sql_list[i].lower() and 'from_' not in sql_list[i].lower():
            end = i
            tmplist = sql_list[start:end]
            tmplist.append(',')
            tmplist.append(',')
            tmplist.append(',')
            tmplist.append(',')
            tmplist.append(',')
            sql_list1.append(tmplist)
        elif 'select' in sql_list[i].lower() or 'show' in sql_list[i].lower():
            start = i
    for sql_list2 in sql_list1:
        jump = 0
        sql_list2 = [x for x in sql_list2 if x != "'" and x != '"']
        sql_list2 = [',' if x.lower() in ['select', 'when', 'cast', 'and', 'then'] else x for x in sql_list2]
        for i in range(len(sql_list2) - 5):
            if jump != 0:
                jump -= 1
                continue
            if sql_list2[i + 2] == ',' and sql_list2[i] == ',':
                # col_list.append(re.findall(r'[a-zA-Z0-9_-]*[.]+[a-zA-Z0-9_-]*', sql_list2[i+1])[0])
                re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                     sql_list2[i + 1])
                if len(re_list) > 0:
                    for re_col in re_list:
                        col_list.append(re_col)
            # elif 'select' in sql_list2[i].lower() or 'when' in sql_list2[i].lower() or 'cast' in sql_list2[i].lower() or 'and' in sql_list2[
            #     i].lower() or 'then' in sql_list2[i].lower() or 'set' in sql_list2[i].lower():
            #     re_list = re.findall(r'[a-zA-Z_*]+[a-zA-Z0-9_.-]*', sql_list2[i + 1])
            #     if len(re_list) > 0:
            #         for re_col in re_list:
            #             col_list.append(re_col)
            elif sql_list2[i] == ',' and sql_list2[i + 3] == ',':
                if sql_list2[i + 1].lower() in ['sum', 'max', 'date', 'count', 'min', 'avg', 'count_big',
                                                'grouping', 'where', 'truncate',
                                                'binary_checksum', 'checksum_agg', 'stdev', 'stdevp', 'var', 'varp',
                                                'ifnull', 'first', 'last', 'ucase', 'lcase', 'mid', 'substring',
                                                'len', 'round', 'format', 'distinct', 'format_type']:
                    re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                         sql_list2[i + 2])
                    if len(re_list) > 0:
                        for re_col in re_list:
                            col_list.append(re_col)
                # elif sql_list2[i+1].lower() == 'truncate':
                #     col_list.append(re.findall(r'[a-zA-Z_]+[a-zA-Z0-9_.-]*', sql_list2[i + 2]))
                #     jump = 3
                else:
                    re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                         sql_list2[i + 1])
                    if len(re_list) > 0:
                        for re_col in re_list:
                            col_list.append(re_col)
            elif sql_list2[i] == ',' and sql_list2[i + 4] == ',':
                if sql_list2[i + 2].lower() != 'as':
                    re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                         sql_list2[i + 2])
                    if len(re_list) > 0:
                        for re_col in re_list:
                            col_list.append(re_col)
                else:
                    re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                         sql_list2[i + 1])
                    if len(re_list) > 0:
                        for re_col in re_list:
                            col_list.append(re_col)
            elif sql_list2[i] == ',' and sql_list2[i + 5] == ',':
                # if sql_list2[i + 3].lower() != 'as':
                re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                     sql_list2[i + 2])
                if len(re_list) > 0:
                    for re_col in re_list:
                        col_list.append(re_col)
            elif sql_list2[i].lower() == 'set':
                re_list = re.findall(r'''[`"'a-zA-Z_+\u4e00-\u9fa5*]+[`"'a-zA-Z0-9_.+\u4e00-\u9fa5-]*''',
                                     sql_list2[i + 1])
                if len(re_list) > 0:
                    for re_col in re_list:
                        col_list.append(re_col)

        # elif i == len(sql_list2) - 1:
        #     if sql_list2[i - 1] == ',':
        #         col_list.append(sql_list2[i])
        #     elif sql_list2[i - 2] == ',':
        #         if sql_list2[i - 1].lower() in ['sum', 'max', 'date', 'count', 'min', 'avg', 'count_big',
        #                                         'grouping',
        #                                         'binary_checksum', 'checksum_agg', 'stdev', 'stdevp', 'var', 'varp',
        #                                         'ifnull', 'first', 'last', 'ucase', 'lcase', 'mid', 'substring',
        #                                         'len', 'round', 'format', 'truncate']:
        #             col_list.append(re.search(r"[a-zA-Z0-9._-]*", sql_list2[i]).group())
        #         else:
        #             col_list.append(sql_list2[i - 1])

    # print(*sql_list1, sep='\n')
    # print(*col_list, sep=',\t')
    table_dic = find_table(sql, p='dict')
    table_dic = [x for x in table_dic if type(x) is dict]
    if len(table_dic) > 0:
        for dic in table_dic:
            key, value = list(dic.items())[0]
            col_list = [key + '.' + x.split('.')[1] if x.split('.')[0] == value else x for x in col_list]
    col_list = "+".join(col_list).split("+")
    col_list = list(set(col_list))
    return col_list


# 返回sql中的表名，a = @udf df by SP.parse_table [with SQL列名] 返回加新列的df表
def parse_table(df1, p=''):
    p = p.strip()
    df = df1.copy(deep=True)
    for index, row in df.iterrows():
        try:
            sql = re.findall(r"""[a-zA-Z0-9_\s*.=,?!(！（）—：‘’“”【Ф】；？、，。《》|￥…)"'`@#$%^+&<>/;:{\[\]}\u4e00-\u9fa5-]+""",
                             row['sqls'])[-1]
            if '/*' in sql:
                substr = re.findall(r"[/]+[*]+.*[*]+[/]+", sql)
                for ss in substr:
                    sql = sql.replace(ss, '')
            # print(sql)
            table_list = find_table(sql, p='table')
            df.at[index, 'table_list'] = table_list
        except Exception as e:
            df.at[index, 'table_list'] = ''
    return df


# 返回sql中的列名，a = @udf df by SP.parse_col [with SQL列名] 返回加新列的df表
def parse_col(df1, p=''):
    p = p.strip()
    df = df1.copy(deep=True)
    for index, row in df.iterrows():
        try:
            sql = re.findall(r"""[a-zA-Z0-9_\s*.=,?!(！（）—：‘’“”【Ф】；？、，。《》|￥…)"'`@#$%^+&<>/;:{\[\]}\u4e00-\u9fa5-]+""",
                             row['sqls'])[-1]
            if '/*' in sql:
                substr = re.findall(r"[/]+[*]+.*[*]+[/]+", sql)
                for ss in substr:
                    sql = sql.replace(ss, '')
            # print(sql)
            col_list = find_col(sql)
            if type(col_list) is list:
                col_list = ','.join(col_list)
            df.at[index, 'col_list'] = col_list
        except Exception as e:
            df.at[index, 'col_list'] = ''
    return df


def find_inject(sql, p=''):
    p = p.strip()
    sql = sql.lower().strip()
    sql_nospace = sql.replace(" ", '')
    str_list = ['and1=(select', 'anduser>0', ';backup', ';exec', 'and0<>', ';createtable', ';insert', ';bulk',
                ';delete', 'and(select', ';use', "'sa'=(selectsystem_user)", ';update', ';drop', 'xp_regwrite',
                'xp_regdeletevalue', 'xp_regdeletekey']
    sql_res = [x for x in str_list if x in sql_nospace]
    if len(sql_res) > 0:
        return '是'
    if "(select" in sql:
        sql = sql.replace("(select", "select")
    while len(
            re.findall(r"""[(][a-zA-Z0-9_\s*.=,?!！—：‘’“”【Ф】；？、，。《》|￥…"'`@#$%^+&<>/;:{\[\]}\u4e00-\u9fa5-]*[)]""",
                       sql)) > 0:
        sql = re.sub(r"""[(][a-zA-Z0-9_\s*.=,?!！—：‘’“”【Ф】；？、，。《》|￥…"'`@#$%^+&<>/;:{\[\]}\u4e00-\u9fa5-]*[)]""", '', sql)
        # print(sql)
    else:
        sql = sql.replace("(", "").replace(")", "")
    sql_list1 = sql.replace("\n", ' ').replace("\t", ' ').replace(",", ' , ').replace("=", ' = ').split(' ')
    sql_list1 = [x for x in sql_list1 if x != '']
    # sql_list = re.sub(r"[\n]+", " ", sql_list.lower())
    # sql_list = [x for x in sql_list if x != '']
    # sql_list = [x.lower() for x in sql_list if '"' not in x]
    # sql_list1 = [sql_list1[sql_list1.index(x)-1]+x+sql_list1[sql_list1.index(x)+1] for x in sql_list1 if x == '=']
    # sql_list2 = []
    # for index,value in enumerate(sql_list1):
    #     if value == '=':
    #         sql_list2.append(sql_list1[index-1]+value+sql_list1[index+1])
    # inject_str = ['1=1', "'1'='1'", '"1"="1"']
    # if len([x for x in inject_str if x in sql_list2]) > 0:
    #     return '是'
    if "rlike" in sql_list1:
        # sql2 = re.findall(r"""[=]+[a-zA-Z'"0-9#$%^&*{_}\s\n\t]+rlike+[a-zA-Z0-9_\s*.=,?!()"'`@#$%^&<>/;:\[\]{}-]+""", sql_list)
        # con_list = []
        # if len(sql2) > 0:
        # sql2 = sql2[0].split("rlike")[1].strip()
        # else:
        #     print(sql2)
        index = sql_list1.index('rlike')
        if sql_list1[index - 2] == '=' or sql_list1[index + 2] == '=':
            # print('是')
            return '是'
    elif "where" in sql:
        if ' or ' in sql or ' and ' in sql:
            if 'or1=1' in sql.lower().replace(' ','') or 'or"1"="1"' in sql.lower().replace(' ','') or "or'1'='1'" in sql.lower().replace(' ',''):
                return '是'
            sql_list = sql.replace("where", "or").replace("and", "or").split("or")
            # print(sql_list)
            for sqls in sql_list:
                if "=" in sqls:
                    sqls = re.findall(
                        r"""[a-zA-Z0-9`'"_?<@#$%^&>/;:{}\u4e00-\u9fa5-]+\s*!*=\s*[a-zA-Z0-9`'"_?@#$%^&<>/;:{}\u4e00-\u9fa5-]+""",
                        sqls)[0]
                    # print(sqls)
                    col, value = sqls.split("=")
                    col, value = col.strip().replace("!", "1"), value.strip()
                    # print(col, value)
                    if 'len' not in col.replace('`', "") and 'num' not in col.replace('`',
                                                                                      "") and 'id' not in col.replace(
                        '`', "") and 'count' not in col.replace('`', "") and 'extent' not in col.replace('`',
                                                                                                         "") and 'size' not in col.replace(
                        '`', "") and 'byte' not in col.replace('`', "") and 'rows' not in col.replace('`',
                                                                                                      "") and 'time' not in col.replace(
                        '`', "") and re.fullmatch(r"[0-9]+", col) == None and "'" not in col:
                        if re.fullmatch(r"[0-9]+", value) != None and "'" not in value:
                            pass
                    elif re.fullmatch(r"[0-9]+", col) != None and re.fullmatch(r"[0-9]+",
                                                                               value) != None and "'" not in value and int(col)==int(value):
                        return '是'
                    elif re.fullmatch(r"[0-9]+", col) != None and re.fullmatch(r"[0-9]+",
                                                                               value) != None and "'" not in value and int(
                        col) != int(value) and f'{col[:-1]}!={value} and' in sql:
                        return '是'
                    elif "'" in col:
                        return '是'
    # sub_str = ['where', 'union']
    # sub_list = [x for x in sub_str if x.lower() in sql_str]

    # inject_list = [x for x in inject_str if x.lower() in sql_str]
    # inject_bool = '是' if len(inject_list)>0 and len(sub_list)>0 else '否'
    return '否'


def parse_inject(df1, p=''):
    p = p.strip()
    df = df1.copy(deep=True)
    for index, row in df.iterrows():
        try:
            sql = re.findall(r"""[a-zA-Z0-9_\s*.=,?!(！（）—：‘’“”【Ф】；？、，。《》|￥…)"'`@#$%^+&<>/;:{\[\]}\u4e00-\u9fa5-]+""",
                             row['sqls'].replace("\n", " ").replace("\t", " ").replace('（', '(').replace('）', ')'))[-1]
            sql = sql.replace("\\", "")
            if '/*' in sql:
                substr = re.findall(r"[/]+[*]+.*[*]+[/]+", sql)
                for ss in substr:
                    sql = sql.replace(ss, '')
            print(index, sql)
            inject_bool = find_inject(sql)
            df.at[index, 'inject'] = inject_bool
        except Exception as e:
            df.at[index, 'inject'] = '否'
            continue
        # sql_list = find_inject(sql)
        # print(sql_list)
    return df


# 判断列表与另一个列表的关系
def list_relation(df, p=''):
    p = p.strip()
    col1, col2, relation = p.split(',')
    df1 = df.copy()
    for index, rows in df1.iterrows():
        if relation == 'common':
            df_list2 = rows[col2].split(',')
            df_list1 = rows[col1].split(',')
            list1 = [x for x in df_list1 if x in df_list2]
            df1.at[index, 'common'] = ','.join(list1)
            # return df1
        elif relation == 'belong':
            df1.at[index, 'belong'] = True
            for col in col1.split("|"):
                df_list2 = rows[col2].strip().split(',')
                df_list1 = rows[col].strip().split(',') if rows[col].strip() != '' else []
                list1 = [x for x in df_list1 if x in df_list2]
                df1.at[index, 'belong'] *= True if df_list1 == list1 else False
            # return df1
        elif relation == 'diff':
            df_list2 = rows[col2].strip().split(',')
            df_list1 = rows[col1].strip().split(',') if rows[col1].strip() != '' else []
            list1 = [x for x in df_list1 if x not in df_list2]
            df1.at[index, 'diff'] = ','.join(list1)
            # return df1
        else:
            raise KeyError("Wrong input args")
    return df1


def baseline(df, p=''):
    p = p.strip()
    ip, port, user, table, col, db = p.split(',')
    df = df.fillna('')
    if ip == 'dest_ip':
        name = 0
        act = ['fw_ip', 'fw_port', 'fw_user', 'fw_table', 'fw_col', 'fw_db']
    else:
        name = 1
        act = ['bfw_ip', 'bfw_port', 'bfw_user', 'bfw_table', 'bfw_col', 'bfw_db']
    res_ip, res_port, res_user, res_table, res_col, res_db = ([], [], [], [], [], [])
    count_ip, count_port, count_user, count_table, count_col, count_db = (0, 0, 0, 0, 0, 0)
    jx_status_ip, jx_status_port, jx_status_user, jx_status_table, jx_status_col, jx_status_db = (0, 0, 0, 0, 0, 0)
    subject = df.iloc[0, 0]
    df['count_sum'] = df['count'].rolling(window=7).sum()
    key1 = df.size >= 7 and max(df['count_sum']) >= 100
    for index, row in df.iterrows():
        if row[ip] == [x for x in row[ip] if x in res_ip] and count_ip < 3:
            count_ip += 1
        elif count_ip >= 3:
            jx_status_ip = 1
            list_ip = res_ip.copy()
        else:
            count_ip = 0
            res_ip.extend(row[ip])

        if row[port] == [x for x in row[port] if x in res_port] and count_port < 3:
            count_port += 1
        elif count_port >= 3:
            jx_status_port = 1
            list_port = res_port.copy()
        else:
            count_port = 0
            res_port.extend(row[port])

        if row[user] == [x for x in row[user] if x in res_user] and count_user < 3:
            count_user += 1
        elif count_user >= 3:
            jx_status_user = 1
            list_user = res_user.copy()
        else:
            count_user = 0
            res_user.extend(row[user])

        if row[table] == [x for x in row[table] if x in res_table] and count_table < 3:
            count_table += 1
        elif count_table >= 3:
            jx_status_table = 1
            list_table = res_table.copy()
        else:
            count_table = 0
            res_table.extend(row[table])

        if row[col] == [x for x in row[col] if x in res_col] and count_col < 3:
            count_col += 1
        elif count_col >= 3:
            jx_status_col = 1
            list_col = res_col.copy()
        else:
            count_col = 0
            res_col.extend(row[col])

        if row[db] == [x for x in row[db] if x in res_db] and count_db < 3:
            count_db += 1
        elif count_db >= 3:
            jx_status_db = 1
            list_db = res_db.copy()
        else:
            count_db = 0
            res_db.extend(row[db])
    if key1:
        return pd.DataFrame({
            'zc_status': 1,
            'name': name,
            'type': 0,
            'act': act,
            'subject': subject,
            'object': [','.join(list(set(list_ip))) if jx_status_ip == 1 else ','.join(list(set(res_ip))),
                       ','.join(list(set(list_port))) if jx_status_port == 1 else ','.join(list(set(res_port))),
                       ','.join(list(set(list_user))) if jx_status_user == 1 else ','.join(list(set(res_user))),
                       ','.join(list(set(list_table))) if jx_status_table == 1 else ','.join(list(set(res_table))),
                       ','.join(list(set(list_col))) if jx_status_col == 1 else ','.join(list(set(res_col))),
                       ','.join(list(set(list_db))) if jx_status_db == 1 else ','.join(list(set(res_db)))],
            'jx_status': [jx_status_ip, jx_status_port, jx_status_user, jx_status_table, jx_status_col, jx_status_db]
        }, index=[1, 2, 3, 4, 5, 6])
    else:
        return pd.DataFrame({
            'zc_status': 0,
            'name': name,
            'type': 0,
            'act': act,
            'subject': subject,
            'object': [','.join(list(set(res_ip))),
                       ','.join(list(set(res_port))),
                       ','.join(list(set(res_user))),
                       ','.join(list(set(res_table))),
                       ','.join(list(set(res_col))),
                       ','.join(list(set(res_db)))],
            'jx_status': 0
        }, index=[1, 2, 3, 4, 5, 6])


def baseline2(df, p=''):
    p = p.strip()
    ip, port, user, table, col, db = p.split(',')
    df = df.fillna('')
    if ip == 'dest_ip':
        name = 0
        act = ['fwpc_ip', 'fwpc_port', 'fwpc_user', 'fwpc_table', 'fwpc_col', 'fwpc_db']
    else:
        name = 1
        act = ['bfwpc_ip', 'bfwpc_port', 'bfwpc_user', 'bfwpc_table', 'bfwpc_col', 'bfwpc_db']
    res_ip, res_port, res_user, res_table, res_col, res_db = ([], [], [], [], [], [])
    count_ip, count_port, count_user, count_table, count_col, count_db = (0, 0, 0, 0, 0, 0)
    jx_status_ip, jx_status_port, jx_status_user, jx_status_table, jx_status_col, jx_status_db = (0, 0, 0, 0, 0, 0)
    subject = df.iloc[0, 0]
    df = df.tail(10)
    dic1 = {ip: ','.join([','.join(x) for x in df[ip].to_list()]).split(',')}
    # df = df.tail(1)
    # df[ip, port, user, table, col, db] = df[ip, port, user, table, col, db].apply(obj_agg, axis=1)
    ip_list = list(set([x.rsplit(':',1)[0] for x in dic1.get(ip)]))
    return ip_list
    # if key1:
    #     return pd.DataFrame({
    #         'zc_status': 1,
    #         'name': name,
    #         'type': 0,
    #         'act': act,
    #         'subject': subject,
    #         'object': [','.join(list(set(list_ip))) if jx_status_ip == 1 else ','.join(list(set(res_ip))),
    #                    ','.join(list(set(list_port))) if jx_status_port == 1 else ','.join(list(set(res_port))),
    #                    ','.join(list(set(list_user))) if jx_status_user == 1 else ','.join(list(set(res_user))),
    #                    ','.join(list(set(list_table))) if jx_status_table == 1 else ','.join(list(set(res_table))),
    #                    ','.join(list(set(list_col))) if jx_status_col == 1 else ','.join(list(set(res_col))),
    #                    ','.join(list(set(list_db))) if jx_status_db == 1 else ','.join(list(set(res_db)))],
    #         'jx_status': [jx_status_ip, jx_status_port, jx_status_user, jx_status_table, jx_status_col, jx_status_db]
    #     }, index=[1, 2, 3, 4, 5, 6])
    # else:
    #     return pd.DataFrame({
    #         'zc_status': 0,
    #         'name': name,
    #         'type': 0,
    #         'act': act,
    #         'subject': subject,
    #         'object': [','.join(list(set(res_ip))),
    #                    ','.join(list(set(res_port))),
    #                    ','.join(list(set(res_user))),
    #                    ','.join(list(set(res_table))),
    #                    ','.join(list(set(res_col))),
    #                    ','.join(list(set(res_db)))],
    #         'jx_status': 0
    #     }, index=[1, 2, 3, 4, 5, 6])


# def privilege(df,p=''):
#     p = p.strip()
#     for index, row in df.iterrows():
#         # 模型七 越权访问
#         sqls = row['sqls']
#         sqls = sqls.strip()



def obj_agg(row):
    df1 = pd.DataFrame({'table': [x.rsplit(':', 1)[0] for x in row],
                        'num': [int(x.rsplit(':', 1)[1]) for x in row]})
    df1 = df1.groupby('table').sum('num')
    # df1['num'] = df1['num'].astype(str)
    df1 = df1.reset_index()
    # df1['table'] = {x:y for x in df1['table'] for y in df1['num']}
    row = {rows['table']: rows['num'] for _, rows in df1.iterrows()}
    # row = df1.iterrows()
    return row


def tag2dict(df1,df2,p=''):
    df = df1.copy()
    p = p.strip()
    col_list = p.split(',')
    for index,rows in df2.iterrows():
        for col_name in col_list:
            df.loc[:,col_name] = df.loc[:,col_name].apply(lambda x:x.replace(index,rows.loc['value']))
    return df


def find_serve(df,p=''):
    df1 = df.copy()
    p = p.strip()
    for index, row in df1.iterrows():
        s1 = row[p]
        list1 = s1.split(',')
        list2 = [(len(','.join(re.findall(r"""[\u4e00-\u9fa5]+""", x))), x) for x in list1]
        row[p] = max(list2)[1]
    return df1


def transform_utf(df,p=''):
    p = p.strip()
    df1 = df.copy()
    for index, row in df1.iterrows():
        s = row['reg']
        s = eval('b'+'\'' + s + '\'').decode('utf-8') if s.startswith('\\') else s
        row['reg'] = s
    return df1



if __name__ == '__main__':
    #     df1 = pd.DataFrame({
    #         'sqls': ["""SELECT DATABASE()'���SELECT @@session.transaction_isolation
    # """,
    #                  """select seq('attack_record',2012)>��INSERT INTO attack_record (min_time,max_time,srcip,dstip,eventname,area,type,count,cz,business,time_count,time_s_count,id,gmt_create,gmt_modified,creator,owner) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?),(?,?,?,?,?,'�""",
    #                  """UPDATE data_api_new SET url = ?,visits_num = ?,dstip_num = ?,account_num = ?,srcip_num = ?,visits_flow = ?,last_time = ?,gmt_modified = ?  WHERE id=?����UPDATE data_api_new SET url = ?,visits_num = ?,dstip_num = ?,account_num = ?,srcip_num = ?,visits_flow = ?,last_time = ?,gmt_modified = ?  WHERE id=?��UPDATE data_api_new SET url = ?,visits_num = ?,dstip_num = ?,account_num = ?,srcip_num = ?,visits_flow = ?,last_time = ?,gmt_modified = ?  WHERE id=?��UPDATE data_api_new SET url = ?,visits_num = ?,dstip_num = ?,account_num = ?,srcip_num = ?,visits_flow = ?,last_time = ?,gmt_modified = ?  WHERE id=?��UPDATE data_api_new SET url = ?,visits_num = ?,dstip_num = ?,account_num = ?,srcip_num = ?,visits_flow = ?,last_time = ?,gmt_modified = ?  WHERE id=?""",
    #                  '''BEGIN DBMS_OUTPUT.ENABLE(1000000); ''',
    #                  '''SELECT  * FROM ALL_TYPES WHERE OWNER=:1  ORDER BY TYPE_NAME''']
    #     }, index=[0, 1, 2, 3, 4])
    df2 = pd.DataFrame({
        'sqls': [
            """select * from users where id=1 and 1=(select 1 from information_schema.tables where table_schema=‘security’ and table_name regexp ‘^us[a-z]’ limit 0,1)"""
        ]}, index=[0])
    # df3 = pd.DataFrame({
    #     'dest_ip': [["192.168.1.138:3306:dcap:2", "192.168.1.138:3306:dcap:1"],
    #                 ["192.168.1.138:3306:dcap:2", "192.168.1.138:3306:dcap:1"],
    #                 ["192.168.1.138:3306:dcap:2", "192.168.1.138:3306:dcap:1"]]}, index=[0,1,2])
    # df3 = parse_table(df3)
    # df1 = parse_inject(df1)
    # df1 = parse_inject(df1)
    # df2 = pd.read_csv("sqls.csv", encoding='utf-8', dtype=str, na_values='')
    # df4 = baseline(df4, p="dest_ip,dest_port,db_type,db,date")
    # df2 = parse_table(df2)
    # df3[['dest_ip', 'src_ip']] = df3[['dest_ip', 'src_ip']].applymap(obj_agg)
    df4 = parse_inject(df2)
    # df3 = baseline2(df3, 'dest_ip,dest_port,user,base_table,base_col,base_db')
    # df2 = find_serve(df2,p='sqls')
    # df4 = transform_utf(df2)
    print(df4)
