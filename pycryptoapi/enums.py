__all__ = [
    "MarketType",
    "Exchange",
    "Timeframe"
]

from enum import StrEnum
from typing import Tuple, Dict


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


class Timeframe(StrEnum):
    """Перечисление таймфреймов."""
    MIN_1 = "1m"
    MIN_3 = "3m"
    MIN_5 = "5m"
    MIN_15 = "15m"
    MIN_30 = "30m"

    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"

    DAY_1 = "1d"
    DAY_3 = "3d"

    WEEK_1 = "1w"

    MONTH_1 = "1M"

    @property
    def mapping(self) -> Dict[Exchange, Dict["Timeframe", str]]:
        return {
            Exchange.BINANCE: {
                Timeframe.MIN_1: "1m", Timeframe.MIN_3: "3m", Timeframe.MIN_5: "5m", Timeframe.MIN_15: "15m",
                Timeframe.MIN_30: "30m", Timeframe.HOUR_1: "1h", Timeframe.HOUR_2: "2h", Timeframe.HOUR_4: "4h",
                Timeframe.HOUR_6: "6h", Timeframe.HOUR_8: "8h", Timeframe.HOUR_12: "12h", Timeframe.DAY_1: "1d",
                Timeframe.DAY_3: "3d", Timeframe.WEEK_1: "1w", Timeframe.MONTH_1: "1M"
            },
            Exchange.BITGET: {
                Timeframe.MIN_1: "1m", Timeframe.MIN_5: "5m", Timeframe.MIN_15: "15m", Timeframe.MIN_30: "30m",
                Timeframe.HOUR_1: "1h", Timeframe.HOUR_4: "4h", Timeframe.HOUR_6: "6h", Timeframe.HOUR_12: "12h",
                Timeframe.DAY_1: "1d", Timeframe.DAY_3: "3d", Timeframe.WEEK_1: "1w", Timeframe.MONTH_1: "1M"
            },
            Exchange.BYBIT: {
                Timeframe.MIN_1: "1", Timeframe.MIN_3: "3", Timeframe.MIN_5: "5", Timeframe.MIN_15: "15",
                Timeframe.MIN_30: "30", Timeframe.HOUR_1: "60", Timeframe.HOUR_2: "120", Timeframe.HOUR_4: "240",
                Timeframe.HOUR_6: "360", Timeframe.HOUR_12: "720", Timeframe.DAY_1: "D", Timeframe.WEEK_1: "W",
                Timeframe.MONTH_1: "M"
            },
            Exchange.MEXC: {
                Timeframe.MIN_1: "Min1", Timeframe.MIN_5: "Min5", Timeframe.MIN_15: "Min15", Timeframe.MIN_30: "Min30",
                Timeframe.HOUR_1: "Min60", Timeframe.HOUR_4: "Hour4", Timeframe.HOUR_8: "Hour8",
                Timeframe.DAY_1: "Day1", Timeframe.WEEK_1: "Week1", Timeframe.MONTH_1: "Month1"
            },
            Exchange.OKX: {
                Timeframe.MIN_1: "1m", Timeframe.MIN_3: "3m", Timeframe.MIN_5: "5m", Timeframe.MIN_15: "15m",
                Timeframe.MIN_30: "30m", Timeframe.HOUR_1: "1H", Timeframe.HOUR_2: "2H", Timeframe.HOUR_4: "4H",
                Timeframe.HOUR_6: "6H", Timeframe.HOUR_12: "12H", Timeframe.DAY_1: "1D", Timeframe.DAY_3: "3D",
                Timeframe.WEEK_1: "1W", Timeframe.MONTH_1: "1M"
            }
        }

    def to_exchange_format(self, exchange: Exchange) -> str:
        """Конвертирует таймфрейм в формат, подходящий для указанной биржи."""
        try:
            return self.mapping[exchange][self]  # noqa
        except KeyError:
            raise ValueError(f"Timeframe {self.value} is not supported for exchange {exchange.value}")

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

# Binance:
# Literal[
# "1m", "3m", "5m", "15m", "30m",
# "1h", "2h", "4h", "6h", "8h", "12h",
# "1d", "3d", "1w", "1M"
# ]
#
#
# Bitget:
# Literal[
# "1m", "5m", "15m", "30m",
# "1h", "4h", "12h", "1d",
# "1w", "6h", "3d", "1M",
# "6Hutc", "12Hutc", "1Dutc",
# "3Dutc", "1Wutc", "1Mutc"
# ]
#
# Bybit:
# Literal[
# "1", "3", "5", "15", "30",
# "60", "120", "240", "360", "720",
# "D", "W", "M"
# ]
#
# MEXC:
# Literal[
# "Min1", "Min5", "Min15", "Min30",
# "Min60", "Hour4", "Hour8", "Day1",
# "Week1", "Month1"
# ]
#
# OKX
# Literal[
# "3M", "1M", "1W", "1D", "2D", "3D", "5D", "12H", "6H", "4H", "2H", "1H",
# "30m", "15m", "5m", "3m", "1m", "1s",
# "3Mutc", "1Mutc", "1Wutc", "1Dutc", "2Dutc", "3Dutc", "5Dutc", "12Hutc", "6Hutc"
# ]
