# Build stage
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod go.sum* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /solprobe-api ./cmd/server

# Runtime stage
FROM scratch
COPY --from=builder /solprobe-api /solprobe-api
EXPOSE 8080
ENTRYPOINT ["/solprobe-api"]
