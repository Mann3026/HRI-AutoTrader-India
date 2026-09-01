import json
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


DEFAULT_FREE_PROVIDER = "Yahoo Finance"


def _fetch_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def _normalize_symbol(symbol: str) -> str:
    cleaned = symbol.strip().upper()
    if not cleaned:
        raise ValueError("Symbol cannot be empty")
    if "." in cleaned:
        return cleaned
    return f"{cleaned}.NS"


def get_free_signal(symbol: str) -> dict:
    normalized_symbol = _normalize_symbol(symbol)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(normalized_symbol)}?range=5d&interval=1d"

    try:
        payload = _fetch_json(url)
        result = payload.get("chart", {}).get("result", [{}])[0]
        quote_data = result.get("indicators", {}).get("quote", [{}])[0]
        prices = quote_data.get("close") or []
        valid_prices = [price for price in prices if price is not None]
        if len(valid_prices) < 2:
            return {
                "symbol": normalized_symbol,
                "mode": "FREE",
                "provider": DEFAULT_FREE_PROVIDER,
                "signal": "HOLD",
                "score": 50,
                "price": None,
                "reason": "Not enough market data to generate a signal.",
            }

        current_price = valid_prices[-1]
        previous_price = valid_prices[-2]
        change_pct = ((current_price - previous_price) / previous_price) * 100 if previous_price else 0
        if change_pct > 0.5:
            signal = "BUY"
        elif change_pct < -0.5:
            signal = "SELL"
        else:
            signal = "HOLD"

        score = max(10, min(95, int(50 + change_pct * 20)))
        return {
            "symbol": normalized_symbol,
            "mode": "FREE",
            "provider": DEFAULT_FREE_PROVIDER,
            "signal": signal,
            "score": score,
            "price": round(float(current_price), 2),
            "change_pct": round(change_pct, 2),
            "reason": "Generated from Yahoo Finance free market data.",
        }
    except Exception:
        return {
            "symbol": normalized_symbol,
            "mode": "FREE",
            "provider": DEFAULT_FREE_PROVIDER,
            "signal": "HOLD",
            "score": 50,
            "price": None,
            "reason": "Free signal source is unavailable right now; the app remains in paper mode.",
        }


def get_paid_signal(symbol: str, provider: str, api_key: str | None = None) -> dict:
    normalized_symbol = _normalize_symbol(symbol)
    return {
        "symbol": normalized_symbol,
        "mode": "PAID",
        "provider": provider or "Paid signal provider",
        "signal": "HOLD",
        "score": 50,
        "price": None,
        "api_key_configured": bool(api_key),
        "reason": "Paid signal stream is configured but live trading remains guarded by approval.",
    }
