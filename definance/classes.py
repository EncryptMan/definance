from enum import Enum

class Exchange(Enum):
    '''
    Enum class to represent the exchange
    '''
    OKX = 'OKX'
    BINANCE = 'Binance'
    BITGET = 'Bitget'


class PriceData:
    """
    Class to store the price data of a cryptocurrency
    """

    def __init__(self,
                 symbol: str,
                 current_price: float,
                 volume: float,
                 high_price: float,
                 low_price: float,
                 change: float,
                 api_url: str,
                 exchange: Exchange):
        '''
        Initialize the PriceData object

        Args:
        - symbol (str): The symbol of the cryptocurrency
        - current_price (float): The current price of the cryptocurrency
        - volume (float): The volume of the cryptocurrency
        - high_price (float): The high price of the cryptocurrency
        - low_price (float): The low price of the cryptocurrency
        - change (float): The change of the cryptocurrency
        - api_url (str): The API URL used to fetch the data
        - exchange (Exchange): The exchange of the cryptocurrency

        Returns:
        - None
        
        '''

        # Set the attributes
        self.symbol = str(symbol).upper()
        self.display_symbol = str(symbol).replace(
            '-', '').replace('SWAP', '-P').replace('/', '')
        self.current_price = float(current_price)
        self.volume = float(volume)
        self.high_price = float(high_price)
        self.low_price = float(low_price)
        self.change = float(change)
        self.api_url = str(api_url)
        self.exchange = exchange

        from .utils import format_price, break_full_symbol
        
        self.base_asset, self.quote_asset = break_full_symbol(
            self.symbol, self.exchange)

        # All non-str attributes will also have a str version for display purposes
        self.str_current_price = format_price(self.current_price)
        self.str_volume = '{:,.2f}'.format(self.volume)
        self.str_high_price = format_price(self.high_price)
        self.str_low_price = format_price(self.low_price)
        self.str_change = '{:,.2f}'.format(self.change)

    def __str__(self):
        lines = []
        lines.append(f'Symbol: {self.symbol}')
        lines.append(f'Current Price: {self.str_current_price}')
        lines.append(f'Volume: {self.str_volume}')
        lines.append(f'High Price: {self.str_high_price}')
        lines.append(f'Low Price: {self.str_low_price}')
        lines.append(f'Change: {self.str_change}')
        lines.append(f'API URL: {self.api_url}')
        lines.append(f'Exchange: {self.exchange.value}')
        return '\n'.join(lines)
    
    def __iter__(self):
        yield 'symbol', self.symbol
        yield 'current_price', self.str_current_price
        yield 'volume', self.str_volume
        yield 'high_price', self.str_high_price
        yield 'low_price', self.str_low_price
        yield 'change', self.str_change
        yield 'api_url', self.api_url
        yield 'exchange', self.exchange.value
