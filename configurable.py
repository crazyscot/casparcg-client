from abc import ABCMeta, abstractproperty

class Configurable(object):
    '''
    Interface class for widgets which play with our config dialog mechanism
    '''
    __metaclass__=ABCMeta

    def get_configurations(self):
        rv = self.my_configurations[:]
        rv.extend((Visible,))
        return rv

    configurations = property(get_configurations, None, None, 'The list of configurable Items for this class')

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
    def default_config(self):
        '''
            A dictionary of default data for this configuration.
            Keys are the label names from the config items.
            For example:

            def MyClass(...):
               default_config = { 'Template' : 'helloworld', 'Layer': 42 }
        '''
        pass

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

class Visible(ConfigItem):
    label='Visible'
    helptext='Show in the interface?'
    # TODO: Checkbox

class Template(ConfigItem):
    label='Template'
    helptext='Name of the Caspar template to use'
    # TODO: Populate as drop-down list from server

class Layer(ConfigItem):
    label='Layer'
    helptext='CG layer number to use'
    # TODO: Integer
