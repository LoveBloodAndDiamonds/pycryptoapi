__all__ = [
    "MarketType",
    "Exchange",
    "MarketCombo",
]

from enum import StrEnum
from typing import Tuple


class MarketType(StrEnum):
    """Перечисление типов криптовалютных рынков."""
    FUTURES = "FUTURES"
    SPOT = "SPOT"

    def __add__(self, exchange: "Exchange") -> "MarketCombo":
        if not isinstance(exchange, Exchange):
            raise TypeError(f"Cannot add MarketType to {type(exchange)}")
        try:
            return MarketCombo(f"{exchange.name}_{self.name}")
        except Exception as e:
            raise ValueError(f"MarketCombo {exchange.name}_{self.name} is not defined: {e}")


class Exchange(StrEnum):
    """Перечисление бирж."""
    BINANCE = "BINANCE"
    BYBIT = "BYBIT"
    BITGET = "BITGET"
    OKX = "OKX"
    MEXC = "MEXC"

    def __add__(self, market_type: "MarketType") -> "MarketCombo":
        if not isinstance(market_type, MarketType):
            raise TypeError(f"Cannot add Exchange to {type(market_type)}")
        try:
            return MarketCombo(f"{self.name}_{market_type.name}")
        except Exception as e:
            raise ValueError(f"MarketCombo {self.name}_{market_type.name} is not defined: {e}")


class MarketCombo(StrEnum):
    """Комбинации биржи и типа рынка."""
    BINANCE_SPOT = f"{Exchange.BINANCE.value}_{MarketType.SPOT.value}"
    BINANCE_FUTURES = f"{Exchange.BINANCE.value}_{MarketType.FUTURES.value}"
    BYBIT_SPOT = f"{Exchange.BYBIT.value}_{MarketType.SPOT.value}"
    BYBIT_FUTURES = f"{Exchange.BYBIT.value}_{MarketType.FUTURES.value}"
    BITGET_SPOT = f"{Exchange.BITGET.value}_{MarketType.SPOT.value}"
    BITGET_FUTURES = f"{Exchange.BITGET.value}_{MarketType.FUTURES.value}"
    OKX_SPOT = f"{Exchange.OKX.value}_{MarketType.SPOT.value}"
    OKX_FUTURES = f"{Exchange.OKX.value}_{MarketType.FUTURES.value}"
    MEXC_SPOT = f"{Exchange.MEXC.value}_{MarketType.SPOT.value}"
    MEXC_FUTURES = f"{Exchange.MEXC.value}_{MarketType.FUTURES.value}"

    def disassemble(self) -> Tuple[Exchange, MarketType]:
        """Разделяет енам на биржу и рынок."""
        exchange_name, market_name = self.value.split("_")
        try:
            return Exchange(exchange_name), MarketType(market_name)
        except Exception as e:
            raise ValueError(f"MarketCombo {self} can not be disassembled: {e}")

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
