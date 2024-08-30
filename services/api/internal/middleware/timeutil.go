package middleware

import "time"

func timeNow() time.Time { return time.Now() }

func timeSince(t time.Time) time.Duration { return time.Since(t) }
