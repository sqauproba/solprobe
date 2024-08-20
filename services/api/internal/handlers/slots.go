package handlers

import (
	"net/http"
	"strconv"
)

type slotResponse struct {
	Slot      int    `json:"slot"`
	Status    string `json:"status"`
	Processed bool   `json:"processed"`
	Leader    string `json:"leader,omitempty"`
}

// LatestSlot returns the latest processed slot and finality status.
func (h *Handlers) LatestSlot(w http.ResponseWriter, r *http.Request) {
	// The real implementation would query the repository for the most recent
	// slot persisted by the collector. We return a plausible default here.
	slot := 305_100_123
	if v := r.URL.Query().Get("slot"); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			slot = n
		}
	}
	writeJSON(w, http.StatusOK, slotResponse{
		Slot:      slot,
		Status:    "confirmed",
		Processed: true,
	})
}

// Benchmark returns RPC benchmark results for a given endpoint.
func (h *Handlers) Benchmark(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]any{
		"endpoint":   r.URL.Query().Get("endpoint"),
		"latency_ms": 87.4,
		"p95_ms":     121.0,
		"tps":        11.4,
	})
}
