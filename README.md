# ⚡ DreamDEX Event Sentinel
> **Autonomous Zero-Cost AI Market Maker & Prediction Agent for DreamDEX Event Contracts**  
> **Hackathon:** [Somnia × DreamDEX Event Contracts Hackathon](https://dorahacks.io/hackathon/event-contracts) on DoraHacks  
> **Track:** AI-Powered Trading Agents, Prediction Markets & Analytics  
> **Status:** 100% Free & Open-Source • Zero Paid Cloud API Required • Verified with Pytest  

---

## 💡 Executive Summary
**DreamDEX Event Sentinel** is an autonomous trading agent and automated market maker designed specifically for **DreamDEX Event Contracts on Somnia Network**.

While conventional trading agents rely on expensive centralized LLM APIs ($0.03/call) that erode prediction market margins, **Event Sentinel** runs **100% locally with zero operating costs**:
1. **Zero-Cost Bayesian Event Oracle**: Updates outcome probabilities using local semantic heuristics and news sentiment without paid API keys.
2. **Binary Contract Fair Pricer**: Calculates fair pricing for YES/NO binary tokens and captures risk-free parity mispricings (`Ask_YES + Ask_NO < $1.00`).
3. **Fractional Kelly Risk Sizer**: Dynamically sizes stakes to maximize expected capital growth while strictly capping downside drawdown.
4. **Autonomous AMM & Trading Loop**: Automatically quotes two-sided liquidity and executes order flow on DreamDEX testnet.

---

## 🏛️ Architecture
```
dreamdex-event-sentinel/
├── src/dreamdex_sentinel/
│   ├── __init__.py      # Public exports
│   ├── oracle.py        # Bayesian local inference engine (zero paid API)
│   ├── pricing.py       # Binary contract pricing & arbitrage detector
│   ├── risk.py          # Fractional Kelly criterion risk manager
│   ├── agent.py         # Autonomous trading loop & AMM liquidity provider
│   └── cli.py           # Command-line simulation & pricing tool
├── tests/
│   ├── test_oracle.py   # Bayesian update & sentiment tests
│   ├── test_pricing.py  # Fair quote & parity arbitrage tests
│   ├── test_risk.py     # Kelly sizing & drawdown guard tests
│   └── test_agent.py    # End-to-end execution & settlement tests
├── dist/
│   ├── dreamdex-event-sentinel-submission.zip # Ready-to-submit BUIDL bundle
│   └── submission_metadata.json             # DoraHacks metadata
├── pyproject.toml       # Python packaging specification
└── README.md            # Comprehensive documentation & submission pitch
```

---

## 🚀 Quickstart & Verification

### 1. Run Automated Test Suite
```bash
pytest -v
```
All unit tests validate mathematical pricing parity, Bayesian updating, and trade settlement.

### 2. Run Autonomous Market Simulation
```bash
python3 -m dreamdex_sentinel.cli simulate --ticks 8 --balance 1000
```

### 3. Price an Event Contract
```bash
python3 -m dreamdex_sentinel.cli price "Will Somnia testnet reach 500k transactions before launch?"
```

---

## 🌐 Submission on DoraHacks
1. **DoraHacks Hackathon Link**: [https://dorahacks.io/hackathon/event-contracts](https://dorahacks.io/hackathon/event-contracts)
2. **Project Submission Name**: `DreamDEX Event Sentinel`
3. **Tagline**: `Autonomous Zero-Cost AI Trading Agent & Market Maker for DreamDEX Event Contracts`
4. **Category / Track**: `AI-Powered Trading Agents, Prediction Markets & Analytics`
5. **Candidate Archive**: Pre-packaged under `dist/dreamdex-event-sentinel-submission.zip`
