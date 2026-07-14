"""Example 58: json.load from a File."""

import json  # => imports the standard-library json module

# json.load() reads and parses JSON directly from an open file object.
with open("config.json", "w") as f:  # => opens config.json for writing
    json.dump({"theme": "dark"}, f)  # => writes a one-key config file

with open("config.json") as f:  # => reopens config.json for reading
    config = json.load(f)  # => reads it back into a plain dict

print(config["theme"])  # => Output: dark
