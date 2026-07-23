"""Example 6: Refactor an Ostrich That Cannot Fly."""


class Bird:  # => the base every bird shares: attributes true of ALL birds
    def __init__(self, name: str) -> None:  # => the constructor
        self.name = name  # => every bird, flying or not, has a name


class FlyingBird(Bird):  # => a SEPARATE capability, not assumed by every Bird
    def fly(self) -> str:  # => only birds that can genuinely fly define this
        return f"{self.name} flies"  # => a real, honest implementation


class Sparrow(FlyingBird):  # => inherits the flying CAPABILITY honestly
    pass  # => no override needed -- FlyingBird.fly() already fits a sparrow


class Ostrich(Bird):  # => inherits ONLY the base Bird -- no fly() exists here at all
    def run(self) -> str:  # => Ostrich gets its OWN capability instead
        return f"{self.name} runs"  # => a real, honest implementation for THIS bird


def make_flock_fly(flock: list[FlyingBird]) -> list[str]:  # => a client typed against FlyingBird only
    return [bird.fly() for bird in flock]  # => every element is GUARANTEED to have fly() -- Ostrich cannot even appear here


flock: list[FlyingBird] = [Sparrow("Jay"), Sparrow("Wren")]  # => only flying birds allowed
results: list[str] = make_flock_fly(flock)  # => calls fly() on every element, safely
print(results)  # => confirms every call succeeded with no exception anywhere
# => Output: ['Jay flies', 'Wren flies']

ostrich: Ostrich = Ostrich("Big Bird")  # => a real, non-flying bird
print(ostrich.run())  # => Ostrich has its own honest method instead of a broken fly()
# => Output: Big Bird runs
# => `Ostrich` was never asked to lie about flying -- it simply never inherits `fly()` in the first place
