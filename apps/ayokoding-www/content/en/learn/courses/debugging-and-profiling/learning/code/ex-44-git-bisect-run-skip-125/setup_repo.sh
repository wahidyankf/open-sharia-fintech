#!/usr/bin/env bash
# Example 44: an 8-commit repo where commit 5 is UNBUILDABLE (a syntax error) and commit 7 seeds
# the real regression, with a valid test point (commit 6) between them -- check.sh exits 125 on
# the unbuildable commit so `git bisect run` skips it automatically instead of stalling. Run:
# bash setup_repo.sh
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

printf '\nA tiny tax and formatting helper.\n' >>README.md
git add README.md
git commit -q -m "commit 4: expand README description (still unrelated)"

cat >>calc.py <<'PYEOF'
def broken_syntax(:
PYEOF
git add calc.py
git commit -q -m "commit 5: UNBUILDABLE -- a stray syntax error slipped in"

sed -i.bak '/def broken_syntax/d' calc.py
rm -f calc.py.bak
git add calc.py
git commit -q -m "commit 6: fix the syntax error (no regression yet)"

sed -i.bak 's/round(amount \* (1 + rate), 2)/round(amount * (1 - rate), 2)  # seeded regression: sign flipped/' calc.py
rm -f calc.py.bak
git add calc.py
git commit -q -m "commit 7: simplify add_tax rounding (seeded regression)"

printf '\nAdds sales tax to a price.\n' >>README.md
git add README.md
git commit -q -m "commit 8: document calc in README"

cat >check.sh <<'SHEOF'
#!/usr/bin/env bash
python3 -c "import calc" 2>/dev/null || exit 125  # co-10: can't even import -- SKIP this commit
python3 -c "
import sys
sys.path.insert(0, '.')
from calc import add_tax
result = add_tax(100.0, 0.1)
sys.exit(0 if result == 110.0 else 1)
"
SHEOF
chmod +x check.sh

echo "repo ready -- 8 commits, commit 5 unbuildable, real regression at commit 7"
git log --oneline
