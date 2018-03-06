#!/usr/bin/env python2

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

if __name__=='__main__':
    import wxclient
    wxclient.run_app([scorebug.ScoreBug, lowerthird.LowerThird, lt_banner.LowerThirdBanner])
