# PROJECT_SPEC.md

# Agentic MEV Arbitrage Lab

## 1. Purpose

This project implements, from scratch, a reproducible research prototype for adversarial and cooperative multi-agent learning for MEV optimization in decentralized finance.

The core problem is atomic triangular arbitrage on Ethereum-style automated market makers. The system must select a feasible three-swap cyclic path and trade size that maximize net profit after gas, failed-inclusion cost, LLM cost, wallet limits, reserve limits, and latency effects. The single-agent system is then extended to repeated adversarial and cooperative multi-agent games.

The implementation must be simulation-first and research-focused. It should produce a clean benchmark, baseline comparisons, trained agents, evaluation reports, and negative-results documentation.

## 2. Proposal Alignment

The implementation follows the proposal scope hierarchy:

| Level | Objective | Required outcome |
|---|---|---|
| Objective 1 | Develop an Agentic AI framework for arbitrage optimization in DeFi | Dataset, constrained environment, PPO optimizer, baseline solvers, LLM benchmark, integrated DRL+LLM agent, evaluation suite |
| Objective 2 | Model adversarial competition between agentic AI systems | Non-cooperative repeated MEV game with priority gas auction, front-running, adversary policies, and equilibrium analysis |
| Objective 3 | Study mixed adversarial-collaborative agentic learning | Coalition mechanisms, information sharing, swap splitting, profit redistribution, and cooperation-benefit regime analysis |

Objective 1 is mandatory. Objectives 2 and 3 are extensions and must not weaken or delay the reproducible single-agent benchmark.

## 3. External Documentation Anchors

Use the following public documentation as implementation anchors:

- AGENTS.md guidance: https://developers.openai.com/codex/guides/agents-md
- GitHub repository README and repository guidance: https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories
- Ethereum MEV overview: https://ethereum.org/developers/docs/mev
- EIP-1559 fee mechanism: https://eips.ethereum.org/EIPS/eip-1559
- Ethereum proof-of-stake slots: https://ethereum.org/developers/docs/consensus-mechanisms/pos/
- Uniswap v2 concepts: https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works
- Stable-Baselines3 PPO: https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html
- Gymnasium API: https://gymnasium.farama.org/
- PettingZoo multi-agent API: https://pettingzoo.farama.org/
- Ray RLlib multi-agent documentation: https://docs.ray.io/en/latest/rllib/multi-agent-envs.html
- CoinGecko API documentation: https://docs.coingecko.com/
- Infura and MetaMask developer documentation: https://docs.metamask.io/services/get-started/infura
- ZeroMEV API guide: https://info.zeromev.org/api.html
- Etherscan API documentation: https://docs.etherscan.io/
- DVC documentation: https://dvc.org/doc
- Weights and Biases artifacts: https://docs.wandb.ai/models/artifacts

These sources support tool and interface choices. The dissertation proposal remains the research-scope source of truth.

## 4. Research Questions and Success Criteria

### RQ1: DRL optimizer versus baselines

Question: How does a DRL arbitrage optimizer perform against heuristic, traditional, and optimization-theoretic baselines under realistic DeFi constraints?

Success criteria:

- Mean profit at least 50 percent of grid-search upper bound.
- End-to-end inference latency below 100 ms for deployable solvers.
- Statistical significance with paired tests, p < 0.05.
- At least five independent random seeds.
- Evaluation across gas, balance, liquidity, and latency regimes.

### RQ2: LLM architectures for structured planning

Question: Which LLM architectures are effective for structured DeFi arbitrage planning tasks?

Success criteria:

- Best model has profit-prediction MAE at least 20 percent lower than the worst evaluated model.
- Structured-output validity rate above 90 percent.
- Per-call cost satisfies economic rationality for most evaluated opportunities.

### RQ3: Integrated DRL+LLM agent

Question: Does constrained LLM planning improve DRL performance and robustness?

Success criteria:

- Integrated agent has statistically higher mean profit than DRL-only and LLM-only baselines.
- Hallucination rate below 10 percent.
- Constraints are never bypassed by LLM output.

### RQ4: Adversarial multi-agent competition

Question: How does a DRL+LLM system perform in non-cooperative MEV competition?

Success criteria:

