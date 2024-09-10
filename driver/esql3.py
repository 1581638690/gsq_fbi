#!/usr/bin/env python

import os
import json
import requests


class Esql3(object):

    def __init__(self, url='http://localhost:8000', username=None, password=None):
        self.url = url[:-1] if url[-1] == '/' else url
        self.username = username
        self.password = password
        self.headers = None
        self.error = None

        if username and password:
            self.auth()
        else:
            result = self.do_sql('show version;')
            self.error = result['msg'] if result['msg'] != 'success' else None

    def auth(self):
        response = None
        try:
            response = requests.post(self.url + '/login', {'username': self.username, 'password': self.password})
            result = json.loads(response.text)
        except Exception as e:
            response_text = response.text if response else self.url + '/login'
            self.error = '[can\'t access server] %s %s %s' % (os.linesep, response_text, str(e))
            return

        if result['msg'] not in ['log in success!', 'System in not need authentication mode!']:
            self.error = result['msg']
            return

        session = response.cookies.get('session', '')
        remember_token = response.cookies.get('remember_token', '')
        self.headers = {'Cookie': 'remember_token=%s; session=%s' % (remember_token, session)}

    def do_sql(self, sql):
        response = None
        try:
            response = requests.post(self.url + '/json_out', {'sql': sql}, headers=self.headers)
            result = json.loads(response.text)
            if result["msg"]=="success":
                result["msg"]=""
        except Exception as e:
            response_text = response.text if response else self.url + '/json_out'
            result = {'msg': '[can\'t access server] %s %s %s' % (os.linesep, response_text, str(e))}
        return result


if __name__ == '__main__':
    #esql = Esql3('http://10.68.23.85:8001')
    esql = Esql3('http://10.68.23.85:8001', 'test', 'tset')
    if esql.error:
        print(('connect error: %s' % esql.error))
        exit(1)
    print((esql.do_sql('show tables;')))
