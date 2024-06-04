from . import exceptions
from .classes import Exchange, PriceData
from .exchange import fetch_binance_price_data, fetch_bitget_price_data, fetch_okx_price_data
from .symbols import update_symbols, get_binance_coins, get_binance_pairs, get_bitget_coins, \
      get_bitget_pairs, get_okx_coins, get_okx_pairs, get_all_coins, get_all_pairs


def fetch_price_data(symbol: str, exchange: Exchange = None) -> PriceData:
    """
    Fetch the cryptocurrency price data from the specified exchange or 

    Args:
    - symbol (str): The symbol of the cryptocurrency. Example: 'BTC/USDT', 'ETH/BTC', 'BTC'.
    - exchange (Exchange): The exchange to fetch the data from. If None, then the function will try to fetch the data from all exchanges.

    Returns:
    - PriceData: The price data

    Example:
    - fetch_price_data('BTC/USDT', Exchange.BINANCE)
    """
    if exchange is None:
        try:
            price_data = fetch_binance_price_data(symbol)
        except exceptions.SymbolNotFound:
            try:
                price_data = fetch_bitget_price_data(symbol)
            except exceptions.SymbolNotFound:
                try:
                    price_data = fetch_okx_price_data(symbol)
                except exceptions.SymbolNotFound:
                    raise exceptions.SymbolNotFound(f"Symbol {symbol} not found in any exchange")
        
        return price_data
    else:
        if exchange == Exchange.BINANCE:
            return fetch_binance_price_data(symbol)
        elif exchange == Exchange.BITGET:
            return fetch_bitget_price_data(symbol)
        elif exchange == Exchange.OKX:
            return fetch_okx_price_data(symbol)

# This cache symbols from different exchanges
update_symbols()
