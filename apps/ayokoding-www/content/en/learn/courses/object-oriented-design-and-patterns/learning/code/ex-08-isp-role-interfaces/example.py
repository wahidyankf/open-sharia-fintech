"""Example 8: Break a Fat Interface into Role Protocols."""

from typing import Protocol, runtime_checkable  # => runtime_checkable enables isinstance()


@runtime_checkable  # => allows isinstance() checks against this Protocol at runtime
class Printable(Protocol):  # => role: can print a document
    def print_doc(self) -> str:  # => the one method this role requires
        ...  # => Protocol methods have no body -- a structural contract only


@runtime_checkable  # => allows isinstance() checks against this Protocol at runtime
class Scannable(Protocol):  # => role: can scan a document
    def scan_doc(self) -> str:  # => the one method this role requires
        ...  # => Protocol methods have no body -- a structural contract only


@runtime_checkable  # => allows isinstance() checks against this Protocol at runtime
class Faxable(Protocol):  # => role: can fax a document
    def fax_doc(self) -> str:  # => the one method this role requires
        ...  # => Protocol methods have no body -- a structural contract only


class SimplePrinter:  # => genuinely satisfies ONLY Printable -- nothing else
    def print_doc(self) -> str:  # => satisfies Printable, nothing more
        return "printed"  # => a real, honest implementation


class AllInOnePrinter:  # => genuinely satisfies all three roles at once
    def print_doc(self) -> str:  # => satisfies Printable
        return "printed"  # => a real, honest implementation

    def scan_doc(self) -> str:  # => satisfies Scannable
        return "scanned"  # => a real, honest implementation

    def fax_doc(self) -> str:  # => satisfies Faxable
        return "faxed"  # => a real, honest implementation


printer: SimplePrinter = SimplePrinter()  # => a plain printer, one capability only
print(isinstance(printer, Printable))  # => structurally matches the Printable protocol
print(isinstance(printer, Scannable))  # => structurally does NOT match Scannable
# => Output: True
# => False
# => `SimplePrinter` depends on exactly one small role -- never a fat, all-in-one interface
