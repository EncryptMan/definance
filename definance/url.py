# Description: This file contains the URL for the API of different exchanges.

# Binance

def get_binance_info_url() -> str:
    return "https://api.binance.com/api/v3/exchangeInfo?permissions=SPOT"


def get_binance_price_api_url(symbol: str) -> str:
    symbol = symbol.replace('/', '').upper()
    return f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"


# Bitget

def get_bitget_info_url() -> str:
    return "https://api.bitget.com/api/v2/spot/public/symbols"


def get_bitget_price_api_url(symbol: str) -> str:
    symbol = symbol.replace('/', '').upper()
    return f"https://api.bitget.com/api/v2/spot/market/tickers?symbol={symbol}"


# OKX

def get_okx_info_url() -> str:
    return "https://www.okx.com/api/v5/public/instruments?instType=SPOT"

def get_okx_price_api_url(symbol: str) -> str:
    symbol = symbol.replace('/', '-').upper()
    return f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"