- Positive mean profit under N in {2, 4, 8} adversarial agents.
- Execution success rate above 50 percent.
- Sharpe degradation below 30 percent relative to single-agent baseline.

### RQ5: Cooperative versus adversarial learning

Question: Can cooperative DRL+LLM coalitions outperform purely adversarial strategies?

Success criteria:

- Coalition aggregate profit statistically exceeds an equal number of adversarial agents in at least one identifiable market regime.
- Boundary conditions separating cooperation-beneficial from cooperation-neutral regimes are characterized.

## 5. System Architecture

```text
External data sources
  CoinGecko, Infura/RPC, Etherscan, ZeroMEV
        |
        v
Data ingestion and block synchronization
        |
        v
Block-level benchmark dataset
        |
        +--> Candidate triangular path builder
        |       |
        |       v
        |   Constrained arbitrage sandbox
        |       |
        |       +--> Baselines: greedy, heuristic, beam, grid, convex, MILP
        |       +--> DRL: PPO, SAC, TD3, behavioral cloning
        |       +--> LLM benchmark: path, constraints, profit, explanation
        |       +--> Integrated DRL+LLM agent
        |
        v
Evaluation harness and failure analysis
        |
        +--> Objective 1 reports
        +--> Objective 2 adversarial game
        +--> Objective 3 coalition game
```

### Main design principle

All executable decisions pass through the same deterministic constraint checker. The LLM can recommend or explain, but cannot override the constraint checker or directly execute trades.

## 6. Repository Layout

```text
.
+-- AGENTS.md
+-- PROJECT_SPEC.md
+-- README.md
+-- LICENSE
+-- CITATION.cff
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
|   +-- raw/
|   +-- interim/
|   +-- processed/
|   `-- samples/
+-- docs/
|   +-- design/
|   +-- experiments/
|   `-- negative_results/
+-- notebooks/
+-- scripts/
+-- src/mev_agentic_ai/
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
`-- outputs/
```

## 7. Domain Model

### 7.1 Core entities

| Entity | Required fields |
|---|---|
| `Token` | `chain_id`, `address`, `symbol`, `decimals`, `coingecko_id`, `is_stablecoin` |
| `Pool` | `pool_address`, `dex`, `version`, `token0`, `token1`, `fee_bps`, `created_block` |
| `PoolReserveSnapshot` | `block_number`, `block_timestamp`, `pool_address`, `reserve0_raw`, `reserve1_raw`, `sqrt_price_x96` optional, `liquidity` optional |
| `GasSnapshot` | `block_number`, `base_fee_per_gas`, `priority_fee_p50`, `priority_fee_p90`, `gas_used`, `gas_limit`, `tx_count` |
| `WalletState` | `timestamp`, `block_number`, token balances, USD value |
| `Swap` | `pool_address`, `token_in`, `token_out`, `amount_in_raw`, `amount_out_raw`, `fee_paid_raw` |
| `TriangularPath` | `path_id`, `swap1_pool`, `swap2_pool`, `swap3_pool`, `token_start`, `token_mid1`, `token_mid2`, `dex_pattern` |
| `ArbitrageAction` | `path_id`, `trade_fraction`, `gas_bid` optional, `llm_planner_used` |
| `ArbitrageResult` | `success`, `gross_gain_usd`, `gas_cost_usd`, `llm_cost_usd`, `failed_tx_cost_usd`, `net_profit_usd`, `failure_label` |

### 7.2 Units

- Store on-chain values as integers in raw token units.
- Store gas prices in wei or gwei with explicit field names.
- Store USD values as Decimal-compatible strings or fixed precision decimals in Parquet.
- Convert units only at module boundaries.

## 8. Dataset Specification

### 8.1 Data source mapping

| Source | Purpose | Required fields |
|---|---|---|
| CoinGecko | Token prices and historical market data | `timestamp`, `token`, `price_usd`, `market_cap`, `volume` |
| Infura / Ethereum RPC | Pool reserve snapshots and block data | `block_number`, `block_timestamp`, `pool_address`, reserves, logs |
| Etherscan | Gas, transaction details, receipts | `tx_hash`, `block_number`, `gas_price`, `gas_used`, status |
| ZeroMEV | MEV and arbitrage records | `tx_hash`, `block_number`, classification, profit, protocol, ordering |
| Local fixtures | Offline testing | Small deterministic rows for all schemas |

### 8.2 Processed dataset files

Use Parquet for processed data.

```text
data/processed/<dataset_version>/
+-- metadata.json
+-- blocks.parquet
+-- tokens.parquet
+-- token_prices.parquet
+-- pools.parquet
+-- pool_reserves.parquet
+-- gas_blocks.parquet
+-- mev_transactions.parquet
+-- arbitrage_records.parquet
+-- candidate_paths.parquet
+-- train_blocks.parquet
+-- validation_blocks.parquet
`-- test_blocks.parquet
```

