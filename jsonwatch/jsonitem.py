"""
    Copyright (c) 2015 by Stefan Lehmann
    Contains the JsonItem class.

"""

import json
from jsonwatch.abstractjsonitem import AbstractJsonItem, nested_dict_from_list, \
    set_in_dict, type_from_str


class JsonItem(AbstractJsonItem):
    def __init__(self, key, **kwargs):
        super().__init__(key)
        self._raw_value = None
        self.readonly = kwargs.get('readonly', True)
        self.name = kwargs.get('name', "")
        self.unit = kwargs.get('unit', "")
        self.decimals = kwargs.get('decimals', 0)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.scalefactor = kwargs.get('scalefactor', 1)
        self.type = kwargs.get('type', None)
        self.latest = True

    def __repr__(self):
        return "<JsonItem object key:'%s', value: '%s'>" % \
               (self.key, self.value)

    def __len__(self):
        return 0

    def _load_config_from_dict(self, dictionary):
        try:
            dictionary.pop('__node__')
        except KeyError:
            pass

        for key, value in dictionary.items():
            setattr(self, key, value)

    def _dump_config_to_dict(self):
        attributes = ['name', 'readonly', 'unit', 'decimals', 'min', 'max',
                      'scalefactor', 'type']

        return dict((attr, getattr(self, attr)) for attr in attributes
                 if getattr(self, attr) is not None)

    @property
    def value(self):
        if self._raw_value is None:
            return None

        if self.type in ('int', 'float', None):
            return self._raw_value * self.scalefactor
        elif self.type == 'bool':
            return self._raw_value

    @value.setter
    def value(self, val):
        if self.readonly:
            raise AttributeError("JsonItem object is readonly")

        if val is None:
            self._raw_value = None
            return

        if self.max is not None and val > self.max:
            raise ValueError("value is bigger than maximum")

        if self.min is not None and val < self.min:
            raise ValueError("value is smaller than minimum")

        # scale to raw value
        if self.type == 'int':
            self._raw_value = round(val / self.scalefactor)
        elif self.type == 'float':
            self._raw_value = val / self.scalefactor
        elif self.type in ('bool', 'str'):
            self._raw_value = val

    def value_str(self):
        if self.value is None:
            return ""

        if self.type in ('float', 'int'):
            return "%.*f" % (self.decimals, self.value)
        else:
            return str(self.value)

    def dump(self):
        json.dumps(self._dump_config_to_dict())

    def load(self, string):
        d = json.loads(string)
        self._load_config_from_dict(d)

    def to_json(self):
        jsondict = nested_dict_from_list(self.path)
        set_in_dict(jsondict, self.path, self._raw_value)
        jsonstr = json.dumps(jsondict)
        return jsonstr