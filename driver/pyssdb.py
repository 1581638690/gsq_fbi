#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pyssdb
~~~~~~~

A SSDB Client Library for Python.

:copyright: (c) 2013-2017 by Yue Du.
:license: BSD 2-clause License, see LICENSE for more details.
'''

from __future__ import print_function
import os
import sys
import socket
import functools
import itertools


__version__ = '0.4.2'
__author__ = 'Yue Du <ifduyue@gmail.com>'
__url__ = 'https://github.com/ifduyue/pyssdb'
__license__ = 'BSD 2-Clause License'


PY3 = sys.version_info >= (3,)

if PY3:
    unicode = str
    from itertools import zip_longest
else:
    from itertools import izip_longest as zip_longest


def utf8(s):
    s = str(s) if isinstance(s, int) else s
    return s.encode('utf8') if isinstance(s, unicode) else s


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    "Copy From itertools Recipes"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


class error(Exception):
    def __init__(self, reason, *args):
        super(error, self).__init__(reason, *args)
        self.reason = reason
        self.message = ' '.join(args)


class Connection(object):
    def __init__(self, host='127.0.0.1', port=8888, socket_timeout=None):
        self.pid = os.getpid()
        self.host = host
        self.port = port
        self.socket_timeout = socket_timeout
        self._sock = None
        self._fp = None

    def connect(self):
        if self._sock:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.socket_timeout)
            sock.connect((self.host, self.port))
            self._sock = sock
            self._fp = sock.makefile('rb')
        except socket.error:
            raise
        #add by gjw on 2023-0210 认证
        self.send("auth","c42c1569a4f651346402e3d6bcd49d2b")
        data = self.recv()
		
    def disconnect(self):
        if self._sock is None:
            return
        try:
            self._sock.close()
        except socket.error:
            pass
        self._sock = self._fp = None

    close = disconnect

    def reconnect(self):
        self.disconnect()
        self.connect()

    def send(self, cmd, *args):
        if cmd == 'delete':
            cmd = 'del'
        self.last_cmd = cmd
        if self._sock is None:
            self.connect()

        args = [utf8(cmd)] + [utf8(i) for i in args]
        buf = utf8('').join(utf8('%d\n%s\n') % (len(i), i) for i in args) + utf8('\n')
        self._sock.sendall(buf)

    def recv(self):
        cmd = self.last_cmd
        ret = []
        while True:
            line = self._fp.readline().rstrip(utf8('\n'))
            if not line:
                break
            data = self._fp.read(int(line))
            self._fp.read(1)  # discard '\n'
            #ret.append(data)
            try:
               ret.append(data.decode("utf8")) #add by gjw on 20201018
            except:
               ret.append(data)

        st, ret = ret[0], ret[1:]
        #st = status.decode('utf8')
                
        if st == 'not_found':
            return None
        elif st == 'ok':
            if cmd.endswith('keys') or cmd.endswith('hgetall') or cmd.endswith('list') or \
                    cmd.endswith('scan') or cmd.endswith('hscan') or cmd.endswith('range') or \
                    (cmd.startswith('multi_') and cmd.endswith('get')) or \
                    cmd.endswith('getall'):
                return ret
            elif cmd == 'info':
                return ret[1:]
            elif len(ret) == 1:
                if cmd.endswith('set') or cmd.endswith('del') or \
                        cmd.endswith('incr') or cmd.endswith('decr') or \
                        cmd.endswith('size') or cmd.endswith('rank') or \
                        cmd in ('setx', 'zget', 'qtrim_front', 'qtrim_back'):
                    return int(ret[0])
                else:
                    return ret[0]
            elif not ret:
                return True
            else:
                return ret 

        raise error(st, *ret)


class ConnectionPool(object):
    def __init__(self, connection_class=Connection, max_connections=1048576,
                 **connection_kwargs):
        self.pid = os.getpid()
        self.connection_class = connection_class
        self.connection_kwargs = connection_kwargs
        self.max_connections = max_connections
        self.idle_connections = []
        self.active_connections = set()

    def checkpid(self):
        if self.pid != os.getpid():
            self.disconnect()
            self.__init__(self.connection_class, self.max_connections,
                          **self.connection_kwargs)

    def get_connection(self):
        self.checkpid()
        try:
            connection = self.idle_connections.pop()
        except IndexError:
            connection = self.new_connection()
            connection = self.idle_connections.pop()
        self.active_connections.add(connection)
        return connection

    def new_connection(self):
        count = len(self.active_connections) + len(self.idle_connections)
        if count > self.max_connections:
            raise error("Too many connections")
        #return self.connection_class(**self.connection_kwargs)
        #modify by gjw on 2021-0816 创建时就链接好
        connection = self.connection_class(**self.connection_kwargs)
        connection.connect()
        self.idle_connections.append(connection)
        return connection

    def release(self, connection, error=False):
        self.checkpid()
        if connection.pid == self.pid:
            if not error:
                self.active_connections.remove(connection)
                self.idle_connections.append(connection)
            else:
                connection.close()
                self.active_connections.remove(connection)

    def disconnect(self):
        acs, self.active_connections = self.active_connections, set()
        ics, self.idle_connections = self.idle_connections, []
        for connection in itertools.chain(acs, ics):
            connection.disconnect()

    close = disconnect


def command_post_processing(func):

    @functools.wraps(func)
    def wrapper(self, cmd, *args):

        data = func(self, cmd, *args)
        if 'info' == cmd:
            return dict(grouper(data, 2, None))
        else:
            return data

    return wrapper


class Client(object):
    def __init__(self, host='127.0.0.1', port=8888, connection_pool=None,
                 socket_timeout=None, max_connections=1000):
        if not connection_pool:
            connection_pool = ConnectionPool(host=host, port=port,
                                             socket_timeout=socket_timeout,
                                             max_connections=max_connections)
        self.connection_pool = connection_pool
        self.connection_pool.new_connection()
        self._close = False
        #connection.connect()
        #self.connection_pool.idle_connections.append(connection)

    @command_post_processing
    def execute_command(self, cmd, *args):
        connection = self.connection_pool.get_connection()
        try:
            connection.send(cmd, *args)
            data = connection.recv()
            self.connection_pool.release(connection)
            return data
        except Exception as e:
            try:
                self.connection_pool.release(connection, error=True)
            except:
                pass
            #add by gjw on 20200808, 出错自动再执行一次
            try:
                connection = self.connection_pool.get_connection()
                connection.send(cmd, *args)
                data = connection.recv()
                self.connection_pool.release(connection)
                return data
            except Exception as e2:
                #add by gjw on 2022-0216 出现异常释放链接
                self.connection_pool.release(connection, error=True)
                raise Exception("SSDB执行{}出现异常,参数:{}".format(cmd,args))
    #end execute_command

    def disconnect(self):
        self.connection_pool.disconnect()
        self._close = True

    def is_close(self):
        return self._close

    #变成一个假的关闭,实际不产生任何影响,modify by gjw on 2022-0210
    def close(self):
        pass
    
    def __getattr__(self, cmd):
        if cmd not in self.__dict__:
            self.__dict__[cmd] = functools.partial(self.execute_command, cmd)

        return self.__dict__[cmd]


if __name__ == '__main__':
    c = Client()
    #print(c.set('key', 'value'))
    #print(c.get('key'))
    print(c.keys('a', 'z', 100))
    print(c.scan('a', 'z', 10))
    #print(c.keys('a', 'z', 10))
    print(c.set('中文', b'gghhh'))
    print(c.get('中文2'))
    print(c.exists('中文'))
    for i in range(10000):
        c.hset("test22",i,i)
    #print(c.info())
    c.disconnect()
