__all__ = ["MexcWebsocket", "MexcSocketManager", ]

import json
import time
from typing import Optional, Union, List, Literal, Callable, Awaitable, Dict, Tuple

from websockets.asyncio.client import ClientConnection
import orjson

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType, Timeframe, Exchange
from ..exceptions import MarketException, TimeframeException
from .spot_proto import PushDataV3ApiWrapper


class MexcWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://wbs-api.mexc.com/ws"
        elif self._market_type == MarketType.FUTURES:
            return "wss://contract.mexc.com/edge"
        else:
            raise MarketException()

    @property
    def _subscribe_message(self) -> Union[str, List[str]]:

        if self._market_type == MarketType.SPOT:
            if self._topic == "spot@public.kline.v3.api.pb":
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
                params: List[Dict] = [
                    {"symbol": t.replace("USDT", "_USDT") if not t.endswith("_USDT") else t} for t in self._tickers
                ]
            elif self._topic == "sub.kline":
                if not self._timeframe:
                    raise TimeframeException()
                params: List[Dict] = [{
                    "symbol": t.replace("USDT", "_USDT") if not t.endswith("_USDT") else t,
                    "interval": self._timeframe
                } for t in self._tickers]
            elif self._topic == "sub.tickers":
                params: List[Dict] = [dict()]
            else:
                params: List[Dict] = [{} for _ in self._tickers]
            return [json.dumps({"method": self._topic, "param": p}) for p in params]

        else:
            raise ValueError("Invalid exchange type. Choose either 'spot' or 'future'.")

    @property
    def _ping_message(self) -> Optional[str]:
        if self._market_type == MarketType.SPOT:
            return json.dumps({"method": "PING"})
        return json.dumps({"method": "ping"})

    async def _handler(self, conn: ClientConnection) -> None:
        """
        Принимает управление над активным подключением.

        Параметры:
            conn (ClientConnection): Активное WebSocket соединение.
        """
        # Слушаем входящие сообщения
        while self._is_active:
            try:
                message = await conn.recv()
                self._last_message_time = time.time()
                self._logger.trace(f"{self} Received message: {message}")
                if self._market_type == MarketType.FUTURES:
                    await self._queue.put(orjson.loads(message))
                else:
                    try:
                        if isinstance(message, bytes):
                            wrapper = PushDataV3ApiWrapper()  # noqa
                            wrapper.ParseFromString(message)
                            await self._queue.put(wrapper)
                        else:
                            self._logger.debug(f"{self} pb recieved string: {message}")
                    except Exception as e:
                        self._logger.info(f"{self} pb error: {e}")
            except orjson.JSONDecodeError:
                if message not in ["ping", "pong"]:
                    self._logger.error(f"{self} orjson.JSONDecodeError whilte handling message: {message}")
                else:
                    self._logger.debug(f"{self} Received ping message: {message}")
            except Exception as e:
                self._logger.error(f"{self} Error({type(e)}) while handling message: {e}")
                break


class MexcSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str] | Tuple[str, ...],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> MexcWebsocket:
        if market_type == MarketType.SPOT:
            topic: str = "spot@public.aggre.deals.v3.api.pb@100ms"  # can be 10 ms
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
            tickers: List[str] | Tuple[str, ...],
            timeframe: Timeframe,
            market_type: MarketType,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> MexcWebsocket:
        if market_type == MarketType.SPOT:
            topic: str = "spot@public.kline.v3.api.pb"
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
            topic: str = "spot@public.miniTickers.v3.api.pb"
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
