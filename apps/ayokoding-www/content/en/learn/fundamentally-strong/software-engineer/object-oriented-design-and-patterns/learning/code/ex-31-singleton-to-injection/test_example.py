"""Example 31: pytest verification for Replacing a Singleton with an Injected Dependency."""

from example import Config, ReportGenerator


def test_debug_mode_report_is_isolated_from_prod_mode_report() -> None:
    # => no Config.reset() call anywhere -- there is no global state left to reset
    prod: ReportGenerator = ReportGenerator(Config(debug=False))
    debug: ReportGenerator = ReportGenerator(Config(debug=True))
    assert prod.summary() == "report (release)"  # => unaffected by the debug instance
    assert debug.summary() == "report (debug)"  # => unaffected by the prod instance


def test_two_instances_never_share_underlying_state() -> None:
    a: Config = Config(debug=False)
    b: Config = Config(debug=False)
    a.debug = True  # => mutate ONLY a's config
    assert b.debug is False  # => b is a genuinely separate object -- no leak at all


# => Run: pytest -- Output: 2 passed
