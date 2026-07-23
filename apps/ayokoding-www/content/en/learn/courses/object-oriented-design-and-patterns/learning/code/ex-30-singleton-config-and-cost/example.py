"""Example 30: A Config Singleton, and the Global-State Seam It Creates."""


class Config:  # => begins the Config class body
    _instance: "Config | None" = None  # => a CLASS attribute -- shared by every caller

    def __init__(self) -> None:  # => never call this directly -- use instance() instead
        self.debug: bool = False  # => the mutable state every caller ends up sharing

    @classmethod
    def instance(cls) -> "Config":  # => cls is Config itself, the shared holder
        if cls._instance is None:  # => only the FIRST call actually constructs one
            cls._instance = cls()  # => every later call reuses this same object
        return cls._instance  # => always the SAME object, never a fresh one

    @classmethod
    def reset(cls) -> None:  # => the escape hatch this pattern FORCES callers to add
        cls._instance = None  # => without this, no caller can ever start clean again


first: Config = Config.instance()  # => the first call constructs the shared instance
second: Config = Config.instance()  # => the second call reuses the SAME instance
print(first is second)  # => proves there is only ever one Config in the whole process
# => Output: True

first.debug = True  # => mutating through ONE reference...
print(second.debug)  # => ...is visible through EVERY OTHER reference -- global state
# => Output: True
# => `Config.instance()` always returns the SAME object, so a mutation anywhere leaks everywhere

Config.reset()  # => the ONLY way to get a clean Config again -- an explicit reset call
fresh: Config = Config.instance()  # => a genuinely NEW instance, post-reset
print(fresh.debug)  # => the leaked True from `first.debug = True` above is gone
# => Output: False
# => Every consumer of a singleton is implicitly coupled to every OTHER consumer through shared state
