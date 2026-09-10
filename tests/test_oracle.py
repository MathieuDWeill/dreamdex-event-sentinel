import pytest
from dreamdex_sentinel.oracle import EventOracle, SentimentSignal

def test_oracle_neutral_prior():
    oracle = EventOracle(default_prior=0.50)
    est = oracle.evaluate_event("EV-TEST", "Will test pass?")
    assert est.posterior_probability == 0.50
    assert est.signals_count == 0

def test_oracle_positive_update():
    oracle = EventOracle(default_prior=0.50)
    sig = oracle.extract_sentiment("Strongly confirmed and approved by governance team", weight=1.0)
    assert sig.polarity > 0.5
    oracle.add_evidence("EV-GOV", sig)
    est = oracle.evaluate_event("EV-GOV", "Will governance pass?")
    assert est.posterior_probability > 0.65

def test_oracle_negative_update():
    oracle = EventOracle(default_prior=0.50)
    sig = oracle.extract_sentiment("Proposal rejected and canceled by committee", weight=1.0)
    assert sig.polarity < -0.5
    oracle.add_evidence("EV-FAIL", sig)
    est = oracle.evaluate_event("EV-FAIL", "Will proposal pass?")
    assert est.posterior_probability < 0.35
