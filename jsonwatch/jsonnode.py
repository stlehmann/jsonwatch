"""
    Copyright © 2015 by Stefan Lehmann

"""
import json
from jsonwatch.jsonitem import JsonItem
import bisect


key = lambda x: x[0]
itm = lambda x: x[1]


class JsonNode():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.child_added_callback = None
        self.__children = []

    def __len__(self):
        return len(self.__children)

    def __getitem__(self, key):
        return self.child_with_key(key)

    def __iter__(self):
        return (itm(child) for child in self.__children)

    def __repr__(self):
        return "<JsonNode object key:'%s', children:%i>" % \
               (self.key, len(self))

    def __data_from_dict(self, jsondict):
        for key, value in jsondict.items():
            child = self.child_with_key(key)
            if child is None:
                # node or item?
                if isinstance(value, dict):
                    child = JsonNode(key)
                    child.__data_from_dict(value)
                else:
                    child = JsonItem(key, value)

                # add new child
                self.add_child(child)

                # run callback function
                if self.child_added_callback is not None:
                    self.child_added_callback(child)

            else:
                if isinstance(child, JsonNode) and isinstance(value, dict):
                    child.__data_from_dict(value)
                elif isinstance(child, JsonItem):
                    child.value = value

    def __data_to_dict(self):
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
        child.parent = self
        bisect.insort(self.__children, (child.key, child))

    def data_from_json(self, jsonstr):
        try:
            jsondata = json.loads(jsonstr)
        except ValueError as e:
            raise ValueError("Corrupt Json string")
        else:
            self.__data_from_dict(jsondata)

    def data_to_json(self):
        jsondict = self.__data_to_dict()
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

    def index(self, item):
        res = (i for (i, child) in enumerate(self.__children)
               if itm(child) == item)
        try:
            return next(res)
        except StopIteration:
            raise ValueError("%s is not in list" % repr(item))
