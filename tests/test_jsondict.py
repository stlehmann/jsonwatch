"""
    Copyright © 2015 by Stefan Lehmann

"""
import pytest
from jsonwatch.jsonitem import JsonItem
from jsonwatch.jsonnode import JsonNode


@pytest.fixture
def simple_json():
    from jsonwatch.jsonnode import JsonNode
    node = JsonNode('root')
    node.data_from_string('{"item1": 1, "item2": 2}')
    return node

def test_simple_len(simple_json):
    node = simple_json
    assert len(node) == 2

def test_simple_types(simple_json):
    node = simple_json
    for child in node:
        assert isinstance(child, JsonItem)

def test_simple_values(simple_json):
    node = simple_json
    assert node["item1"].value == 1
    assert node["item2"].value == 2

def test_simple_updateitems(simple_json):
    node = simple_json
    node.data_from_string('{"item1": 3, "item2": 4}')
    assert node["item1"].value == 3
    assert node["item2"].value == 4


@pytest.fixture
def nested_json():
    from jsonwatch.jsonnode import JsonNode
    node = JsonNode('root')
    node.data_from_string('''
    {
        "item1": 1,
        "item2": 2,
        "item3": {
            "item1": 1,
            "item2": 2
        }
    }''')
    return node

def test_nested_len(nested_json):
    node = nested_json
    assert len(node) == 3
    assert len(node["item3"]) == 2

def test_nested_type(nested_json):
    node = nested_json
    nesteditem = node['item3']
    assert isinstance(nesteditem, JsonNode)

def test_nested_children(nested_json):
    node = nested_json
    nesteditem = node['item3']
    assert nesteditem['item1'].value == 1
    assert nesteditem['item2'].value == 2
    assert nesteditem['foo'] == None

def test_nested_update(nested_json):
    node = nested_json
    new_json = '''
    {
        "item1": 2,
        "item2": 3,
        "item3": {
            "item1": 4,
            "item2": 5
        }
    }'''
    node.data_from_string(new_json)
    assert node["item1"].value == 2
    assert node["item2"].value == 3
    assert node["item3"]["item1"].value == 4
    assert node["item3"]["item2"].value == 5