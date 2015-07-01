"""
    Copyright © 2015 by Stefan Lehmann

"""

import pytest
from jsonwatch.jsonitem import JsonItem
from jsonwatch.jsonnode import JsonNode


nested_json_string = ('{"root":\n'
                      '  {\n'
                      '    "item1": 1,\n'
                      '    "item2": 2,\n'
                      '    "item3": {\n'
                      '        "item1": 1,\n'
                      '        "item2": 2\n'
                      '    }\n'
                      '  }\n'
                      '}')


@pytest.fixture
def nested_json():
    from jsonwatch.jsonnode import JsonNode
    node = JsonNode('root')
    node.from_json(nested_json_string)
    return node

@pytest.fixture
def one_jsonitem():
    return JsonItem('key', name="item1", readonly=False, unit="°C",
                    decimals=1, min=0, max=100, scalefactor=0.01, type='int')

def test_eq(nested_json):
    node = nested_json

    # same object
    item1 = node['item1']
    assert item1 == node['item1']

    # same key, no parent
    item1 = JsonItem('item1')
    assert not item1 == node['item1']

    # same key, different parent
    item1 = node['item3']['item1']
    assert not item1 == node['item1']

def test_init_arguments(one_jsonitem):
    item = one_jsonitem
    assert item.name == 'item1'
    assert item.key == 'key'
    assert item.unit == "°C"
    assert item.decimals == 1
    assert item.min == 0
    assert item.max == 100
    assert item.scalefactor == 0.01

def test_value_conversion(one_jsonitem):
    item = one_jsonitem

    # value to raw value
    item.value = 1.5
    assert item._raw_value == 150

    # raw value to value
    item._raw_value = 150
    assert item.value == 1.5

    # minimum
    with pytest.raises(ValueError) as e:
        item.value = -1
    assert "smaller than minimum" in str(e)

    # maximum
    with pytest.raises(ValueError) as e:
        item.value = 100.1
    assert "bigger than maximum" in str(e)

    # readonly
    item.readonly = True
    with pytest.raises(AttributeError) as e:
        item.value = 20
    assert "JsonItem object is readonly" in str(e)
