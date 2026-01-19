# Quickstart

Get SolProbe running locally with Docker Compose.

## Prerequisites

- Docker + Docker Compose
- An RPC endpoint (defaults to the public mainnet-beta endpoint)

## Steps

```bash
git clone https://github.com/<your-username>/solprobe.git
cd solprobe
cp .env.example .env      # fill in RPC endpoint and secrets
docker compose -f infra/docker-compose.yml up --build
```

Open `http://localhost:3000` once containers are healthy.

## Next steps

- Use the CLI standalone: `pip install -e apps/cli && solprobe status`
- Configure watch targets in `.env` (`WATCH_ADDRESSES`, `WATCH_PROGRAM_IDS`)
- Connect Railway/Vercel for auto-deploys on push
