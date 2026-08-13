#!/usr/bin/env bash

set -euo pipefail

if ! jq -e '.implicitDependencies | index("beavernest-app")' apps/beavernest-be/project.json >/dev/null; then
	echo "beavernest-be must declare its combined-image dependency on beavernest-app" >&2
	exit 1
fi

beavernest_affected_projects=$(npm exec -- nx show projects --affected --base=origin/main --head=HEAD)

if ! grep -Fxq "beavernest-app" <<<"$beavernest_affected_projects"; then
	echo "expected the Flutter workspace to be affected by the current delivery branch" >&2
	exit 1
fi

if ! grep -Fxq "beavernest-be" <<<"$beavernest_affected_projects"; then
	echo "expected the combined runtime to be affected by its frontend dependency" >&2
	exit 1
fi
