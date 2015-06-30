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


class AbstractJsonItem:
    """
    Abstract base clas for JsonNode and JsonItem.

    :ivar "JsonNode" parent: parent node
    :ivar str key: key for this item

    """
    def __init__(self, key):
        self.parent = None
        self.key = key
        self.name = ""

    def __eq__(self, other):
        return type(self) == type(other) and self.path == other.path

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

