"""
    JsonNode.py, Copyright © 2015 by Stefan Lehmann

    Contains the JsonNode class.

"""
import json
from jsonwatch.abstractjsonitem import AbstractJsonItem
from jsonwatch.jsonitem import JsonItem
import bisect


key = lambda x: x[0]
itm = lambda x: x[1]


class JsonNode(AbstractJsonItem):
    """
    This is a json object containing other objects or properties. It is
    identified by a key.

    """
    def __init__(self, key: str, jsonstr: str=None):
        """

        :param str key: name of the object
        :param str jsonstr: json string for the objects and properties of
                            this object

        """
        super().__init__(key)
        self.child_added_callback = None
        self.latest = True
        self.__children = []

        if jsonstr is not None:
            self.values_from_json(jsonstr)

    def __len__(self):
        return len(self.__children)

    def __getitem__(self, key):
        child = self.child_with_key(key)
        if child is None:
            raise KeyError(key)
        return child

    def __iter__(self):
        return (itm(child) for child in self.__children)

    def __repr__(self):
        return "<JsonNode object key:'%s', children:%i>" % \
               (self.key, len(self))

    def __from_dict(self, jsondict):
        def iter_reset_latest(parent):
            for key, child in parent.__children:
                child.latest = False
                if isinstance(child, JsonNode): iter_reset_latest(child)

        # reset the *latest* flag of all children
        iter_reset_latest(self)

        for key, value in jsondict.items():
            child = self.child_with_key(key)
            if child is None:
                # node or item?
                if isinstance(value, dict):
                    child = JsonNode(key)
                    child.__from_dict(value)
                else:
                    child = JsonItem(key)
                    child._raw_value = value

                # add new child
                self.add_child(child)

                # run callback function
                if self.child_added_callback is not None:
                    self.child_added_callback(child)
            else:
                if isinstance(child, JsonNode) and isinstance(value, dict):
                    child.__from_dict(value)
                elif isinstance(child, JsonItem):
                    child._raw_value = value
                    child.latest = True

        self.latest = True

    def __to_dict(self):
        def iter_children(parent):
            jsondict = {}
            for key, child in parent.__children:
                if isinstance(child, JsonNode):
                    jsondict[key] = iter_children(child)
                else:
                    jsondict[key] = child.value
            return jsondict
        return iter_children(self)

    def add_child(self, child):
        """
        Add a child node or item.

        :param AbstractJsonItem child:

        """
        child.parent = self
        bisect.insort(self.__children, (child.key, child))

    def values_from_json(self, jsonstr):
        try:
            jsondata = json.loads(jsonstr)
        except ValueError as e:
            raise ValueError("Corrupt Json string")
        else:
            self.__from_dict(jsondata)

    def values_to_json(self):
        jsondict = self.__to_dict()
        jsonstr = json.dumps(jsondict)
        return jsonstr

    @property
    def keys(self):
        return list(map(key, self.__children))

    def child_at(self, index):
        return itm(self.__children[index])

    def child_with_key(self, key):
        try:
            return next((v for k, v in self.__children if k == key))
        except StopIteration:
            return None

    def child_from_path(self, path: str):
        keys = path.split('/')
        if not keys[0] == self.key:
            return None
        node = self
        for key in  keys[1:]:
            node = node.child_with_key(key)
        return node

    def index(self, item):
        res = (i for (i, child) in enumerate(self.__children)
               if itm(child) == item)
        try:
            return next(res)
        except StopIteration:
            raise ValueError("%s is not in list" % repr(item))

    def update(self, other):
        self.values_from_json(other.values_to_json())

    def remove_child(self, key):
        for k, child in self.__children:
            if k == key: self.__children.remove((k, child))

    def dump(self):
        d = dict((key, child.dump())
                    for key, child in self.__children)
        d['__node__'] = True
        return d

    def _load_config_from_dict(self, jsondict):
        jsondict.pop('__node__')
        for key, item in jsondict.items():
            if item.get('__node__') == True:
                child = JsonNode(key)
            else:
                child = JsonItem(key)
            child._load_config_from_dict(item)
            if self.child_with_key(key) is not None:
                self.remove_child(key)

            self.add_child(child)

    def load(self, string):
        jsondict = json.loads(string)
        self._load_config_from_dict(jsondict)