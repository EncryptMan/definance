from typing import Callable

from .utils import fetch_api_data, clean_symbol
from .exceptions import SymbolNotFound
from .url import *
from .symbols import get_binance_pairs, get_bitget_pairs, get_okx_pairs, get_binance_coins, get_bitget_coins, get_okx_coins
from .symbols import find_pair_with_base_coin, search_symbol
from .classes import PriceData, Exchange


def fetch_binance_price_data(symbol: str) -> PriceData:
    '''
    Fetch the price data of a cryptocurrency from Binance exchange
    
    Args:
    - symbol (str): The symbol of the cryptocurrency. Example: 'BTC/USDT', 'ETH/BTC', 'BTC'.

    Returns:
    - PriceData: The price data of the cryptocurrency
    '''

    symbol = clean_symbol(symbol)

    api_links = generate_api_links_from_symbol(
        symbol=symbol, 
        coins=get_binance_coins(), 
        pairs=get_binance_pairs(), 
        api_function=get_binance_price_api_url
    )


    for api_url in api_links:
        price_data = fetch_api_data(api_url)

        if price_data is None:
            continue

        return PriceData(
            symbol=price_data['symbol'],
            current_price=price_data['lastPrice'],
            volume=price_data['volume'],
            high_price=price_data['highPrice'],
            low_price=price_data['lowPrice'],
            change=price_data['priceChangePercent'],
            api_url=api_url,
            exchange=Exchange.BINANCE
        ) 

    raise SymbolNotFound(f'Symbol {symbol} not found in Binance exchange')


def fetch_bitget_price_data(symbol: str) -> PriceData:
    '''
    Fetch the price data of a cryptocurrency from Bitget exchange

    Args:
    - symbol (str): The symbol of the cryptocurrency. Example: 'BTC/USDT', 'ETH/BTC', 'BTC'.
    
    Returns:
    - PriceData: The price data of the cryptocurrency
    '''

    symbol = clean_symbol(symbol)

    symbol = symbol.upper()
    api_links = generate_api_links_from_symbol(
        symbol=symbol, 
        coins=get_bitget_coins(), 
        pairs=get_bitget_pairs(), 
        api_function=get_bitget_price_api_url
    )

    for api_url in api_links:
        price_data = fetch_api_data(api_url)

        if price_data is None:
            continue

        price_data = price_data['data'][0]

        # Bitget provide 24h change between 0 and 1, so we multiply it by 100 to get percentage
        change = float(price_data['change24h']) * 100

        return PriceData(
            symbol=price_data['symbol'],
            current_price=price_data['lastPr'],
            volume=price_data['baseVolume'],
            high_price=price_data['high24h'],
            low_price=price_data['low24h'],
            change=change,
            api_url=api_url,
            exchange=Exchange.BITGET
        )

    raise SymbolNotFound(f'Symbol {symbol} not found in Bitget exchange')


def fetch_okx_price_data(symbol: str) -> PriceData:
    '''
    Fetch the price data of a cryptocurrency from OKX exchange
    
    Args:
    - symbol (str): The symbol of the cryptocurrency. Example: 'BTC/USDT', 'ETH/BTC', 'BTC'.

    Returns:
    - PriceData: The price data of the cryptocurrency
    '''
    
    symbol = clean_symbol(symbol)

    api_links = generate_api_links_from_symbol(
        symbol=symbol, 
        coins=get_okx_coins(), 
        pairs=get_okx_pairs(), 
        api_function=get_okx_price_api_url
    )

    for api_url in api_links:
        price_data = fetch_api_data(api_url)
        if len(price_data['data']) != 0:

            price_data = price_data['data'][0]

            # OKX doesn't provide 24h change, so we calculate it
            change = ((float(price_data['last']) / float(price_data['sodUtc0'])) * 100 - 100)
    
            return PriceData(
                symbol=price_data['instId'],
                current_price=price_data['last'],
                volume=price_data['vol24h'],
                high_price=price_data['high24h'],
                low_price=price_data['low24h'],
                change=change, 
                api_url=api_url,
                exchange=Exchange.OKX
            )

    raise SymbolNotFound(f'Symbol {symbol} not found in OKX exchange')
   

def generate_api_links_from_symbol(*, symbol: str, coins: list[str], pairs: list[str], api_function: Callable) -> list[str]:
    
    api_links = []

    # We need to take into account many combinations of symbols
    # Possible inputs: BTC, BTC/USDT, BTCUSDT

    # First try to find exact match for case like BTC
    if not '/' in symbol and symbol in coins:
        matching_pair = find_pair_with_base_coin(symbol, pairs)
        if matching_pair:
            api_links.append(api_function(matching_pair))

    # Then try to find exact match for case like BTC/USDT or BTCUSDT
    matching_pair = search_symbol(symbol, pairs) # This function will ignore the / in symbol
    if matching_pair:
        api_links.append(api_function(matching_pair))

    # If no match then it means either the symbol is not cached or symbol is incorrect, still try it
    if len(api_links) == 0:
        api_links.append(api_function(symbol))
        api_links.append(api_function(symbol + '/USDT'))

    return api_links
