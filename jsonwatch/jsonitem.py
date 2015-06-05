"""
    Copyright © 2015 by Stefan Lehmann

"""


class JsonItem():
    def __init__(self, key, value):
        self.__value = None
        self.parent = None
        self.key = key
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