import pytest
from dreamdex_sentinel.risk import KellyPositionSizer, RiskProfile

def test_kelly_position_sizer_positive_edge():
    sizer = KellyPositionSizer(RiskProfile(total_capital=1000.0, fractional_kelly=0.5))
    # Estimated fair prob 0.70 vs market price 0.50 -> 20% edge
    assessment = sizer.calculate_position(fair_prob=0.70, market_price=0.50, side="YES")
    assert assessment.allowed is True
    assert assessment.suggested_size > 0.0
    assert assessment.suggested_size <= 150.0  # Respects 15% cap

def test_kelly_position_sizer_negative_edge():
    sizer = KellyPositionSizer()
    # Fair prob 0.40 vs market price 0.50 -> negative edge
    assessment = sizer.calculate_position(fair_prob=0.40, market_price=0.50, side="YES")
    assert assessment.allowed is False
    assert assessment.suggested_size == 0.0
