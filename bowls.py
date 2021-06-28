#!/usr/bin/env python3

#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Lawn bowls mode
'''

import amcp
import wx
import sys
from configurable import Configurable,FieldValidator
import configurable
from widget import Widget
import datetime
from scoreextra import ScoreExtra
import scorebug
import lowerthird
import lt_banner
import history

if __name__=='__main__':
    import wxclient
    wxclient.run_app([history.ScoreHistory1, lowerthird.LowerThird, lt_banner.LowerThirdBanner])
