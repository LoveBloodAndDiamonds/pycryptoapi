__all__ = [
    "GateWebsocket",
    "GateSocketManager",
]

import json
import time
from typing import Awaitable, Callable, List, Literal, Optional, Tuple, Union

import orjson
from websockets.asyncio.client import ClientConnection

from ..abstract import AbstractSocketManager, AbstractWebsocket
from ..enums import MarketType, Timeframe
from ..exceptions import MarketException


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
                payload = []
                for t in self._tickers:
                    if t.endswith("_USDT"):
                        payload.append(t)
                    else:
                        payload.append(t.replace("USDT", "_USDT"))
                data = {
                    "time": int(time.time()),
                    "channel": self._topic,
                    "event": "subscribe",
                    "payload": payload,
                }
                return json.dumps(data)
            else:
                raise ValueError("Invalid topic.")

        elif self._market_type == MarketType.FUTURES:
            if self._topic == "futures.trades":
                payload = []
                for t in self._tickers:
                    if t.endswith("_USDT"):
                        payload.append(t)
                    else:
                        payload.append(t.replace("USDT", "_USDT"))
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

    @property
    def _pong_message(self) -> str:
        if self._market_type == MarketType.SPOT:
            return json.dumps({"time": int(time.time()), "channel": "spot.pong"})
        elif self._market_type == MarketType.FUTURES:
            return json.dumps({"time": int(time.time()), "channel": "futures.pong"})
        else:
            raise MarketException()

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
                if message.lower() == "ping":
                    await conn.send(self._pong_message)
                    self._logger.debug(f"Sent pong message: {self._pong_message}")
                self._last_message_time = time.time()
                self._logger.trace(f"{self} Received message: {message}")
                await self._queue.put(orjson.loads(message))
            except orjson.JSONDecodeError:
                if message not in ["ping", "pong"]:
                    self._logger.error(
                        f"{self} orjson.JSONDecodeError whilte handling message: {message}"
                    )
                else:
                    self._logger.debug(f"{self} Received ping message: {message}")
            except Exception as e:
                self._logger.error(
                    f"{self} Error({type(e)}) while handling message: {e}"
                )
                break


class GateSocketManager(AbstractSocketManager):
    @classmethod
    def aggtrades_socket(
        cls,
        market_type: MarketType,
        tickers: List[str] | Tuple[str, ...],
        callback: Callable[..., Awaitable],
        **kwargs,
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
            **kwargs,
        )

    @classmethod
    def klines_socket(
        cls,
        tickers: List[str] | Tuple[str, ...],
        timeframe: Timeframe,
        market_type: MarketType,
        callback: Callable[..., Awaitable],
        **kwargs,
    ) -> GateWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(
        cls,
        market_type: MarketType,
        callback: Callable[..., Awaitable],
        timezone: Literal[""] = "+8",
        **kwargs,
    ) -> GateWebsocket:
        raise NotImplementedError()

    @classmethod
    def liquidations_socket(cls) -> GateWebsocket:
        raise NotImplementedError()
