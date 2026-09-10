import pytest
from dreamdex_sentinel.pricing import BinaryMarketPricer

def test_binary_market_pricer_spread():
    pricer = BinaryMarketPricer(base_spread=0.04)
    quote = pricer.generate_quote("EV-01", estimated_prob=0.70)
    assert quote.fair_yes_price == 0.70
    assert quote.bid_yes < 0.70
    assert quote.ask_yes > 0.70
    assert quote.bid_no < 0.30
    assert quote.ask_no > 0.30

def test_arbitrage_detection_parity():
    pricer = BinaryMarketPricer()
    # If ask_yes + ask_no = 0.40 + 0.50 = 0.90 < 1.00 USD, free arbitrage!
    arb = pricer.check_arbitrage("EV-ARB", market_ask_yes=0.40, market_ask_no=0.50, fair_prob=0.50)
    assert arb is not None
    assert arb.type == "parity_mispricing"
    assert arb.profit_margin >= 0.10
