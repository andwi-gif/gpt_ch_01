from pathlib import Path
import yaml


def test_configs_exist_and_parse() -> None:
    base = Path("configs")
    paths = [
        base / "data/default.yaml", base / "env/single_agent.yaml", base / "env/multi_agent.yaml",
        base / "train/ppo.yaml", base / "train/sac.yaml", base / "train/td3.yaml", base / "train/bc.yaml",
        base / "llm/benchmark.yaml", base / "eval/default.yaml",
    ]
    for p in paths:
        assert p.exists()
        assert isinstance(yaml.safe_load(p.read_text()), dict)
