# AGENTS.md

## Project Mission

Build a reproducible research prototype for **Adversarial and Cooperative Multi-Agent Learning for MEV Optimization in Decentralized Finance**.

The system must support research on atomic triangular arbitrage under realistic Ethereum DeFi execution constraints, then extend the single-agent optimizer into adversarial and cooperative multi-agent settings. The mandatory core is Objective 1: dataset, sandbox, DRL optimizer, baselines, LLM benchmark, and constrained DRL+LLM integration. Objectives 2 and 3 must not be implemented until Objective 1 gates pass.

This repository is research software. It must default to simulation, offline datasets, and reproducible evaluation. It must not default to live trading, private-key usage, or mainnet transaction submission.

## Source-of-Truth Priority

When making implementation decisions, follow this order:

1. `PROJECT_SPEC.md`
2. The dissertation proposal PDF supplied with the project
3. Existing tests and configs in the repository
4. Public official documentation linked in `PROJECT_SPEC.md`
5. A small, well-documented implementation choice that preserves reproducibility

When the proposal and current code disagree, update the code or open an issue. Do not silently change the research scope.

## Scope Hierarchy

### Objective 1: Mandatory Core

Implement first:

1. Constrained atomic triangular arbitrage formulation.
2. Synchronized block-level Ethereum DeFi dataset pipeline.
3. Gymnasium-compatible single-agent sandbox environment.
4. PPO-based DRL optimizer.
5. Baselines: greedy, heuristic, beam search, grid search, convex fixed-path solver, MILP path-selection solver, SAC, TD3, and behavioral cloning.
6. LLM benchmark on four bounded tasks: path selection, constraint verification, profit estimation, and error explanation.
7. DRL+LLM integration with deterministic validation and DRL-only fallback.
8. Evaluation harness with statistical tests, seed control, metrics, failure taxonomy, and negative-results logging.

### Objective 2: First Extension

Implement only after Objective 1 passes:

1. Repeated non-cooperative MEV game.
2. Multi-agent observation and action spaces.
3. Priority gas auction and adversarial front-running simulation.
4. Equilibrium and convergence analysis outputs.

### Objective 3: Final Extension

Implement only after Objective 2 passes:

1. Mixed cooperative and adversarial game.
2. Coalition formation and profit-sharing mechanisms.
3. Information sharing, swap splitting, and coordination protocols.
4. Coalition stability and regime-boundary analysis.

## Non-Goals

Do not implement these unless a human maintainer explicitly changes the project scope:

- Live mainnet transaction submission.
- Private-key management or wallet signing flows.
- Code that targets real users for front-running, sandwich attacks, or liquidation sniping.
- Production trading infrastructure.
- Cross-chain arbitrage.
- MEV strategies beyond triangular arbitrage, except as future-work stubs.
- Claims of profitability without out-of-sample evaluation and transaction-cost accounting.

## Safety and Ethics Rules

- Keep the default mode as offline or sandbox simulation.
- Never request, store, print, commit, or log private keys, seed phrases, wallet secrets, or API keys.
- Keep `.env`, credentials, raw private datasets, and model checkpoints out of Git unless explicitly approved.
- API adapters must have mock or fixture-backed tests.
- Any live-chain integration must be read-only by default.
- The project may simulate adversarial MEV behavior for research, but must not provide a turnkey live front-running bot.
- Document negative results and failure modes rather than hiding them.

## Expected Repository Layout

Use this layout unless there is a strong reason to change it:

