__all__ = ["OkxWebsocket", "OkxSocketManager"]

import json
from typing import Optional, List, Callable, Awaitable

from ..abstract import AbstractWebsocket, AbstractSocketManager
from ..enums import Timeframe, Exchange
from ..exceptions import TickersException


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
            raise TickersException()

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
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic="trades-all",
            tickers=tickers,
            callback=callback,
            **kwargs
        )

    @classmethod
    def klines_socket(
            cls,
            tickers: List[str],
            timeframe: Timeframe,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic=f"candle{timeframe.to_exchange_format(Exchange.OKX)}",
            tickers=tickers,
            callback=callback,
            **kwargs
        )

    @classmethod
    def tickers_socket(
            cls,
            tickers: List[str],
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic="tickers",
            tickers=tickers,
            callback=callback,
            **kwargs
        )

    @classmethod
    def liquidations_socket(
            cls,
            callback: Callable[..., Awaitable],
            **kwargs
    ) -> OkxWebsocket:
        return OkxWebsocket(
            topic="liquidation-orders",
            tickers=["SWAP"],
            callback=callback,
            **kwargs
        )
