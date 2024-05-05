# Build stage
FROM rust:1.75-slim AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock* ./
COPY src ./src
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/solprobe-collector /usr/local/bin/solprobe-collector
EXPOSE 50051
ENTRYPOINT ["solprobe-collector"]
