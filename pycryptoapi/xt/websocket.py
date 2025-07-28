__all__ = ["XtWebsocket", "XtSocketManager", ]

import json
import time
import uuid
from typing import Optional, Callable, List, Awaitable, Tuple

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType
from ..exceptions import MarketException


class XtWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://stream.xt.com/public"
        elif self._market_type == MarketType.FUTURES:
            return "wss://fstream.xt.com/ws/market"
        else:
            raise MarketException()

    @property
    def _subscribe_message(self) -> Optional[str]:
        params = [f"{self._topic}@{s}" for s in self._tickers]
        subscribe_message = json.dumps({
            "method": "subscribe",
            "params": params,
            "id": str(uuid.uuid4())
        })
        return subscribe_message

    @property
    def _ping_message(self) -> Optional[str]:
        return "ping"


class XtSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str] | Tuple[str, ...],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> XtWebsocket:
        return XtWebsocket(
            topic="trade",
            ping_interval=10,
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def klines_socket(cls, *args, **kwargs) -> XtWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(cls, *args, **kwargs) -> XtWebsocket:
        raise NotImplementedError()

    @classmethod
    def liquidations_socket(cls, *args, **kwargs) -> XtWebsocket:
        raise NotImplementedError()
