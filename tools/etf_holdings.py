import requests

def get_etf_holdings(symbol: str):
    symbol_map = {
        "NIFTYBEES": "NIFTY 50",
        "BANKBEES": "NIFTY BANK",
        "ITBEES": "NIFTY IT",
        "MIDCAPETF": "NIFTY MIDCAP",
        "SENSEXETF": "SENSEX"
    }

    index_name = symbol_map.get(symbol.upper())
    if not index_name:
        return []

    try:
        url = "https://www.niftyindices.com/Backpage.aspx/getSectoralHeatMap"
        r = requests.get(url, timeout=5).json()
        companies = []

        for item in r["d"]["Data"]:
            if item["IndexName"] == index_name:
                companies.append(item["CompanyName"])

        return companies
    except:
        return []
