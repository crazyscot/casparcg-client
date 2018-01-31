#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Interface class for our Widgets
'''

import abc
from configurable import Configurable, Layer, Template
import amcp

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

    def channel(self):
        return self.parent.channel()
    def layer(self):
        return self.config.get_int(self.config_section, Layer.label, self.my_default_config[Layer.label])
    def template(self):
        return self.config.get(self.config_section, Template.label, self.my_default_config[Template.label])

    @abc.abstractmethod
    def templateData(self):
        pass

    def validate(self):
        return True

    def do_anim_on(self, event):
        if not self.validate():
            return
        # CG channel-layer ADD 1 template 1 data
        self.parent.transact('CG %d-%d ADD 1 %s 1 %s'%(self.channel(), self.layer(), amcp.quote(self.template()), self.templateData()))

    def do_anim_off(self, event):
        # CG channel STOP layer
        self.parent.transact('CG %d-%d STOP 1'%(self.channel(), self.layer()))

    def do_remove(self, event):
        # CG channel-layer REMOVE 1
        self.parent.transact('CG %d-%d REMOVE 1'%(self.channel(), self.layer()))
