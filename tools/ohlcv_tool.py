import requests
import datetime
import time


def nse_get(url):
    """NSE GET request with headers + cookies"""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # get cookies
    time.sleep(0.5)
    resp = session.get(url, headers=headers)
    if resp.status_code != 200:
        return None
    return resp.json()


def fetch_etf_ohlcv(symbol: str):
    """Fetch OHLCV for NSE ETFs using the correct ETF API"""
    url = f"https://www.nseindia.com/api/etf?symbol={symbol}"
    data = nse_get(url)
    if not data or "data" not in data:
        return None

    timestamp = data.get("timestamp", None)
    if not timestamp:
        return None

    ohlcvs = []
    for row in data["data"]:
        try:
            ohlcvs.append({
                "date": timestamp.split()[0],  # YYYY-MM-DD
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["ltP"]),
                "volume": int(row["qty"]),
                "nav": float(row["nav"])
            })
        except Exception:
            continue
    if not ohlcvs:
        return None
    return ohlcvs


def fetch_equity_ohlcv(symbol: str):
    """Fallback for NSE equities using historical API"""
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

    ohlcvs = []
    for row in data["data"]:
        try:
            ohlcvs.append({
                "date": row["CH_TIMESTAMP"],
                "open": float(row["CH_OPENING_PRICE"]),
                "high": float(row["CH_HIGH_PRICE"]),
                "low": float(row["CH_LOW_PRICE"]),
                "close": float(row["CH_CLOSING_PRICE"]),
                "volume": int(row["CH_TOT_TRADED_QTY"]),
            })
        except Exception:
            continue
    if not ohlcvs:
        return None
    return ohlcvs


def fetch_ohlcv(symbol: str):
    """
    Unified entry point: try ETF API first, then fallback to equity
    """
    data = fetch_etf_ohlcv(symbol)
    if data:
        return data

    data = fetch_equity_ohlcv(symbol)
    if data:
        return data

    raise ValueError(f"Failed to fetch OHLCV for symbol {symbol}")
