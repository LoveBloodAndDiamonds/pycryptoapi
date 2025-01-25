__all__ = ["MexcClient"]

from typing import Any

from ..abstract import AbstractClient


class MexcClient(AbstractClient):
    _BASE_SPOT_URL: str = "https://api.mexc.com"
    _BASE_FUTURES_URL: str = "https://contract.mexc.com"

    async def tickers(self) -> Any:
        url = f"{self._BASE_SPOT_URL}/api/v3/defaultSymbols"
        return await self._make_request(method="GET", url=url)

    async def futures_tickers(self) -> Any:
        url = f"{self._BASE_FUTURES_URL}/api/v1/contract/detail"
        return await self._make_request(method="GET", url=url)
