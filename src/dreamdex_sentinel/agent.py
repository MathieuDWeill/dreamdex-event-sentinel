"""Autonomous Trading Agent & Market Maker for DreamDEX Event Contracts."""
from __future__ import annotations
import enum
import time
from dataclasses import dataclass, field
from typing import Any
from .oracle import EventOracle
from .pricing import BinaryMarketPricer, ContractQuote
from .risk import KellyPositionSizer, RiskProfile

class OrderType(str, enum.Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"

class OrderSide(str, enum.Enum):
    BUY_YES = "BUY_YES"
    SELL_YES = "SELL_YES"
    BUY_NO = "BUY_NO"
    SELL_NO = "SELL_NO"

@dataclass
class Order:
    id: str
    contract_id: str
    side: OrderSide
    order_type: OrderType
    price: float
    amount: float
    timestamp: float = field(default_factory=time.time)
    status: str = "FILLED"

@dataclass
class AgentState:
    cash_balance: float
    positions: dict[str, dict[str, float]]
    total_trades: int
    pnl: float
    open_orders_count: int

class AutonomousTradingAgent:
    """Self-contained autonomous trading agent and automated market maker (AMM)."""

    def __init__(
        self,
        agent_id: str = "sentinel-01",
        initial_balance: float = 1000.0,
        oracle: EventOracle | None = None,
        pricer: BinaryMarketPricer | None = None,
        risk_sizer: KellyPositionSizer | None = None,
    ):
        self.agent_id = agent_id
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.positions: dict[str, dict[str, float]] = {}  # contract_id -> {"YES": qty, "NO": qty}
        self.orders: list[Order] = []
        self.oracle = oracle or EventOracle()
        self.pricer = pricer or BinaryMarketPricer()
        self.risk_sizer = risk_sizer or KellyPositionSizer(RiskProfile(total_capital=initial_balance))

    def on_market_tick(
        self,
        contract_id: str,
        question: str,
        market_ask_yes: float,
        market_ask_no: float,
    ) -> list[Order]:
        """Process live book updates, evaluate probability, and execute optimal orders."""
        executed: list[Order] = []

        # 1. Oracle inference
        estimate = self.oracle.evaluate_event(contract_id, question)
        fair_p = estimate.posterior_probability

        # 2. Check for parity / mispricing arbitrage
        arb = self.pricer.check_arbitrage(contract_id, market_ask_yes, market_ask_no, fair_p)
        if arb and arb.type == "parity_mispricing":
            size = min(self.balance * 0.15, 150.0)
            if size > 10.0:
                cost_per_pair = market_ask_yes + market_ask_no
                units = size / cost_per_pair
                self._record_trade(contract_id, OrderSide.BUY_YES, market_ask_yes, units)
                self._record_trade(contract_id, OrderSide.BUY_NO, market_ask_no, units)
                return self.orders[-2:]

        # 3. Kelly evaluation on YES
        risk_yes = self.risk_sizer.calculate_position(fair_p, market_ask_yes, side="YES")
        if risk_yes.allowed and risk_yes.suggested_size > 5.0 and self.balance >= risk_yes.suggested_size:
            units = risk_yes.suggested_size / market_ask_yes
            order = self._record_trade(contract_id, OrderSide.BUY_YES, market_ask_yes, units)
            executed.append(order)

        # 4. Kelly evaluation on NO
        risk_no = self.risk_sizer.calculate_position(fair_p, market_ask_no, side="NO")
        if risk_no.allowed and risk_no.suggested_size > 5.0 and self.balance >= risk_no.suggested_size:
            units = risk_no.suggested_size / market_ask_no
            order = self._record_trade(contract_id, OrderSide.BUY_NO, market_ask_no, units)
            executed.append(order)

        return executed

    def provide_liquidity(
        self,
        contract_id: str,
        question: str,
        capital_to_quote: float = 200.0,
    ) -> ContractQuote:
        """Provide continuous two-sided liquidity around fair value (Market Making)."""
        estimate = self.oracle.evaluate_event(contract_id, question)
        quote = self.pricer.generate_quote(
            contract_id,
            estimated_prob=estimate.posterior_probability,
            market_liquidity=capital_to_quote * 5.0,
            uncertainty=(1.0 - estimate.confidence_score),
        )
        return quote

    def settle_event(self, contract_id: str, outcome: str) -> float:
        """Settle contract at outcome ('YES' or 'NO') paying $1.00 per winning share."""
        pos = self.positions.get(contract_id, {"YES": 0.0, "NO": 0.0})
        winning_shares = pos.get(outcome.upper(), 0.0)
        payout = winning_shares * 1.00
        self.balance += payout
        self.positions[contract_id] = {"YES": 0.0, "NO": 0.0}
        return payout

    def _record_trade(self, contract_id: str, side: OrderSide, price: float, amount: float) -> Order:
        cost = price * amount
        self.balance -= cost
        if contract_id not in self.positions:
            self.positions[contract_id] = {"YES": 0.0, "NO": 0.0}

        if side in (OrderSide.BUY_YES, OrderSide.SELL_YES):
            self.positions[contract_id]["YES"] += amount if side == OrderSide.BUY_YES else -amount
        else:
            self.positions[contract_id]["NO"] += amount if side == OrderSide.BUY_NO else -amount

        order = Order(
            id=f"ord_{len(self.orders)+1}",
            contract_id=contract_id,
            side=side,
            order_type=OrderType.MARKET,
            price=price,
            amount=amount,
        )
        self.orders.append(order)
        return order

    def get_state(self) -> AgentState:
        pnl = self.balance - self.initial_balance
        return AgentState(
            cash_balance=round(self.balance, 2),
            positions=self.positions,
            total_trades=len(self.orders),
            pnl=round(pnl, 2),
            open_orders_count=0,
        )
