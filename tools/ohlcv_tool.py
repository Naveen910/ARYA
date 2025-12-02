import requests
import datetime
import time


# --------------------------
# Helpers
# --------------------------

def safe_float(x):
    try:
        v = float(x)
        # reject NaN / Infinity
        if v != v or v in (float("inf"), float("-inf")):
            return None
        return v
    except:
        return None


def safe_int(x):
    try:
        return int(float(x))
    except:
        return None


def safe_premium(price, nav):
    price = safe_float(price)
    nav = safe_float(nav)
    if price is None or nav is None or nav == 0:
        return None
    return ((price - nav) / nav) * 100


# --------------------------
# NSE GET
# --------------------------
def nse_get(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)

    time.sleep(0.4)
    resp = session.get(url, headers=headers)
    if resp.status_code != 200:
        return None
    return resp.json()


# --------------------------
# ETF OHLCV
# --------------------------
def fetch_etf_ohlcv(symbol: str):
    url = "https://www.nseindia.com/api/etf"
    data = nse_get(url)

    if not data or "data" not in data:
        return None

    timestamp = data.get("timestamp")
    if not timestamp:
        return None

    symbol = symbol.upper()
    results = []

    for row in data["data"]:
        if row.get("symbol", "").upper() != symbol:
            continue

        results.append({
            "date": timestamp,

            # Price Action
            "assets": row.get("assets"),
            "open": safe_float(row.get("open")),
            "high": safe_float(row.get("high")),
            "low": safe_float(row.get("low")),
            "close": safe_float(row.get("ltP")),
            "prevClose": safe_float(row.get("prevClose")),
            "dayChange": safe_float(row.get("chn")),
            "dayPercent": safe_float(row.get("per")),

            # Liquidity
            "volume": safe_int(row.get("qty")),
            "tradeValue": safe_float(row.get("trdVal")),

            # NAV Premium/Discount
            "nav": safe_float(row.get("nav")),
            "premium_discount": safe_premium(
                row.get("ltP"), row.get("nav")
            ),

            # Trend
            "monthChangePercent": safe_float(row.get("perChange30d")),
            "yearChangePercent": safe_float(row.get("perChange365d")),
            "monthPositionChange": safe_float(row.get("mpc")),
            "yearPositionChange": safe_float(row.get("ypc")),

            # 52-week levels
            "wkHigh": safe_float(row.get("wkhi")),
            "wkLow": safe_float(row.get("wklo")),
            "nearWKH": safe_float(row.get("nearWKH")),
            "nearWKL": safe_float(row.get("nearWKL")),

            # Metadata
            "companyName": row.get("meta", {}).get("companyName"),
            "industry": row.get("meta", {}).get("industry"),
        })

    return results if results else None


# --------------------------
# EQUITY OHLCV (fallback)
# --------------------------
def fetch_equity_ohlcv(symbol: str):
    end = datetime.date.today()
    start = end - datetime.timedelta(days=90)

    url = (
        "https://www.nseindia.com/api/historical/secure/"
        f"equity?symbol={symbol}&series=[\"EQ\"]"
        f"&from={start:%d-%m-%Y}&to={end:%d-%m-%Y}"
    )

    data = nse_get(url)
    if not data or "data" not in data:
        return None

    results = []

    for row in data["data"]:
        results.append({
            "date": row.get("date"),

            # Price Action
            "assets": None,
            "open": safe_float(row.get("OPEN_PRICE")),
            "high": safe_float(row.get("HIGH_PRICE")),
            "low": safe_float(row.get("LOW_PRICE")),
            "close": safe_float(row.get("CH_LAST_TRADED_PRICE")),
            "prevClose": safe_float(row.get("PREV_CLOSE")),
            "dayChange": safe_float(row.get("CH_TRADE_PERCENT")),
            "dayPercent": None,

            # Liquidity
            "volume": safe_int(row.get("TOTAL_TRADES")),
            "tradeValue": safe_float(row.get("TOT_TRD_VAL")),

            # NAV Premium/Discount — not applicable for equities
            "nav": None,
            "premium_discount": None,

            # Trend — not present in equity history
            "monthChangePercent": None,
            "yearChangePercent": None,
            "monthPositionChange": None,
            "yearPositionChange": None,

            # 52-week — not present
            "wkHigh": None,
            "wkLow": None,
            "nearWKH": None,
            "nearWKL": None,

            # Metadata
            "companyName": None,
            "industry": None,
        })

    return results if results else None


# --------------------------
# Unified Entry
# --------------------------
def fetch_ohlcv(symbol: str):
    symbol = symbol.upper()

    # Try ETF first
    etf_data = fetch_etf_ohlcv(symbol)
    if etf_data:
        return etf_data

    # Fallback to equity
    eq_data = fetch_equity_ohlcv(symbol)
    if eq_data:
        return eq_data

    raise ValueError(f"Failed to fetch OHLCV for symbol {symbol}")
