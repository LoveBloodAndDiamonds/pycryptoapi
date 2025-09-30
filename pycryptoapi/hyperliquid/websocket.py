import json
from typing import Optional, Union, List, Tuple, Callable, Awaitable

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType


class HyperliquidWebsocket(AbstractWebsocket):

    @property
    def _subscribe_message(self) -> Optional[Union[str, List[str]]]:
        return [
            json.dumps(
                {
                    "method": "subscribe",
                    "subscription": {
                        "type": self._topic,
                        "coin": symbol
                    }
                }
            ) for symbol in self._tickers
        ]

    @property
    def _ping_message(self) -> Optional[str]:
        pass

    @property
    def _connection_uri(self) -> str:
        return "wss://api.hyperliquid.xyz/ws"


class HyperliquidSocketManager(AbstractSocketManager):

    @classmethod
    def liquidations_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str] | Tuple[str, ...],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> HyperliquidWebsocket:
        return HyperliquidWebsocket(
            topic="trades",
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )
    @classmethod
    def klines_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()
