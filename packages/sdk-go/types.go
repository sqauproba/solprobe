package sdk

type HealthResponse struct {
	Status   string            `json:"status"`
	Score    int               `json:"score"`
	Services map[string]string `json:"services"`
}
