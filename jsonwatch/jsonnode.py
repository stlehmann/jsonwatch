"""
    Copyright © 2015 by Stefan Lehmann

"""
import json
from jsonwatch.jsonitem import JsonItem


class JsonNode():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.__children = {}
        self.__keys = []

    def __len__(self):
        return len(self.__children)

    def __getitem__(self, key):
        return self.__children.get(key)

    def __iter__(self):
        return iter(self.__children.values())

    def __data_from_dict(self, jsondict):
        for key, value in jsondict.items():
            child = self.__children.get(key)
            if child is None:
                if isinstance(value, dict):
                    new_node = JsonNode(key)
                    new_node.__data_from_dict(value)
                    new_node.parent = self
                    self.__children[key] = new_node
                else:
                    new_item = JsonItem(key, value)
                    new_item.parent = self
                    self.__children[key] = new_item
            else:
                if isinstance(child, JsonNode) and isinstance(value, dict):
                    child.__data_from_dict(value)
                elif isinstance(child, JsonItem):
                    child.value = value

        self.__keys = sorted(list(self.__children.keys()))

    def data_from_json(self, jsonstr):
        try:
            jsondata = json.loads(jsonstr)
        except ValueError as e:
            raise ValueError("Corrupt Json string")
        else:
            self.__data_from_dict(jsondata)

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
        raise ValueError("%s is not in list" % repr(child))