```text
.
+-- AGENTS.md
+-- PROJECT_SPEC.md
+-- README.md
+-- pyproject.toml
+-- .env.example
+-- configs/
|   +-- data/default.yaml
|   +-- env/single_agent.yaml
|   +-- env/multi_agent.yaml
|   +-- train/ppo.yaml
|   +-- train/sac.yaml
|   +-- train/td3.yaml
|   +-- train/bc.yaml
|   +-- llm/benchmark.yaml
|   `-- eval/default.yaml
+-- data/
|   +-- raw/              # ignored by Git
|   +-- interim/          # ignored by Git
|   +-- processed/        # ignored by Git or tracked by DVC
|   `-- samples/          # small public fixtures only
+-- docs/
|   +-- design/
|   +-- experiments/
|   `-- negative_results/
+-- notebooks/            # exploratory only, not source of truth
+-- scripts/
|   +-- ingest_data.py
|   +-- preprocess_blocks.py
|   +-- build_candidate_paths.py
|   +-- train_ppo.py
|   +-- run_baselines.py
|   +-- benchmark_llms.py
|   +-- evaluate_agent.py
|   `-- reproduce_objective1.py
+-- src/mev_agentic_ai/
|   +-- __init__.py
|   +-- config/
|   +-- data/
|   +-- domain/
|   +-- envs/
|   +-- solvers/
|   +-- llm/
|   +-- agents/
|   +-- multiagent/
|   +-- evaluation/
|   +-- experiments/
|   `-- utils/
+-- tests/
|   +-- unit/
|   +-- integration/
|   +-- regression/
|   `-- fixtures/
`-- outputs/              # ignored by Git
```

## Module Responsibilities

### `src/mev_agentic_ai/domain/`

Pure domain logic only. No network calls. No ML framework dependencies unless unavoidable.

Required components:

- Token, pool, path, swap, arbitrage, block, gas, wallet, transaction records.
- CPMM swap math with fees and reserve updates.
- Profit and ROI calculations.
- Constraint checks C1 through C10.
- Unit conversions for wei, gwei, ETH, token decimals, and USD.

Use integer arithmetic for on-chain units where possible. Use `decimal.Decimal` for money-like calculations when exactness matters. Avoid unbounded floating-point drift in tests that validate economics.

### `src/mev_agentic_ai/data/`

Data ingestion and block synchronization.

Required adapters:

- CoinGecko price adapter.
- Infura or Ethereum RPC pool-reserve adapter.
- Etherscan gas and transaction adapter.
- ZeroMEV arbitrage and MEV classification adapter.
- Local fixture adapter for tests.

Rules:

- All raw responses must be cached with timestamps and source metadata.
- Processed datasets must include schema version, chain ID, block number, block timestamp, and source provenance.
- Temporal train, validation, and test splits must prevent future leakage.
- Do not forward-fill across gaps larger than the configured block tolerance.

### `src/mev_agentic_ai/envs/`

Simulation environments.

Required environments:

- `TriangularArbEnv`: Gymnasium-style single-agent environment for Objective 1.
- `AdversarialMEVEnv`: repeated non-cooperative environment for Objective 2.
- `CoalitionMEVEnv`: mixed cooperative and adversarial environment for Objective 3.

Rules:

- Reset must be deterministic under a seed.
- Step outputs must include rich `info` fields for profit, gas, inclusion, latency, selected path, constraints, and failure labels.
- Atomic execution must either complete all swaps or revert and apply the configured failure cost.
- The latency model must include pool-state drift and opportunity decay. Do not reproduce the preliminary static-latency flaw.

### `src/mev_agentic_ai/solvers/`

Baseline and learning solvers.

Required solvers:

- Greedy path and size baseline.
- Heuristic baseline.
- Beam search.
- Exhaustive grid search upper-bound baseline.
- Fixed-path convex sizing solver.
- MILP path-selection solver with documented linearization.
- PPO.
- SAC.
- TD3.
- Behavioral cloning from historical searcher actions.

Rules:

- All solvers expose a common interface: `fit`, `predict`, `evaluate`, `save`, and `load`.
- All solver decisions must pass the same constraint checker before execution.
- Grid search is an offline upper-bound benchmark, not a deployable policy.

### `src/mev_agentic_ai/llm/`

Constrained LLM planning layer.

Allowed LLM tasks:

1. Path selection from a finite candidate set.
2. Constraint satisfaction verification.
3. Profit estimation.
4. Error explanation from a fixed taxonomy.

Rules:

- All prompts must use structured JSON input.
- All outputs must be validated by Pydantic or JSON Schema before use.
- Invalid outputs count as hallucinations and must trigger DRL-only fallback.
- The LLM must not directly execute trades.
- The LLM must not bypass constraints.
- Log token usage, latency, API cost, validation status, and fallback status.

### `src/mev_agentic_ai/agents/`

High-level policy orchestration.

Required agents:

- `DRLAgent`: wraps the trained numerical policy.
- `LLMPlanner`: wraps constrained planner responses.
- `IntegratedDRLLLMAgent`: ranks actions with DRL, validates or critiques with LLM, then executes DRL-approved actions.

Rules:

- DRL retains execution authority.
- LLM can only approve, reject, annotate, or rerank candidates inside allowed bounds.
- Fallback must be deterministic and benchmarked.

### `src/mev_agentic_ai/multiagent/`

Objective 2 and Objective 3 logic.

Required components:

- Stochastic adversary policy calibrated from historical searcher behavior.
- Priority gas auction ordering.
- Front-running and preemption model.
- Coalition sharing protocol.
- Profit-weighted reward redistribution.
- Coalition stability calculations.

## Testing Requirements

Every non-trivial change must include or update tests.

Minimum test categories:

- CPMM formula and reserve update tests.
- Profit, gas, and unit-conversion tests.
- Constraint C1 through C10 tests.
- Dataset schema tests.
- Train/validation/test leakage tests.
- Environment reset and step determinism tests.
- Baseline solver smoke tests.
- PPO train/evaluate smoke tests on a small fixture.
- LLM schema-validation tests with mocked LLM responses.
- Failure taxonomy tests.
- Multi-agent ordering and coalition accounting tests.

Recommended local checks before marking work complete:

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
mypy src
pytest -q
```

