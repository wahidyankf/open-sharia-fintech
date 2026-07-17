"""Example 28: Guarding a None-Returning Function."""


def find_user_age(
    users: dict[str, int], name: str
) -> int | None:  # => None means "not found"
    return users.get(
        name
    )  # => dict.get returns None on a missing key -- no exception raised


directory = {"ana": 30, "budi": 25}  # => the lookup table this example queries

found_age = find_user_age(directory, "ana")  # => a hit -- found_age is 30
if found_age is not None:  # => the guard: caller MUST check before trusting the value
    print(f"ana is {found_age}")  # => Output: ana is 30
else:  # => the miss branch -- never taken for this particular lookup
    print("ana not found")  # => unreachable here -- ana IS in the directory

missing_age = find_user_age(directory, "citra")  # => a miss -- missing_age is None
if (
    missing_age is not None
):  # => same guard pattern, this time it takes the OTHER branch
    print(
        f"citra is {missing_age}"
    )  # => unreachable here -- citra is NOT in the directory
else:  # => the miss branch -- taken this time, since citra is not in directory
    print("citra not found")  # => Output: citra not found