### 8.3 Required schema fields

#### `blocks.parquet`

| Field | Type | Notes |
|---|---|---|
| `chain_id` | int | Ethereum mainnet is 1 |
| `block_number` | int | Primary key |
| `block_timestamp` | timestamp | UTC |
| `slot` | int optional | If available |
| `tx_count` | int | Transaction count |
| `gas_used` | int | Block gas used |
| `gas_limit` | int | Block gas limit |
| `base_fee_per_gas_wei` | int optional | EIP-1559 blocks |

#### `token_prices.parquet`

| Field | Type | Notes |
|---|---|---|
| `timestamp` | timestamp | Source timestamp |
| `block_number` | int | Nearest synchronized block |
| `token_address` | string | Lowercase checksum-normalized |
| `symbol` | string | Token symbol |
| `price_usd` | decimal | USD price |
| `source` | string | Data provider |

#### `pool_reserves.parquet`

| Field | Type | Notes |
|---|---|---|
| `block_number` | int | Snapshot block |
| `pool_address` | string | Pool contract |
| `dex` | string | Example: `uniswap_v2`, `uniswap_v3` |
| `token0_address` | string | Token0 |
| `token1_address` | string | Token1 |
| `reserve0_raw` | string | Integer as string to avoid overflow |
| `reserve1_raw` | string | Integer as string to avoid overflow |
| `fee_bps` | int | Swap fee basis points |
| `source` | string | Provider |

#### `arbitrage_records.parquet`

| Field | Type | Notes |
|---|---|---|
| `tx_hash` | string | Transaction hash |
| `block_number` | int | Execution block |
| `inclusion_status` | string | `included`, `failed`, `reverted`, `unknown` |
| `profit_usd` | decimal | Source-estimated realized profit |
| `gas_price_wei` | int | Effective gas price |
| `gas_used` | int | Gas used |
| `path_tokens` | string | JSON list |
| `path_pools` | string | JSON list |
| `number_of_tokens` | int | Usually 3 for triangular arbitrage |
| `number_of_dexes` | int | 1 or more |
| `dexes` | string | JSON list |
| `source_url` | string | Etherscan or ZeroMEV URL |

### 8.4 Synchronization rules

- All features must be aligned at block level.
- Use temporal splits by block number, not random row splitting.
- Do not let validation or test blocks influence training normalization, candidate generation labels, or imitation targets.
- Forward-fill reserves only inside the configured tolerance window. Gaps above tolerance are excluded and logged.
- Persist dropped rows and reasons under `outputs/data_quality/`.

### 8.5 Dataset versioning

- Each processed dataset has a semantic version: `vMAJOR.MINOR.PATCH`.
- `metadata.json` must include source ranges, provider versions if available, schema version, row counts, exclusions, and checksum hashes.
- Use DVC or equivalent for large data and model artifacts.

## 9. Mathematical Formulation

### 9.1 CPMM swap

For a constant product pool with reserves `x` and `y`, fee rate `gamma`, and input `delta_x`, the effective input is:

```text
delta_x_eff = (1 - gamma) * delta_x
```

The output is:

```text
delta_y = y - (x * y) / (x + delta_x_eff)
```

The post-trade reserves are:

```text
x_next = x + delta_x_eff
y_next = y - delta_y
```

The implementation must preserve the invariant within numerical tolerance and must reject swaps that violate reserve feasibility.

### 9.2 Single-agent objective

For arbitrage action `a`:

```text
profit(a) = T_gain(a) - T_cost(a) - LLM_cost(a)
```

