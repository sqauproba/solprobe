//! RPC configuration and JSON-RPC client helpers.

use anyhow::Result;
use std::env;
use std::time::Duration;

use serde::Deserialize;

/// Collector configuration, resolved from the environment.
#[derive(Clone, Debug)]
pub struct RpcConfig {
    pub http_endpoint: String,
    pub ws_endpoint: String,
    pub max_subscriptions: usize,
    pub reconnect_max_seconds: u64,
    pub watch_addresses: Vec<String>,
    pub watch_programs: Vec<String>,
}

impl RpcConfig {
    pub fn from_env() -> Result<Self> {
        let watch_addresses = env::var("WATCH_ADDRESSES")
            .unwrap_or_default()
            .split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect();

        let watch_programs = env::var("WATCH_PROGRAM_IDS")
            .unwrap_or_default()
            .split(',')
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect();

        Ok(Self {
            http_endpoint: env::var("SOLANA_RPC_ENDPOINT")
                .unwrap_or_else(|_| "https://api.mainnet-beta.solana.com".into()),
            ws_endpoint: env::var("SOLANA_WS_ENDPOINT")
                .unwrap_or_else(|_| "wss://api.mainnet-beta.solana.com/".into()),
            max_subscriptions: env::var("COLLECTOR_MAX_SUBSCRIPTIONS")
                .ok()
                .and_then(|v| v.parse().ok())
                .unwrap_or(500),
            reconnect_max_seconds: env::var("COLLECTOR_RECONNECT_MAX_SECONDS")
                .ok()
                .and_then(|v| v.parse().ok())
                .unwrap_or(60),
            watch_addresses,
            watch_programs,
        })
    }
}

/// A minimal JSON-RPC response envelope for decoding typed results.
#[derive(Debug, Deserialize)]
pub struct RpcResponse<T> {
    pub jsonrpc: String,
    pub result: T,
}

impl RpcConfig {
    /// Number of seconds of backoff for a given reconnect attempt.
    pub fn backoff_for(&self, attempt: u64) -> Duration {
        let secs = (1u64 << attempt.min(10)).min(self.reconnect_max_seconds);
        Duration::from_secs(secs)
    }
}
