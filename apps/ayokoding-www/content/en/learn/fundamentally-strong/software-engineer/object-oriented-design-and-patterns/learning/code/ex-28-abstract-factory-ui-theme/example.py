"""Example 28: An Abstract Factory for UI Widget Families."""  # => module docstring

import abc  # => imports the abc module


class Button(abc.ABC):  # => the ABSTRACT product: every theme has SOME Button
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def paint(self) -> str:  # => no body -- a required contract for subclasses
        ...  # => the ellipsis stub -- concrete Buttons below fill this in


class Checkbox(abc.ABC):  # => the ABSTRACT product: every theme has SOME Checkbox
    @abc.abstractmethod  # => marks the next method as required for every subclass
    def paint(self) -> str:  # => no body -- a required contract for subclasses
        ...  # => the ellipsis stub -- concrete Checkboxes below fill this in


class DarkButton(Button):  # => a CONCRETE product belonging to the dark family
    def paint(self) -> str:  # => defines the paint() method
        return "dark-button"  # => tags this product with its family name


class DarkCheckbox(Checkbox):  # => a CONCRETE product belonging to the dark family
    def paint(self) -> str:  # => defines the paint() method
        return "dark-checkbox"  # => tags this product with its family name


class LightButton(Button):  # => a CONCRETE product belonging to the light family
    def paint(self) -> str:  # => defines the paint() method
        return "light-button"  # => tags this product with its family name


class LightCheckbox(Checkbox):  # => a CONCRETE product belonging to the light family
    def paint(self) -> str:  # => defines the paint() method
        return "light-checkbox"  # => tags this product with its family name


class WidgetFactory(abc.ABC):  # => the ABSTRACT FACTORY -- produces a MATCHED family
    @abc.abstractmethod  # => marks the next method as required for every WidgetFactory subclass
    def create_button(self) -> Button:  # => no body -- required for every factory
        ...  # => the ellipsis stub -- concrete factories below fill this in

    @abc.abstractmethod  # => marks the next method as required for every WidgetFactory subclass
    def create_checkbox(self) -> Checkbox:  # => no body -- required for every factory
        ...  # => the ellipsis stub -- concrete factories below fill this in


class DarkThemeFactory(WidgetFactory):  # => produces ONLY dark-family products
    def create_button(self) -> Button:  # => defines the create_button() method
        return DarkButton()  # => always matches the dark family, never mixed

    def create_checkbox(self) -> Checkbox:  # => defines the create_checkbox() method
        return DarkCheckbox()  # => always matches the dark family, never mixed


class LightThemeFactory(WidgetFactory):  # => produces ONLY light-family products
    def create_button(self) -> Button:  # => defines the create_button() method
        return LightButton()  # => always matches the light family, never mixed

    def create_checkbox(self) -> Checkbox:  # => defines the create_checkbox() method
        return LightCheckbox()  # => always matches the light family, never mixed


def build_toolbar(  # => signature spans multiple lines: parameter below, return type on the closing line
    factory: WidgetFactory,  # => the single parameter -- typed as the ABSTRACT WidgetFactory, never a concrete subclass
) -> tuple[str, str]:  # => the ONE function every caller uses, regardless of theme
    # => the client depends ONLY on WidgetFactory -- it never names a concrete class
    button: Button = factory.create_button()  # => whichever family the factory picks
    checkbox: Checkbox = factory.create_checkbox()  # => the SAME family, guaranteed
    return button.paint(), checkbox.paint()  # => returns this value to the caller


dark_ui: tuple[str, str] = build_toolbar(DarkThemeFactory())  # => swap the ONE argument
light_ui: tuple[str, str] = build_toolbar(LightThemeFactory())  # => whole family swaps
print(dark_ui)  # => both products come from the dark family together
# => Output: ('dark-button', 'dark-checkbox')
print(light_ui)  # => both products come from the light family together
# => Output: ('light-button', 'light-checkbox')
# => Swapping ONE factory argument swaps the ENTIRE matched product family at once
