//! SolProbe collector — high-throughput Solana event ingestion.
//!
//! The collector maintains persistent RPC/WebSocket connections to a Solana
//! node, manages a registry of subscriptions (slots, accounts, programs,
//! logs), normalizes incoming events into typed messages, emits metrics, and
//! exposes health/readiness information. Downstream integration (gRPC publish)
//! is wired through the `publisher` module.

pub mod decoders;
pub mod health;
pub mod metrics;
pub mod publisher;
pub mod rpc;
pub mod subscriptions;
pub mod websocket;

use std::time::Duration;

use anyhow::Result;

use crate::rpc::RpcConfig;
use crate::subscriptions::SubscriptionRegistry;
use crate::websocket::{Channel, SocketClient};

/// Run the collector with configuration loaded from the environment.
pub async fn run() -> Result<()> {
    init_tracing();

    let config = RpcConfig::from_env()?;
    tracing::info!(
        endpoint = %config.http_endpoint,
        ws = %config.ws_endpoint,
        "starting solprobe-collector"
    );

    let registry = SubscriptionRegistry::new();
    let metrics = metrics::Metrics::new();

    // Open the WebSocket connection and subscribe to live feeds.
    let mut socket = SocketClient::connect(config.ws_endpoint.clone()).await?;
    tracing::info!("websocket connected; establishing subscriptions");

    let mut channels = vec![
        Channel::Slot,
        Channel::Logs("11111111111111111111111111111111".to_string()),
    ];
    if !config.watch_addresses.is_empty() {
        for addr in &config.watch_addresses {
            channels.push(Channel::Account(addr.clone()));
            registry.add(format!("account:{addr}")).await;
        }
    }
    if !config.watch_programs.is_empty() {
        for id in &config.watch_programs {
            channels.push(Channel::Program(id.clone()));
            registry.add(format!("program:{id}")).await;
        }
    }

    for ch in channels {
        socket.subscribe(ch).await?;
    }

    // Main event loop: read notifications, decode, record metrics.
    tracing::info!(
        active_subscriptions = registry.count().await,
        "collector running; press ctrl-c to stop"
    );

    let mut reconnects: u64 = 0;
    loop {
        match socket.next().await {
            Ok(notification) => {
                if let Some(event) = decoders::parse_notification(&notification) {
                    metrics.record_event();
                    publisher::publish(event).await?;
                }
            }
            Err(e) => {
                reconnects += 1;
                metrics.record_reconnect();
                tracing::warn!(error = %e, reconnect = reconnects, "socket dropped; reconnecting");
                let backoff = config.reconnect_max_seconds.min(1u64 << reconnects.min(10));
                tokio::time::sleep(Duration::from_secs(backoff)).await;
                socket = SocketClient::connect(config.ws_endpoint.clone()).await?;
                for ch in &channels {
                    let _ = socket.subscribe(ch.clone()).await;
                }
            }
        }
    }
}

fn init_tracing() {
    let filter = tracing_subscriber::EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| "info".into());
    let _ = tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_target(false)
        .try_init();
}
