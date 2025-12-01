import yfinance as yf

def fetch_ohlcv(symbol: str, source="NSE"):
    ticker = symbol + ".NS" if source == "NSE" else symbol + ".BO"
    data = yf.download(ticker, period="3mo", interval="1d")

    return data.reset_index().to_dict(orient="records")
