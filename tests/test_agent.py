import pytest
from dreamdex_sentinel.agent import AutonomousTradingAgent, OrderSide
from dreamdex_sentinel.oracle import EventOracle

def test_agent_execution_and_settlement():
    oracle = EventOracle()
    oracle.add_evidence("EV-100", oracle.extract_sentiment("Breakout confirmed with major partnership", weight=1.5))
    agent = AutonomousTradingAgent(initial_balance=1000.0, oracle=oracle)

    # Tick with cheap YES price
    orders = agent.on_market_tick("EV-100", "Will project launch?", market_ask_yes=0.45, market_ask_no=0.58)
    assert len(orders) >= 1
    assert orders[0].side == OrderSide.BUY_YES

    # Settle
    payout = agent.settle_event("EV-100", outcome="YES")
    assert payout > 0.0
    state = agent.get_state()
    assert state.cash_balance > 1000.0
