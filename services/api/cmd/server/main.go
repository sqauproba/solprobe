// SolProbe API gateway — REST and WebSocket relay over collector data.
package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"go.uber.org/zap"

	"github.com/solprobe/solprobe/services/api/internal/handlers"
	"github.com/solprobe/solprobe/services/api/internal/middleware"
	"github.com/solprobe/solprobe/services/api/internal/ratelimit"
)

func main() {
	logger, err := zap.NewProduction()
	if err != nil {
		log.Fatalf("init logger: %v", err)
	}
	defer logger.Sync()

	host := getenv("API_HOST", "0.0.0.0")
	port := getenv("API_PORT", "8080")
	jwtSecret := getenv("JWT_SECRET", "dev-secret")
	ratePerMinute := getint("API_RATE_LIMIT_PER_MINUTE", 120)

	// Per-client rate limiter (token bucket).
	limiter := ratelimit.New(float64(ratePerMinute)/60.0, float64(ratePerMinute))

	h := handlers.New(logger, handlers.Deps{
		JWTSecret:   jwtSecret,
		RateLimiter: limiter,
	})

	r := chi.NewRouter()
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(30 * time.Second))
	r.Use(middleware.Compress(5))

	// Public routes.
	r.Route("/v1", func(r chi.Router) {
		r.Get("/health", h.Health)
		r.Get("/network", h.Network)
		r.Get("/slots/latest", h.LatestSlot)
		r.Get("/rpc/benchmark", h.Benchmark)
		r.Get("/wallets/{address}", h.Wallet)
		r.Get("/programs/{id}", h.Program)
		r.Get("/programs/{id}/logs", h.ProgramLogs)
		r.Get("/transactions/{signature}", h.Transaction)
	})

	// Authenticated routes (API key / JWT).
	r.Route("/v1/secure", func(r chi.Router) {
		r.Use(middleware.RequireAuth(jwtSecret))
		r.Use(middleware.RequireRateLimit(limiter))
		r.Post("/alerts", h.CreateAlert)
		r.Get("/alerts", h.ListAlerts)
	})

	// WebSocket relay for live events.
	r.HandleFunc("/v1/stream", h.Stream)

	srv := &http.Server{
		Addr:         host + ":" + port,
		Handler:      r,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	go func() {
		logger.Info("solprobe-api listening", zap.String("addr", srv.Addr))
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatal("server error", zap.Error(err))
		}
	}()

	// Graceful shutdown on SIGINT/SIGTERM.
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop
	logger.Info("shutting down")

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		logger.Error("shutdown error", zap.Error(err))
	}
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func getint(key string, fallback int) int {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return fallback
}
