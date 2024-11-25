"use strict";

/**
 * Telegram notification channel using a bot token + chat id.
 * Posting is stubbed; a real deployment calls the Bot API sendMessage.
 */
class TelegramChannel {
  constructor(botToken, chatId) {
    this.botToken = botToken;
    this.chatId = chatId;
    this.name = "telegram";
  }

  async send(text, event) {
    console.log(`[telegram] ${text}`);
    // Real impl:
    // await fetch(`https://api.telegram.org/bot${this.botToken}/sendMessage`, {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify({ chat_id: this.chatId, text }),
    // });
  }
}

module.exports = { TelegramChannel };
