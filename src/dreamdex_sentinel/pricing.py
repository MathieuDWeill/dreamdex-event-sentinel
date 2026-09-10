"""Binary event contract pricing and arbitrage detection for DreamDEX."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class ContractQuote:
    contract_id: str
    fair_yes_price: float
    bid_yes: float
    ask_yes: float
    bid_no: float
    ask_no: float
    spread: float
    liquidity_depth: float

@dataclass
class ArbitrageOpportunity:
    contract_id: str
    type: str  # "negative_risk_spread" or "mispricing"
    profit_margin: float
    action: str

class BinaryMarketPricer:
    """Calculates fair value, quotes bid/ask spreads, and detects on-chain arbitrage."""

    def __init__(self, base_spread: float = 0.04):
        self.base_spread = base_spread

    def generate_quote(
        self,
        contract_id: str,
        estimated_prob: float,
        market_liquidity: float = 1000.0,
        uncertainty: float = 0.20,
    ) -> ContractQuote:
        p = max(0.01, min(0.99, estimated_prob))
        # Spread widens with uncertainty and tightens with liquidity
        spread = max(0.01, min(0.12, self.base_spread * (1.0 + uncertainty) * (1000.0 / max(100.0, market_liquidity))))
        half_spread = spread / 2.0

        bid_yes = max(0.01, p - half_spread)
        ask_yes = min(0.99, p + half_spread)
        bid_no = max(0.01, (1.0 - p) - half_spread)
        ask_no = min(0.99, (1.0 - p) + half_spread)

        return ContractQuote(
            contract_id=contract_id,
            fair_yes_price=round(p, 4),
            bid_yes=round(bid_yes, 4),
            ask_yes=round(ask_yes, 4),
            bid_no=round(bid_no, 4),
            ask_no=round(ask_no, 4),
            spread=round(spread, 4),
            liquidity_depth=market_liquidity,
        )

    def check_arbitrage(
        self,
        contract_id: str,
        market_ask_yes: float,
        market_ask_no: float,
        fair_prob: float,
    ) -> Optional[ArbitrageOpportunity]:
        # Condition 1: Direct parity arbitrage: If Buy(YES) + Buy(NO) < 1.00 USD, free money
        sum_cost = market_ask_yes + market_ask_no
        if sum_cost < 0.985:
            profit = 1.00 - sum_cost
            return ArbitrageOpportunity(
                contract_id=contract_id,
                type="parity_mispricing",
                profit_margin=round(profit, 4),
                action=f"Simultaneously BUY YES at {market_ask_yes:.3f} and BUY NO at {market_ask_no:.3f} to lock in {profit*100:.1f}% risk-free payout.",
            )

        # Condition 2: Statistical edge (fair value discount)
        edge_yes = fair_prob - market_ask_yes
        if edge_yes > 0.08:
            return ArbitrageOpportunity(
                contract_id=contract_id,
                type="statistical_edge_yes",
                profit_margin=round(edge_yes, 4),
                action=f"BUY YES at {market_ask_yes:.3f} (Fair value: {fair_prob:.3f}, edge: +{edge_yes*100:.1f}%)",
            )

        edge_no = (1.0 - fair_prob) - market_ask_no
        if edge_no > 0.08:
            return ArbitrageOpportunity(
                contract_id=contract_id,
                type="statistical_edge_no",
                profit_margin=round(edge_no, 4),
                action=f"BUY NO at {market_ask_no:.3f} (Fair value: {1.0-fair_prob:.3f}, edge: +{edge_no*100:.1f}%)",
            )

        return None
