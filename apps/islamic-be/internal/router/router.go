// Package router wires the HTTP surface. It builds an engine in memory and
// never binds a socket, which is what lets the Unit layer exercise every route
// through httptest rather than over a real network boundary.
package router

import (
	"github.com/gin-gonic/gin"

	generatedcontracts "github.com/wahidyankf/ose-public/apps/islamic-be/generated-contracts"
	"github.com/wahidyankf/ose-public/apps/islamic-be/internal/health"
)

// Server implements the contract-generated ServerInterface. Declaring it here
// rather than registering handlers ad hoc means a new operation in the OpenAPI
// document fails compilation until it is implemented, instead of returning 404
// at runtime.
type Server struct{}

// GetHealth serves GET /api/v1/health.
func (Server) GetHealth(c *gin.Context) {
	health.Handler(c)
}

// New builds the engine with every contract route registered.
//
// gin.New is used rather than gin.Default: Default installs the Logger and
// Recovery middleware, and Logger writes request lines to stdout, which would
// make Unit output depend on an OS stream. Recovery is added back explicitly
// because a panicking handler should return 500, not kill the process.
func New() *gin.Engine {
	gin.SetMode(gin.ReleaseMode)

	engine := gin.New()
	engine.Use(gin.Recovery())

	generatedcontracts.RegisterHandlers(engine, Server{})

	return engine
}
