# DeFinance

DeFinance is a Python library designed to abstract the APIs of various cryptocurrency exchanges and fetch cryptocurrency market data. Currently, it supports spot prices in Binance, Bitget, and OKX exchanges. This library simplifies the process of retrieving cryptocurrency price data by providing a unified interface.

## Features

- Fetch spot price data from Binance, Bitget, and OKX.
- Unified interface to handle data retrieval from multiple exchanges.
- Automatic fallback mechanism to fetch data from other exchanges if the symbol is not found in one of the exchange.

## Installation

To install DeFinance, you can use pip:

```bash
pip install definance
```

## Usage

Here's a quick example of how to use DeFinance to fetch cryptocurrency price data:

### Importing the Library

```python
from definance import fetch_price_data, Exchange
```

### Fetching Price Data from a Specific Exchange

To fetch price data from a specific exchange, you can specify the exchange as an argument:

```python
price_data = fetch_price_data('BTC/USDT', Exchange.BINANCE)
print(price_data)
```

### Fetching Price Data from Any Exchange

If you do not specify an exchange, DeFinance will attempt to fetch the data from all supported exchanges in the following order: Binance, Bitget, and OKX.

```python
price_data = fetch_price_data('BTC/USDT')
print(price_data)
```

### Handling Symbol Not Found

If the symbol is not found in any of the exchanges, an exception will be raised:

```python
from definance.exceptions import SymbolNotFound

try:
    price_data = fetch_price_data('INVALID_SYMBOL')
except SymbolNotFound as e:
    print(e)
```

## API Reference

### `fetch_price_data(symbol: str, exchange: Exchange = None) -> PriceData`

Fetches the cryptocurrency price data from the specified exchange or from all exchanges if none is specified.

#### Arguments

- `symbol` (str): The symbol of the cryptocurrency. Example: 'BTC/USDT', 'ETH/BTC', 'BTC'.
- `exchange` (Exchange, optional): The exchange to fetch the data from. If `None`, the function will try to fetch the data from all exchanges.

#### Returns

- `PriceData`: The price data object containing the fetched price data.

### Supported Exchanges

- `Exchange.BINANCE`
- `Exchange.BITGET`
- `Exchange.OKX`

## Contributing

Contributions are welcome! If you'd like to contribute to DeFinance, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request.

## License

DeFinance is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or inquiries, please contact thymus_bleep.0u@icloud.com.
