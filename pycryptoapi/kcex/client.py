from typing import Any

from ..abstract import AbstractClient


class KcexClient(AbstractClient):
    async def futures_last_price(self) -> Any:
        return await self.futures_ticker()

    async def depth(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def open_interest(self) -> Any:
        return await self.futures_ticker()

    async def funding_rate(self) -> Any:
        return await self.futures_ticker()

    async def futures_ticker(self, *args, **kwargs) -> Any:
        url = "https://www.kcex.com/fapi/v1/contract/ticker?"
        async with self._session.get(url) as response:
            return await response.json()

    async def ticker(self, *args, **kwargs) -> Any:
        raise NotImplementedError()
