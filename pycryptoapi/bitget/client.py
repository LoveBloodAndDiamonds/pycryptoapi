__all__ = ["BitgetClient"]

from typing import Any

from ..abstract import AbstractClient


class BitgetClient(AbstractClient):
    _BASE_URL: str = "https://api.bitget.com"

    async def tickers(self) -> Any:
        url = f"{self._BASE_URL}/api/v2/spot/public/symbols"
        return await self._make_request(method="GET", url=url)

    async def futures_tickers(self) -> Any:
        url = f"{self._BASE_URL}/api/v2/mix/market/tickers?productType=USDT-FUTURES"
        return await self._make_request(method="GET", url=url)