With probabilistic inclusion:

```text
expected_profit(a) = P_inc(a, b) * (T_gain(a) - T_cost(a) - LLM_cost(a))
```

Failed inclusion or reverted execution applies the configured failed-transaction gas cost.

### 9.3 Inclusion probability

Model inclusion as a function of the submitted gas bid and block gas threshold:

```text
P_inc(a, b) = Pr(gas_price(a) >= gas_threshold_b)
```

Initial implementation:

- Estimate `gas_threshold_b` from historical block-level fee and priority fee distributions.
- Support KDE and empirical-quantile variants.
- Condition on block congestion features such as `tx_count`, `gas_used / gas_limit`, and priority fee quantiles.

### 9.4 LLM cost

Use the proposal cost decomposition:

```text
LLM_cost(a) = w1 * C_reason(a)
            + w2 * C_api(a)
            + w3 * C_energy(a)
            + w4 * C_latency(a)
            - w5 * G_memory(a)
```

The default implementation may set energy and memory terms to zero until measured, but must keep the fields in logs and configs.

## 10. Constraints

The environment must enforce the following constraints before and during execution.

| ID | Constraint | Implementation requirement |
|---|---|---|
| C1 | Economic rationality | `T_gain > T_cost + LLM_cost + failed_tx_cost` |
| C2 | Wallet feasibility | Cannot sell more than wallet balance |
| C3 | Pool reserve feasibility | Cannot buy more than available reserve and must model slippage |
| C4 | Path continuity | Swap k input token equals previous swap output token for k in {2, 3} |
| C5 | Loop closure | Final output token equals first input token |
| C6 | Block-time budget | End-to-end decision and execution must fit within configured slot budget; latency must cause state drift |
| C7 | Coalition profit weights | Cooperative weights sum to 1 |
| C8 | Shared swap constraint | Coalition swap amount equals sum of member contributions |
| C9 | Priority gas auction ordering | Higher gas bid executes before lower gas bid |
| C10 | Coalition LLM budget | Coalition LLM costs cannot exceed configured budget |

Objective 1 must enforce C1 through C6. Objectives 2 and 3 must enforce all applicable constraints.

## 11. Environment Specification

### 11.1 Single-agent environment: `TriangularArbEnv`

Interface: Gymnasium-compatible.

#### Observation

Observation is a flattened or dict representation of:

```text
s_t = (
  wallet balances,
  pool reserves,
  token USD prices,
  gas estimate features,
  candidate path features,
  latency budget,
  recent opportunity decay features
)
```

Recommended dict spaces:

| Key | Shape | Description |
|---|---:|---|
| `wallet` | `[num_tokens]` | Normalized token balances and USD values |
| `pool_features` | `[num_pools, features]` | Reserves, fee, DEX ID, last update age |
| `candidate_paths` | `[K, path_features]` | Token continuity, estimated gross profit, reserve depth, DEX pattern |
| `gas` | `[features]` | Base fee, priority quantiles, congestion, sampled bid |
| `time` | `[features]` | Block number, slot budget, latency estimate |

#### Action

Objective 1 action:

```text
a_t = (path_index, trade_fraction)
```

- `path_index`: integer in `[0, K - 1]`.
- `trade_fraction`: continuous value in `[0.001, 0.1]` by default.

Objective 2 and 3 may extend action with:

```text
gas_bid_multiplier or gas_bid_wei
```

#### Reward

Default reward:

```text
reward = realized_net_profit_usd
```

Penalties:

- Constraint violation: large negative reward with failure label.
- Reverted or failed inclusion: failed gas cost penalty.
- Invalid LLM output: no direct reward penalty by default, but logged and fallback used. Experiments may add an ablation penalty.

#### Step info

`info` must include:

```text
{
  "block_number": int,
  "path_id": str,
  "trade_fraction": float,
  "gross_gain_usd": float,
  "gas_cost_usd": float,
  "llm_cost_usd": float,
  "failed_tx_cost_usd": float,
  "net_profit_usd": float,
  "roi_pct": float,
  "inclusion_probability": float,
  "included": bool,
  "latency_ms": float,
  "state_drift": {...},
  "constraints": {...},
  "failure_label": str | null
}
```

