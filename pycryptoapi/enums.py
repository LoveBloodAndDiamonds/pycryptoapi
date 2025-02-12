__all__ = [
    "MarketType",
    "Exchange",
]

from enum import StrEnum
from typing import Tuple


class MarketType(StrEnum):
    """Перечисление типов криптовалютных рынков."""
    FUTURES = "FUTURES"
    SPOT = "SPOT"

    def __add__(self, exchange: "Exchange") -> Tuple["Exchange", "MarketType"]:
        return exchange, self


class Exchange(StrEnum):
    """Перечисление бирж."""
    BINANCE = "BINANCE"
    BYBIT = "BYBIT"
    BITGET = "BITGET"
    OKX = "OKX"
    MEXC = "MEXC"

    def __add__(self, market_type: "MarketType") -> Tuple["Exchange", "MarketType"]:
        return self, market_type


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
