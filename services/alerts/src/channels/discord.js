"use strict";

/**
 * Discord notification channel using a webhook URL.
 * Posting is stubbed; swap the body with a `fetch`/`axios` call to the
 * Discord webhook endpoint in a real deployment.
 */
class DiscordChannel {
  constructor(webhookUrl) {
    this.webhookUrl = webhookUrl;
    this.name = "discord";
  }

  async send(text, event) {
    console.log(`[discord] ${text}`);
    // Real impl:
    // await fetch(this.webhookUrl, {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ content: text }),
    // });
  }
}

module.exports = { DiscordChannel };
