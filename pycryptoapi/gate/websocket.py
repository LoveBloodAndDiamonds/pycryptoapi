__all__ = ["GateWebsocket", "GateSocketManager", ]

import json
from typing import Optional, Union, List, Literal, Callable, Awaitable, Dict, Tuple
import time

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType, Timeframe, Exchange
from ..exceptions import MarketException, TimeframeException


class GateWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://api.gateio.ws/ws/v4/"
        elif self._market_type == MarketType.FUTURES:
            return "wss://fx-ws.gateio.ws/v4/ws/usdt"
        else:
            raise MarketException()

    @property
    def _subscribe_message(self) -> Union[str, List[str]]:

        if self._market_type == MarketType.SPOT:
            if self._topic == "spot.trades":
                payload = [t.replace("USDT", "_USDT") if t.endswith("_USDT") else t for t in self._tickers]
                data = {
                    "time": int(time.time()),
                    "channel": self._topic,
                    "event": "subscribe",
                    "payload": payload,
                }
                print(data)
                return json.dumps(data)
            else:
                raise ValueError("Invalid topic.")

        elif self._market_type == MarketType.FUTURES:
            if self._topic == "futures.trades":
                payload = [t.replace("USDT", "_USDT") if t.endswith("_USDT") else t for t in self._tickers]
                data = {
                    "time": int(time.time()),
                    "channel": self._topic,
                    "event": "subscribe",
                    "payload": payload,
                }
                return json.dumps(data)
            else:
                raise ValueError("Invalid topic.")
        else:
            raise ValueError("Invalid exchange type. Choose either 'spot' or 'future'.")

    @property
    def _ping_message(self) -> Optional[str]:
        if self._market_type == MarketType.SPOT:
            return json.dumps({"time": int(time.time()), "channel": "spot.ping"})
        elif self._market_type == MarketType.FUTURES:
            return json.dumps({"time": int(time.time()), "channel": "futures.ping"})
        else:
            raise MarketException()


class GateSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str] | Tuple[str, ...],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> GateWebsocket:
        if market_type == MarketType.SPOT:
            topic: str = "spot.trades"
        elif market_type == MarketType.FUTURES:
            topic: str = "futures.trades"
        else:
            raise MarketException()
        return GateWebsocket(
            topic=topic,
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def klines_socket(
            cls,
            tickers: List[str] | Tuple[str, ...],
            timeframe: Timeframe,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> GateWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(
            cls,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            timezone: Literal[""] = "+8",
            **kwargs
    ) -> GateWebsocket:
        raise NotImplementedError()

    @classmethod
    def liquidations_socket(cls) -> GateWebsocket:
        raise NotImplementedError()
