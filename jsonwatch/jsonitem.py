"""
    Copyright © 2015 by Stefan Lehmann

"""

class JsonItem():
    def __init__(self, key, value):
        self.__value = None
        self.key = key
        self.value = value

    def __repr__(self):
        return "<JsonItem object key:'%s', value: '%s'>" % \
               (self.key, self.value)

    def __eq__(self, other):
        return self.key == other.key