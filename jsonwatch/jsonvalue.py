"""
    Copyright © 2015 by Stefan Lehmann

"""
from jsonwatch.abstractjsonitem import AbstractJsonItem


class JsonValue(AbstractJsonItem):
    def __init__(self, key, **kwargs):
        super().__init__(key)
        self._raw_value = None
        self.readonly = kwargs.get('readonly', True)
        self.name = kwargs.get('name', "")
        self.unit = kwargs.get('unit', "")
        self.decimals = kwargs.get('decimals', 3)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.numerator = kwargs.get('numerator', 1)
        self._denominator = kwargs.get('denominator', 1)
        self.latest = True

    def __repr__(self):
        return "<JsonItem object key:'%s', value: '%s'>" % \
               (self.key, self.value)

    def __len__(self):
        return 0

    @property
    def value(self):
        if self._raw_value is None:
            return None

        return self._raw_value * self.denominator / self.numerator

    @value.setter
    def value(self, val):
        if self.readonly:
            raise AttributeError("JsonValue object is readonly")

        if val is None:
            self._raw_value = None
            return

        if self.max is not None and val > self.max:
            raise ValueError("value is bigger than maximum")

        if self.min is not None and val < self.min:
            raise ValueError("value is smaller than minimum")

        self._raw_value = val * self.numerator / self.denominator

    @property
    def denominator(self):
        return self._denominator

    @denominator.setter
    def denominator(self, val):
        if val == 0: raise ValueError("denominator can not be 0")
        self._denominator = val

    def value_str(self):
        if self.value is None:
            return ""
        return "%.*f" % (self.decimals, self.value)