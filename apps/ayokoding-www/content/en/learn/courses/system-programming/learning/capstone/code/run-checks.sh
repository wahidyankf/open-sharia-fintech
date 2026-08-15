#!/usr/bin/env sh
set -eu

compiler=${CC:-cc}
flags="-std=c11 -Wall -Wextra -Werror -g"

$compiler $flags -fsanitize=address,undefined system_component.c -o system_component_asan
if [ "$(uname -s)" = "Linux" ]; then
	ASAN_OPTIONS=detect_leaks=1
	export ASAN_OPTIONS
fi
./system_component_asan

if command -v valgrind >/dev/null 2>&1; then
	$compiler $flags system_component.c -o system_component_valgrind
	valgrind --leak-check=full --show-leak-kinds=all --errors-for-leak-kinds=definite --error-exitcode=1 \
		./system_component_valgrind
else
	printf '%s\n' "Valgrind not installed; ASan/UBSan completed. Run Valgrind on Linux to complete the second check."
fi
