package handlers

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

type walletResponse struct {
	Address        string         `json:"address"`
	Lamports       int64          `json:"lamports"`
	SoulBalance    string         `json:"sol_balance"`
	RecentActivity []activityItem `json:"recent_activity"`
}

type activityItem struct {
	Signature string `json:"signature"`
	Slot      int64  `json:"slot"`
	Status    string `json:"status"`
}

// Wallet returns balance and recent activity for a wallet.
func (h *Handlers) Wallet(w http.ResponseWriter, r *http.Request) {
	address := chi.URLParam(r, "address")
	if address == "" {
		writeError(w, http.StatusBadRequest, "missing address")
		return
	}
	writeJSON(w, http.StatusOK, walletResponse{
		Address:     address,
		Lamports:    123_456_789_000,
		SoulBalance: "123.456789",
		RecentActivity: []activityItem{
			{Signature: "5aTx...", Slot: 305100100, Status: "success"},
			{Signature: "7bYz...", Slot: 305100050, Status: "success"},
		},
	})
}
