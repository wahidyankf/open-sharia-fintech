// Package bdd binds the roots-be behaviour corpus at the Unit layer.
//
// Every step drives the router in process through net/http/httptest. Nothing
// here binds a socket, reads the real environment, or starts a subprocess:
// those are E2E concerns, and the corpus marks the scenarios that need them.
package bdd

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"

	"github.com/cucumber/godog"

	"github.com/wahidyankf/ose-public/apps/roots-be/internal/config"
	"github.com/wahidyankf/ose-public/apps/roots-be/internal/router"
)

// state carries one scenario's inputs and outputs. It is rebuilt per scenario so
// no value leaks between them.
type state struct {
	handler http.Handler
	env     map[string]string
	portArg string

	response    *httptest.ResponseRecorder
	resolved    int
	resolveErr  error
	resolveDone bool
}

func (s *state) lookup(key string) (string, bool) {
	v, ok := s.env[key]
	return v, ok
}

// --- health steps -----------------------------------------------------------

func (s *state) theServiceIsRunning() error {
	s.handler = router.New()
	return nil
}

func (s *state) iSendGET(path string) error {
	if s.handler == nil {
		return fmt.Errorf("no service is running; the Given step must run first")
	}
	s.response = httptest.NewRecorder()
	s.handler.ServeHTTP(s.response, httptest.NewRequest(http.MethodGet, path, nil))
	return nil
}

func (s *state) theResponseStatusIs(expected int) error {
	if s.response == nil {
		return fmt.Errorf("no response was captured")
	}
	if s.response.Code != expected {
		return fmt.Errorf("expected status %d, got %d", expected, s.response.Code)
	}
	return nil
}

func (s *state) theResponseBodyHasFieldEqualTo(field, expected string) error {
	if s.response == nil {
		return fmt.Errorf("no response was captured")
	}
	var body map[string]any
	if err := json.Unmarshal(s.response.Body.Bytes(), &body); err != nil {
		return fmt.Errorf("expected a JSON body, got %q", s.response.Body.String())
	}
	actual, ok := body[field]
	if !ok {
		return fmt.Errorf("expected a %q field, got %v", field, body)
	}
	if actual != expected {
		return fmt.Errorf("expected %q to equal %q, got %v", field, expected, actual)
	}
	return nil
}

func (s *state) theResponseHeaderStartsWith(header, prefix string) error {
	if s.response == nil {
		return fmt.Errorf("no response was captured")
	}
	actual := s.response.Header().Get(header)
	if !strings.HasPrefix(actual, prefix) {
		return fmt.Errorf("expected %q to start with %q, got %q", header, prefix, actual)
	}
	return nil
}

// --- port-resolution steps --------------------------------------------------

func (s *state) noVariableIsSet(name string) error {
	delete(s.env, name)
	return nil
}

func (s *state) variableIsSetTo(name, value string) error {
	s.env[name] = value
	return nil
}

func (s *state) noPortFlagIsSupplied() error {
	s.portArg = ""
	return nil
}

func (s *state) thePortFlagIsSuppliedWith(value string) error {
	s.portArg = value
	return nil
}

func (s *state) theServiceResolvesItsListenerPort() error {
	s.resolved, s.resolveErr = config.ResolvePort(s.portArg, s.lookup, "ROOTS_BE_PORT")
	s.resolveDone = true
	return nil
}

func (s *state) theResolvedPortIs(expected int) error {
	if !s.resolveDone {
		return fmt.Errorf("port resolution has not run")
	}
	if s.resolveErr != nil {
		return fmt.Errorf("expected port %d, got error %v", expected, s.resolveErr)
	}
	if s.resolved != expected {
		return fmt.Errorf("expected port %d, got %d", expected, s.resolved)
	}
	return nil
}

func (s *state) startupFailsWithAMessageNaming(name string) error {
	if !s.resolveDone {
		return fmt.Errorf("port resolution has not run")
	}
	if s.resolveErr == nil {
		return fmt.Errorf("expected startup to fail, got port %d", s.resolved)
	}
	if !strings.Contains(s.resolveErr.Error(), name) {
		return fmt.Errorf("expected the message to name %s, got %q", name, s.resolveErr.Error())
	}
	return nil
}

func (s *state) theServiceDoesNotFallBackToTheDefault() error {
	if s.resolved == config.DefaultPort {
		return fmt.Errorf("expected no fallback, but the resolved port was the default %d", config.DefaultPort)
	}
	return nil
}

// InitializeScenario registers every binding the corpus needs.
//
// The keyword-specific Given/When/Then registrations are used rather than the
// keyword-agnostic Step, so a step written under the wrong keyword fails as
// undefined instead of silently matching.
func InitializeScenario(sc *godog.ScenarioContext) {
	s := &state{env: map[string]string{}}

	sc.Before(func(ctx context.Context, _ *godog.Scenario) (context.Context, error) {
		*s = state{env: map[string]string{}}
		return ctx, nil
	})

	sc.Given(`^the roots-be service is running$`, s.theServiceIsRunning)
	sc.Given(`^no ([A-Z_]+) variable is set$`, s.noVariableIsSet)
	sc.Given(`^([A-Z_]+) is set to "([^"]*)"$`, s.variableIsSetTo)
	sc.Given(`^no --port flag is supplied$`, s.noPortFlagIsSupplied)
	sc.Given(`^the --port flag is supplied with "([^"]*)"$`, s.thePortFlagIsSuppliedWith)

	sc.When(`^I send GET (\S+)$`, s.iSendGET)
	sc.When(`^the service resolves its listener port$`, s.theServiceResolvesItsListenerPort)

	sc.Then(`^the response status is (\d+)$`, s.theResponseStatusIs)
	sc.Then(`^the response body has a "([^"]*)" field equal to "([^"]*)"$`, s.theResponseBodyHasFieldEqualTo)
	sc.Then(`^the response "([^"]*)" header starts with "([^"]*)"$`, s.theResponseHeaderStartsWith)
	sc.Then(`^the resolved port is (\d+)$`, s.theResolvedPortIs)
	sc.Then(`^startup fails with a message naming ([A-Z_]+)$`, s.startupFailsWithAMessageNaming)
	sc.Then(`^the service does not fall back to the default$`, s.theServiceDoesNotFallBackToTheDefault)
}
