import requests
from typing import Set, List
import logging

from url import get_binance_info_url, get_okx_info_url, get_bitget_info_url


# Example {'BTC', 'ETH', 'BNB'}
binance_coins: Set[str] = set() 
okx_coins: Set[str] = set()
bitget_coins: Set[str] = set()
all_coins: Set[str] = set()

# Example {'BTC/USDT', 'ETH/USDT', 'BNB/USDT'}
binance_pairs: Set[str] = set()
okx_pairs: Set[str] = set()
bitget_pairs: Set[str] = set()
all_pairs: Set[str] = set()


def update_symbols():
    '''    
    This function will update the symbols of Binance, OKX and Bitget exchanges.
    '''
    global all_coins, all_pairs

    update_binance_symbols()
    update_bitget_symbols()
    update_okx_symbols()

    all_coins = binance_coins.union(okx_coins).union(bitget_coins)
    all_pairs = binance_pairs.union(okx_pairs).union(bitget_pairs)


def update_binance_symbols():
    global binance_coins, binance_pairs

    try:
        update_binance_coins: Set[str] = set()
        updated_binance_pairs: Set[str] = set()

        response = requests.get(get_binance_info_url())
        response.raise_for_status()
        data = response.json()

        binance_pairs = data['symbols']

        for pair in binance_pairs:
            base_asset = str(pair['baseAsset']).upper()
            quote_asset = str(pair['quoteAsset']).upper()

            update_binance_coins.add(base_asset)
            updated_binance_pairs.add(f'{base_asset}/{quote_asset}')

        binance_coins = update_binance_coins
        binance_pairs = updated_binance_pairs

    except Exception as error:
        logging.error(f"Failed to update Binance symbols: {error}")


def update_bitget_symbols():
    global bitget_coins, bitget_pairs

    try:
        updated_bitget_coins: Set[str] = set()
        updated_bitget_pairs: Set[str] = set()

        response = requests.get(get_bitget_info_url())
        response.raise_for_status()
        data = response.json()

        bitget_pairs = data['data']

        for pair in bitget_pairs:
            base_coin = str(pair['baseCoin']).upper()
            quote_coin = str(pair['quoteCoin']).upper()

            updated_bitget_coins.add(base_coin)
            updated_bitget_pairs.add(f'{base_coin}/{quote_coin}')

        bitget_coins = updated_bitget_coins
        bitget_pairs = updated_bitget_pairs

    except Exception as error:
        logging.error(f"Failed to update Bitget symbols: {error}")
        

def update_okx_symbols():
    global okx_coins, okx_pairs

    try:
        updated_okx_coins: Set[str] = set()
        updated_okx_pairs: Set[str] = set()

        response = requests.get(get_okx_info_url())
        response.raise_for_status()
        data = response.json()

        for pair in data['data']:
            base_asset = str(pair['baseCcy']).upper()
            quote_asset = str(pair['quoteCcy']).upper()
            
            updated_okx_coins.add(base_asset)
            updated_okx_pairs.add(f'{base_asset}/{quote_asset}')

        okx_coins = updated_okx_coins
        okx_pairs = updated_okx_pairs

    except Exception as error:
        logging.error(f"Failed to update OKX symbols: {error}")


def get_binance_coins() -> List[str]:
    '''
    Return the list of coins available in Binance exchange.

    Returns:
    - List[str]: The list of coins available in Binance exchange.

    Example:
    - get_binance_coins() -> ['BTC', 'ETH', 'BNB']
    '''
    return list(binance_coins)


def get_okx_coins() -> List[str]:
    '''
    Return the list of coins available in OKX exchange.

    Returns:
    - List[str]: The list of coins available in OKX exchange.

    Example:
    - get_okx_coins() -> ['BTC', 'ETH', 'BNB']
    '''
    return list(okx_coins)


def get_bitget_coins() -> List[str]:
    '''
    Return the list of coins available in Bitget exchange.

    Returns:
    - List[str]: The list of coins available in Bitget exchange.

    Example:
    - get_bitget_coins() -> ['BTC', 'ETH', 'BNB']
    '''

    return list(bitget_coins)


def get_binance_pairs() -> List[str]:
    '''
    Return the list of pairs available in Binance exchange.

    Returns:
    - List[str]: The list of pairs available in Binance exchange.

    Example:
    - get_binance_pairs() -> ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    '''

    return list(binance_pairs)


def get_okx_pairs() -> List[str]:
    '''
    Return the list of pairs available in OKX exchange.

    Returns:
    - List[str]: The list of pairs available in OKX exchange.

    Example:
    - get_okx_pairs() -> ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    '''

    return list(okx_pairs)


def get_bitget_pairs() -> List[str]:
    '''
    Return the list of pairs available in Bitget exchange.
    
    Returns:
    - List[str]: The list of pairs available in Bitget exchange.
    
    Example:
    - get_bitget_pairs() -> ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    '''

    return list(bitget_pairs)


def get_all_coins() -> List[str]:
    '''
    Return the list of all coins available in all exchanges.
    
    Returns:
    - List[str]: The list of all coins available in all exchanges.
    
    Example:
    - get_all_coins() -> ['BTC', 'ETH', 'BNB']
    '''

    return list(all_coins)


def get_all_pairs() -> List[str]:
    '''
    Return the list of all pairs available in all exchanges.

    Returns:
    - List[str]: The list of all pairs available in all exchanges.

    Example:
    - get_all_pairs() -> ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    '''
    
    return list(all_pairs)


def find_pair_with_base_coin(base_coin: str, pairs: list[str]) -> str | None:
    # First priotize the USDT pair
    found_symbol = search_symbol(f'{base_coin}/USDT', pairs)

    if found_symbol:
        return found_symbol
    
    # If not found, then try to find the BTC pair
    found_symbol = search_symbol(f'{base_coin}/BTC', pairs)

    if found_symbol:
        return found_symbol
    
    # If not found, then try to find the ETH pair
    found_symbol = search_symbol(f'{base_coin}/ETH', pairs)

    if found_symbol:
        return found_symbol
    
    # If not found, then find any pair
    for symbol in pairs:
        if symbol.split('/')[0] == base_coin:
            return symbol

    return None


def search_symbol(search_symbol: str, symbols: list[str]) -> str | None:
    '''
    Search for a symbol in a list of symbols and return the symbol if found, otherwise return None.
    This function will ignore spaces, dashes, underscores and slashes in the search_symbol.
    '''

    search_symbol = search_symbol.upper().replace(' ', '').replace('-', '').replace('_', '').replace('/', '')
    for symbol in symbols:
        if search_symbol == symbol.replace('/', '').replace('-', '').replace('_', '').replace(' ', '').upper():
            return symbol

    return None