### 11.2 Latency redesign requirement

The preliminary results found no measurable effect from changing latency because observation and execution states were identical. The implementation must fix this.

Required latency behavior:

1. Sample decision latency from solver runtime or configured distribution.
2. Between observation and execution, sample intervening transactions from the block-level dataset.
3. Apply reserve and price drift to affected pools.
4. Re-evaluate constraints at execution state.
5. Record stale-state failures and opportunity decay.

A test must verify that increasing latency can change execution state and realized profit on a controlled fixture.

### 11.3 Multi-agent environments

Objective 2:

- Use a repeated non-cooperative game.
- Agents compete for shared candidate paths.
- Priority gas auction orders execution.
- Front-running is modeled by adversaries observing a pending action and submitting the same or overlapping path with a higher gas bid.

Objective 3:

- Add coalition membership.
- Coalition agents can share path, size, state, and profit observations.
- Support coordination mechanisms: full path sharing, swap amount splitting, and profit-weighted redistribution.
- Evaluate coalition stability and regime boundaries.

Recommended APIs:

- Use PettingZoo for custom multi-agent environment compatibility.
- Use RLlib when scalable multi-agent training is needed.

## 12. Solver Specification

### 12.1 Common solver interface

All solvers must expose:

```python
class SolverProtocol(Protocol):
    def fit(self, env, config): ...
    def predict(self, observation, deterministic: bool = True): ...
    def evaluate(self, env, episodes: int, seed: int): ...
    def save(self, path: str): ...
    @classmethod
    def load(cls, path: str): ...
```

### 12.2 Baselines

| Solver | Purpose | Expected behavior |
|---|---|---|
| Greedy | Fast lower bound | Select best immediate estimated path and default size |
| Heuristic | Rule-based baseline | Use hand-coded thresholds for gas, reserve depth, and profit |
| Beam search | Limited combinatorial search | Explore top candidate paths with bounded branching |
| Grid search | Offline upper bound | Exhaustively search path and size grid; not deployable |
| Convex fixed-path solver | Optimization-theoretic sizing | Optimize trade size for a known path |
| MILP path selection | Discrete optimizer | Select path under linearized constraints |
| SAC | Off-policy RL baseline | Compare continuous-control behavior |
| TD3 | Off-policy actor-critic baseline | Compare deterministic policy behavior |
| Behavioral cloning | Offline imitation | Learn from historical searcher actions |

### 12.3 PPO primary solver

PPO is the primary online DRL solver for Objective 1 because it is stable, widely used, and extendable to multi-agent settings. Implementation must still empirically compare PPO against all required baselines.

Required PPO features:

- Multi-input policy for dict observations, or deterministic flattened feature encoder.
- Separate handling of discrete path selection and continuous trade fraction.
- Reward normalization as an ablation option.
- Entropy or exploration bonus as an ablation option.
- TensorBoard or W&B-compatible logging.
- Seeded evaluation.

### 12.4 Algorithm selection rule

If PPO underperforms a non-DRL method in static single-agent settings, do not hide the result. Document it and test whether PPO has an advantage in dynamic latency, stale-state, or adversarial settings.

## 13. LLM Benchmark Specification

### 13.1 Allowed tasks

| Task | Input | Output | Ground truth |
|---|---|---|---|
| Path selection | State JSON and candidate paths | Valid `path_index` | Environment or grid-search best path |
| Constraint verification | State JSON and proposed action | Valid/invalid plus violated constraints | Deterministic constraint checker |
| Profit estimation | State JSON and action | Expected profit components | Environment simulation |
| Error explanation | Failed action trace | Failure label and short reason | Failure taxonomy label |

### 13.2 Structured output schemas

#### Path selection

```json
{
  "path_index": 0,
  "confidence": 0.0,
  "reason": "short bounded explanation"
}
```

#### Constraint verification

```json
{
  "valid": true,
  "violations": [],
  "reason": "short bounded explanation"
}
```

#### Profit estimation

```json
{
  "gross_gain_usd": 0.0,
  "gas_cost_usd": 0.0,
  "llm_cost_usd": 0.0,
  "expected_net_profit_usd": 0.0,
  "confidence": 0.0
}
```

#### Error explanation

