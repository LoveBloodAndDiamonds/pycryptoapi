__all__ = ["BinanceWebsocket", "BinanceSocketManager", ]

from typing import Optional, Callable, Awaitable, List, Literal

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType
from ..exc import MarketException


class BinanceWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        # define base url
        if self._market_type == MarketType.FUTURES or self._topic == "!forceOrder@arr":
            base_url: str = "wss://fstream.binance.com"
        elif self._market_type == MarketType.SPOT:
            base_url: str = "wss://stream.binance.com:9443"
        else:
            raise MarketException()

        if not self._tickers:  # Case with all market streams with no ticker
            uri: str = f"{base_url}/ws/{self._topic}"
        elif len(self._tickers) > 1:  # Case with many tickers
            uri: str = f"{base_url}/stream?streams="
            for s in self._tickers:
                uri += s.lower() + self._topic + "/"
            uri: str = uri[:-1]
        elif len(self._tickers) == 1:  # Case with single tickers
            uri: str = f"{base_url}/ws/{self._tickers[0].lower()}{self._topic}"
        else:
            raise Exception("Can not define uri")
        return uri

    @property
    def _ping_message(self) -> Optional[str]:
        return None

    @property
    def _subscribe_message(self) -> Optional[str]:
        return None


class BinanceSocketManager(AbstractSocketManager):

    @classmethod
    def liquidations_socket(
            cls,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BinanceWebsocket:
        return BinanceWebsocket(
            topic="!forceOrder@arr",
            callback=callback,
            **kwargs
        )

    @classmethod
    def klines_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            timeframe: Literal[
                "1m", "3m", "5m", "15m", "30m",
                "1h", "2h", "4h", "6h", "8h", "12h",
                "1d", "3d", "1w", "1M"
            ],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BinanceWebsocket:
        return BinanceWebsocket(
            topic="@kline" + "_" + timeframe,
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            tickers: List[str],
            **kwargs
    ) -> BinanceWebsocket:
        return BinanceWebsocket(
            topic="@aggTrade",
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def tickers_socket(
            cls,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BinanceWebsocket:
        return BinanceWebsocket(
            topic="!ticker@arr",
            market_type=market_type,
            callback=callback,
            **kwargs
        )
