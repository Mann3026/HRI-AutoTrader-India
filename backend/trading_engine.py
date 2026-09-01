from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TradeRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    side: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0, le=100000)
    entry_price: Decimal = Field(gt=0)
    stop_loss: Decimal = Field(gt=0)
    virtual_capital: Decimal = Field(gt=0)
    risk_per_trade_percent: Decimal = Field(default=Decimal("0.5"), gt=0, le=Decimal("0.5"))
    confirmed: bool = False
    trading_mode: Literal["PAPER"] = "PAPER"

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.strip().upper()


def place_trade(request: TradeRequest) -> dict:
    if not request.confirmed:
        return {"status": "REJECTED", "reason": "Explicit trade confirmation is required"}

    if request.side == "BUY" and request.stop_loss >= request.entry_price:
        return {"status": "REJECTED", "reason": "For a BUY order, stop-loss must be below entry price"}
    if request.side == "SELL" and request.stop_loss <= request.entry_price:
        return {"status": "REJECTED", "reason": "For a SELL order, stop-loss must be above entry price"}

    risk_per_share = abs(request.entry_price - request.stop_loss)
    maximum_risk = request.virtual_capital * request.risk_per_trade_percent / Decimal("100")
    risk_quantity = int(maximum_risk // risk_per_share)
    capital_quantity = int(request.virtual_capital // request.entry_price)
    permitted_quantity = min(request.quantity, risk_quantity, capital_quantity)

    if permitted_quantity < 1:
        return {"status": "REJECTED", "reason": "Order exceeds the configured capital or risk limit"}

    return {
        "status": "PAPER_ORDER_ACCEPTED",
        "mode": request.trading_mode,
        "symbol": request.symbol,
        "side": request.side,
        "quantity": permitted_quantity,
        "entry_price": str(request.entry_price),
        "stop_loss": str(request.stop_loss),
        "maximum_risk": str(risk_per_share * permitted_quantity),
    }