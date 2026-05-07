# Agentic MEV Arbitrage Lab

Research prototype for **Adversarial and Cooperative Multi-Agent Learning for MEV Optimization in Decentralized Finance**.

This repository implements a simulation-first framework for Ethereum DeFi triangular arbitrage. The mandatory core builds a synchronized block-level dataset, a constrained arbitrage sandbox, PPO and baseline optimizers, an LLM structured-planning benchmark, and a validated DRL+LLM integrated agent. Extensions study adversarial competition and cooperative coalitions among multiple agentic systems.

> Research-only default: this project is for offline analysis, simulation, and reproducible benchmarking. It does not provide live mainnet trading, private-key management, transaction signing, or a turnkey front-running bot.

## What this project does

- Models atomic triangular arbitrage across single-DEX and cross-DEX paths.
- Enforces realistic constraints: net profit after costs, wallet balance, pool reserve feasibility, path continuity, loop closure, block-time budget, probabilistic inclusion, and failed-transaction penalties.
- Builds a block-level Ethereum DeFi dataset from price, reserve, gas, and arbitrage records.
- Trains a PPO-based DRL optimizer and compares it against greedy, heuristic, beam search, grid search, convex, MILP, SAC, TD3, and behavioral cloning baselines.
- Benchmarks LLMs on bounded structured tasks: path selection, constraint verification, profit estimation, and error explanation.
- Integrates DRL with a constrained LLM planner using schema validation and DRL-only fallback.
- Extends the framework to adversarial priority-gas-auction competition and cooperative coalition learning.

## Scope hierarchy

| Objective | Status | Description |
|---|---|---|
| Objective 1 | Mandatory core | Dataset, environment, PPO, baselines, LLM benchmark, DRL+LLM integration |
| Objective 2 | Extension | Non-cooperative repeated MEV game with adversarial agents and front-running |
| Objective 3 | Extension | Mixed adversarial-cooperative game with coalitions and information sharing |

Objective 1 must be reproducible before Objectives 2 and 3 are treated as final results.

## Architecture

```text
Data sources
  CoinGecko, Infura/RPC, Etherscan, ZeroMEV
        |
        v
Block-level synchronization pipeline
        |
        v
Processed benchmark dataset
        |
        +--> Candidate triangular paths
        |       |
        |       v
        |   Constrained arbitrage sandbox
        |       |
        |       +--> PPO / SAC / TD3 / behavioral cloning
        |       +--> Greedy / heuristic / beam / grid / convex / MILP
        |       +--> LLM structured-planning benchmark
        |       +--> Integrated DRL+LLM agent
        |
        v
Evaluation, statistics, failure analysis, reports
```

## Repository layout

```text
.
+-- AGENTS.md                  # Instructions for coding agents and contributors
+-- PROJECT_SPEC.md            # Full implementation specification
+-- README.md                  # This file
+-- configs/                   # YAML configs for data, envs, training, LLM, eval
+-- data/
|   +-- raw/                   # Raw provider data, ignored by Git
|   +-- interim/               # Intermediate data, ignored by Git
|   +-- processed/             # Versioned benchmark data
|   `-- samples/               # Small deterministic fixtures
+-- docs/
|   +-- design/                # Architecture notes
|   +-- experiments/           # Experiment protocols and reports
|   `-- negative_results/      # Failed hypotheses and limitations
+-- notebooks/                 # Exploration only
+-- scripts/                   # CLI entry points
+-- src/mev_agentic_ai/        # Python package
+-- tests/                     # Unit, integration, and regression tests
`-- outputs/                   # Experiment outputs, ignored by Git
```

## Quickstart

### 1. Create an environment

```bash
git clone <repo-url>
cd agentic-mev-arbitrage-lab
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Expected variables:

```text
COINGECKO_API_KEY=
INFURA_API_KEY=
ETHERSCAN_API_KEY=
ZEROMEV_API_BASE_URL=
OPENAI_API_KEY=
WANDB_API_KEY=
```

All variables are optional for fixture tests. Never commit `.env`.

### 3. Run tests

```bash
ruff check .
ruff format --check .
mypy src
pytest -q
```

### 4. Run a fixture-only Objective 1 smoke test

```bash
python scripts/reproduce_objective1.py --config configs/eval/default.yaml --dataset data/samples
```

The smoke test should produce:

```text
outputs/objective1/<timestamp>/
+-- metrics_summary.json
+-- per_episode_results.parquet
+-- failure_breakdown.csv
+-- statistical_tests.json
`-- report.md
```

## Data workflow

### Ingest data

```bash
python scripts/ingest_data.py --config configs/data/default.yaml
```

### Preprocess and synchronize at block level

```bash
python scripts/preprocess_blocks.py --config configs/data/default.yaml
```

### Build candidate triangular paths

```bash
python scripts/build_candidate_paths.py --config configs/data/default.yaml
```

Processed data is expected under:

```text
data/processed/<dataset_version>/
+-- metadata.json
+-- blocks.parquet
+-- tokens.parquet
+-- token_prices.parquet
+-- pools.parquet
+-- pool_reserves.parquet
+-- gas_blocks.parquet
+-- arbitrage_records.parquet
`-- candidate_paths.parquet
```

Use DVC, W&B Artifacts, or an equivalent system for large datasets and checkpoints. Keep raw data out of Git.

## Training

