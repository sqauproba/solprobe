package ratelimit

import (
	"sync"
	"time"
)

// Limiter is a token-bucket rate limiter, safe for concurrent use.
type Limiter struct {
	mu      sync.Mutex
	tokens  float64
	rate    float64
	burst   float64
	lastRef time.Time
}

// New creates a limiter allowing `rate` tokens per second with a burst
// capacity of `burst`.
func New(rate float64, burst float64) *Limiter {
	return &Limiter{
		tokens:  burst,
		rate:    rate,
		burst:   burst,
		lastRef: time.Now(),
	}
}

// Allow consumes one token if available, otherwise returns false.
func (l *Limiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()
	now := time.Now()
	l.tokens += now.Sub(l.lastRef).Seconds() * l.rate
	if l.tokens > l.burst {
		l.tokens = l.burst
	}
	if l.tokens >= 1 {
		l.tokens--
		l.lastRef = now
		return true
	}
	l.lastRef = now
	return false
}

// Remaining reports how many tokens are available right now.
func (l *Limiter) Remaining() float64 {
	l.mu.Lock()
	defer l.mu.Unlock()
	now := time.Now()
	tokens := l.tokens + now.Sub(l.lastRef).Seconds()*l.rate
	if tokens > l.burst {
		tokens = l.burst
	}
	return tokens
}
