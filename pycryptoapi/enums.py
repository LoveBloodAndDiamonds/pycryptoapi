__all__ = [
    "MarketType",
    "Exchange",
    "StorageKeys",
]

from enum import StrEnum


class MarketType(StrEnum):
    """Перечисление типов криптовалютных рынков."""
    FUTURES: str = "FUTURES"
    SPOT: str = "SPOT"


class Exchange(StrEnum):
    """Перечисление бирж."""
    BINANCE: str = "BINANCE"
    BYBIT: str = "BYBIT"
    BITGET: str = "BITGET"
    OKX: str = "OKX"
    MEXC: str = "MEXC"
    # BITMEX: str = "BITMEX"
    # BINGX: str = "BINGX"
    # COINBASE: str = "COINBASE"
    # GATEIO: str = "GATEIO"
    # KUCOIN: str = "KUCOIN"
    # DERIBIT: str = "DERIBIT"
    # HUOBI: str = "HUOBI"
    # WHITEBIT: str = "WHITEBIT"
    # KRAKEN: str = "KRAKEN"
    # BITFINEX: str = "BITFINEX"
    # DYDX: str = "DYDX"
    # BINANCE_US: str = "BINANCE_US"
    # POLONIEX: str = "POLONIEX"
    # BITSTAMP: str = "BITSTAMP"


class StorageKeys(StrEnum):
    """Строковые ключи для хранения данных в Redis."""
    CMC_RATING: str = "CMC_RATING"
    TICKERS_24H: str = "TICKERS_24H"
    FUNDING_RATE: str = "FUNDING_RATE"
