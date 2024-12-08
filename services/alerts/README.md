# SolProbe Alerts

The notification layer. Subscribes to rule-matched events and fans them out
to Discord, Telegram, or arbitrary webhooks.

- `discord.js` for Discord integration
- `telegraf` for Telegram bots
- Declarative YAML rules (see `src/rules/example.yml`)

## Run

```bash
npm install
npm run dev
```
