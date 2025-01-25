__all__ = ["BybitClient"]

from typing import Any

from ..abstract import AbstractClient


class BybitClient(AbstractClient):
    # _BASE_URL: str = "https://api.bybit.kz"  # Kazakhstan
    # _BASE_URL: str = "https://api.bybit.nl"  # Netherland
    # _BASE_URL: str = "https://api.bybit-tr.com"  # Turkey
    _BASE_URL: str = "https://api.byhkbit.com"  # Hong Kong

    async def tickers(self) -> Any:
        url = f"{self._BASE_URL}/v5/market/tickers?category=spot"
        return await self._make_request(method="GET", url=url)

    async def futures_tickers(self) -> Any:
        url = f"{self._BASE_URL}/v5/market/tickers?category=linear"
        return await self._make_request(method="GET", url=url)
