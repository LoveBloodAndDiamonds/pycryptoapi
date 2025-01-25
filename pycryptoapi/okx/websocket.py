__all__ = ["OkxWebsocket", "OkxSocketManager"]

import json
from typing import Optional, List, Callable, Awaitable, Literal

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..exceptions import WrongTickers


class OkxWebsocket(AbstractWebsocket):

    @property
    def _connection_uri(self) -> str:
        business_topics = ["trades-all", "candle"]
        uri_map = {
            "business": "wss://ws.okx.com:8443/ws/v5/business",
            "public": "wss://ws.okx.com:8443/ws/v5/public",
        }
        return uri_map["business"] if any(self._topic.startswith(topic) for topic in business_topics) else \
            uri_map["public"]

    @property
    def _subscribe_message(self) -> Optional[str]:
        if not self._tickers:
            raise WrongTickers()

        if self._topic == "liquidation-orders":
            streams: list[dict] = [
                {
                    "channel": self._topic,
                    "instType": self._tickers[0]
                }
            ]
        else:
            streams: list[dict] = [
                {
                    "channel": self._topic,
                    "instId": ticker.upper()
                } for ticker in self._tickers
            ]
        subscribe_message = json.dumps({
            "op": "subscribe",
            "args": streams
        })
        return subscribe_message

    @property
    def _ping_message(self) -> Optional[str]:
        return None


class OkxSocketManager(AbstractSocketManager):

    @classmethod
    def aggtrades_socket(
            cls,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic="trades-all",
            tickers=tickers,
            callback=callback
        )

    @classmethod
    def klines_socket(
            cls,
            tickers: List[str],
            timeframe: Literal[
                "3M", "1M", "1W", "1D", "2D", "3D", "5D", "12H", "6H", "4H", "2H", "1H",
                "30m", "15m", "5m", "3m", "1m", "1s",
                "3Mutc", "1Mutc", "1Wutc", "1Dutc", "2Dutc", "3Dutc", "5Dutc", "12Hutc", "6Hutc"
            ],
            callback: Callable[..., Awaitable]
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic=f"candle{timeframe}",
            tickers=tickers,
            callback=callback
        )

    @classmethod
    def tickers_socket(
            cls,
            tickers: List[str],
            callback: Callable[..., Awaitable]
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic="tickers",
            tickers=tickers,
            callback=callback
        )

    @classmethod
    def liquidations_socket(
            cls,
            callback: Callable[..., Awaitable]
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic="liquidation-orders",
            tickers=["SWAP"],
            callback=callback
        )
