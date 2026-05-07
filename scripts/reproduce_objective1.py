#!/usr/bin/env python3
import argparse
import yaml
from mev_agentic_ai.experiments.objective1 import run_objective1_smoke

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    if not cfg.get("offline_mode", True):
        raise SystemExit("Only offline mode is supported in scaffold.")
    result = run_objective1_smoke()
    print("offline fixture reproduction", result)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
