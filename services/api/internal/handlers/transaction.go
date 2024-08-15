package handlers

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

type txResponse struct {
	Signature string   `json:"signature"`
	Status    string   `json:"status"`
	Slot      int64    `json:"slot"`
	FeeLamports int64  `json:"fee_lamports"`
	Logs      []string `json:"logs"`
}

// Transaction returns diagnostic details for a transaction.
func (h *Handlers) Transaction(w http.ResponseWriter, r *http.Request) {
	sig := chi.URLParam(r, "signature")
	if sig == "" {
		writeError(w, http.StatusBadRequest, "missing signature")
		return
	}
	writeJSON(w, http.StatusOK, txResponse{
		Signature:   sig,
		Status:      "success",
		Slot:        305_100_123,
		FeeLamports: 5_000,
		Logs: []string{
			"Program invoke [1]",
			"Program log: Instruction: Transfer",
			"Program success",
		},
	})
}
