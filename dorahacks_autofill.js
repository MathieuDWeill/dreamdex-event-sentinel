/**
 * DoraHacks BUIDL Auto-Fill Script
 * 
 * Instructions:
 * 1. Open https://dorahacks.io/hackathon/event-contracts/buidl in your browser (logged in).
 * 2. Open Developer Tools (F12 or Ctrl+Shift+I) -> Console tab.
 * 3. Paste this script and hit Enter.
 * 4. All fields will be filled automatically!
 */
(() => {
  const data = {
    name: "DreamDEX Event Sentinel",
    tagline: "Autonomous Zero-Cost AI Trading Agent & Market Maker for DreamDEX Event Contracts",
    github: "https://github.com/MathieuDWeill/dreamdex-event-sentinel",
    description: `# ⚡ DreamDEX Event Sentinel

Autonomous Zero-Cost AI Market Maker & Prediction Agent for DreamDEX Event Contracts on Somnia Network.

### Key Features
- Zero-Cost Bayesian Event Oracle (Zero paid API fees)
- Fair Binary Contract Pricing & Parity Arbitrage Detection
- Fractional Kelly Criterion Risk Management
- Autonomous AMM Liquidity Provider on DreamDEX Testnet
- 100% Tested with Pytest & Verified Live Simulation

GitHub: https://github.com/MathieuDWeill/dreamdex-event-sentinel`
  };

  // Helper to trigger React / Vue change events
  function setInput(selector, val) {
    const el = document.querySelector(selector);
    if (!el) return false;
    el.focus();
    el.value = val;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    return true;
  }

  console.log("🚀 Auto-filling DoraHacks BUIDL form with DreamDEX Event Sentinel...");

  // Try matching common DoraHacks inputs
  const inputs = document.querySelectorAll('input, textarea');
  inputs.forEach(input => {
    const placeholder = (input.placeholder || "").toLowerCase();
    const name = (input.name || "").toLowerCase();
    const id = (input.id || "").toLowerCase();

    if (name.includes('name') || placeholder.includes('project name') || placeholder.includes('buidl name')) {
      input.value = data.name;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (name.includes('tagline') || placeholder.includes('tagline') || placeholder.includes('slogan')) {
      input.value = data.tagline;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (name.includes('github') || placeholder.includes('github') || placeholder.includes('repo')) {
      input.value = data.github;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (input.tagName === 'TEXTAREA' || name.includes('description') || placeholder.includes('description')) {
      input.value = data.description;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }
  });

  alert("✔ Champs pré-remplis automatiquement par NightShift ! Vérifiez et cliquez sur Submit.");
})();
