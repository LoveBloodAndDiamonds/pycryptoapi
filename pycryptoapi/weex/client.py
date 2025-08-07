from typing import Any, Optional, List
from ..abstract import AbstractClient


class WeexClient(AbstractClient):
    # _BASE_SPOT_URL = "https://api-spot.weex.com"
    # _BASE_FUTURES_URL = "https://api-contract.weex.com"

    _BASE_SPOT_URL = "https://api.weex.com"
    _BASE_FUTURES_URL = "https://api.weex.com"

    async def ticker(self, symbol: Optional[str] = None, symbols: Optional[List[str]] = None) -> Any:
        """
        24h ticker – как для всех символов, так и для конкретного.
        """
        url = f"{self._BASE_SPOT_URL}/public/ticker/24h"
        params = self.filter_params({'symbol': symbol, 'symbols': symbols})
        return await self._make_request("GET", url, params=params)

    async def futures_ticker(self) -> Any:
        """
        Фьючерсный 24h ticker (USDT‑M perpetual).
        """
        url = f"{self._BASE_FUTURES_URL}/capi/v2/market/tickers"
        return await self._make_request("GET", url)

    async def funding_rate(self, symbol: str) -> Any:
        raise NotImplementedError()

    async def open_interest(self, symbol: str) -> Any:
        raise NotImplementedError()

    async def klines(self, symbol: str, interval: str, limit: Optional[int] = None) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, symbol: str, interval: str, limit: Optional[int] = None) -> Any:
        raise NotImplementedError()

    async def depth(self, symbol: str, limit: Optional[int] = None) -> Any:
        raise NotImplementedError()