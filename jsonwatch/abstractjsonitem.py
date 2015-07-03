"""
    Copyright © 2015 by Stefan Lehmann

"""

def nested_dict_from_list(parents, dict_={}):
    if len(parents):
        return {parents[0]: nested_dict_from_list(parents[1:], dict_)}
    else:
        return {}


def set_in_dict(data_dict, maplist, value):
    for k in maplist[:-1]: data_dict = data_dict[k]
    data_dict[maplist[-1]] = value


VALUETYPES = [('int', int), ('float', float), ('bool', bool), ('str', str)]


def type_from_str(typestring):
    for s, t in VALUETYPES:
        if s == typestring:
            return t

def type_to_str(type_):
    for s, t in VALUETYPES:
        if t == type_:
            return s

class AbstractJsonItem:
    """
    Abstract base clas for JsonNode and JsonItem.

    :ivar "JsonNode" parent: parent node
    :ivar str key: key for this item

    """
    def __init__(self, key):
        self.parent = None
        self._key = key
        self.name = ""

    def __eq__(self, other):
        return type(self) == type(other) and self.path == other.path

    # path property
    @property
    def path(self):
        """
        Return the complete key pass for the current item.

        :rtype: list of str

        """
        def iter_keys(item):
            path = []
            if item.parent is not None:
                path.extend(iter_keys(item.parent))
            path.append(item.key)
            return path

        return list(iter_keys(self))

    # key property
    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if self.parent is None: return
        self.parent.remove(self.key)
        self._key = value
        self.parent.add(self)



