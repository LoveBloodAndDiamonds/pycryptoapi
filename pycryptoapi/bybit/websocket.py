__all__ = ["BybitWebsocket", "BybitSocketManager", ]

import json
from typing import Optional, Callable, List, Awaitable

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType, Timeframe, Exchange
from ..exc import MarketException


class BybitWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://stream.bybit.com/v5/public/spot"
        elif self._market_type == MarketType.FUTURES:
            return "wss://stream.bybit.com/v5/public/linear"
        else:
            raise MarketException()

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
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="publicTrade",
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def klines_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            timeframe: Timeframe,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="kline" + "." + timeframe.to_exchange_format(Exchange.BYBIT),
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def tickers_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="tickers",
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def liquidations_socket(
            cls,
            tickers: List[str],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BybitWebsocket:
        return BybitWebsocket(
            topic="allLiquidation",
            tickers=tickers,
            market_type=MarketType.FUTURES,
            callback=callback,
            **kwargs
        )
