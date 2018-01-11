
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
