'''
    Python (2) interface to v2.1 of the CasparCG AMCP protocol
    Note that not all parts of the protocol are implemented - only what I needed.
'''

import socket
import configparser

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
        return 'Status %s (%s): %s' %(self.code, code_lookup(self.code), self.info)

class ClientError(AMCPException):
    pass
class ServerError(AMCPException):
    pass

class Connection(object):
    def __init__(self, server='127.0.0.1', port=5250):
        self.server = server
        self.port = port
        self.socket = None # we'll connect on demand
        self.read_config() # INI file overrides parameters

    def read_config(self):
        cp = configparser.ConfigParser()
        cp.read('amcp.ini')
        try:
            self.server = cp.get('server','host')
        except configparser.ConfigParser.Error:
            pass
        try:
            self.port = int(cp.get('server','port'))
        except configparser.ConfigParser.Error:
            pass

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server, self.port))
        self.socket = s

    def transact_raw(self, command):
        ''' Sends command, returns raw response '''
        if self.socket is None:
            self.connect()
        self.socket.send( (command+'\r\n').encode('utf-8') )
        response = ''
        while not response.endswith('\r\n'):
            response += self.socket.recv(4096).decode('utf-8')
            # N.B. This may not read all the response, if you're unlucky.
        return response

    def info(self, what=''):
        ''' INFO command/subcommand '''
        return self.transact('INFO '+what)
    def version(self, what=''):
        ''' VERSION command/subcommand '''
        return self.transact('VERSION '+what)

    def transact(self, command):
        '''
        Error-checking transaction
        '''
        if self.socket is None:
            self.connect()
        self.socket.send( (command+'\r\n').encode('utf-8') )
        # Read until we see a \r\n
        response = ''
        while not response.endswith('\r\n'):
            response += self.socket.recv(4096).decode('utf-8')

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


if __name__=='__main__':
    for s in ['abc', 'abc"', 'a b', 'a "b c"', 'a\\b', 'a\nb', 'a\n"b \\c"']:
        assert unquote(quote(s)) == s, 'quote unquote test: %s'%s
