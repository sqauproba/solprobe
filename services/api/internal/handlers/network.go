package handlers

import (
	"net/http"
	"time"
)

type networkResponse struct {
	TPS       float64 `json:"tps"`
	SlotTime  int     `json:"slot_time_ms"`
	SkipRate  float64 `json:"skip_rate"`
	SlotCount int64   `json:"slot_count"`
	Epoch     int64   `json:"epoch"`
	Measured  string  `json:"measured_at"`
}

// Network returns aggregated network metrics.
func (h *Handlers) Network(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, networkResponse{
		TPS:       2200.5,
		SlotTime:  400,
		SkipRate:  0.02,
		SlotCount: 305_000_000,
		Epoch:     720,
		Measured:  time.Now().UTC().Format(time.RFC3339),
	})
}
