# HRI AutoTrader India

HRI AutoTrader is being developed in controlled stages for NSE paper trading. Real-money trading is disabled by design.

## ✨ Features

- **Paper Trading** - Simulated trading with virtual capital
- **Admin & User Management** - Create users, role-based access
- **Investment Tracking** - Log trades/investments per user
- **Profit/Loss Reporting** - View returns by fund and user
- **Signal Configuration** - Choose FREE (Yahoo Finance) or PAID signal providers
- **Safety Gates** - Real-money trading locked until manual approval with specific code
- **Broker Connection Form** - Demat setup (not live by default)

## 🚀 Quick Deploy (Free)

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guide to deploy on **Render.com** (free tier).

### Deploy in 4 Steps:
1. Push code to GitHub
2. Connect GitHub repo to Render
3. Render auto-deploys with live URL
4. Share URL with testers

## 📱 Run Locally

Python 3.11+ is required.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
python -m uvicorn backend.app:app --reload
```

Then open:
- Frontend: `file:///path/to/frontend/index.html` (in browser)
- API: `http://127.0.0.1:8000/docs` (interactive docs)

## Example Paper Order

```json
{
  "symbol": "RELIANCE",
  "side": "BUY",
  "quantity": 100,
  "entry_price": 500,
  "stop_loss": 490,
  "virtual_capital": 100000,
  "risk_per_trade_percent": 0.5,
  "confirmed": true,
  "trading_mode": "PAPER"
}
```

The engine caps quantity at the smallest quantity allowed by requested quantity, virtual capital, and configured per-trade risk. It does not place a broker order.

## Tests

```powershell
python -m pytest
```

Never add broker credentials to source control. Use `.env` for local secrets after a real integration has been designed and reviewed.
