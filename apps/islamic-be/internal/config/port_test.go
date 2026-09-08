package config_test

import (
	"strings"
	"testing"

	"github.com/wahidyankf/ose-public/apps/islamic-be/internal/config"
)

// envOf builds a Lookup over a fixed map. Unit proof must not read the real
// process environment, so every case injects its own.
func envOf(pairs map[string]string) config.Lookup {
	return func(key string) (string, bool) {
		v, ok := pairs[key]
		return v, ok
	}
}

// Scenario: The default port applies when nothing is set
func TestDefaultPortAppliesWhenNothingIsSet(t *testing.T) {
	got, err := config.ResolvePort("", envOf(map[string]string{}), "ISLAMIC_BE_PORT")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if got != 8402 {
		t.Errorf("expected 8402, got %d", got)
	}
}

// Scenario: The prefixed variable overrides the default
func TestPrefixedVariableOverridesTheDefault(t *testing.T) {
	got, err := config.ResolvePort("", envOf(map[string]string{"ISLAMIC_BE_PORT": "9402"}), "ISLAMIC_BE_PORT")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if got != 9402 {
		t.Errorf("expected 9402, got %d", got)
	}
}

// Scenario: The flag overrides the prefixed variable
func TestFlagOverridesThePrefixedVariable(t *testing.T) {
	got, err := config.ResolvePort("9500", envOf(map[string]string{"ISLAMIC_BE_PORT": "9402"}), "ISLAMIC_BE_PORT")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if got != 9500 {
		t.Errorf("expected 9500, got %d", got)
	}
}

// Scenario: A malformed port fails at startup
func TestMalformedPortFailsAtStartup(t *testing.T) {
	got, err := config.ResolvePort("", envOf(map[string]string{"ISLAMIC_BE_PORT": "not-a-port"}), "ISLAMIC_BE_PORT")
	if err == nil {
		t.Fatalf("expected an error, got port %d", got)
	}
	if !strings.Contains(err.Error(), "ISLAMIC_BE_PORT") {
		t.Errorf("expected the message to name ISLAMIC_BE_PORT, got %q", err.Error())
	}
	// "And the service does not fall back to the default" -- the zero value must
	// not be the default, or a caller ignoring err would silently listen on 8402.
	if got == 8402 {
		t.Errorf("expected no fallback to the default, got %d", got)
	}
}

// Scenario: A bare PORT variable is ignored
func TestBarePortVariableIsIgnored(t *testing.T) {
	got, err := config.ResolvePort("", envOf(map[string]string{"PORT": "9999"}), "ISLAMIC_BE_PORT")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if got != 8402 {
		t.Errorf("expected the bare PORT to be ignored and 8402 used, got %d", got)
	}
}

// A malformed flag must fail too. The corpus does not cover it -- flags are a
// developer-facing surface, not a user journey -- but silently defaulting on a
// typo'd --port would be the same defect the env case forbids.
func TestMalformedFlagFailsAtStartup(t *testing.T) {
	_, err := config.ResolvePort("not-a-port", envOf(map[string]string{}), "ISLAMIC_BE_PORT")
	if err == nil {
		t.Fatal("expected an error for a malformed --port flag")
	}
	if !strings.Contains(err.Error(), "--port") {
		t.Errorf("expected the message to name --port, got %q", err.Error())
	}
}

// Out-of-range values are not ports. 0 is reserved and >65535 is unrepresentable.
func TestOutOfRangePortsAreRejected(t *testing.T) {
	for _, raw := range []string{"0", "65536", "-1"} {
		if _, err := config.ResolvePort("", envOf(map[string]string{"ISLAMIC_BE_PORT": raw}), "ISLAMIC_BE_PORT"); err == nil {
			t.Errorf("expected %q to be rejected", raw)
		}
	}
}
