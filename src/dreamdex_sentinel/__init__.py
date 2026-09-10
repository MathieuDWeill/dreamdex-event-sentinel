"""DreamDEX Event Sentinel: Autonomous Zero-Cost AI Prediction Market & Event Contract Agent."""

from .oracle import EventOracle, SentimentSignal, ProbabilityEstimate
from .pricing import BinaryMarketPricer, ContractQuote, ArbitrageOpportunity
from .risk import KellyPositionSizer, RiskProfile, RiskAssessment
from .agent import AutonomousTradingAgent, Order, OrderType, OrderSide, AgentState

__version__ = "1.0.0"
__all__ = [
    "EventOracle",
    "SentimentSignal",
    "ProbabilityEstimate",
    "BinaryMarketPricer",
    "ContractQuote",
    "ArbitrageOpportunity",
    "KellyPositionSizer",
    "RiskProfile",
    "RiskAssessment",
    "AutonomousTradingAgent",
    "Order",
    "OrderType",
    "OrderSide",
    "AgentState",
]
