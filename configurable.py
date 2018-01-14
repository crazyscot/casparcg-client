from abc import ABCMeta, abstractproperty
import wx

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
               default_config = { 'Template' : 'helloworld', 'Layer': 42 }
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
    __metaclass__=ABCMeta

    @abstractproperty
    def label(self):
        ''' Label to display in the dialog and the config file '''
        pass

    @abstractproperty
    def helptext(self):
        ''' Help text in the dialog '''
        pass

    @classmethod
    def create_control(cls, parent, value):
        ''' Creates the new wx control for the field and any tooltip.
            May be overridden for special (non-string) types.
        '''
        rv = wx.TextCtrl(parent, value=str(value))
        rv.SetToolTip(wx.ToolTip(cls.helptext))
        return rv

    @classmethod
    def get_value(cls, control):
        ''' Reads out the field, as a string. May be overridden for unusual types. '''
        return control.GetValue()

class CheckBox(ConfigItem):
    '''
        Subclass for boolean (checkbox) types
    '''
    @classmethod
    def create_control(cls, parent, value):
        rv = wx.CheckBox(parent, label='')
        rv.SetValue(str(value).lower() in ('yes','true','t','1'))
        rv.SetToolTip(wx.ToolTip(cls.helptext))
        return rv

    @classmethod
    def get_value(cls, control):
        return str(control.IsChecked())

class Visible(CheckBox):
    label='Visible'
    helptext='Show this widget in the interface?'

class Template(ConfigItem):
    label='Template'
    helptext='Name of the Caspar template (use the CasparCG client to determine this if unsure)'
    # TODO: Populate as drop-down list from server

class Layer(ConfigItem):
    label='Layer'
    helptext='CG layer number to use'
    # TODO: Integer
