# SolProbe Analyzer

The intelligence layer for SolProbe. Processes collected metrics and
historical data to identify RPC degradation, slot lag, transaction failure
spikes, abnormal compute consumption, and network anomalies.

- Data: `pandas`, `numpy`
- Modeling: `scikit-learn`
- Scheduling: `celery` + Redis

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
