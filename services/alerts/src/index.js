"use strict";

const { RuleEngine } = require("./rules/engine");
const { loadRules } = require("./rules/loader");
const { DiscordChannel } = require("./channels/discord");
const { TelegramChannel } = require("./channels/telegram");
const { WebhookChannel } = require("./channels/webhook");
const { AlertWorker } = require("./workers/alert-worker");

/**
 * Bootstrap the alerts service: load rules, build channels from the
 * environment, start the worker, and wire graceful shutdown.
 */
async function main() {
  const rulesDir = process.env.ALERTS_RULES_DIR || "./rules";
  const rules = loadRules(rulesDir);
  console.log(`solprobe-alerts: loaded ${rules.length} rule(s) from ${rulesDir}`);

  const channels = [];

  if (process.env.DISCORD_WEBHOOK_URL) {
    channels.push(new DiscordChannel(process.env.DISCORD_WEBHOOK_URL));
    console.log("solprobe-alerts: discord channel enabled");
  }
  if (process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_CHAT_ID) {
    channels.push(
      new TelegramChannel(
        process.env.TELEGRAM_BOT_TOKEN,
        process.env.TELEGRAM_CHAT_ID
      )
    );
    console.log("solprobe-alerts: telegram channel enabled");
  }
  channels.push(new WebhookChannel());

  const engine = new RuleEngine(rules, channels);
  const worker = new AlertWorker(engine, {
    pollIntervalMs: Number(process.env.ALERTS_POLL_INTERVAL_MS || 2000),
    sourceUrl: process.env.ALERTS_SOURCE_URL || "http://localhost:8080/v1/stream",
  });

  await worker.start();
  console.log(`solprobe-alerts: worker running (poll ${worker.options.pollIntervalMs}ms)`);

  const shutdown = async (signal) => {
    console.log(`solprobe-alerts: received ${signal}, shutting down`);
    await worker.stop();
    process.exit(0);
  };
  process.on("SIGINT", () => shutdown("SIGINT"));
  process.on("SIGTERM", () => shutdown("SIGTERM"));
}

main().catch((err) => {
  console.error("solprobe-alerts: fatal error", err);
  process.exit(1);
});
