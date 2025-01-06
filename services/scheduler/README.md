# Scheduler

Background jobs for SolProbe: periodic analytics runs, cleanup, and
maintenance tasks. Jobs are queued to Redis and executed by workers.

## Layout

- `jobs/` — job definitions (one file per job)
- `queues/` — queue definitions and routing
- `workers/` — worker entrypoints

## Example job

```bash
python jobs/analytics-daily.py --window 24h
```
