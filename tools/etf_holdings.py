import requests
import tempfile
import tabula
import pandas as pd

# -------------------------------
# MASTER MAPPING (AMC + Scheme Code)
# -------------------------------
ETF_MAP = {
    "NIFTYBEES": {"amc": "nippon", "code": 103},
    "BANKBEES": {"amc": "nippon", "code": 105},
    "ITBEES": {"amc": "nippon", "code": 106},
    "MIDCAPETF": {"amc": "nippon", "code": 112},
    "SENSEXETF": {"amc": "nippon", "code": 118},

    # Motilal Oswal
    "MOM50": {"amc": "motilal", "code": "MOF50"},
    "MOM100": {"amc": "motilal", "code": "MOF100"},

    # Mirae Asset
    "MAFNIFTY50": {"amc": "mirae", "code": "MAFN50"},

    # ICICI Prudential
    "ICICINIFTYETF": {"amc": "icici", "code": "ICNIFTY"},

    # HDFC
    "HDFCNIFETF": {"amc": "hdfc", "code": "HDN50"},
}

# -------------------------------
# AMC-SPECIFIC FETCHERS
# -------------------------------

def fetch_nippon(code: int):
    """ Fetch holdings from Nippon India ETF JSON API """
    url = f"https://www.nipponindiamf.com/api/v1/etf/holdings/{code}"
    try:
        r = requests.get(url, timeout=5).json()
        holdings = r.get("data", [])
        return [
            {
                "name": h["security_name"],
                "weight": float(h["weightage"]),
                "quantity": h["quantity"]
            }
            for h in holdings
        ]
    except:
        return None


def fetch_motilal(code: str):
    """ Motilal Oswal → Holdings PDF → Tabula Parse """
    url = f"https://www.motilaloswalmf.com/Downloads/ETF/{code}-Holdings.pdf"
    return parse_pdf_holdings(url)


def fetch_mirae(code: str):
    url = f"https://www.miraeassetmf.co.in/downloads/etf-holdings/{code}.pdf"
    return parse_pdf_holdings(url)


def fetch_icici(code: str):
    url = f"https://www.icicipruamc.com/Download/ETF/Holdings/{code}.pdf"
    return parse_pdf_holdings(url)


def fetch_hdfc(code: str):
    url = f"https://www.hdfcfund.com/sites/default/files/etf-holdings/{code}.pdf"
    return parse_pdf_holdings(url)


# -------------------------------
# UNIVERSAL PDF PARSER
# -------------------------------

def parse_pdf_holdings(pdf_url: str):
    """ Download PDF → Extract table → Standardize format """
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            r = requests.get(pdf_url, timeout=10)
            tmp.write(r.content)
            tmp.flush()

            dfs = tabula.read_pdf(tmp.name, pages="all", multiple_tables=True)
            df = next((d for d in dfs if "Name" in d.columns or "Security" in str(d.columns)), None)
            if df is None:
                return None

            # Try to guess columns
            df.columns = [c.strip().lower() for c in df.columns]

            name_col = next((c for c in df.columns if "name" in c or "security" in c), None)
            weight_col = next((c for c in df.columns if "weight" in c), None)

            if name_col is None:
                return None

            holdings = []
            for _, row in df.iterrows():
                holdings.append({
                    "name": str(row[name_col]).strip(),
                    "weight": float(row.get(weight_col, 0)) if weight_col else None
                })

            return holdings

    except:
        return None


# -------------------------------
# MASTER WRAPPER
# -------------------------------

def get_etf_holdings(symbol: str):
    symbol = symbol.upper()

    if symbol not in ETF_MAP:
        return {"error": "ETF not supported"}

    amc = ETF_MAP[symbol]["amc"]
    code = ETF_MAP[symbol]["code"]

    fetcher = {
        "nippon": fetch_nippon,
        "motilal": fetch_motilal,
        "mirae": fetch_mirae,
        "icici": fetch_icici,
        "hdfc": fetch_hdfc,
    }.get(amc)

    print(f"Fetching from: {amc.upper()}…")

    holdings = fetcher(code)
    if holdings:
        return {
            "symbol": symbol,
            "amc": amc,
            "holdings": holdings
        }

    return {
        "symbol": symbol,
        "amc": amc,
        "error": "Unable to fetch holdings",
        "holdings": []
    }

print(get_etf_holdings("MAHKTECH"))
