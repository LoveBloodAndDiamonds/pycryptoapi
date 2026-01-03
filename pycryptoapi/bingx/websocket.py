__all__ = ["BingxWebsocket", "BingxSocketManager"]

import gzip
import json
import time
from typing import Awaitable, Callable, List, Optional, Tuple

import orjson
from websockets.asyncio.client import ClientConnection

from ..abstract import AbstractSocketManager, AbstractWebsocket
from ..enums import MarketType
from ..exceptions import MarketException


class BingxWebsocket(AbstractWebsocket):
    @property
    def _connection_uri(self) -> str:
        if self._market_type == MarketType.SPOT:
            return "wss://open-api-ws.bingx.com/market"
        if self._market_type == MarketType.FUTURES:
            return "wss://open-api-swap.bingx.com/swap-market"
        raise MarketException()

    @property
    def _ping_message(self) -> Optional[str]:
        return None

    @property
    def _subscribe_message(self) -> Optional[List[str]]:
        return [
            json.dumps(
                {
                    "reqType": "sub",
                    "dataType": f"{ticker.upper()}@{self._topic}",
                }
            )
            for ticker in self._tickers
        ]

    @staticmethod
    def _decode_message(message: str | bytes) -> dict | str:
        if isinstance(message, bytes):
            try:
                message = gzip.decompress(message).decode("utf-8")
            except OSError:
                message = message.decode("utf-8")
        if message == "Ping":
            return "ping"
        return orjson.loads(message)

    async def _handler(self, conn: ClientConnection) -> None:
        while self._is_active:
            try:
                message = await conn.recv()
                self._last_message_time = time.time()
                self._logger.trace(f"{self} Received message: {message}")

                decoded = self._decode_message(message)
                if decoded == "ping":
                    await conn.send("Pong")
                    self._logger.debug(f"{self} Pong sent.")
                    continue
                await self._queue.put(decoded)
            except orjson.JSONDecodeError:
                if message not in ["Ping", "Pong"]:
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


class BingxSocketManager(AbstractSocketManager):
    @classmethod
    def aggtrades_socket(
        cls,
        market_type: MarketType,
        tickers: List[str] | Tuple[str, ...],
        callback: Callable[..., Awaitable],
        **kwargs,
    ) -> BingxWebsocket:
        return BingxWebsocket(
            topic="trade",
            tickers=tickers,
            market_type=market_type,
            callback=callback,
            **kwargs,
        )

    @classmethod
    def klines_socket(cls, *args, **kwargs) -> BingxWebsocket:
        raise NotImplementedError()

    @classmethod
    def tickers_socket(cls, *args, **kwargs) -> BingxWebsocket:
        raise NotImplementedError()

    @classmethod
    def liquidations_socket(cls, *args, **kwargs) -> BingxWebsocket:
        raise NotImplementedError()
