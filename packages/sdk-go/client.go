// Package sdk provides a Go client for the SolProbe API.
package sdk

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type Client struct {
	base   string
	apiKey string
	http   *http.Client
}

func New(base string, opts ...Option) *Client {
	c := &Client{base: base, http: &http.Client{Timeout: 30 * time.Second}}
	for _, o := range opts {
		o(c)
	}
	return c
}

type Option func(*Client)

func WithAPIKey(key string) Option {
	return func(c *Client) { c.apiKey = key }
}

func (c *Client) get(path string, out any) error {
	req, err := http.NewRequest(http.MethodGet, c.base+path, nil)
	if err != nil {
		return err
	}
	if c.apiKey != "" {
		req.Header.Set("Authorization", "Bearer "+c.apiKey)
	}
	resp, err := c.http.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("solprobe api error: %s", resp.Status)
	}
	return json.NewDecoder(resp.Body).Decode(out)
}

func (c *Client) Health() (HealthResponse, error) {
	var out HealthResponse
	err := c.get("/v1/health", &out)
	return out, err
}
