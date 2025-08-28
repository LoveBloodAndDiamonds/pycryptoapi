import json
import time
from typing import Optional, Union, List, Tuple, Callable, Awaitable

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType


class BitunixWebsocket(AbstractWebsocket):

    @property
    def _subscribe_message(self) -> Optional[Union[str, List[str]]]:
        streams: list[dict] = [{"symbol": ticker, "ch": self._topic} for ticker in self._tickers]
        subscribe_message = json.dumps({
            "op": "subscribe",
            "args": streams
        })
        return subscribe_message

    @property
    def _ping_message(self) -> Optional[str]:
        if self._market_type == MarketType.FUTURES:
            return json.dumps({
                "op": "ping",
                "ping": int(time.time())
            })
        else:
            raise Exception("todo")

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.FUTURES:
            return "wss://fapi.bitunix.com/public/"
        else:
            raise Exception("todo")


class BitunixSocketManager(AbstractSocketManager):

    @classmethod
    def liquidations_socket(cls, *args, **kwargs) -> BitunixWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(cls, *args, **kwargs) -> BitunixWebsocket:
        raise NotImplementedError()

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str] | Tuple[str, ...],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> BitunixWebsocket:
        if market_type == MarketType.SPOT:
            raise NotImplementedError("Can not be implemented for 28.08.2025")
        return BitunixWebsocket(
            topic="trade",
            callback=callback,
            tickers=tickers,
            market_type=market_type,
            **kwargs
        )

    @classmethod
    def klines_socket(cls, *args, **kwargs) -> BitunixWebsocket:
        raise NotImplementedError()
