__all__ = [
    "MarketType",
    "Exchange",
]

from enum import StrEnum
from typing import Tuple


class MarketType(StrEnum):
    """Перечисление типов криптовалютных рынков."""
    FUTURES: str = "FUTURES"
    SPOT: str = "SPOT"

    def __add__(self, exchange: "Exchange") -> Tuple["Exchange", "MarketType"]:
        if not isinstance(exchange, Exchange):
            raise TypeError(f"Cannot add MarketType to {type(exchange)}")
        return exchange, self


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