### PPO primary optimizer

```bash
python scripts/train_ppo.py --config configs/train/ppo.yaml --seed 1
```

Run five seeds for research reporting:

```bash
for seed in 1 2 3 4 5; do
  python scripts/train_ppo.py --config configs/train/ppo.yaml --seed "$seed"
done
```

### Baselines

```bash
python scripts/run_baselines.py \
  --config configs/eval/default.yaml \
  --methods greedy heuristic beam grid convex milp sac td3 bc
```

Grid search is an offline upper-bound benchmark. It should not be described as deployable unless it satisfies the latency budget.

## LLM benchmark

The LLM layer is intentionally constrained. It can only perform four structured tasks:

1. Select a path index from a finite candidate set.
2. Verify deterministic constraints.
3. Estimate profit components.
4. Explain a failed arbitrage using a fixed failure taxonomy.

Run:

```bash
python scripts/benchmark_llms.py \
  --config configs/llm/benchmark.yaml \
  --tasks path constraints profit explanation
```

Every LLM response must pass schema validation. Invalid responses count as hallucinations and trigger DRL-only fallback.

## Evaluate agents

```bash
python scripts/evaluate_agent.py --config configs/eval/default.yaml --agent drl_only
python scripts/evaluate_agent.py --config configs/eval/default.yaml --agent llm_only
python scripts/evaluate_agent.py --config configs/eval/default.yaml --agent drl_llm
```

Required metrics:

- Mean profit in USD.
- Mean ROI percent.
- Sharpe ratio.
- Maximum drawdown.
- CVaR at 5 percent.
- Gas cost share.
- Execution success rate.
- Arbitrage type distribution.
- Mean inference time.
- Hallucination rate.
- Structured-output validity rate.
- Profit prediction MAE.
- Failure taxonomy counts.

Research reports should use at least five seeds and paired statistical tests where applicable.

## Multi-agent experiments

After Objective 1 is reproducible:

### Objective 2: adversarial competition

```bash
python scripts/evaluate_agent.py \
  --config configs/env/multi_agent.yaml \
  --agent drl_llm \
  --scenario adversarial \
  --num-agents 4
```

Expected mechanisms:

- Priority gas auction ordering.
- Front-running and adversarial preemption.
- Stochastic adversary policies calibrated from historical data.
- Profit degradation and execution success under N in {2, 4, 8} agents.

### Objective 3: cooperative coalitions

```bash
python scripts/evaluate_agent.py \
  --config configs/env/multi_agent.yaml \
  --agent drl_llm \
  --scenario coalition \
  --coalition-size 3
```

Expected mechanisms:

- Path sharing.
- Swap amount splitting.
- Profit-weighted redistribution.
- Coalition stability and cooperation-benefit regime analysis.

## Failure analysis

All experiments must produce a failure breakdown. Core labels include:

- `no_profitable_path`
- `wallet_insufficient`
- `reserve_insufficient`
- `path_discontinuous`
- `loop_not_closed`
- `latency_budget_exceeded`
- `stale_state_loss`
- `opportunity_decayed`
- `gas_spike`
- `failed_inclusion`
- `reverted_execution`
- `llm_invalid_json`
- `llm_schema_violation`
- `llm_bad_numeric_value`
- `adversarial_preemption`
- `coordination_collapse`
- `training_instability`

Unexpected or negative results should be recorded in `docs/negative_results/`.

## Development workflow

1. Read `AGENTS.md` and `PROJECT_SPEC.md` before changing code.
2. Implement the smallest testable unit.
3. Add or update tests.
4. Run linting, type checks, and tests.
5. Update docs and configs.
6. Save experiment outputs under `outputs/` without overwriting previous runs.

Recommended checks:

```bash
ruff check .
ruff format --check .
mypy src
pytest -q
```

## Reproducibility checklist

Before publishing a result, confirm:

- Dataset version is recorded.
- Git commit hash is recorded.
- All seeds are recorded.
- Hyperparameters are stored in YAML.
- Train, validation, and test splits are temporal.
- No future information leaks into training.
- All costs are included in net profit.
- All LLM outputs are validated.
- Raw per-trade and per-episode outputs are saved.
- Negative or surprising findings are documented.

## Roadmap

- [ ] Project skeleton, configs, and CI.
- [ ] Domain models, CPMM math, constraints C1-C6.
- [ ] Block-level dataset ingestion and synchronization.
- [ ] Candidate triangular path builder.
- [ ] Single-agent Gymnasium environment with latency drift.
- [ ] Baselines and PPO training.
- [ ] Objective 1 five-seed evaluation report.
- [ ] LLM structured benchmark.
- [ ] DRL+LLM integrated agent.
- [ ] Objective 2 adversarial game.
- [ ] Objective 3 cooperative coalition game.
- [ ] Dataset and reproducibility package release.

## Citation

If you use this project, cite the related dissertation proposal and any associated publications once available.

```bibtex
@phdproposal{faiz2026agenticmev,
  title = {Adversarial and Cooperative Multi-Agent Learning for MEV Optimization in Decentralized Finance},
  author = {Faiz, Syahirul},
  institution = {Khalifa University of Science and Technology},
  year = {2026},
  note = {PhD dissertation proposal}
}
```

## License

Add a `LICENSE` file before public release. Until then, treat the repository as all-rights-reserved research work under the owner's institutional policy.
