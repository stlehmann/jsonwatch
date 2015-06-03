"""
    Copyright © 2015 by Stefan Lehmann

"""
import json
from jsonwatch.jsonitem import JsonItem


class JsonNode():
    def __init__(self, key):
        self.key = key
        self.__children = {}

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
                    self.__children[key] = new_node
                else:
                    new_item = JsonItem(key, value)
                    self.__children[key] = new_item
            else:
                if isinstance(child, JsonNode) and isinstance(value, dict):
                    child.__data_from_dict(value)
                elif isinstance(child, JsonItem):
                    child.value = value

    def data_from_string(self, jsonstr):
        try:
            jsondata = json.loads(jsonstr)
        except ValueError as e:
            raise e
        else:
            self.__data_from_dict(jsondata)