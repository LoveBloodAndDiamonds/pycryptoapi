__all__ = ["BybitWebsocket", "BybitSocketManager", ]

import json
from typing import Optional, Callable, List, Awaitable, Literal

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType
from ..exceptions import WrongMarketType


class BybitWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://stream.bybit.com/v5/public/spot"
        elif self._market_type == MarketType.FUTURES:
            return "wss://stream.bybit.com/v5/public/linear"
        else:
            raise WrongMarketType()

    @property
    def _subscribe_message(self) -> Optional[str]:
        streams: list[str] = [f"{self._topic}.{ticker}" for ticker in self._tickers]
        subscribe_message = json.dumps({
            "op": "subscribe",
            "args": streams
        })
        return subscribe_message

    @property
    def _ping_message(self) -> Optional[str]:
        return json.dumps({"op": "ping"})


class BybitSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="publicTrade",
            tickers=tickers,
            market_type=market_type,
            callback=callback
        )

    @classmethod
    def klines_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            timeframe: Literal[
                "1", "3", "5", "15", "30",
                "60", "120", "240", "360", "720",
                "D", "W", "M"
            ],
            callback: Callable[..., Awaitable]
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="kline" + "." + timeframe,
            tickers=tickers,
            market_type=market_type,
            callback=callback
        )

    @classmethod
    def tickers_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="tickers",
            tickers=tickers,
            market_type=market_type,
            callback=callback
        )

    @classmethod
    def liquidations_socket(
            cls,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="liquidation",
            tickers=tickers,
            market_type=MarketType.FUTURES,
            callback=callback
        )
