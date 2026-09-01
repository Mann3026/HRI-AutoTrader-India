from decimal import Decimal

from fastapi.testclient import TestClient
from backend.app import app
from backend.trading_engine import TradeRequest, place_trade


def make_request(**overrides):
    values = {
        "symbol": "reliance",
        "side": "BUY",
        "quantity": 100,
        "entry_price": Decimal("500"),
        "stop_loss": Decimal("490"),
        "virtual_capital": Decimal("100000"),
        "confirmed": True,
    }
    values.update(overrides)
    return TradeRequest(**values)


def test_trade_requires_confirmation():
    result = place_trade(make_request(confirmed=False))

    assert result["status"] == "REJECTED"
    assert "confirmation" in result["reason"]


def test_buy_quantity_is_limited_by_risk():
    result = place_trade(make_request())

    assert result["status"] == "PAPER_ORDER_ACCEPTED"
    assert result["symbol"] == "RELIANCE"
    assert result["quantity"] == 50


def test_sell_order_uses_above_entry_stop():
    result = place_trade(make_request(side="SELL", entry_price=Decimal("500"), stop_loss=Decimal("510")))

    assert result["status"] == "PAPER_ORDER_ACCEPTED"
    assert result["quantity"] == 50


def test_signal_config_defaults_to_free_mode():
    client = TestClient(app)
    response = client.get('/signals/status')

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "FREE"


def test_paid_signal_mode_requires_api_key():
    client = TestClient(app)
    response = client.post('/signals/config', json={"mode": "PAID", "provider": "paid-provider"})

    assert response.status_code == 400
    payload = response.json()
    assert 'API key' in payload["detail"]


def test_free_signal_endpoint_returns_signal_payload():
    client = TestClient(app)
    response = client.get('/signals/free/reliance')

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "FREE"
    assert payload["provider"] == "Yahoo Finance"
    assert payload["signal"] in {"BUY", "SELL", "HOLD"}