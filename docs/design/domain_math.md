# Gate 1 Domain Math

- Units: internal token amounts are integer raw units; ETH/wei/gwei and USD conversions use `Decimal`.
- CPMM formula: Uniswap-v2 style integer floor output with fee basis points.
- Reserve semantics: full input amount is added to input reserve; output amount is removed from output reserve.
- Profit accounting: gross gain, gas/LLM/failed costs, conservative C1 margin, realized net profit, ROI.
- Constraints implemented: C1-C6 only for Objective 1.
- C7-C10 remain locked future multi-agent constraints.
- This gate is simulation-only. Live trading, key management, signing, and transaction submission are out of scope.
