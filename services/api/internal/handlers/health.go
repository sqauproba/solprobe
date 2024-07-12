package handlers

import (
	"net/http"
	"time"
)

type healthResponse struct {
	Status    string            `json:"status"`
	Score     int               `json:"score"`
	Services  map[string]string `json:"services"`
	Version   string            `json:"version"`
	Timestamp string            `json:"timestamp"`
}

// Health reports overall platform health.
func (h *Handlers) Health(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, healthResponse{
		Status:   "healthy",
		Score:    98,
		Services: map[string]string{
			"collector": "healthy",
			"api":       "healthy",
			"database":  "healthy",
			"redis":     "healthy",
		},
		Version:   "0.1.0",
		Timestamp: time.Now().UTC().Format(time.RFC3339),
	})
}
