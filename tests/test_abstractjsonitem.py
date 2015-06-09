"""
    Copyright © 2015 by Stefan Lehmann

"""

import pytest

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

