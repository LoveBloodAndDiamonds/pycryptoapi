__all__ = ["MexcWebsocket", "MexcSocketManager", ]

import json
from typing import Optional, Union, List, Literal, Callable, Awaitable, Dict

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType, Timeframe, Exchange
from ..exceptions import MarketException, TimeframeException


class MexcWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://wbs.mexc.com/ws"
        elif self._market_type == MarketType.FUTURES:
            return "wss://contract.mexc.com/edge"
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
            if self._topic == "sub.deal":
                params: List[Dict] = [{"symbol": t.replace("USDT", "_USDT")} for t in self._tickers]
            elif self._topic == "sub.kline":
                if not self._timeframe:
                    raise TimeframeException()
                params: List[Dict] = [{"symbol": t.replace("USDT", "_USDT"), "interval": self._timeframe} for t in
                                      self._tickers]
            elif self._topic == "sub.tickers":
                params: List[Dict] = [dict()]
            else:
                params: List[Dict] = [{} for _ in self._tickers]
            return [json.dumps({"method": self._topic, "param": p}) for p in params]

        else:
            raise ValueError("Invalid exchange type. Choose either 'spot' or 'future'.")

    @property
    def _ping_message(self) -> Optional[str]:
        return json.dumps({"method": "ping"})


class MexcSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> MexcWebsocket:
        if market_type == MarketType.SPOT:
            topic: str = "spot@public.deals.v3.api"
        elif market_type == MarketType.FUTURES:
            topic: str = "sub.deal"
        else:
            raise MarketException()
        return MexcWebsocket(
            topic=topic,
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs
        )

    @classmethod
    def klines_socket(
            cls,
            tickers: List[str],
            timeframe: Timeframe,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> MexcWebsocket:
        if market_type == MarketType.SPOT:
            topic: str = "spot@public.kline.v3.api"
        elif market_type == MarketType.FUTURES:
            topic: str = "sub.kline"
        else:
            raise MarketException()
        return MexcWebsocket(
            topic=topic,
            market_type=market_type,
            timeframe=timeframe.to_exchange_format(Exchange.MEXC),
            tickers=tickers,
            callback=callback,
            **kwargs
        )

    @classmethod
    def tickers_socket(
            cls,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            timezone: Literal[""] = "+8",
            **kwargs
    ) -> MexcWebsocket:
        if market_type == MarketType.SPOT:
            topic: str = "spot@public.miniTickers.v3.api"
        elif market_type == MarketType.FUTURES:
            topic: str = "sub.tickers"
        else:
            raise MarketException()
        return MexcWebsocket(
            topic=topic,
            market_type=market_type,
            timeframe=timezone,
            callback=callback,
            **kwargs
        )

    @classmethod
    def liquidations_socket(cls) -> MexcWebsocket:
        """https://mexcdevelop.github.io/apidocs/contract_v1_en/#public-channels"""
        raise NotImplementedError("Metod can not be imlemented at this exchange")
