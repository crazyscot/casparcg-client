#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Interface class for configurable wx widgets and various helper types
'''

from abc import ABCMeta, abstractproperty
import wx
import string

class classproperty(object):
    ''' Decorator for read-only class properties '''
    def __init__(self, fget):
        self.fget = fget
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class Configurable(object):
    '''
    Interface class for widgets which play with our config dialog mechanism
    '''
    __metaclass__=ABCMeta

    @classproperty
    def configurations(cls):
        rv = cls.my_configurations[:]
        rv.extend((Visible,))
        return rv

    @abstractproperty
    def my_configurations(self):
        '''
            Returns this class's list of Items.
            This is a read-only property, so you should initialise it like this:
            def MyClass(...):
                configurations_=[foo,bar]

            NOTE: Do not include 'Visible', that is implicit.
            NOTE: All items must have distinct labels.
        '''
        pass

    @abstractproperty
    def config_section(self):
        '''
            The name of the section in the INI file to use for this widget.
        '''
        pass

    @abstractproperty
    def my_default_config(self):
        '''
            A dictionary of default data for this configuration.
            Keys are the label names from the config items.
            For example:

            def MyClass(...):
               default_config = { 'Template' : 'lowerthird', 'Layer': 42 }
        '''
        pass

    @classmethod
    def default_config(self):
        ''' Default data including implicit fields '''
        rv = {}
        rv.update({'Visible' : 1}) # TODO Default visibility for new config items
        rv.update(self.my_default_config)
        return rv

class ConfigItem(object):
    '''
        Class representing a configurable item
    '''
    def __init__(self, label, helptext):
        self.label = label
        self.helptext = helptext

    def create_control(self, parent, value):
        ''' Creates the new wx control for the field and any tooltip.
            May be overridden for special (non-string) types.
        '''
        rv = wx.TextCtrl(parent, value=str(value))
        rv.SetToolTip(wx.ToolTip(self.helptext))
        return rv

    def get_value(self, control):
        ''' Reads out the field, as a string. May be overridden for unusual types. '''
        return control.GetValue()

class BoolConfigItem(ConfigItem):
    '''
        Subclass for boolean (checkbox) types
    '''
    def create_control(self, parent, value):
        rv = wx.CheckBox(parent, label='')
        rv.SetValue(str(value).lower() in ('yes','true','t','1'))
        rv.SetToolTip(wx.ToolTip(self.helptext))
        return rv

    def get_value(self, control):
        return str(control.IsChecked())


class FieldValidator(wx.PyValidator):
    ''' A configurable validator for text controls '''
    def __init__(self, allowDigits=True, allowLetters=True, allowColon=False):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.onChar)
        self.allowDigits=allowDigits
        self.allowLetters=allowLetters
        self.allowColon=allowColon
    def Clone(self):
        return FieldValidator(self.allowDigits, self.allowLetters, self.allowColon)
    def Validate(self, win):
        return True
    def TransferToWindow(self):
        return True
    def TransferFromWindow(self):
        return True
    def onChar(self, event):
        keycode = int(event.GetUnicodeKey())
        if keycode == wx.WXK_NONE or keycode == 8:
            # Always allow cursor keys, backspace (8), etc.
            event.Skip()
            return

        if keycode < 256:
            key = chr(keycode)
            if key in string.letters:
                if not self.allowLetters: return
            elif key in string.digits:
                if not self.allowDigits: return
            elif key == ':':
                if not self.allowColon: return
            else: # key not in any set we recognise
                return
            event.Skip()
        else:
            # extended unicode, not allowed for now
            return

class IntConfigItem(ConfigItem):
    def create_control(self, parent, value):
        rv = wx.TextCtrl(parent, value=str(value), validator=FieldValidator(allowLetters=False))
        rv.SetToolTip(wx.ToolTip(self.helptext))
        return rv

class ListConfigItem(ConfigItem):
    '''
    A multiple-choice item. @items must be an array of strings.
    '''
    def __init__(self, label, helptext, items):
        '''
        @items should be an array of strings.
        '''
        super(ListConfigItem, self).__init__(label, helptext)
        self.items = items

    def create_control(self, parent, value):
        rv = wx.Choice(parent, choices=self.items)
        rv.SetSelection( self.items.index(value) )
        rv.SetToolTip(wx.ToolTip(self.helptext))
        return rv
    def get_value(self, control):
        return self.items[control.GetSelection()]


Visible = BoolConfigItem('Visible', 'Show this widget in the master client? (Quit and reopen to take effect)')

Template = ConfigItem(label='Template', helptext='Name of the Caspar template (use the CasparCG client to determine this if unsure)')

Layer = IntConfigItem('Layer', 'CG layer number to use')

