from collections import defaultdict
from typing import Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.signal_provider import get_free_signal, get_paid_signal
from backend.trading_engine import TradeRequest, place_trade

app = FastAPI()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

users: dict[str, dict] = {
    ADMIN_USERNAME: {
        "full_name": "System Admin",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
        "role": "ADMIN",
    }
}
current_user: Optional[str] = None
broker_setup: dict = {}
signal_config: dict = {"mode": "FREE", "provider": "demo-free", "api_key": "", "notes": "Free signal feed is enabled by default."}
portfolio_records: dict[str, list[dict]] = defaultdict(list)


class UserCreateRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=80)
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6, max_length=100)
    role: Literal["ADMIN", "USER"] = "USER"


class UserLoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=6, max_length=100)


class BrokerSetupRequest(BaseModel):
    broker_name: str = Field(min_length=2, max_length=50)
    api_key: str = Field(min_length=6, max_length=200)
    api_secret: str = Field(min_length=6, max_length=200)
    demat_account: str = Field(min_length=6, max_length=30)
    account_number: str = Field(min_length=6, max_length=30)


class ApprovalRequest(BaseModel):
    approved: bool = False
    approval_code: str = ""


class SignalConfigRequest(BaseModel):
    mode: Literal["FREE", "PAID"] = "FREE"
    provider: str = ""
    api_key: str = ""
    notes: str = ""


class TradeRecordRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    fund_name: str = Field(min_length=1, max_length=80)
    side: Literal["BUY", "SELL"]
    quantity: int = Field(gt=0, le=100000)
    entry_price: float = Field(gt=0)
    exit_price: float | None = None
    status: Literal["OPEN", "CLOSED"] = "CLOSED"
    notes: str = ""


