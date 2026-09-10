"""Zero-cost local event probability inference engine.
Uses deterministic Bayesian inference and semantic signals without requiring paid third-party APIs.
"""
from __future__ import annotations
import math
import re
from dataclasses import dataclass, field
from typing import Any

@dataclass
class SentimentSignal:
    source: str
    text: str
    weight: float
    polarity: float  # -1.0 (strongly NO) to +1.0 (strongly YES)
    confidence: float  # 0.0 to 1.0

@dataclass
class ProbabilityEstimate:
    event_id: str
    question: str
    prior_probability: float
    posterior_probability: float
    confidence_score: float
    signals_count: int
    summary: str

class EventOracle:
    """Decentralized, zero-cost Bayesian event probability estimation."""

    POSITIVE_CUES = {
        "likely": 0.4, "probable": 0.5, "confirmed": 0.9, "approved": 0.8,
        "passed": 0.85, "success": 0.7, "win": 0.7, "rise": 0.5, "bullish": 0.6,
        "yes": 0.8, "guaranteed": 0.95, "certain": 0.9, "high chance": 0.75,
        "completed": 0.9, "delivered": 0.8, "exceed": 0.6, "support": 0.4
    }

    NEGATIVE_CUES = {
        "unlikely": -0.5, "improbable": -0.6, "rejected": -0.85, "denied": -0.8,
        "failed": -0.9, "loss": -0.7, "drop": -0.5, "bearish": -0.6,
        "no": -0.8, "impossible": -0.95, "canceled": -0.9, "cancelled": -0.9,
        "delayed": -0.4, "doubt": -0.4, "fall": -0.5, "opposition": -0.4
    }

    def __init__(self, default_prior: float = 0.50):
        self.default_prior = default_prior
        self.evidence_history: dict[str, list[SentimentSignal]] = {}

    def extract_sentiment(self, text: str, source: str = "local_feed", weight: float = 1.0) -> SentimentSignal:
        clean = text.lower()
        pos_score = 0.0
        neg_score = 0.0
        matched_tokens = 0

        for cue, val in self.POSITIVE_CUES.items():
            if cue in clean:
                pos_score += val
                matched_tokens += 1

        for cue, val in self.NEGATIVE_CUES.items():
            if cue in clean:
                neg_score += abs(val)
                matched_tokens += 1

        total = pos_score + neg_score
        if total == 0:
            polarity = 0.0
            confidence = 0.2
        else:
            polarity = (pos_score - neg_score) / total
            confidence = min(0.95, 0.3 + (matched_tokens * 0.15))

        return SentimentSignal(
            source=source,
            text=text,
            weight=weight,
            polarity=max(-1.0, min(1.0, polarity)),
            confidence=confidence,
        )

    def add_evidence(self, event_id: str, signal: SentimentSignal) -> None:
        if event_id not in self.evidence_history:
            self.evidence_history[event_id] = []
        self.evidence_history[event_id].append(signal)

    def evaluate_event(self, event_id: str, question: str, prior: float | None = None) -> ProbabilityEstimate:
        p0 = prior if prior is not None else self.default_prior
        p0 = max(0.01, min(0.99, p0))

        signals = self.evidence_history.get(event_id, [])
        if not signals:
            return ProbabilityEstimate(
                event_id=event_id,
                question=question,
                prior_probability=p0,
                posterior_probability=p0,
                confidence_score=0.25,
                signals_count=0,
                summary="No external signals yet; using neutral prior.",
            )

        # Bayesian Odds Update: Odds_new = Odds_prior * Likelihood_Ratio
        prior_odds = p0 / (1.0 - p0)
        total_weight = 0.0
        weighted_polarity = 0.0

        for s in signals:
            # Shift polarity [-1, 1] into a Bayes factor (likelihood ratio) [0.1, 10.0]
            eff_weight = s.weight * s.confidence
            total_weight += eff_weight
            weighted_polarity += s.polarity * eff_weight

        avg_polarity = weighted_polarity / total_weight if total_weight > 0 else 0.0
        # Likelihood ratio: exp(avg_polarity * 2.0)
        lr = math.exp(avg_polarity * 2.2)
        posterior_odds = prior_odds * lr
        p_post = posterior_odds / (1.0 + posterior_odds)
        p_post = max(0.02, min(0.98, p_post))

        conf = min(0.95, 0.35 + (0.15 * math.log1p(len(signals))) + (0.35 * abs(avg_polarity)))

        summary = f"Bayesian update over {len(signals)} signals: P(YES) = {p_post:.3f} (prior: {p0:.2f})"
        return ProbabilityEstimate(
            event_id=event_id,
            question=question,
            prior_probability=p0,
            posterior_probability=round(p_post, 4),
            confidence_score=round(conf, 3),
            signals_count=len(signals),
            summary=summary,
        )
