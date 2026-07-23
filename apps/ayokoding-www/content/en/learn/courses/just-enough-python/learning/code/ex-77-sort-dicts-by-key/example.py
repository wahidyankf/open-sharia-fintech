"""Example 77: Sort Dicts by Key."""

# sort()'s key= callable extracts the value to compare -- here, each dict's "age".
people: list[dict[str, int | str]] = [  # => a list of 3 dicts, each with name and age
    {"name": "Grace", "age": 36},  # => age 36 -- currently the middle entry
    {"name": "Ada", "age": 28},  # => age 28 -- currently the first entry
    {"name": "Alan", "age": 41},  # => age 41 -- currently the last entry
]  # => closes the people list literal
people.sort(key=lambda person: person["age"])  # => sorts IN PLACE by the "age" field
for person in people:  # => iterates the now-sorted list, youngest to oldest
    print(person["name"], person["age"])  # => Output: Ada 28, Grace 36, Alan 41
