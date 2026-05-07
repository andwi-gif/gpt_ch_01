#!/usr/bin/env python3
import argparse
import yaml

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--live", action="store_true", help="Future mode; disabled in scaffold")
    args = parser.parse_args()
    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    if args.live or cfg.get("enable_live_providers") or cfg.get("enable_live_llm"):
        raise SystemExit("Live provider/LLM mode is not implemented in scaffold.")
    print(f"offline fixture mode: would run {__file__} with {args.config}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
