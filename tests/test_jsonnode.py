"""
    Copyright © 2015 by Stefan Lehmann

"""
import pytest
import json
from jsonwatch.jsonitem import JsonItem
from jsonwatch.jsonnode import JsonNode


simple_json_string = '{"item1": 1, "item2": 2}'
nested_json_string = ('\n'
                      '    {\n'
                      '        "item1": 1,\n'
                      '        "item2": 2,\n'
                      '        "item3": {\n'
                      '            "item1": 1,\n'
                      '            "item2": 2\n'
                      '        }\n'
                      '    }')


@pytest.fixture
def simple_json():
    from jsonwatch.jsonnode import JsonNode
    node = JsonNode('root')
    node.data_from_json(simple_json_string)
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
    node.data_from_json('{"item1": 3, "item2": 4}')
    assert node["item1"].value == 3
    assert node["item2"].value == 4

def test_data_to_json(simple_json):
    node = simple_json
    jsonstr = node.data_to_json()
    assert json.loads(jsonstr) == json.loads(simple_json_string)

@pytest.fixture
def nested_json():
    from jsonwatch.jsonnode import JsonNode
    node = JsonNode('root')
    node.data_from_json(nested_json_string)
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
        "item2": 3,
        "item1": 2,
        "item3": {
            "item1": 4,
            "item2": 5
        }
    }'''
    node.data_from_json(new_json)
    assert node["item1"].value == 2
    assert node["item2"].value == 3
    assert node["item3"]["item1"].value == 4
    assert node["item3"]["item2"].value == 5

def test_keys(nested_json):
    node = nested_json
    new_json = '''
    {
        "first": 10,
        "last": 20
    }
    '''
    node.data_from_json(new_json)
    assert node.keys[0] == "first"
    assert node.keys[1] == "item1"
    assert node.keys[2] == "item2"
    assert node.keys[3] == "item3"
    assert node.keys[4] == "last"

def test_item_at(nested_json):
    node = nested_json
    assert node.child_at(0).key == "item1"
    assert node.child_at(1).key == "item2"
    assert node.child_at(2).key == "item3"

def test_index(nested_json):
    node = nested_json
    item1 = node["item1"]
    item2 = node["item2"]
    assert node.index(item1) == 0
    assert node.index(item2) == 1

    # Test for ValueError if not in list
    noitem = JsonItem("noitem", 0)
    with pytest.raises(ValueError) as e:
        node.index(noitem) == None
    assert "is not in list" in str(e.value)

def test_repr(nested_json):
    node = nested_json
    assert repr(node) == "<JsonNode object key:'root', children:3>"

def test_corruptjson():
    node = JsonNode('root')
    with pytest.raises(ValueError) as e:
        node.data_from_json('''
        {
            "item1": True,
            "item2": False
            "item3": "something"
        }
        ''')
    assert 'Corrupt Json string' in str(e.value)

def test_latest(nested_json):
    node = nested_json
    new_json_string = ('\n'
                      '    {\n'
                      '        "item1": 1,\n'
                      '        "item3": {\n'
                      '            "item1": 1\n'
                      '        }\n'
                      '    }')
    node.data_from_json(new_json_string)
    assert node["item1"].latest
    assert not node["item2"].latest
    assert node["item3"].latest
    assert node["item3"]["item1"].latest
    assert not node["item3"]["item2"].latest