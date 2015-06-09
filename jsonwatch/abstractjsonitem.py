"""
    Copyright © 2015 by Stefan Lehmann

"""


class AbstractJsonItem:
    """
    Abstract base clas for JsonNode and JsonItem.

    :ivar "JsonNode" parent: parent node
    :ivar str key: key for this item

    """
    def __init__(self, key):
        self.parent = None
        self.key = key

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

        return iter_keys(self)

