from typing import Any, Dict

from ..abstract import AbstractClient


class HyperliquidClient(AbstractClient):

    _BASE_URL = "https://api.hyperliquid.xyz/info"
    _BASE_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async def futures_last_price(self, *args, **kwargs) -> Any:
        return await self.futures_ticker()

    async def depth(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def open_interest(self, *args, **kwargs) -> Any:
        return await self.futures_ticker()

    async def funding_rate(self, *args, **kwargs) -> Any:
        return await self.futures_ticker()

    async def futures_ticker(self) -> Dict:
        """https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-perpetuals-asset-contexts-includes-mark-price-current-funding-open-interest-etc"""
        json_data = {"type": "metaAndAssetCtxs"}
        async with self._session.post(self._BASE_URL, json=json_data, headers=self._BASE_HEADERS) as response:
            return await response.json()

    async def ticker(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
