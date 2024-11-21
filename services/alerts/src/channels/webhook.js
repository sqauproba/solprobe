"use strict";

/**
 * Generic webhook channel. Posts JSON to a configurable URL (env
 * `ALERTS_WEBHOOK_URL`). Posting is stubbed for the scaffold.
 */
class WebhookChannel {
  constructor(url) {
    this.url = url || process.env.ALERTS_WEBHOOK_URL || null;
    this.name = "webhook";
  }

  async send(text, event) {
    console.log(`[webhook] ${text}`);
    // Real impl:
    // if (this.url) await fetch(this.url, { method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ text, event }) });
  }
}

module.exports = { WebhookChannel };
