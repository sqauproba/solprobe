# SolProbe Python SDK

Python client library for the SolProbe API.

```python
from sdk_python import SolProbeClient

client = SolProbeClient(base_url="http://localhost:8080")
health = client.health()
print(health.status)
```
