package handlers

import (
	"encoding/json"
	"net/http"
	"sync"
)

// AlertRule is a declarative alerting rule.
type AlertRule struct {
	Name    string `json:"name"`
	Metric  string `json:"metric"`
	Op      string `json:"operator"`
	Value   float64 `json:"value"`
	Channel string `json:"channel"`
}

type alertStore struct {
	mu    sync.RWMutex
	rules map[string]AlertRule
}

func newAlertStore() *alertStore {
	return &alertStore{rules: make(map[string]AlertRule)}
}

var alerts = newAlertStore()

// CreateAlert registers a new alert rule.
func (h *Handlers) CreateAlert(w http.ResponseWriter, r *http.Request) {
	var rule AlertRule
	if err := json.NewDecoder(r.Body).Decode(&rule); err != nil {
		writeError(w, http.StatusBadRequest, "invalid body: "+err.Error())
		return
	}
	if rule.Name == "" || rule.Metric == "" {
		writeError(w, http.StatusBadRequest, "name and metric are required")
		return
	}
	alerts.mu.Lock()
	alerts.rules[rule.Name] = rule
	alerts.mu.Unlock()
	writeJSON(w, http.StatusCreated, rule)
}

// ListAlerts returns all registered alert rules.
func (h *Handlers) ListAlerts(w http.ResponseWriter, r *http.Request) {
	alerts.mu.RLock()
	defer alerts.mu.RUnlock()
	out := make([]AlertRule, 0, len(alerts.rules))
	for _, rule := range alerts.rules {
		out = append(out, rule)
	}
	writeJSON(w, http.StatusOK, out)
}