@app.get("/")
def home():
    return {
        "message": "HRI AutoTrader backend running",
        "mode": "PAPER",
        "live_trading_enabled": False,
        "user_registered": len(users) > 0,
        "broker_connected": bool(broker_setup),
        "admin_default": {"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
    }


@app.get("/status")
def status():
    return {
        "mode": "PAPER",
        "live_trading_enabled": False,
        "approval_required": True,
        "logged_in_user": current_user,
        "user_count": len(users),
        "broker_connected": bool(broker_setup),
        "broker_name": broker_setup.get("broker_name"),
    }


def get_current_user_record():
    if not current_user:
        raise HTTPException(status_code=401, detail="Login required")
    user = users.get(current_user)
    if not user:
        raise HTTPException(status_code=401, detail="User session is invalid")
    return user


def require_admin():
    user = get_current_user_record()
    if user.get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@app.post("/login")
def login_user(payload: UserLoginRequest):
    user = users.get(payload.username.strip())
    if not user or user["password"] != payload.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    global current_user
    current_user = user["username"]
    return {"status": "LOGGED_IN", "username": current_user, "role": user["role"]}


@app.post("/admin/login")
def admin_login(payload: UserLoginRequest):
    if payload.username.strip() != ADMIN_USERNAME or payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    global current_user
    current_user = ADMIN_USERNAME
    return {"status": "ADMIN_LOGGED_IN", "username": current_user, "role": "ADMIN"}


@app.post("/users/register")
def register_user(payload: UserCreateRequest):
    username = payload.username.strip()
    if username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    if payload.role == "ADMIN" and not current_user:
        raise HTTPException(status_code=403, detail="Admin login required to create an admin user")
    if payload.role == "ADMIN" and users.get(current_user, {}).get("role") != "ADMIN":
        raise HTTPException(status_code=403, detail="Only admin can create another admin")

    users[username] = {
        "full_name": payload.full_name.strip(),
        "username": username,
        "password": payload.password,
        "role": payload.role,
    }
    return {"status": "USER_CREATED", "username": username, "role": payload.role, "full_name": payload.full_name.strip()}


@app.get("/users")
def list_users():
    require_admin()
    return {"users": [
        {"username": item["username"], "full_name": item["full_name"], "role": item["role"]}
        for item in users.values()
    ]}


@app.get("/users/me")
def current_user_profile():
    user = get_current_user_record()
    return {"username": user["username"], "full_name": user["full_name"], "role": user["role"]}


@app.post("/broker/connect")
def connect_broker(payload: BrokerSetupRequest):
    if not current_user:
        raise HTTPException(status_code=401, detail="Login required before connecting a Demat account")

    broker_setup.update({
        "broker_name": payload.broker_name.strip(),
        "api_key": payload.api_key,
        "api_secret": payload.api_secret,
        "demat_account": payload.demat_account.strip(),
        "account_number": payload.account_number.strip(),
        "owner": current_user,
        "connected": True,
        "live_trading_enabled": False,
    })
    return {"status": "BROKER_CONNECTED", "broker_name": payload.broker_name.strip()}


@app.post("/live-trading/approve")
def approve_live_trading(payload: ApprovalRequest):
    if not current_user:
        raise HTTPException(status_code=401, detail="Login required before enabling live trading")
    if not broker_setup:
        raise HTTPException(status_code=400, detail="Connect a Demat account before enabling live trading")
    if not payload.approved:
        broker_setup["live_trading_enabled"] = False
        return {"status": "LIVE_TRADING_DISABLED", "message": "Live trading remains disabled until approval is granted"}
    if payload.approval_code != "ENABLE-LIVE-TRADING":
        raise HTTPException(status_code=400, detail="Incorrect approval code")

    broker_setup["live_trading_enabled"] = True
    return {
        "status": "LIVE_TRADING_ENABLED",
        "message": "Live trading is enabled only after explicit approval.",
        "broker_name": broker_setup.get("broker_name"),
        "owner": current_user,
    }


@app.get("/signals/status")
def get_signal_status():
    return {
        "mode": signal_config["mode"],
        "provider": signal_config["provider"],
        "notes": signal_config["notes"],
        "paid_api_configured": bool(signal_config.get("api_key")),
    }


@app.post("/signals/config")
def configure_signal(payload: SignalConfigRequest):
    mode = payload.mode.upper()
    if mode == "PAID" and not payload.api_key:
        raise HTTPException(status_code=400, detail="Paid signal mode requires an API key or provider token")

    signal_config["mode"] = mode
    signal_config["provider"] = payload.provider or ("demo-paid" if mode == "PAID" else "demo-free")
    signal_config["api_key"] = payload.api_key
    signal_config["notes"] = payload.notes or (
        "Using free demo signal feed. No live execution is activated.",
        "Using paid signal provider. Live trading remains gated by manual approval.",
    )[0 if mode == "FREE" else 1]
    return {
        "status": "SIGNAL_CONFIG_UPDATED",
        "mode": signal_config["mode"],
        "provider": signal_config["provider"],
        "notes": signal_config["notes"],
    }


@app.get("/signals/free/{symbol}")
def free_signal(symbol: str):
    return get_free_signal(symbol)


@app.get("/signals/paid/{symbol}")
def paid_signal(symbol: str, provider: str = "", api_key: str = ""):
    if not api_key:
        raise HTTPException(status_code=400, detail="Paid signal mode requires an API key or provider token")
    return get_paid_signal(symbol, provider or signal_config.get("provider") or "Paid signal provider", api_key)


@app.post("/users/{username}/trade")
def add_trade_for_user(username: str, payload: TradeRecordRequest):
    current = get_current_user_record()
    if current["role"] != "ADMIN" and current["username"] != username:
        raise HTTPException(status_code=403, detail="You can only update your own portfolio")
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    pnl = 0.0
    if payload.exit_price is not None:
        if payload.side == "BUY":
            pnl = payload.quantity * (payload.exit_price - payload.entry_price)
        else:
            pnl = payload.quantity * (payload.entry_price - payload.exit_price)
    record = {
        "symbol": payload.symbol.strip().upper(),
        "fund_name": payload.fund_name.strip(),
        "side": payload.side,
        "quantity": payload.quantity,
        "entry_price": float(payload.entry_price),
        "exit_price": float(payload.exit_price) if payload.exit_price is not None else None,
        "status": payload.status,
        "notes": payload.notes,
        "pnl": round(float(pnl), 2),
    }
    portfolio_records[username].append(record)
    return {"status": "TRADE_ADDED", "user": username, "record": record}


@app.get("/reports/portfolio")
def portfolio_report(username: str | None = None):
    current = get_current_user_record()
    if username is None:
        target_user = current["username"]
    elif current["role"] != "ADMIN" and current["username"] != username:
        raise HTTPException(status_code=403, detail="You can only view your own report")
    else:
        target_user = username

    records = portfolio_records.get(target_user, [])
    total_invested = round(sum(record["quantity"] * record["entry_price"] for record in records), 2)
    total_profit = round(sum(record["pnl"] for record in records if record["status"] == "CLOSED"), 2)
    fund_breakdown = defaultdict(float)
    for record in records:
        fund_breakdown[record["fund_name"]] += record["pnl"]

    return {
        "username": target_user,
        "role": users[target_user]["role"],
        "total_invested": total_invested,
        "total_profit_loss": total_profit,
        "trade_count": len(records),
        "open_positions": [record for record in records if record["status"] == "OPEN"],
        "closed_positions": [record for record in records if record["status"] == "CLOSED"],
        "fund_breakdown": {key: round(value, 2) for key, value in sorted(fund_breakdown.items())},
        "records": records,
    }


@app.get("/reports/summary")
def admin_report_summary():
    require_admin()
    report = []
    all_profit = 0.0
    all_invested = 0.0
    all_funds = defaultdict(float)

    for username, user in users.items():
        records = portfolio_records.get(username, [])
        invested = sum(record["quantity"] * record["entry_price"] for record in records)
        profit = sum(record["pnl"] for record in records if record["status"] == "CLOSED")
        all_invested += invested
        all_profit += profit
        for record in records:
            all_funds[record["fund_name"]] += record["pnl"]
        report.append({
            "username": username,
            "role": user["role"],
            "total_invested": round(invested, 2),
            "profit_loss": round(profit, 2),
        })

    return {
        "total_users": len(users),
        "total_invested": round(all_invested, 2),
        "total_profit_loss": round(all_profit, 2),
        "fund_breakdown": {key: round(value, 2) for key, value in sorted(all_funds.items())},
        "users": report,
    }


@app.post("/trade")
def trade(request: TradeRequest):
    return place_trade(request)
