"""Example 57: pytest verification for the SRP Cohesion Metric."""

from example import cohesion_ratio


def test_mixed_class_has_a_low_cohesion_ratio() -> None:
    before_split: dict[str, set[str]] = {
        "update_profile": {"name", "bio"},
        "get_display_name": {"name"},
        "send_welcome_email": {"email", "smtp_host"},
        "send_password_reset": {"email", "smtp_host"},
    }
    ratio: float = cohesion_ratio(before_split)
    assert round(ratio, 2) == 0.33  # => only 2 of 6 possible pairs share a field


def test_split_classes_have_a_higher_cohesion_ratio() -> None:
    profile_methods: dict[str, set[str]] = {
        "update_profile": {"name", "bio"},
        "get_display_name": {"name"},
    }
    email_methods: dict[str, set[str]] = {
        "send_welcome_email": {"email", "smtp_host"},
        "send_password_reset": {"email", "smtp_host"},
    }
    profile_ratio: float = cohesion_ratio(profile_methods)
    email_ratio: float = cohesion_ratio(email_methods)
    assert profile_ratio == 1.0  # => strictly better than the mixed class's 0.33
    assert email_ratio == 1.0  # => strictly better than the mixed class's 0.33


def test_single_method_class_is_trivially_cohesive() -> None:
    assert cohesion_ratio({"only_method": {"field"}}) == 1.0  # => no pairs to disagree


# => Run: pytest -- Output: 3 passed
