# Docker deployment

Run the full SolProbe stack:

```bash
cp .env.example .env
docker compose -f infra/docker-compose.yml up --build
```

Services:

| Service | Port |
|---|---|
| dashboard | 3000 |
| api | 8080 |
| collector | 50051 |
| postgres | 5432 |
| redis | 6379 |
| prometheus | 9090 |
| grafana | 3001 |

Open `http://localhost:3000`.
