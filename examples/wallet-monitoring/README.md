# Wallet monitoring

Watch a wallet's SOL balance over time from the CLI:

```bash
solprobe wallet inspect <ADDRESS>
solprobe wallet watch <ADDRESS>
```

Or monitor it on the dashboard (Wallets panel) after configuring watch
targets in `.env`:

```env
WATCH_ADDRESSES=<ADDRESS1>,<ADDRESS2>
```
