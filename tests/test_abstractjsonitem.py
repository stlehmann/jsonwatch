"""
    Copyright © 2015 by Stefan Lehmann

"""

import pytest
from jsonwatch.jsonitem import JsonItem

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


def test_path(nested_json):
    root = nested_json
    assert root['item3']['item2'].path == ['root', 'item3', 'item2']
    assert root.path == ['root']
    assert root['item2'].path == ['root', 'item2']

def test_key(nested_json):
    root = nested_json
    item = root["item2"]
    item.key = "item4"
    with pytest.raises(KeyError):
        root["item2"]
    assert root["item4"] == item