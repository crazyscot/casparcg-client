#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Interface class for our Widgets
'''

import abc
from configurable import Configurable

class Widget(Configurable):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def ui_label(self):
        '''
            The label to use in the UI, as a string
        '''
        pass

    @classmethod
    def is_visible(cls, config):
        return config.get_bool(cls.config_section, 'visible', True)
