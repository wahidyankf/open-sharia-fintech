"""Example 57: Measuring Cohesion Before and After an SRP Split."""  # => module docstring

import itertools  # => imports itertools


def cohesion_ratio(methods_to_fields: dict[str, set[str]]) -> float:  # => parameter maps each method name to the fields it reads or writes
    # => a simplified LCOM-style metric: of every PAIR of methods, what fraction
    # => share at least one field? Higher means the methods genuinely belong together.
    methods: list[str] = list(methods_to_fields.keys())  # => every method name being measured
    pairs: list[tuple[str, str]] = list(itertools.combinations(methods, 2))  # => every UNORDERED pair of methods, once each
    if not pairs:  # => 0 or 1 methods -- nothing to compare, trivially cohesive
        return 1.0  # => returns this value to the caller
    sharing_pairs: int = sum(  # => builds a running total across every method pair computed above
        1  # => the per-pair contribution: one when the condition below holds, else skipped
        for a, b in pairs  # => iterates every unordered pair from the combinations computed above
        if methods_to_fields[a] & methods_to_fields[b]  # => True when the field sets overlap
    )  # => counts pairs that share at least one field
    return sharing_pairs / len(pairs)  # => returns this value to the caller


# => BEFORE: one God-ish class mixing profile concerns with email-sending concerns
before_split: dict[str, set[str]] = {  # => maps each method name to the fields it touches, BEFORE the SRP split
    "update_profile": {"name", "bio"},  # => touches profile fields only
    "get_display_name": {"name"},  # => touches profile fields only
    "send_welcome_email": {"email", "smtp_host"},  # => touches email-sending fields only
    "send_password_reset": {"email", "smtp_host"},  # => touches email-sending fields only
}
before_ratio: float = cohesion_ratio(before_split)  # => most pairs share NOTHING
print(round(before_ratio, 2))  # => only the two profile methods, and the two email methods, agree
# => Output: 0.33

# => AFTER: split into two smaller, individually MORE cohesive classes
profile_methods: dict[str, set[str]] = {  # => the profile-only methods, isolated into their own mapping
    "update_profile": {"name", "bio"},  # => the SAME two methods, isolated together
    "get_display_name": {"name"},  # => the SAME two methods, isolated together
}
email_methods: dict[str, set[str]] = {  # => the email-only methods, isolated into their own mapping
    "send_welcome_email": {"email", "smtp_host"},  # => the SAME two methods, isolated together
    "send_password_reset": {"email", "smtp_host"},  # => the SAME two methods, isolated together
}
profile_ratio: float = cohesion_ratio(profile_methods)  # => every remaining pair shares a field
email_ratio: float = cohesion_ratio(email_methods)  # => every remaining pair shares a field
print(round(profile_ratio, 2), round(email_ratio, 2))  # => both split classes are fully cohesive
# => Output: 1.0 1.0
# => Splitting the mixed class raised the methods-share-fields ratio from 0.33 to 1.0 in BOTH halves
