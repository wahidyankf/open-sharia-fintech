#!/usr/bin/env bash
# Example 22: builds a throwaway 5-commit repo with ONE seeded regression at commit 4,
# then bisects it by hand. Run this script from an empty directory: bash setup_repo.sh
set -euo pipefail

git init -q
git config user.email "demo@example.com"
git config user.name "Demo Author"

cat >calc.py <<'PYEOF'
def add_tax(amount: float, rate: float) -> float:
    return round(amount * (1 + rate), 2)
PYEOF
git add calc.py
git commit -q -m "commit 1: add_tax computes amount * (1 + rate)"

cat >>calc.py <<'PYEOF'

def format_currency(amount: float) -> str:
    return f"${amount:.2f}"
PYEOF
git add calc.py
git commit -q -m "commit 2: add format_currency helper"

echo "# calc" >README.md
git add README.md
git commit -q -m "commit 3: add README (unrelated to calc logic)"

sed -i.bak 's/round(amount \* (1 + rate), 2)/round(amount * (1 - rate), 2)  # seeded regression: sign flipped/' calc.py
rm -f calc.py.bak
git add calc.py
git commit -q -m "commit 4: simplify add_tax rounding"

printf '\nAdds sales tax to a price.\n' >>README.md
git add README.md
git commit -q -m "commit 5: document calc in README"

cat >check.py <<'PYEOF'
import sys
sys.path.insert(0, ".")
from calc import add_tax
result = add_tax(100.0, 0.1)
assert result == 110.0, f"expected 110.0, got {result}"
print("PASS:", result)
PYEOF

echo "repo ready -- 5 commits, HEAD is commit 5, regression seeded at commit 4"
git log --oneline
