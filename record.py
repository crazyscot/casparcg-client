#!/usr/bin/env python

import sys
import amcp
import config

if len(sys.argv)==1:
    raise Exception('Usage: %s verb [filename]'%sys.argv[0])

verb = sys.argv[1]

if len(sys.argv)>2:
    filename = sys.argv[2]
    #key_name = '%s_key.mov'%fn
    #fill_name= '%s_fill.mov'%fn

configfile = 'config.ini'

config = config.config(configfile)
server = amcp.Connection(config, None)

if verb == 'start':
    #server.transact('ADD %d-600 FILE %s' % (config.channel(), fill_name))
    server.transact('ADD %d FILE %s SEPARATE_KEY' % (config.channel(), filename))
elif verb == 'stop':
    #server.transact('REMOVE %d-600' % (config.channel()))
    server.transact('REMOVE %d FILE' % (config.channel()))
else:
    raise Exception('Unknown verb %s'%verb)
