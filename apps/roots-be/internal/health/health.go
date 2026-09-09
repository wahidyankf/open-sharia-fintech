// Package health serves the service's liveness endpoint.
package health

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Response is the health endpoint's body. The literal "healthy" is asserted by
// specs/apps/roots/be/behaviours/health/health.feature and by the OpenAPI
// contract's example, so the three must change together.
type Response struct {
	Status string `json:"status"`
}

// StatusHealthy is the only value Handler reports. The endpoint answers
// liveness -- whether the process is up and routing -- so there is no degraded
// state to express here; readiness of downstream dependencies would be a
// separate endpoint with its own contract.
const StatusHealthy = "healthy"

// Handler responds 200 with a JSON body of {"status":"healthy"}.
func Handler(c *gin.Context) {
	c.JSON(http.StatusOK, Response{Status: StatusHealthy})
}
