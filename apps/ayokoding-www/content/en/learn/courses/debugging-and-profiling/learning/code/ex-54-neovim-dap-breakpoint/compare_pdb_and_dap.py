"""Example 54: compare CLI pdb's stop location/values against the Neovim DAP
session's captured JSON (ex54-dap-result.json), to verify they agree exactly.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the comparison itself

import json  # => co-06: the DAP session's captured scope variables are read back from a plain JSON file
import sys  # => co-06: only used for sys.argv below -- the DAP result path is passed on the command line

# co-01/co-06: these are the REAL values captured from each tool's own run
# (see the "pdb transcript" and "nvim-dap headless run" Output blocks) -- pulled
# in here as plain constants so this script can assert on them directly.
PDB_STOPPED_LINE = 11  # => co-01: the real line number `break 11` stopped at in the pdb transcript above
PDB_LOCALS = {
    "cost": "34.3",
    "weight_kg": "12.0",
    "distance_km": "430.0",
}  # => co-01: pdb's own `p` output, as strings


def main() -> (
    None
):  # => co-06: reads the DAP JSON and asserts it matches pdb's own captured session exactly
    dap_result_path = (
        sys.argv[1] if len(sys.argv) > 1 else "dap_result.json"
    )  # => co-06: defaults for a bare local run
    with open(
        dap_result_path
    ) as f:  # => co-06: the file run_nvim_dap_headless.lua wrote at session end
        dap_result = json.load(
            f
        )  # => co-06: parses the REAL scopes/variables response the DAP session captured

    print(
        f"pdb stopped at line {PDB_STOPPED_LINE}; DAP stopped at line {dap_result['stopped_line']}"
    )  # => co-01/co-06
    assert dap_result["stopped_line"] == PDB_STOPPED_LINE, (
        "pdb and DAP stopped at different lines"
    )  # => co-01/co-06

    for (
        name,
        pdb_value,
    ) in PDB_LOCALS.items():  # => co-06: checks EVERY local pdb printed, not just one
        dap_value = dap_result["locals"][
            name
        ]  # => co-06: the SAME variable name, read from the DAP scope instead
        print(
            f"  {name}: pdb={pdb_value!r} dap={dap_value!r}"
        )  # => co-06: prints both sides for a visible diff
        assert dap_value == pdb_value, (
            f"{name} disagrees between pdb ({pdb_value}) and DAP ({dap_value})"
        )  # => co-06

    print(
        "confirmed: the Neovim DAP session stopped at the SAME line with the SAME values as CLI pdb"
    )  # => co-01/co-06


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that performs the full pdb-vs-DAP comparison
