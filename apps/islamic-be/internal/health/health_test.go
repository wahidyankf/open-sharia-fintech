package health_test

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/wahidyankf/ose-public/apps/islamic-be/internal/health"
)

func TestHandlerReturns200WithHealthyStatus(t *testing.T) {
	gin.SetMode(gin.TestMode)
	rec := httptest.NewRecorder()
	ctx, _ := gin.CreateTestContext(rec)
	ctx.Request = httptest.NewRequest(http.MethodGet, "/api/v1/health", nil)

	health.Handler(ctx)

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

func TestHandlerReportsJSONContentType(t *testing.T) {
	gin.SetMode(gin.TestMode)
	rec := httptest.NewRecorder()
	ctx, _ := gin.CreateTestContext(rec)
	ctx.Request = httptest.NewRequest(http.MethodGet, "/api/v1/health", nil)

	health.Handler(ctx)

	if got := rec.Header().Get("Content-Type"); len(got) < 16 || got[:16] != "application/json" {
		t.Errorf(`expected Content-Type to start with "application/json", got %q`, got)
	}
}
