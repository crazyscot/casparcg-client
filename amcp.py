'''
    Python (2) interface to v2.1 of the CasparCG AMCP protocol
    Note that not all parts of the protocol are implemented - only what I needed.
'''

import socket
import configparser

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

    def transact(self, command):
        ''' Sends command, returns raw response '''
        if self.socket is None:
            self.connect()
        self.socket.send( (command+'\r\n').encode('utf-8') )
        # Read until we see a \r\n
        response = ''
        while not response.endswith('\r\n\r\n'):
            response += self.socket.recv(4096).decode('utf-8')
        return response

    def info(self, what=''):
        ''' INFO command/subcommand '''
        return self.transact('INFO '+what)
