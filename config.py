
from ConfigParser import *

SERVER='server'
CHANNEL='channel'

class config(object):
    '''
        Proxy class to the config on disk.
        Wraps a ConfigParser, but with syntactic sugar.
    '''
    def __init__(self, filename='config.ini'):
        '''
            The initialiser also loads the config from disk, assuming it can.
            (If the file does not exist, you get an empty config.)
        '''
        self.filename = filename
        self.reload()

    def reload(self, filename=None):
        if filename is None:
            filename=self.filename
        self.parser = ConfigParser()
        self.parser.read(filename)

    def write(self, filename=None):
        ''' Write to disk. Defaults to the filename we read from. '''
        if filename is None:
            filename=self.filename
        with open(filename, 'w') as cf:
            self.parser.write(cf)

    def get(self, section, item, default=None):
        '''
            Config accessor.
            Returns the default if the section or item do not exist.
        '''
        try:
            return self.parser.get(section,item)
        except:
            return default

    def get_int(self, section, item, default=0):
        '''
            Convenience wrapper to get() which coerces the result to an int.
        '''
        return int(self.get(section, item, default))

    def get_bool(self, section, item, default=0):
        '''
            Convenience wrapper to get() which does the boolean interpretation thing
        '''
        try:
            return self.parser.getboolean(section,item)
        except:
            return default

    def put(self, section, item, value):
        '''
            Config accessor.
            Creates the section if it doesn't exist.
            Overwrites the item if it doesn't exist.
            Does NOT write - call write() for that.
        '''
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, item, value)

    def section(self, section):
        '''
            Bulk access to the dict for a config section.
            Creates the section if it doesn't already exist.
            (Note that keys and values are always Unicode strings.)
            (Note that configparser matches case-insensitively!)
        '''
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        return self.parser._sections[section]

    def channel(self):
        '''
            Quick access to the Caspar channel this system is to use globally.
            Configure as
                [server]
                channel=1
        '''
        return self.get_int(SERVER, CHANNEL, 1)
