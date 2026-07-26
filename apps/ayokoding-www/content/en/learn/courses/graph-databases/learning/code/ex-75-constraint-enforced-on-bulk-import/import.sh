#!/usr/bin/env bash
# Example 75: Constraint Enforcement During Bulk Import. (co-22, co-20)
set -euo pipefail

# nodes_person.csv deliberately contains TWO rows with the SAME name ("Ada", "Ada") -- a
# duplicate that a person_name uniqueness constraint (Example 20's pattern) rejects.
# neo4j-admin import checks node-id uniqueness structurally as part of the tool's own
# contract -- a genuinely duplicate NAME value additionally violates any constraint created
# on that property once the imported database starts up and enforces it going forward.
neo4j-admin database import full \
	--nodes=Person=nodes_person.csv \
	neo4j
echo "import finished -- constraint enforcement, if any, applies once the database next starts"
