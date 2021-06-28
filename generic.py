#!/usr/bin/env python3
#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Entrypoint for the generic client window

To make this work:
    * You MUST be using Caspar 2.1.0beta or later, 2.0 isn't good enough
    * Install the templates to the caspar server's template directory
'''

import wxclient

wxclient.run_app(None)
