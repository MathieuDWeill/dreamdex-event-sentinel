"""Risk management and Kelly-criterion position sizing for prediction markets."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RiskProfile:
    total_capital: float
    max_position_fraction: float = 0.15  # Max 15% per contract
    fractional_kelly: float = 0.50      # Half-Kelly for capital preservation
    min_edge_threshold: float = 0.04    # At least 4% edge required to bet

@dataclass
class RiskAssessment:
    suggested_size: float
    kelly_fraction: float
    edge: float
    allowed: bool
    reason: str

class KellyPositionSizer:
    """Calculates optimal bet sizing via fractional Kelly Criterion."""

    def __init__(self, profile: RiskProfile | None = None):
        self.profile = profile or RiskProfile(total_capital=1000.0)

    def calculate_position(
        self,
        fair_prob: float,
        market_price: float,
        side: str = "YES",
    ) -> RiskAssessment:
        p = fair_prob if side.upper() == "YES" else (1.0 - fair_prob)
        price = max(0.01, min(0.99, market_price))

        # Net decimal odds: b = (Payout - Cost) / Cost = (1.0 - price) / price
        b = (1.0 - price) / price
        q = 1.0 - p

        # Full Kelly fraction: f* = (b*p - q) / b = (p*(b+1) - 1) / b = (p - price) / (1 - price)
        edge = p - price
        if edge < self.profile.min_edge_threshold:
            return RiskAssessment(
                suggested_size=0.0,
                kelly_fraction=0.0,
                edge=round(edge, 4),
                allowed=False,
                reason=f"Insufficient edge ({edge*100:.1f}% < threshold {self.profile.min_edge_threshold*100:.1f}%)",
            )

        full_kelly = edge / (1.0 - price)
        fractional = full_kelly * self.profile.fractional_kelly
        capped_fraction = min(self.profile.max_position_fraction, max(0.0, fractional))
        suggested_capital = round(self.profile.total_capital * capped_fraction, 2)

        return RiskAssessment(
            suggested_size=suggested_capital,
            kelly_fraction=round(capped_fraction, 4),
            edge=round(edge, 4),
            allowed=True,
            reason=f"Optimal Half-Kelly allocation: {capped_fraction*100:.1f}% of capital (${suggested_capital})",
        )