If a check is too expensive, run the nearest fast subset and document what was skipped.

## Reproducibility Rules

- Use config files for all hyperparameters.
- Log Git commit hash, dataset version, random seed, package versions, and command-line arguments.
- Report mean plus standard deviation across at least five seeds for research metrics.
- Use temporal train, validation, and test splits.
- Store run outputs under `outputs/<experiment_name>/<timestamp>/`.
- Keep generated tables and figures machine-readable as CSV or Parquet in addition to images.
- Do not overwrite previous experiment outputs unless explicitly requested.

## Metrics That Must Be Preserved

Profitability and risk:

- Mean profit in USD.
- Mean ROI percent.
- Sharpe ratio.
- Maximum drawdown.
- CVaR at 5 percent.
- Gas cost share relative to gross profit.

Execution quality:

- Execution success rate.
- Arbitrage type distribution.
- Mean inference time.
- Inclusion success probability and realized inclusion status.

LLM reliability:

- Structured-output validity rate.
- Hallucination rate.
- Profit prediction MAE.
- LLM cost per arbitrage.
- DRL fallback rate.

Failure analysis:

- Insufficient reserve.
- Wallet constraint violation.
- Gas spike.
- Stale state.
- Failed inclusion.
- Incorrect path.
- LLM validation failure.
- Adversarial preemption.
- Coordination collapse.

## Implementation Style

- Prefer simple, typed, testable Python modules.
- Keep IO at the edges and domain math pure.
- Use clear dataclasses or Pydantic models for records crossing module boundaries.
- Do not hide important assumptions in notebooks.
- Avoid global mutable state.
- Make random seeds explicit.
- Use structured logging rather than print-heavy scripts.
- Keep notebooks exploratory; production logic belongs in `src/`.
- Do not commit large data, credentials, or opaque binary artifacts.

## Documentation Rules

Update documentation when changing behavior:

- `README.md`: quickstart, commands, and user-facing workflow.
- `PROJECT_SPEC.md`: architecture, metrics, acceptance gates, and research scope.
- `docs/experiments/`: experiment protocols and results.
- `docs/negative_results/`: failed hypotheses, limitations, and mitigation attempts.

## Pull Request Checklist

A complete PR should answer:

- Which objective and milestone does this support?
- Which constraints are enforced or changed?
- Which datasets and config files are affected?
- Which metrics changed?
- Were all random seeds fixed and logged?
- Were schema and leakage checks run?
- Were LLM outputs validated or mocked in tests?
- Is the change still simulation-first and safe by default?
- Are negative or unexpected results documented?

## Common Mistakes to Avoid

- Treating gross arbitrage gain as net profit without gas, failed-transaction, and LLM costs.
- Ignoring wallet balance or pool-reserve feasibility.
- Letting LLM output directly become an executable action without validation.
- Training or evaluating with future information.
- Reporting single-seed results as final.
- Calling grid search deployable despite high inference time.
- Recreating the preliminary latency inconsistency by using identical observation and execution states.
- Letting multi-agent experiments begin before Objective 1 is reproducible.
