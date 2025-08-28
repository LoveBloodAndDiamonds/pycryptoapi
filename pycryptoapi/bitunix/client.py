from typing import Any, Optional

from ..abstract import AbstractClient


class BitunixClient(AbstractClient):

    _SPOT_BASE_URL = "https://openapi.bitunix.com"
    _FUTURES_BASE_URL = "https://fapi.bitunix.com"

    async def futures_last_price(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def depth(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def open_interest(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def funding_rate(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_ticker(self, symbols: Optional[str] = None) -> Any:
        """https://openapidoc.bitunix.com/doc/market/get_tickers.html"""
        url = self._FUTURES_BASE_URL + "/api/v1/futures/market/tickers"
        params = {}
        if symbols:
            params["symbols"] = symbols
        async with self._session.get(url, params=params) as response:
            return await response.json()

    async def ticker(self) -> Any:
        url = self._SPOT_BASE_URL + "/api/spot/v1/common/coin_pair/list"
        async with self._session.get(url) as response:
            return await response.json()
