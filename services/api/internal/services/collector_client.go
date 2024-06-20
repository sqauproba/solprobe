// Package services wraps interactions with downstream components.
package services

import (
	"context"
	"time"
)

// CollectorClient talks to the Rust collector over gRPC.
type CollectorClient struct {
	endpoint string
	timeout  time.Duration
}

func NewCollectorClient(endpoint string) *CollectorClient {
	return &CollectorClient{endpoint: endpoint, timeout: 5 * time.Second}
}

func (c *CollectorClient) Endpoint() string {
	return c.endpoint
}

// LatestSlot asks the collector for the most recent processed slot.
func (c *CollectorClient) LatestSlot(ctx context.Context) (int64, error) {
	// Real impl: gRPC call to the collector's health/latest service.
	select {
	case <-ctx.Done():
		return 0, ctx.Err()
	case <-time.After(c.timeout):
		return 305_100_123, nil
	}
}
