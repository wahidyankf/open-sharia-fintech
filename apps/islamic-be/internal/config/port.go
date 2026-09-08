// Package config resolves the service's startup configuration from injected
// inputs. Nothing here reads the process environment directly: the caller
// supplies a Lookup, which is what lets Unit proof cover every branch without
// touching a real OS boundary.
package config

import (
	"fmt"
	"strconv"
)

// DefaultPort is the listener port when neither the flag nor the prefixed
// variable supplies one.
const DefaultPort = 8402

// PortVariable is the only environment variable consulted for the port. A bare
// PORT is deliberately ignored: one exported variable must not be able to
// retarget every app in the monorepo at once.
const PortVariable = "ISLAMIC_BE_PORT"

// Lookup reports the value of an environment variable and whether it was set.
// It has the same shape as os.LookupEnv so main can pass that directly.
type Lookup func(key string) (string, bool)

// ResolvePort applies the resolution order flag -> ISLAMIC_BE_PORT -> default.
//
// A malformed value from either source is an error, never a fall back to the
// default: a typo'd port that silently starts the service on 8402 is harder to
// diagnose than a refusal to start. On error the returned port is 0, which is
// not a usable port, so a caller that ignores the error still cannot listen.
func ResolvePort(flagValue string, lookup Lookup) (int, error) {
	if flagValue != "" {
		return parsePort(flagValue, "--port")
	}

	if raw, ok := lookup(PortVariable); ok && raw != "" {
		return parsePort(raw, PortVariable)
	}

	return DefaultPort, nil
}

// parsePort converts raw to a usable TCP port, naming source in any error so
// the operator learns which input to correct.
func parsePort(raw string, source string) (int, error) {
	port, err := strconv.Atoi(raw)
	if err != nil {
		return 0, fmt.Errorf("%s must be a number, got %q", source, raw)
	}

	// 0 asks the kernel to choose a port, which defeats a fixed contract, and
	// anything above 65535 is not addressable.
	if port < 1 || port > 65535 {
		return 0, fmt.Errorf("%s must be between 1 and 65535, got %d", source, port)
	}

	return port, nil
}
