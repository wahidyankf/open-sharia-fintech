"""Example 31: Replacing a Singleton with an Injected Dependency."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => a PLAIN, ordinary object now -- no shared instance() anywhere
class Config:  # => begins the Config class body
    debug: bool = False  # => a normal field with a normal default


class ReportGenerator:  # => begins the ReportGenerator class body
    def __init__(self, config: Config) -> None:  # => the config is INJECTED, never looked up globally
        self.config = config  # => held as an ordinary instance field

    def summary(self) -> str:  # => defines the summary() method
        mode: str = "debug" if self.config.debug else "release"  # => reads ONLY its own injected config
        return f"report ({mode})"  # => returns this value to the caller


prod_config: Config = Config(debug=False)  # => one INDEPENDENT Config instance
debug_config: Config = Config(debug=True)  # => a SECOND, unrelated Config instance

prod_report: ReportGenerator = ReportGenerator(prod_config)  # => wired to prod_config
debug_report: ReportGenerator = ReportGenerator(debug_config)  # => wired to debug_config
print(prod_report.summary())  # => reads ONLY prod_config -- unaffected by debug_config
# => Output: report (release)
print(debug_report.summary())  # => reads ONLY debug_config -- unaffected by prod_config
# => Output: report (debug)
# => Two ReportGenerators, each holding its OWN Config, never share state -- no reset() needed anywhere
