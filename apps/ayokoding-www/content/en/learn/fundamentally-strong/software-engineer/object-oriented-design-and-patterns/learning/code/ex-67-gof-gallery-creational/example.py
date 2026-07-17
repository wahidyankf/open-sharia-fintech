"""Example 67: GoF Gallery -- Creational Patterns.

co-32 (gof-pattern-gallery): a single-file tour of the four essential creational
patterns -- factory method (co-16), abstract factory (co-17), builder (co-18), and
singleton (co-19) -- each constructs correctly, verified independently.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from dataclasses import dataclass, field  # => field() supplies mutable defaults safely, used by HttpRequest

# ============================================================
# 1. Factory Method -- defer instantiation to a creation method
# ============================================================


class Shape:  # => the shared abstract product every factory-method output implements
    def area(self) -> float:  # => no body -- every concrete Shape must override this
        raise NotImplementedError  # => a plain-class stand-in for @abstractmethod, still enforces the contract


class Circle(Shape):  # => one concrete product
    def __init__(self, radius: float) -> None:  # => the constructor
        self.radius = radius  # => stores radius on this instance

    def area(self) -> float:  # => satisfies Shape's contract
        return 3.14159 * self.radius**2  # => pi * r^2


def shape_factory(kind: str, size: float) -> Shape:  # => the FACTORY METHOD -- caller never names Circle directly
    if kind == "circle":  # => the ONLY place that knows which concrete class to build
        return Circle(size)  # => constructs the concrete product internally, hidden from the caller
    raise ValueError(f"unknown shape kind: {kind}")  # => an honest failure for any kind this factory cannot build


# ============================================================
# 2. Abstract Factory -- a family of factory methods producing a matched set
# ============================================================


@dataclass  # => generates __init__ from the field below
class Button:  # => one member of the "widget family"
    theme: str  # => the family tag, part of the generated __init__


@dataclass  # => generates __init__ from the field below
class Checkbox:  # => the other member of the "widget family" -- must match Button's theme
    theme: str  # => the family tag, part of the generated __init__


class WidgetFactory:  # => the abstract factory interface
    def create_button(self) -> Button:  # => no body -- every concrete factory must override this
        raise NotImplementedError  # => a plain-class stand-in for @abstractmethod

    def create_checkbox(self) -> Checkbox:  # => no body -- every concrete factory must override this
        raise NotImplementedError  # => a plain-class stand-in for @abstractmethod


class DarkWidgetFactory(WidgetFactory):  # => one concrete factory -- produces a MATCHED dark-themed family
    def create_button(self) -> Button:  # => overrides the abstract factory method
        return Button(theme="dark")  # => always builds the dark-family Button, never mixed with other themes

    def create_checkbox(self) -> Checkbox:  # => overrides the abstract factory method
        return Checkbox(theme="dark")  # => always builds the dark-family Checkbox, matching create_button()


# ============================================================
# 3. Builder -- assemble a complex object step by step
# ============================================================


@dataclass  # => generates __init__ from the fields below
class HttpRequest:  # => the complex object being assembled
    url: str  # => the one required field
    headers: dict[str, str] = field(default_factory=dict)  # => field() avoids a shared mutable default dict
    body: str | None = None  # => optional, defaults to no body


class RequestBuilder:  # => the fluent builder -- no telescoping constructor needed
    def __init__(self, url: str) -> None:  # => the constructor takes only the one required part
        self._url = url  # => the one required part
        self._headers: dict[str, str] = {}  # => optional parts, added incrementally
        self._body: str | None = None  # => optional, starts unset until with_body() is called

    def with_header(self, key: str, value: str) -> "RequestBuilder":  # => returns self -- enables chaining
        self._headers[key] = value  # => accumulates one header per call, in-place
        return self  # => returning self is what makes .with_header(...).with_body(...) chainable

    def with_body(self, body: str) -> "RequestBuilder":  # => also returns self
        self._body = body  # => sets the optional body, overwriting any previous value
        return self  # => same chaining trick as with_header()

    def build(self) -> HttpRequest:  # => assembles the final immutable-in-spirit object
        return HttpRequest(url=self._url, headers=self._headers, body=self._body)  # => one call, fully assembled


# ============================================================
# 4. Singleton -- exactly one shared instance
# ============================================================


class AppConfig:  # => a minimal singleton, deliberately small for this gallery tour (see Example 30 for the cost)
    _instance: "AppConfig | None" = None  # => the one shared instance, or None before first use

    def __new__(cls) -> "AppConfig":  # => overridden so every AppConfig() returns the SAME object
        if cls._instance is None:  # => first call: create the one instance
            cls._instance = super().__new__(cls)  # => allocate it exactly once
        return cls._instance  # => every subsequent call returns the SAME object


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    circle = shape_factory("circle", 2.0)  # => 1. factory method
    print(round(circle.area(), 2))  # => constructs a Circle without the caller importing Circle
    # => Output: 12.57

    dark_factory: WidgetFactory = DarkWidgetFactory()  # => 2. abstract factory
    print(dark_factory.create_button().theme, dark_factory.create_checkbox().theme)  # => both match the same theme
    # => Output: dark dark

    # => 3. builder -- four chained calls assemble one HttpRequest, no telescoping constructor needed
    request = RequestBuilder("https://api.example.com").with_header("Accept", "json").with_body("{}").build()
    print(request.url, request.headers, request.body)  # => 3. builder, assembled without a telescoping constructor
    # => Output: https://api.example.com {'Accept': 'json'} {}

    print(AppConfig() is AppConfig())  # => 4. singleton -- exactly one shared instance
    # => Output: True
