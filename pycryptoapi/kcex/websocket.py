import json
from typing import Optional, Union, List, Callable, Awaitable, Tuple

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType
from ..exceptions import MarketException


class KcexWebsocket(AbstractWebsocket):
    @property
    def _subscribe_message(self) -> Optional[Union[str, List[str]]]:
        if self._market_type == MarketType.FUTURES:
            if self._topic == "sub.deal":
                sub_msg = []
                for symbol in self._tickers:
                    sub_msg.append(
                        json.dumps(
                            {
                                "method": self._topic,
                                "param": {
                                    "symbol": symbol,
                                    "compress": True
                                },
                            }
                        )
                    )
                return sub_msg
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

    @property
    def _ping_message(self) -> Optional[str]:
        if self._market_type == MarketType.FUTURES:
            return json.dumps({"method": "ping"})
        else:
            return json.dumps({"method": "PING"})

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.FUTURES:
            return "wss://www.kcex.com/fapi/edge"
        else:
            raise NotImplementedError()


class KcexSocketManager(AbstractSocketManager):
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
    ) -> KcexWebsocket:
        if market_type == MarketType.SPOT:
            raise NotImplementedError()
        elif market_type == MarketType.FUTURES:
            topic: str = "sub.deal"
        else:
            raise MarketException()
        return KcexWebsocket(
            topic=topic,
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            ping_interval=10,
            **kwargs
        )

    @classmethod
    def klines_socket(cls, *args, **kwargs) -> AbstractWebsocket:
        raise NotImplementedError()
