package handlers

import (
	"encoding/json"
	"net/http"

	"go.uber.org/zap"

	"github.com/solprobe/solprobe/services/api/internal/ratelimit"
)

// Deps carries shared dependencies into the handlers.
type Deps struct {
	JWTSecret   string
	RateLimiter *ratelimit.Limiter
}

// Handlers bundles the HTTP handlers for the API gateway.
type Handlers struct {
	logger *zap.Logger
	deps   Deps
}

func New(logger *zap.Logger, deps Deps) *Handlers {
	return &Handlers{logger: logger, deps: deps}
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"error": msg})
}
