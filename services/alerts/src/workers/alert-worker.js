"use strict";

const { WebhookChannel } = require("../channels/webhook");

/**
 * Alert worker: pulls events from the API event stream and feeds them to the
 * rule engine on a polling interval. A production build would subscribe to
 * Redis pub/sub instead of polling; this keeps the scaffold dependency-free.
 */
class AlertWorker {
  constructor(engine, options = {}) {
    this.engine = engine;
    this.options = {
      pollIntervalMs: options.pollIntervalMs || 2000,
      sourceUrl: options.sourceUrl || "http://localhost:8080/v1/stream",
    };
    this.timer = null;
    this.running = false;
  }

  async start() {
    this.running = true;
    this.timer = setInterval(() => this.tick(), this.options.pollIntervalMs);
  }

  async tick() {
    try {
      const events = await this.fetchEvents();
      for (const event of events) {
        await this.engine.handle(event);
      }
    } catch (err) {
      console.error(`solprobe-alerts: tick error: ${err.message}`);
    }
  }

  async fetchEvents() {
    // Stub: returns a synthetic event batch so the worker is runnable
    // without a live backend.
    return [
      {
        rpc_latency_ms: 120,
        slot_lag: 5,
        failure_rate: 0.01,
        ts: Date.now(),
      },
    ];
  }

  async stop() {
    this.running = false;
    if (this.timer) clearInterval(this.timer);
    await this.engine.stop();
  }
}

module.exports = { AlertWorker };
