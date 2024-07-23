package handlers

import (
	"net/http"

	"github.com/go-chi/chi/v5"
)

type programResponse struct {
	ProgramID string `json:"program_id"`
	Owner     string `json:"owner"`
	Size      int64  `json:"size_bytes"`
	Executable bool  `json:"executable"`
}

// Program returns metadata for an on-chain program.
func (h *Handlers) Program(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	if id == "" {
		writeError(w, http.StatusBadRequest, "missing program id")
		return
	}
	writeJSON(w, http.StatusOK, programResponse{
		ProgramID:  id,
		Owner:      "BPFLoaderUpgradeab1e11111111111111111111111",
		Size:       284_160,
		Executable: true,
	})
}

// ProgramLogs returns recent logs emitted by a program.
func (h *Handlers) ProgramLogs(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")
	if id == "" {
		writeError(w, http.StatusBadRequest, "missing program id")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{
		"program_id": id,
		"logs": []string{
			"Program invoke [1]",
			"Program log: Instruction: Transfer",
			"Program consumed: 3,500 of 200,000 compute units",
			"Program success",
		},
	})
}
