# SolProbe Go SDK

Go client library for the SolProbe API.

```go
import "github.com/solprobe/solprobe/packages/sdk-go"

client := sdk.New("http://localhost:8080")
health, _ := client.Health()
```
