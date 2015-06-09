"""
    Copyright © 2015 by Stefan Lehmann

"""
from jsonwatch.abstractjsonitem import AbstractJsonItem


class JsonItem(AbstractJsonItem):
    def __init__(self, key, value):
        super().__init__(key)
        self.__value = None
        self.value = value
        self.latest = True

    def __repr__(self):
        return "<JsonItem object key:'%s', value: '%s'>" % \
               (self.key, self.value)

    def __eq__(self, other):
        return self.parent == other.parent and self.key == other.key

    def __len__(self):
        return 0

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.latest = True
        self.__value = val