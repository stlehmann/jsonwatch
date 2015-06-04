"""
    Copyright © 2015 by Stefan Lehmann

"""
import json
from jsonwatch.jsonitem import JsonItem


class JsonNode():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.child_added_callback = None
        self.__children = {}
        self.__keys = []

    def __len__(self):
        return len(self.__children)

    def __getitem__(self, key):
        return self.__children.get(key)

    def __iter__(self):
        return iter(self.__children.values())

    def __repr__(self):
        return "<JsonNode object key:'%s', children:%i>" % \
               (self.key, len(self))

    def __data_from_dict(self, jsondict):
        for key, value in jsondict.items():
            child = self.__children.get(key)
            if child is None:
                # node or item?
                if isinstance(value, dict):
                    child = JsonNode(key)
                    child.__data_from_dict(value)
                else:
                    child = JsonItem(key, value)

                # add new child to children
                child.parent = self
                self.__children[key] = child

                # create keys
                self.__keys = sorted(list(self.__children.keys()))

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
            for key, child in parent.__children.items():
                if isinstance(child, JsonNode):
                    jsondict[key] = iter_children(child)
                else:
                    jsondict[key] = child.value
            return jsondict
        return iter_children(self)

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
        return self.__keys

    def item_at(self, index):
        key = self.__keys[index]
        return self.__children[key]

    def index(self, item):
        for i, key in enumerate(self.keys):
            child = self.__children[key]
            if child == item:
                return i
        raise ValueError("%s is not in list" % repr(item))
