"""Example 56: json.loads."""

import json  # => imports the standard-library json module

# json.loads() parses a JSON string into Python objects (dict, list, str, int, ...).
data = json.loads('{"a": 1}')  # => parses a JSON str into a Python dict
print(data["a"])  # => Output: 1
