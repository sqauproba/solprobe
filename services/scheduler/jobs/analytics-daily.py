#!/usr/bin/env python3
"""Daily analytics rollup job."""

import argparse
from datetime import datetime, timedelta

import redis


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window", default="24h")
    args = parser.parse_args()

    r = redis.Redis.from_url("redis://localhost:6379")
    end = datetime.utcnow()
    start = end - timedelta(hours=24)

    r.set("analytics:last_run", end.isoformat())
    print(f"analytics rollup {start.isoformat()} -> {end.isoformat()}")


if __name__ == "__main__":
    main()
