__all__ = ["OkxClient"]

from typing import Any

from ..abstract import AbstractClient


class OkxClient(AbstractClient):
    _BASE_URL: str = "https://www.okx.com"

    async def tickers(self) -> Any:
        url = f"{self._BASE_URL}/api/v5/market/tickers?instType=SPOT"
        return await self._make_request(method="GET", url=url)

    async def futures_tickers(self) -> Any:
        url = f"{self._BASE_URL}/api/v5/market/tickers?instType=SWAP"
        return await self._make_request(method="GET", url=url)
