"""Example 73: ISP -- Protocol Decomposition.

co-04: a fat `Worker` service (print + scan + fax) forces every implementation to
stub methods it does not need. Decomposing it into fine-grained `Printer`,
`Scanner`, and `FaxMachine` protocols lets a minimal implementation (a
print-only device) satisfy only the protocol it actually needs, structurally --
no explicit inheritance, no unused-method stubs.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from typing import Protocol, runtime_checkable  # => runtime_checkable enables isinstance() checks below

# ============================================================
# BEFORE: one fat protocol -- every implementer forced to support all three
# ============================================================


# => BEFORE: a print-only device would be FORCED to stub scan_document() and send_fax() just to satisfy this
class FatWorker(Protocol):  # => the ISP violation: three unrelated responsibilities bundled into one contract
    def print_document(self, name: str) -> str: ...  # => any implementer must support this, even if print-only
    def scan_document(self, name: str) -> str: ...  # => forces a print-only device to stub this method too
    def send_fax(self, name: str) -> str: ...  # => forces a print-only device to stub this method as well


# ============================================================
# AFTER: three fine-grained protocols -- each implementer depends on only what it uses
# ============================================================


@runtime_checkable  # => enables isinstance(obj, Printer) structural checks, used in the demonstration below
class Printer(Protocol):  # => co-04: the narrow protocol for print-capable devices only
    def print_document(self, name: str) -> str: ...  # => the ONE method this narrow protocol requires


@runtime_checkable  # => enables isinstance(obj, Scanner) structural checks
class Scanner(Protocol):  # => a second, independent narrow protocol
    def scan_document(self, name: str) -> str: ...  # => the ONE method this narrow protocol requires


@runtime_checkable  # => enables isinstance(obj, FaxMachine) structural checks
class FaxMachine(Protocol):  # => a third, independent narrow protocol
    def send_fax(self, name: str) -> str: ...  # => the ONE method this narrow protocol requires


class BasicPrinter:  # => a MINIMAL implementation -- satisfies Printer only, no stub methods needed
    def print_document(self, name: str) -> str:  # => satisfies Printer structurally
        return f"printed: {name}"  # => a real, honest implementation


class MultiFunctionDevice:  # => satisfies all three protocols structurally -- no explicit inheritance declared
    def print_document(self, name: str) -> str:  # => satisfies Printer structurally
        return f"printed: {name}"  # => a real, honest implementation

    def scan_document(self, name: str) -> str:  # => satisfies Scanner structurally
        return f"scanned: {name}"  # => a real, honest implementation

    def send_fax(self, name: str) -> str:  # => satisfies FaxMachine structurally
        return f"faxed: {name}"  # => a real, honest implementation


def run_print_job(printer: Printer, name: str) -> str:  # => depends on the NARROW Printer protocol only
    return printer.print_document(name)  # => works for BasicPrinter or MultiFunctionDevice, unchanged either way


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    basic = BasicPrinter()  # => a print-only device, structurally
    print(run_print_job(basic, "invoice.pdf"))  # => a print-only device satisfies the narrow protocol
    # => Output: printed: invoice.pdf

    print(isinstance(basic, Printer))  # => structurally satisfies Printer
    # => Output: True
    print(isinstance(basic, Scanner))  # => correctly does NOT satisfy Scanner -- ISP kept the protocols apart
    # => Output: False

    mfd = MultiFunctionDevice()  # => a device satisfying all three narrow protocols at once, still with zero inheritance
    print(isinstance(mfd, Printer) and isinstance(mfd, Scanner) and isinstance(mfd, FaxMachine))  # => satisfies all three
    # => Output: True
