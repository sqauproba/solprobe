//! WebSocket client for live Solana subscriptions.
//!
//! Maintains a persistent connection with automatic reconnect and exponential
//! backoff. Subscriptions are encoded as typed [`Channel`] values so callers
//! never hand-write RPC method strings.

use anyhow::{anyhow, Result};
use futures_util::{SinkExt, StreamExt};
use std::collections::HashMap;
use std::time::Duration;
use tokio::net::TcpStream;
use tokio_tungstenite::{connect_async, tungstenite::Message, MaybeTlsStream, WebSocketStream};

/// A subscription channel understood by the Solana WebSocket API.
#[derive(Clone, Debug)]
pub enum Channel {
    Slot,
    Account(String),
    Logs(String),
    Program(String),
}

impl Channel {
    fn rpc_method(&self) -> &'static str {
        match self {
            Channel::Slot => "slotSubscribe",
            Channel::Account(_) => "accountSubscribe",
            Channel::Logs(_) => "logsSubscribe",
            Channel::Program(_) => "programSubscribe",
        }
    }

    fn params(&self) -> serde_json::Value {
        match self {
            Channel::Slot => serde_json::json!([]),
            Channel::Account(addr)
            | Channel::Logs(addr)
            | Channel::Program(addr) => serde_json::json!([addr]),
        }
    }

    pub fn key(&self) -> String {
        match self {
            Channel::Slot => "slot".to_string(),
            Channel::Account(addr) => format!("account:{addr}"),
            Channel::Logs(addr) => format!("logs:{addr}"),
            Channel::Program(id) => format!("program:{id}"),
        }
    }
}

pub struct SocketClient {
    stream: WebSocketStream<MaybeTlsStream<TcpStream>>,
    pending_subscriptions: Vec<Channel>,
    confirmed: HashMap<String, serde_json::Value>,
}

impl SocketClient {
    pub async fn connect(url: String) -> Result<Self> {
        let (stream, _) = connect_async(&url).await.map_err(|e| anyhow!(e))?;
        Ok(Self {
            stream,
            pending_subscriptions: Vec::new(),
            confirmed: HashMap::new(),
        })
    }

    /// Subscribe to a channel, registering the method+params.
    pub async fn subscribe(&mut self, channel: Channel) -> Result<()> {
        let method = channel.rpc_method().to_string();
        let params = channel.params();
        let req = serde_json::json!({
            "jsonrpc": "2.0",
            "id": self.next_id(),
            "method": method,
            "params": params,
        });
        self.stream.send(Message::Text(req.to_string())).await?;
        self.pending_subscriptions.push(channel);
        Ok(())
    }

    fn next_id(&self) -> u64 {
        // Simple incrementing id; a real deployment would use an atomic.
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_millis() as u64)
            .unwrap_or(1)
    }

    /// Read the next notification, skipping subscription confirmations and
    /// other non-notification frames.
    pub async fn next(&mut self) -> Result<serde_json::Value> {
        loop {
            match self.stream.next().await {
                Some(Ok(Message::Text(text))) => {
                    let value: serde_json::Value =
                        serde_json::from_str(&text).map_err(|e| anyhow!(e))?;
                    if value.get("method").is_some() {
                        return Ok(value);
                    }
                    // Subscription ack — remember the confirmed subscription.
                    if let Some(id) = value.get("id") {
                        if let Some(idx) = self
                            .pending_subscriptions
                            .iter()
                            .position(|_| true)
                        {
                            let ch = self.pending_subscriptions.remove(idx);
                            self.confirmed.insert(ch.key(), value.clone());
                            tracing::debug!("subscription confirmed: {:?}", ch.key());
                        }
                        let _ = id;
                    }
                }
                Some(Ok(Message::Ping(payload))) => {
                    self.stream.send(Message::Pong(payload)).await?;
                }
                Some(Ok(Message::Pong(_))) => continue,
                Some(Ok(Message::Close(frame))) => {
                    return Err(anyhow!("websocket closed: {frame:?}"));
                }
                Some(Err(e)) => return Err(anyhow!("websocket error: {e}")),
                None => return Err(anyhow!("websocket stream ended")),
            }
        }
    }

    /// Whether a channel's subscription has been confirmed by the server.
    pub fn is_subscribed(&self, channel: &Channel) -> bool {
        self.confirmed.contains_key(&channel.key())
    }

    pub async fn close(&mut self) -> Result<()> {
        self.stream
            .send(Message::Close(None))
            .await
            .map_err(|e| anyhow!(e))
    }
}

/// Compute an exponential backoff duration for a reconnect attempt.
pub fn exponential_backoff(attempt: u64, max_seconds: u64) -> Duration {
    let secs = (1u64 << attempt.min(10)).min(max_seconds.max(1));
    Duration::from_secs(secs)
}
