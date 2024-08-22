package handlers

import (
	"net/http"
	"strconv"
	"time"
)

// Stream is a WebSocket relay for live slot events. The scaffold responds
// with a lightweight SSE-style stream until the collector gRPC feed is wired.
func (h *Handlers) Stream(w http.ResponseWriter, r *http.Request) {
	flusher, ok := w.(http.Flusher)
	if !ok {
		writeError(w, http.StatusInternalServerError, "streaming unsupported")
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")

	ctx := r.Context()
	slot := int64(305_100_123)
	for {
		select {
		case <-ctx.Done():
			return
		case <-time.After(2 * time.Second):
			slot++
			data := "event: slot\ndata: {\"slot\": " +
				strconv.FormatInt(slot, 10) + "}\n\n"
			if _, err := w.Write([]byte(data)); err != nil {
				return
			}
			flusher.Flush()
		}
	}
}
