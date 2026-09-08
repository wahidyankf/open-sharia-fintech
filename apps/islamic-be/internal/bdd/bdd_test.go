package bdd

import (
	"os"
	"testing"

	"github.com/cucumber/godog"
	"github.com/cucumber/godog/colors"
)

// TestBehaviours runs the canonical corpus at the Unit layer. The paths point
// into specs/, which is the single source of truth -- the features are never
// copied into the app, so they cannot drift.
func TestBehaviours(t *testing.T) {
	suite := godog.TestSuite{
		ScenarioInitializer: InitializeScenario,
		Options: &godog.Options{
			Format: "pretty",
			Output: colors.Colored(os.Stdout),
			Paths: []string{
				"../../../../specs/apps/islamic/be/behaviours/health",
				"../../../../specs/apps/islamic/be/behaviours/config",
			},
			// Strict fails the run on pending or undefined steps. Without it an
			// unbound scenario reports as a skip and the suite still exits 0.
			Strict:      true,
			TestingT:    t,
			Concurrency: 1,
		},
	}

	if suite.Run() != 0 {
		t.Fatal("behaviour suite failed")
	}
}
