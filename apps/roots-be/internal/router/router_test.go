package router_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	generatedcontracts "github.com/wahidyankf/ose-public/apps/roots-be/generated-contracts"
	"github.com/wahidyankf/ose-public/apps/roots-be/internal/router"
)

// Scenario: Health endpoint returns 200
func TestHealthEndpointReturns200(t *testing.T) {
	rec := httptest.NewRecorder()
	router.New().ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/api/v1/health", nil))

	if rec.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d", rec.Code)
	}

	var body map[string]any
	if err := json.Unmarshal(rec.Body.Bytes(), &body); err != nil {
		t.Fatalf("expected a JSON body, got %q", rec.Body.String())
	}
	if body["status"] != "healthy" {
		t.Errorf(`expected status "healthy", got %v`, body["status"])
	}
}

// Scenario: Health endpoint reports the JSON content type
func TestHealthEndpointReportsJSONContentType(t *testing.T) {
	rec := httptest.NewRecorder()
	router.New().ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/api/v1/health", nil))

	if got := rec.Header().Get("Content-Type"); !strings.HasPrefix(got, "application/json") {
		t.Errorf(`expected Content-Type to start with "application/json", got %q`, got)
	}
}

// Scenario: An unknown route is rejected
func TestUnknownRouteIsRejected(t *testing.T) {
	rec := httptest.NewRecorder()
	router.New().ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/api/v1/does-not-exist", nil))

	if rec.Code != http.StatusNotFound {
		t.Errorf("expected 404, got %d", rec.Code)
	}
}

// The router must satisfy the contract-generated interface, so a contract change
// that adds an operation breaks the build rather than silently 404ing at runtime.
func TestServerSatisfiesGeneratedInterface(t *testing.T) {
	var _ generatedcontracts.ServerInterface = router.Server{}
}
