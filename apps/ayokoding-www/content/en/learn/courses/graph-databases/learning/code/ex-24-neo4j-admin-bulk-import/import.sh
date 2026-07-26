#!/usr/bin/env bash
# Example 24: Offline Bulk Import with neo4j-admin. (co-20)
set -euo pipefail # => fail fast on any error, unset variable, or failed pipe stage

# neo4j-admin import ONLY runs against a stopped, empty database -- this is the offline path,
# distinct from LOAD CSV's online, transactional row-at-a-time write (Example 23).
neo4j-admin database import full \
	--nodes=Person=nodes_person.csv \
	--relationships=KNOWS=rels_knows.csv \
	neo4j
# => "neo4j" here names the target database, not a node label
echo "import finished"
