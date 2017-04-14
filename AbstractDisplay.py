from abc import ABCMeta, abstractmethod


class AbstractDisplay(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def hide(self):
        pass