```json
{
  "failure_label": "gas_spike",
  "violated_constraints": ["C1"],
  "reason": "short bounded explanation"
}
```

### 13.3 Validation

Every LLM response must be checked for:

- Valid JSON.
- Required fields.
- Correct types.
- Valid path index.
- Valid constraint IDs.
- Profit fields finite and within configured numeric bounds.
- Failure label in fixed taxonomy.
- Token and cost limits.

Invalid response handling:

1. Log response and validation error.
2. Increment hallucination count.
3. Trigger DRL-only fallback.
4. Continue safely without letting the LLM action execute.

### 13.4 Models

Benchmark model families configured by file, not hard-coded:

- Open-source local or hosted models, such as LLaMA-family and Qwen-family models.
- Proprietary API models, such as GPT-family models.
- Retrieval-augmented baseline using historical arbitrage records.

The benchmark must support a mock model for CI tests.

## 14. Integrated DRL+LLM Agent

### 14.1 Control flow

```text
1. DRL policy observes state.
2. DRL ranks candidate actions.
3. Top candidate or top-N candidates are serialized to JSON.
4. LLM planner performs bounded task: validate, estimate, explain, or rerank.
5. Validation layer checks LLM output.
6. If valid, integration policy may adjust candidate ranking inside safe bounds.
7. If invalid, DRL-only fallback executes.
8. Environment executes and logs result.
9. Feedback is stored for later offline fine-tuning or prompt improvement.
```

### 14.2 Integration modes

| Mode | Description | Use |
|---|---|---|
| `drl_only` | PPO or other DRL policy executes directly | Baseline |
| `llm_only` | LLM selects from candidates after validation | Baseline, never bypass constraints |
| `llm_validate` | LLM checks DRL candidate | Primary safe integration |
| `llm_rerank_top_n` | LLM reranks top-N DRL candidates | Ablation |
| `llm_explain_only` | LLM explains failures after execution | Low-risk interpretability |

### 14.3 Integration metrics

- Mean profit.
- Delta profit versus DRL-only.
- Delta profit versus LLM-only.
- LLM call rate.
- LLM fallback rate.
- Hallucination rate.
- Added latency.
- Added cost.
- Profit prediction MAE.

## 15. Evaluation Protocol

### 15.1 Required regimes

Evaluate across combinations of:

- Wallet balance levels.
- Latency budgets.
- Gas price regimes or multipliers.
- Liquidity depth regimes.
- Candidate path counts.
- Market volatility or state-drift regimes.
- Number of adversarial agents for Objective 2.
- Coalition sizes for Objective 3.

### 15.2 Metrics

Profitability and risk:

```text
mean_profit_usd
mean_roi_pct
sharpe_ratio
max_drawdown_usd
cvar_5pct_usd
gas_cost_share
```

Execution quality:

```text
execution_success_rate
inclusion_success_rate
arbitrage_type_distribution
mean_inference_time_ms
state_drift_magnitude
opportunity_decay_rate
```

LLM reliability:

```text
structured_output_validity_rate
hallucination_rate
profit_prediction_mae
llm_cost_usd_per_call
fallback_rate
```

Multi-agent:

```text
profit_degradation_vs_single_agent
front_run_rate
priority_gas_overpayment
nash_gap_proxy
coalition_aggregate_profit
coalition_stability_margin
coordination_overhead
```

### 15.3 Statistical reporting

- Report mean plus standard deviation over at least five seeds.
- Use paired t-tests when comparing methods on matched scenarios.
- Use non-parametric tests as robustness checks if distributions are non-normal.
- Store raw per-episode results so all tables and figures can be regenerated.

### 15.4 Experiment output layout

