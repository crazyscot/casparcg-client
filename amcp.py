#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
    Python (2) interface to v2.1 of the CasparCG AMCP protocol
    Note that not all parts of the protocol are implemented - only what I needed.
'''

import socket
import ConfigParser
import json
import globalwidget

def code_lookup(c):
    if c==400:
        return 'Unspecified client error'
    elif c==401:
        return 'Illegal video channel'
    elif c==402:
        return 'Parameter missing'
    elif c==403:
        return 'Illegal parameter'
    elif c==404:
        return 'Media file not found'
    elif c>=400 and c<500:
        return 'Unknown client error code'
    elif c==500:
        return 'Unspecified internal server error'
    elif c==501:
        return 'Internal server error'
    elif c==502:
        return 'Media file unreadable'
    elif c==503:
        return 'Access error'
    elif c>=500 and c<600:
        return 'Unknown server error code'
    else:
        return 'Unknown error code'

class AMCPException(Exception):
    def __init__(self, code, info):
        self.code = code
        self.info = info
    def __str__(self):
        return '%s (%s): %s' %(self.code, code_lookup(self.code), self.info)

class ClientError(AMCPException):
    pass
class ServerError(AMCPException):
    pass

class Connection(object):
    def __init__(self, config, reporter=None):
        '''
        Initialise a connection wrapping object.
        Doesn't actually connect until we need to.

        If reporter is not None, its status() method may be called
        at any time with a human-readable text string.
        '''
        self.socket = None # we'll connect on demand
        self.server = None
        self.port = None
        self.reporter = reporter
        self.config = config

    def connect(self):
        self.server = globalwidget.get_server(self.config)
        self.port = globalwidget.get_port(self.config)
        self.socket = socket.create_connection((self.server, self.port), 5)

    def server_changed(self):
        return not ( (self.server == globalwidget.get_server(self.config)) and (self.port == globalwidget.get_port(self.config)) )

    def info(self, what=''):
        ''' INFO command/subcommand '''
        return self.transact('INFO '+what)
    def version(self, what=''):
        ''' VERSION command/subcommand '''
        return self.transact('VERSION '+what)

    def report(self,msg):
        if self.reporter is not None:
            self.reporter.status(msg)
            self.reporter.update()

    def transact(self, command):
        '''
        Error-checking transaction
        '''
        if self.socket and self.server_changed():
            self.socket.close()
            self.socket = None
        if self.socket is None:
            self.report('Connecting to server...')
            self.connect()
        try:
            self.socket.send( (command+'\r\n').encode('utf-8') )
        except Exception as e:
            self.socket=None
            raise Exception('server connection lost (%s)'%e)

        # Read until we see a \r\n
        response = ''
        while not response.endswith('\r\n'):
            tmp = self.socket.recv(4096).decode('utf-8')
            if len(tmp) is 0: # socket closed
                self.socket=None
                raise Exception('server connection lost')
            response += tmp

        raw = response.strip().split('\r\n')
        (status, info) = raw[0].split(' ',1)
        status=int(status)
        if status==202:
            # OK, no data beyond the status line
            return info
        elif status==201:
            # OK, one line data
            return raw[1]
        elif status==200:
            # OK, multiline data, make sure we've got it all
            while not response.endswith('\r\n\r\n'):
                response += self.socket.recv(4096).decode('utf-8')
            return response.strip().split('\r\n')[1:]
        elif status>=400 and status<500:
            raise ClientError(status, info)
        elif status>=500 and status<600:
            raise ServerError(status, info)
        # That's interesting, we didn't recognise the status code.
        raise AMCPException(status, info)

def quote(s):
    '''
        Quotes a parameter for transit over AMCP
        Rules:
            \ -> \\
            Newline -> \n
            " -> \"
            Then, if there's a space, put double quotes around the whole thing.
    '''
    s=s.replace('\\','\\\\')
    s=s.replace('\r\n', '\n')
    s=s.replace('\n\r', '\n')
    s=s.replace('\n', '\\n')
    s=s.replace('"', '\\"')
    if '"' in s:
        s="\"%s\""%s
    return s

def unquote(s):
    ''' Reverse of quote() '''
    if s[0]=='"' and s[-1]=='"':
        s = s[1:-1]
    s=s.replace('\\"','"')
    s=s.replace('\\n', '\n')
    s=s.replace('\\\\','\\')
    return s

def jsondata(obj):
    '''
        Serialises an object (dictionary) as JSON, quoted for Caspar/AMCP
    '''
    return quote(json.dumps(obj))

if __name__=='__main__':
    for s in ['abc', 'abc"', 'a b', 'a "b c"', 'a\\b', 'a\nb', 'a\n"b \\c"']:
        assert unquote(quote(s)) == s, 'quote unquote test: %s'%s
