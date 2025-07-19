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
            # return "wss://wbs.mexc.com/ws"
            raise MarketException()
        elif self._market_type == MarketType.FUTURES:
            return "wss://fx-ws.gateio.ws/v4/ws/usdt"
        else:
            raise MarketException()

    @property
    def _subscribe_message(self) -> Union[str, List[str]]:

        if self._market_type == MarketType.SPOT:
            if self._topic == "spot@public.kline.v3.api":
                if not self._timeframe:
                    raise TimeframeException()
                params: List[str] = [f"{self._topic}@{t}@{self._timeframe}" for t in self._tickers]
            elif self._topic == "spot@public.miniTickers.v3.api":
                params: List[str] = [f"spot@public.miniTickers.v3.api@UTC{self._timeframe}"]
            else:
                params: List[str] = [f"{self._topic}@{t}" for t in self._tickers]
            return json.dumps({
                "method": "SUBSCRIPTION",
                "params": params
            })

        elif self._market_type == MarketType.FUTURES:
            payload = [t.replace("USDT", "_USDT") for t in self._tickers if not t.endswith("_USDT")]
            data = {
                "time": int(time.time()),
                "channel": "futures.trades",
                "event": "subscribe",
                "payload": payload,
            }
            return json.dumps(data)
            # if self._topic == "sub.deal":
            #     params: List[Dict] = [
            #         {"symbol": t.replace("USDT", "_USDT") if not t.endswith("_USDT") else t} for t in self._tickers
            #     ]
            # elif self._topic == "sub.kline":
            #     if not self._timeframe:
            #         raise TimeframeException()
            #     params: List[Dict] = [{
            #         "symbol": t.replace("USDT", "_USDT") if not t.endswith("_USDT") else t,
            #         "interval": self._timeframe
            #     } for t in self._tickers]
            # elif self._topic == "sub.tickers":
            #     params: List[Dict] = [dict()]
            # else:
            #     params: List[Dict] = [{} for _ in self._tickers]
            # return [json.dumps({"method": self._topic, "param": p}) for p in params]

        else:
            raise ValueError("Invalid exchange type. Choose either 'spot' or 'future'.")

    @property
    def _ping_message(self) -> Optional[str]:
        if self._market_type == MarketType.SPOT:
            raise MarketException()
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
            raise MarketException()
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
