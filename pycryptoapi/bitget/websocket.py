__all__ = ["BitgetWebsocket", "BitgetSocketManager", ]

import json
from typing import Optional, Callable, Awaitable, List, Literal

from ..abstract.websocket import AbstractWebsocket, AbstractSocketManager
from ..enums import MarketType


class BitgetWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        return "wss://ws.bitget.com/v2/ws/public"

    @property
    def _ping_message(self) -> Optional[str]:
        return "ping"

    @property
    def _subscribe_message(self) -> Optional[str]:
        streams: list[dict] = [
            {
                "instType": "SPOT" if self._market_type == MarketType.SPOT else "USDT-FUTURES",
                "channel": self._topic,
                "instId": ticker.upper()
            } for ticker in self._tickers
        ]
        return json.dumps(
            {
                "op": "subscribe",
                "args": streams
            }
        )


class BitgetSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> BitgetWebsocket:
        return BitgetWebsocket(
            topic="trade",
            tickers=tickers,
            market_type=market_type,
            callback=callback
        )

    @classmethod
    def klines_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable],
            timeframe: Literal[
                "1m", "5m", "15m", "30m",
                "1h", "4h", "12h", "1d",
                "1w", "6h", "3d", "1M",
                "6Hutc", "12Hutc", "1Dutc",
                "3Dutc", "1Wutc", "1Mutc"
            ],
    ) -> BitgetWebsocket:
        return BitgetWebsocket(
            topic="candle" + timeframe,
            tickers=tickers,
            market_type=market_type,
            callback=callback
        )

    @classmethod
    def tickers_socket(
            cls,
            market_type: MarketType,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> BitgetWebsocket:
        return BitgetWebsocket(
            topic="ticker",
            tickers=tickers,
            market_type=market_type,
            callback=callback
        )

    @classmethod
    def liquidations_socket(cls) -> BitgetWebsocket:
        raise NotImplementedError("Can not be implemented at this exchange")
