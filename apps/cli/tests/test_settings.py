"""Settings defaults tests."""

from solprobe.config.settings import Settings


def test_settings_defaults():
    s = Settings()
    assert s.cluster == "mainnet-beta"
    assert s.rpc_endpoint.startswith("https://")
    assert s.log_level == "info"