```text
outputs/<objective>/<experiment_name>/<timestamp>/
+-- config.yaml
+-- metrics_summary.json
+-- per_episode_results.parquet
+-- per_trade_results.parquet
+-- failure_breakdown.csv
+-- statistical_tests.json
+-- figures/
+-- checkpoints/
`-- report.md
```

## 16. Failure Taxonomy

Each failure must be assigned exactly one primary label and zero or more secondary labels.

| Label | Description |
|---|---|
| `no_profitable_path` | No candidate path satisfies C1 |
| `wallet_insufficient` | C2 violation |
| `reserve_insufficient` | C3 violation |
| `path_discontinuous` | C4 violation |
| `loop_not_closed` | C5 violation |
| `latency_budget_exceeded` | C6 violation |
| `stale_state_loss` | Observation state changed before execution |
| `opportunity_decayed` | Competing transactions removed expected profit |
| `gas_spike` | Gas cost increase caused loss |
| `failed_inclusion` | Transaction not included or displaced |
| `reverted_execution` | Atomic transaction reverted |
| `llm_invalid_json` | LLM output was not parseable JSON |
| `llm_schema_violation` | LLM JSON failed schema validation |
| `llm_bad_numeric_value` | LLM produced impossible or unsafe numeric values |
| `adversarial_preemption` | Competitor executed overlapping path first |
| `coordination_collapse` | Coalition agents conflicted or depleted shared pools |
| `training_instability` | RL policy diverged or oscillated |

## 17. CLI Commands

The repository should expose module commands and script wrappers.

### Data

```bash
python scripts/ingest_data.py --config configs/data/default.yaml
python scripts/preprocess_blocks.py --config configs/data/default.yaml
python scripts/build_candidate_paths.py --config configs/data/default.yaml
```

### Training

```bash
python scripts/train_ppo.py --config configs/train/ppo.yaml --seed 1
python scripts/train_ppo.py --config configs/train/ppo.yaml --seed 2
python scripts/train_ppo.py --config configs/train/ppo.yaml --seed 3
python scripts/train_ppo.py --config configs/train/ppo.yaml --seed 4
python scripts/train_ppo.py --config configs/train/ppo.yaml --seed 5
```

### Baselines

```bash
python scripts/run_baselines.py --config configs/eval/default.yaml --methods greedy heuristic beam grid convex milp sac td3 bc
```

### LLM benchmark

```bash
python scripts/benchmark_llms.py --config configs/llm/benchmark.yaml --tasks path constraints profit explanation
```

### Evaluation

```bash
python scripts/evaluate_agent.py --config configs/eval/default.yaml --agent drl_only
python scripts/evaluate_agent.py --config configs/eval/default.yaml --agent llm_only
python scripts/evaluate_agent.py --config configs/eval/default.yaml --agent drl_llm
```

### Reproduction

```bash
python scripts/reproduce_objective1.py --config configs/eval/default.yaml
```

## 18. Configuration Requirements

Use YAML configs. No hard-coded research settings.

Minimum config groups:

- `data`: sources, tokens, pools, block ranges, cache settings, split boundaries.
- `env`: candidate path count, trade fraction range, slot budget, latency model, failure costs.
- `train`: algorithm hyperparameters, seeds, timesteps, checkpoint cadence.
- `llm`: model list, prompt templates, schema paths, cost weights, token limits.
- `eval`: methods, metrics, regimes, statistical tests, output paths.

## 19. Acceptance Gates

### Gate 0: Skeleton

- Repository structure exists.
- `pyproject.toml` installs package.
- `pytest` runs.
- README quickstart works on fixtures.

### Gate 1: Domain math

- CPMM, gas, unit conversion, profit, ROI, and constraints C1 through C6 have unit tests.
- Known examples reproduce expected outputs within tolerance.

### Gate 2: Dataset pipeline

- Adapters can load fixtures and at least one real provider sample.
- Processed Parquet schema validates.
- Temporal split prevents leakage.
- Data quality report is generated.

### Gate 3: Single-agent environment

- `TriangularArbEnv` is Gymnasium-compatible.
- Deterministic under seed.
- Latency drift test passes.
- Failure taxonomy appears in `info`.

### Gate 4: Baselines

- Greedy, heuristic, beam, grid, convex, and MILP baselines run on fixtures.
- Grid search clearly marked as offline upper bound.

### Gate 5: PPO and RL baselines

- PPO, SAC, TD3, and behavioral cloning train and evaluate on fixture data.
- PPO meets smoke-test performance threshold.
- Training outputs are reproducible under seed.

### Gate 6: LLM benchmark

- Mock LLM CI tests pass.
- At least one local or API model runs on sample tasks.
- Hallucination, validity, cost, and MAE metrics are reported.

### Gate 7: Integrated DRL+LLM

- `drl_only`, `llm_only`, and `drl_llm` modes run on the same evaluation set.
- Invalid LLM outputs trigger fallback.
- Added cost and latency are included in net profit.

### Gate 8: Objective 1 report

- Five-seed evaluation complete.
- Metrics, statistical tests, figures, and failure analysis are generated.
- Negative results are documented.

### Gate 9: Objective 2

- Adversarial multi-agent environment runs with N in {2, 4, 8}.
- Priority gas auction and front-running tests pass.
- Profit degradation and equilibrium proxy metrics reported.

### Gate 10: Objective 3

- Coalition environment runs.
- Profit-sharing and swap-splitting tests pass.
- Cooperation-beneficial regimes are identified or negative result documented.

## 20. Implementation Milestones

### Milestone 1: Project bootstrap

- Create package skeleton.
- Add configs, tests, linters, CI.
- Add small fixture dataset.

### Milestone 2: Domain and environment core

- Implement domain models.
- Implement CPMM and constraints.
- Implement single-agent environment.

### Milestone 3: Data benchmark

- Implement adapters.
- Build synchronization pipeline.
- Generate processed dataset and metadata.

### Milestone 4: Baselines and PPO

- Implement baselines.
- Implement PPO training and evaluation.
- Reproduce preliminary speed-profit frontier on available data.

### Milestone 5: LLM benchmark

- Implement prompt templates and schemas.
- Implement validation layer.
- Benchmark models and select planner.

### Milestone 6: Integrated agent

- Implement DRL+LLM agent.
- Compare against DRL-only and LLM-only.
- Document hallucination and cost results.

### Milestone 7: Adversarial extension

- Implement repeated game.
- Calibrate stochastic adversaries.
- Evaluate front-running and PGA effects.

### Milestone 8: Coalition extension

- Implement cooperation protocols.
- Evaluate coalition stability and market regimes.

## 21. Security, Compliance, and Research Boundaries

- No secrets in source control.
- No private keys or mnemonic phrases in configs or tests.
- Read-only blockchain RPC by default.
- Mainnet transaction submission is out of scope.
- The system can simulate MEV strategies for measurement and research, but must not become a turnkey harmful trading bot.
- All outputs must clearly distinguish simulated profit from realized on-chain profit.
- Dataset licenses and API terms must be checked before public release.

## 22. Minimum Dependencies

Recommended stack:

- Python 3.11+
- NumPy, pandas, pyarrow
- pydantic
- web3.py or eth libraries for Ethereum data decoding
- Gymnasium
- Stable-Baselines3
- PyTorch
- PettingZoo and/or Ray RLlib for multi-agent extensions
- scipy and statsmodels for statistical tests
- cvxpy for convex fixed-path baseline
- scipy.optimize or python-mip / pulp / OR-Tools for MILP experiments
- pytest, ruff, mypy
- DVC or W&B Artifacts for large dataset and model tracking

Pin versions in `pyproject.toml` or lock files once implementation starts.

## 23. Documentation Deliverables

- `README.md`: user quickstart and overview.
- `PROJECT_SPEC.md`: this technical specification.
- `AGENTS.md`: coding-agent instructions.
- `docs/design/architecture.md`: diagrams and implementation rationale.
- `docs/experiments/objective1.md`: single-agent protocol and results.
- `docs/experiments/llm_benchmark.md`: LLM benchmark protocol and results.
- `docs/experiments/objective2_adversarial.md`: adversarial game results.
- `docs/experiments/objective3_coalitions.md`: coalition results.
- `docs/negative_results/`: documented failures and limitations.

## 24. Definition of Done

The project is complete when:

1. Objective 1 can be reproduced from raw or fixture data to final report with a single documented command.
2. PPO is compared against all required baselines under the same constraints.
3. LLM benchmark produces validity, hallucination, cost, latency, and MAE metrics.
4. Integrated DRL+LLM is compared against DRL-only and LLM-only.
5. Failure analysis and negative results are present.
6. Objective 2 and Objective 3 experiments are implemented or explicitly deferred with documented rationale.
7. The repository can be installed, tested, and evaluated by a new researcher without hidden state.
