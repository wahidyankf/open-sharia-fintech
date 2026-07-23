# learning/code/ex-61-end-to-end-injection-audit/scanner.py
"""Example 61: a real, hand-written AST scanner -- sweeps a .py file for concatenated-untrusted-input sinks (co-03, co-04, co-01)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the AST-walking logic itself

import ast  # => co-01: Python's OWN stdlib parser -- the SAME tree the interpreter itself would build
from dataclasses import (
    dataclass,
)  # => co-01: a real, typed finding record -- not a loose tuple


@dataclass  # => co-01: one real finding per detected sink
class Finding:  # => co-03: the shape every scanner hit takes -- line, sink kind, and a real one-line reason
    line: int  # => co-01: the REAL source line number this finding came from, taken straight from the AST node
    sink_type: str  # => co-03: which category of sink this is -- "sql", "command", or "template"
    reason: (
        str  # => co-04: a real, human-readable explanation of WHY this call was flagged
    )


def _is_built_from_input(
    node: ast.expr,
) -> bool:  # => co-01: real, structural check -- NOT a value/data-flow guess
    # => co-01: a JoinedStr is a real f-string node; a BinOp(Add) on strings is real concatenation --
    # => BOTH shapes mean "this string's content depends on something computed at runtime, not a fixed literal"
    if isinstance(
        node, ast.JoinedStr
    ):  # => co-03: e.g. f"... {term} ..." -- a REAL f-string AST node
        return True  # => co-03: an f-string is, by construction, never a fixed literal
    if isinstance(node, ast.BinOp) and isinstance(
        node.op, ast.Add
    ):  # => co-04: e.g. "a" + host -- REAL concatenation
        return True  # => co-04: string concatenation via + is the classic "built, not literal" shape
    return False  # => co-01: anything else (a plain Constant, a placeholder, ...) is NOT flagged by this check


class InjectionScanner(
    ast.NodeVisitor
):  # => co-01: a real ast.NodeVisitor -- walks the WHOLE real parsed tree
    def __init__(
        self,
    ) -> None:  # => co-01: constructor -- starts with an empty, real findings list
        self.findings: list[
            Finding
        ] = []  # => co-01: every REAL Finding this scan produces, in traversal order

    def visit_Call(
        self, node: ast.Call
    ) -> None:  # => co-01: fires for EVERY real function/method call in the file
        self._check_sql_sink(
            node
        )  # => co-03: does THIS call look like a SQL-injection sink
        self._check_command_sink(
            node
        )  # => co-04: does THIS call look like a command-injection sink
        self._check_template_sink(
            node
        )  # => co-06: does THIS call look like a template-injection sink
        self.generic_visit(
            node
        )  # => co-01: continues walking into this call's own arguments -- real recursive descent

    def _check_sql_sink(
        self, node: ast.Call
    ) -> None:  # => co-03: real check -- .execute()/.executescript() calls
        if not isinstance(
            node.func, ast.Attribute
        ):  # => co-03: only method calls have a real `.attr` shape
            return  # => co-03: not a method call at all -- cannot be conn.execute(...)
        if node.func.attr not in {
            "execute",
            "executescript",
        }:  # => co-03: the REAL sqlite3 sink method names
            return  # => co-03: some other method entirely -- not a SQL sink candidate
        if node.args and _is_built_from_input(
            node.args[0]
        ):  # => co-03: the FIRST real argument is the query text
            self.findings.append(  # => co-03: a REAL finding -- built, not bound, SQL text reached execute()
                Finding(
                    node.lineno,
                    "sql",
                    "query string built via f-string/concatenation, not bound parameters",
                )
            )

    def _check_command_sink(
        self, node: ast.Call
    ) -> None:  # => co-04: real check -- os.system() / subprocess shell=True
        func = (
            node.func
        )  # => co-04: the real callable expression this Call node invokes
        if (
            isinstance(func, ast.Attribute) and func.attr == "system"
        ):  # => co-04: matches os.system(...) by attr name
            if node.args and _is_built_from_input(
                node.args[0]
            ):  # => co-04: the command string itself, built or not
                self.findings.append(  # => co-04: a REAL finding -- os.system with a concatenated command string
                    Finding(
                        node.lineno,
                        "command",
                        "os.system() argument built via f-string/concatenation",
                    )
                )
        for keyword in (
            node.keywords
        ):  # => co-04: real subprocess.run/Popen calls signal danger via shell=True
            if (
                keyword.arg == "shell"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
            ):
                self.findings.append(  # => co-04: a REAL finding -- an explicit, real shell=True keyword argument
                    Finding(node.lineno, "command", "subprocess call passes shell=True")
                )

    def _check_template_sink(
        self, node: ast.Call
    ) -> None:  # => co-06: real check -- Template(...) from a non-literal
        func = (
            node.func
        )  # => co-06: the real callable expression this Call node invokes
        name = (
            func.id
            if isinstance(func, ast.Name)
            else (func.attr if isinstance(func, ast.Attribute) else None)
        )
        if (
            name != "Template"
        ):  # => co-06: only matches a REAL call literally named/attributed "Template"
            return  # => co-06: any other callable name -- not a template-construction candidate
        if not node.args:  # => co-06: Template() with no positional argument at all -- nothing to inspect
            return  # => co-06: real guard against an IndexError on the check below
        first_arg = node.args[
            0
        ]  # => co-06: the REAL argument this Template(...) call was constructed from
        if not isinstance(
            first_arg, ast.Constant
        ):  # => co-06: a plain string LITERAL is the only safe shape here
            self.findings.append(  # => co-06: a REAL finding -- Template() built from something other than a literal
                Finding(
                    node.lineno,
                    "template",
                    "Template() built from a non-literal (f-string/concat/variable)",
                )
            )


def scan_file(
    path: str,
) -> list[
    Finding
]:  # => co-01: parses a REAL file on disk and runs the REAL scanner over it
    with open(path) as f:  # => co-01: reads the real, on-disk source text
        source = f.read()  # => co-01: the exact real bytes/text this scan operates on
    tree = ast.parse(
        source, filename=path
    )  # => co-01: Python's OWN real parser -- the SAME grammar CPython itself uses
    scanner = (
        InjectionScanner()
    )  # => co-01: a fresh, real scanner instance for this one file
    scanner.visit(
        tree
    )  # => co-01: the REAL traversal -- every Call node in the file is actually visited
    return (
        scanner.findings
    )  # => co-01: every REAL finding this specific file produced, in source order
