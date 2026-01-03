__all__ = ["BingxClient"]

import time
from typing import Any, Dict, Optional

from ..abstract import AbstractClient
from ..enums import Timeframe
from ..types import JsonLike


class BingxClient(AbstractClient):
    _BASE_URL: str = "https://open-api.bingx.com"

    def _prepare_params(
        self, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        params = params.copy() if params else {}
        if not params.get("timestamp"):
            params["timestamp"] = int(time.time() * 1000)
        return self.filter_params(params)

    async def _request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> JsonLike:
        url = f"{self._BASE_URL}{endpoint}"
        return await self._make_request(
            method="GET", url=url, params=self._prepare_params(params)
        )

    async def ticker(self, symbol: Optional[str] = None) -> JsonLike:
        params = {"symbol": symbol}
        return await self._request("/openApi/spot/v1/ticker/24hr", params=params)

    async def futures_ticker(self, symbol: Optional[str] = None) -> JsonLike:
        params = {"symbol": symbol}
        return await self._request("/openApi/swap/v2/quote/ticker", params=params)

    async def funding_rate(self, symbol: Optional[str] = None) -> JsonLike:
        params = {"symbol": symbol}
        return await self._request("/openApi/swap/v2/quote/premiumIndex", params=params)

    async def open_interest(self, symbol: str) -> JsonLike:
        if not symbol:
            raise ValueError("symbol is required for BingX open interest")
        params = {"symbol": symbol}
        return await self._request("/openApi/swap/v2/quote/openInterest", params=params)

    async def klines(
        self,
        symbol: str,
        interval: Timeframe | str,
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> JsonLike:
        interval = interval.value if isinstance(interval, Timeframe) else interval
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": start_time,
            "endTime": end_time,
        }
        return await self._request("/openApi/spot/v2/market/kline", params=params)

    async def futures_klines(
        self,
        symbol: str,
        interval: Timeframe | str,
        limit: int = 500,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> JsonLike:
        interval = interval.value if isinstance(interval, Timeframe) else interval
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": start_time,
            "endTime": end_time,
        }
        return await self._request("/openApi/swap/v3/quote/klines", params=params)

    async def depth(self, symbol: str, limit: int = 100) -> JsonLike:
        params = {"symbol": symbol, "limit": limit}
        return await self._request("/openApi/spot/v1/market/depth", params=params)

    async def futures_last_price(self, symbol: Optional[str] = None) -> JsonLike:
        params = {"symbol": symbol}
        return await self._request("/openApi/swap/v1/ticker/price", params=params)
