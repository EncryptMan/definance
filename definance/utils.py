
import requests

from .classes import Exchange
from .symbols import get_binance_pairs, get_bitget_pairs


def fetch_api_data(api_link: str):    
    response = requests.get(api_link)

    if response.status_code >= 400 and response.status_code < 500:
        # Data not found
        return None

    response.raise_for_status()

    # Return data
    return response.json()


def format_price(price: float) -> str:
    price = float(price)
    precision = count_decimal_places(price)
    formatter = '{:,.' + str(precision) + 'f}'
    return formatter.format(price)


def count_decimal_places(number: str) -> int:
    number = str(number)
        
    if "e-" in number:
        return int(number.split("e-")[1]) + len(number.split("e-")[0]) - 1
    elif "." in number:
        return len(number.split(".")[1])
    else:
        return 0


def clean_symbol(symbol: str) -> str:
    return symbol.upper().replace(' ', '').replace('_', '/').replace('-', '/')


def break_full_symbol(symbol: str, exchange: Exchange) -> tuple[str, str]:
    """
    Break the full symbol into base and quote assets

    Args:
    - symbol (str): The full symbol
    - exchange (Exchange): The exchange

    Returns:
    - tuple[str, str]: The base and quote assets

    Example:
    - break_full_symbol('BTCUSDT', Exchange.BINANCE) -> ('BTC', 'USDT')
    """

    if exchange == Exchange.BINANCE:
        pairs = get_binance_pairs()
    elif exchange == Exchange.BITGET:
        pairs = get_bitget_pairs()
    elif exchange == Exchange.OKX:
        return symbol.split('-')[0], symbol.split('-')[1] # OKX uses '-' in all pairs to separate base and quote assets
    else:
        raise ValueError(f'Invalid exchange: {exchange}')
    
    # Try to find exact match
    for pair in pairs:
        if '/' in pair and pair.replace('/', '') == symbol.replace('/', '').replace('-', ''):
            return pair.split('/')[0], pair.split('/')[1]
        
    # If no match then try to match quote assets of other pairs
    for pair in pairs:
        quote_asset = pair.split('/')[1]

        if len(symbol) > len(quote_asset) and symbol[-len(quote_asset):] == quote_asset:
            return symbol[:-len(quote_asset)], quote_asset
        
    # If still no match then try to match base assets of other pairs
    for pair in pairs:
        base_asset = pair.split('/')[0]

        if len(symbol) > len(base_asset) and symbol[:len(base_asset)] == base_asset:
            return base_asset, symbol[len(base_asset):]
        
    # If still no match then slice the symbol in half 😂      
    return symbol[:len(symbol) // 2], symbol[len(symbol) // 2:]
