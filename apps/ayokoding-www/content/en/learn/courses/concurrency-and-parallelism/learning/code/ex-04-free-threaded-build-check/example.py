"""Example 4: Detecting a Free-Threaded (No-GIL) Build."""

import sys  # => sys carries the runtime introspection hooks this example uses
import sysconfig  # => sysconfig exposes the BUILD-time flag, independent of runtime state


def gil_is_enabled() -> bool:  # => wraps the version-gated check so callers don't repeat it
    if hasattr(sys, "_is_gil_enabled"):  # => `sys._is_gil_enabled` only exists on Python 3.13+
        return sys._is_gil_enabled()  # pyright: ignore[reportPrivateUsage]
        # => leading underscore is CPython's naming, not a privacy signal -- this IS the documented
        # => runtime check (co-04); True on a normal build, False on a running 3.14t build
    return True  # => pre-3.13: no free-threaded option existed, so the GIL was always enabled


def built_free_threaded() -> bool:  # => was THIS interpreter binary compiled with PEP 703 support?
    flag = sysconfig.get_config_var("Py_GIL_DISABLED")  # => 1 if compiled --disable-gil, else 0/None
    return bool(flag)  # => True only for a `python3.14t`-style build, regardless of runtime state


if __name__ == "__main__":  # => module entry point
    runtime_gil_enabled = gil_is_enabled()  # => runtime_gil_enabled: is the GIL ON right now?
    compiled_free_threaded = built_free_threaded()  # => compiled_free_threaded: was this a `t` build?
    print(f"runtime_gil_enabled={runtime_gil_enabled}")  # => Output: runtime_gil_enabled=True
    print(f"compiled_free_threaded={compiled_free_threaded}")  # => Output: compiled_free_threaded=False

    # => On STANDARD CPython 3.13/3.14 (what this file was verified against), both print exactly
    # => this: the GIL is enabled and this binary was not built free-threaded. A reader who
    # => installs `python3.14t` (PEP 703/779; "[experimental]" checkbox in the macOS installer,
    # => even though free-threading is officially "supported"/Phase II as of 3.14) would instead
    # => see runtime_gil_enabled=False and compiled_free_threaded=True on this exact script.
    assert runtime_gil_enabled is True  # => confirms the GIL is serializing bytecode on THIS build
    assert compiled_free_threaded is False  # => confirms this is a normal (non-`t`) CPython build
    print("ex-04 OK")  # => Output: ex-04 OK
