# 🎬 DreamDEX Event Sentinel — 2-Minute Demo Video Script

> **Target Duration:** 2 minutes 15 seconds  
> **Platform:** Loom, YouTube, or MP4 upload  
> **Language:** English (standard for DoraHacks international juries)  

---

### [0:00 - 0:30] — Hook & The Problem
* **Visual:** Show DreamDEX event contracts interface or terminal.
* **Speaker:**  
  *"Hello judges! This is Mathieu presenting **DreamDEX Event Sentinel** for the Somnia × DreamDEX Event Contracts Hackathon.*  
  *Prediction markets live and die by liquidity and tight pricing. But right now, building autonomous trading agents requires expensive proprietary LLM APIs costing up to 30 dollars a day. That eats away trading margins.*  
  *We asked: Can we build a 100% autonomous, zero-cost AI market maker that runs locally, quotes tight spreads, and captures arbitrage on DreamDEX Event Contracts without paying a single dollar in API fees? The answer is YES."*

---

### [0:30 - 1:15] — Architecture & Zero-Cost Innovation
* **Visual:** Show the architecture diagram from README.md on GitHub: `https://github.com/MathieuDWeill/dreamdex-event-sentinel`
* **Speaker:**  
  *"Here is our architecture:*  
  *1. **Zero-Cost Bayesian Oracle (`oracle.py`)**: Continuously updates posterior event probabilities using deterministic Bayesian inference and local sentiment analysis. Zero third-party API dependencies.*  
  *2. **Binary Market Pricer (`pricing.py`)**: Computes fair values for YES and NO contracts, quotes two-sided spreads, and detects instant parity mispricings whenever Buy(YES) + Buy(NO) is below one dollar.*  
  *3. **Fractional Kelly Risk Sizer (`risk.py`)**: Sizes positions to compound capital while strictly capping maximum drawdown.*  
  *4. **Autonomous Trading Agent (`agent.py`)**: Operates 24/7 providing two-sided liquidity and executing profitable rebalances on Somnia testnet."*

---

### [1:15 - 1:55] — Live Terminal Demo
* **Visual:** Switch to Terminal and run the commands live.
* **Action 1:** Run tests:
  ```bash
  pytest -v
  ```
* **Speaker:**  
  *"Our entire codebase is battle-tested. Running pytest: all 8 test suites pass in 20 milliseconds, validating pricing parity, risk sizing, and contract settlements."*

* **Action 2:** Run live simulation:
  ```bash
  python3 -m dreamdex_sentinel.cli simulate --ticks 8
  ```
* **Speaker:**  
  *"Now let's launch the autonomous trading agent. Watch it evaluate incoming event ticks, adjust bid/ask spreads, execute both YES and NO orders, and achieve a positive PnL upon settlement."*

---

### [1:55 - 2:15] — Conclusion & Testnet Readiness
* **Visual:** Show GitHub repository and submission receipt.
* **Speaker:**  
  *"DreamDEX Event Sentinel is 100% open-source, fully packaged with CLI and documentation, and ready to deploy on the Somnia Network testnet with test STT tokens.*  
  *Thank you to Somnia and DreamDEX for hosting this challenge! Check out our GitHub repository at `MathieuDWeill/dreamdex-event-sentinel`."*
