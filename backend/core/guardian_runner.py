#!/usr/bin/env python3
import argparse
import json
import time
from core import guardian

def main():
    parser = argparse.ArgumentParser(description="Hermes Guardian daemon")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=300)
    parser.add_argument("--auto-safe", action="store_true")
    args = parser.parse_args()

    if args.once:
        print(json.dumps(guardian.run_once(auto_safe=args.auto_safe), ensure_ascii=False, indent=2))
        return

    while True:
        result = guardian.run_once(auto_safe=args.auto_safe)
        print(json.dumps({
            "timestamp": result.get("timestamp"),
            "ok": result.get("ok"),
            "errors": result.get("errors"),
            "open_incidents": (result.get("incidents") or {}).get("stats", {}).get("open"),
        }, ensure_ascii=False), flush=True)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
