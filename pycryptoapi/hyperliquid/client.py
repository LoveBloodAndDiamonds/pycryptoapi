from typing import Any

from ..abstract import AbstractClient


class HyperliquidClient(AbstractClient):

    _BASE_URL = "https://api.hyperliquid.xyz"

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

    async def futures_ticker(self, *args, **kwargs) -> Any:
        """https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals"""
        url = self._BASE_URL + "/info"
        json_data = {"type": "perpDexs"}
        headers = {"Content-Type": "application/json"}
        async with self._session.post(url, json=json_data, headers=headers) as response:
            return await response.json()

    async def ticker(self, *args, **kwargs) -> Any:
        """https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot"""
        url = self._BASE_URL + "/info"
        json_data = {"type": "spotMeta"}
        headers = {"Content-Type": "application/json"}
        async with self._session.post(url, json=json_data, headers=headers) as response:
            return await response.json()
