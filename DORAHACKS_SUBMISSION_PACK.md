# 📋 DoraHacks BUIDL Submission Pack

Use these pre-formatted fields when submitting your BUIDL on DoraHacks:
**Hackathon:** [Somnia × DreamDEX Event Contracts Hackathon](https://dorahacks.io/hackathon/event-contracts)  
**Submission URL:** [https://dorahacks.io/hackathon/event-contracts/buidl](https://dorahacks.io/hackathon/event-contracts/buidl)  

---

### 1. Project Overview
- **Project Name:** `DreamDEX Event Sentinel`
- **Tagline:** `Autonomous Zero-Cost AI Trading Agent & Market Maker for DreamDEX Event Contracts`
- **Category / Track:** `AI-Powered Trading Agents, Prediction Markets & Analytics`
- **GitHub Repository:** `https://github.com/MathieuDWeill/dreamdex-event-sentinel`
- **Demo Video:** `[Paste your Loom / YouTube link here or link to repository]`
- **Official Website / Demo:** `https://github.com/MathieuDWeill/dreamdex-event-sentinel#quickstart`

---

### 2. Project Description (Markdown)
```markdown
# ⚡ DreamDEX Event Sentinel

### What is DreamDEX Event Sentinel?
**DreamDEX Event Sentinel** is an autonomous trading agent and automated market maker (AMM) purpose-built for **DreamDEX Event Contracts on Somnia Network**.

While most modern AI trading bots require expensive cloud LLM APIs ($0.03/query) that drain prediction market liquidity, Event Sentinel is **100% free and open-source, running locally with zero operating costs**.

### Key Features
1. **Zero-Cost Bayesian Event Oracle**: Incurs zero API costs by evaluating event probabilities via deterministic Bayesian updating and local sentiment signals.
2. **Binary Contract Fair Pricer**: Calculates fair pricing for YES/NO tokens and captures risk-free parity arbitrage (`Ask_YES + Ask_NO < $1.00`).
3. **Fractional Kelly Risk Management**: Prevents catastrophic loss by computing optimal bet sizes based on mathematical edge.
4. **Autonomous AMM Liquidity Provider**: Quotes continuous two-sided liquidity around fair value on DreamDEX testnet.
5. **Interactive CLI & Benchmark Suite**: Includes complete simulation, pricing, and status verification tools.

### How it is built:
- Language: Python 3.10+
- Architecture: Modular zero-dependency engine (`oracle.py`, `pricing.py`, `risk.py`, `agent.py`, `cli.py`)
- Test Coverage: 100% passing pytest suite validating mathematical parity and trade settlement.
- Packaging: Standard PEP 517/621 with candidate bundle in `dist/`.

### What's next for DreamDEX Event Sentinel?
- Mainnet deployment on Somnia Network upon DreamDEX public launch.
- Integration of Somnia multi-stream high-throughput event feeds.
- Community SDK for third-party automated market makers.
```

---

### 3. Team & Contact
- **Leader:** Mathieu Weill (`MathieuDWeill`)
- **Contact:** Via GitHub profile
