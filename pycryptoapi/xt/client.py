__all__ = ["XtClient"]

from typing import Any, Optional

from ..abstract import AbstractClient


class XtClient(AbstractClient):
    _BASE_SPOT_URL: str = "https://dapi.xt.com"
    _BASE_FUTURES_URL: str = "https://fapi.xt.com"

    async def ticker(self, symbol: Optional[str] = None) -> Any:
        """Возвращает JSON, в котором содержится информация о изменении цены и объеме монет за 24ч."""
        url = f"{self._BASE_SPOT_URL}/v4/public/ticker/24h"
        params = self.filter_params({'symbol': symbol})
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker(self) -> Any:
        """Возвращает JSON, в котором содержится информация о изменении цены и объеме монет за 24ч."""
        url = f"{self._BASE_FUTURES_URL}/future/market/v1/public/q/tickers"
        return await self._make_request(method="GET", url=url)

    async def funding_rate(self, *args, **kwargs) -> Any:
        """Возвращает JSON, в котором содержится информация о ставке финансирования."""
        raise NotImplementedError()

    async def open_interest(self, *args, **kwargs) -> Any:
        """Возаращает JSON, в котором содержится информация об открытом интересе."""
        raise NotImplementedError()

    async def klines(self, *args, **kwargs) -> Any:
        """Возаращает JSON, в котором содержится информация о свечах на монете на спотовом рынке."""
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        """Возаращает JSON, в котором содержится информация о свечах на монете на фьючерсном рынке."""
        raise NotImplementedError()

    async def depth(self, *args, **kwargs) -> Any:
        """Возаращает JSON, в котором содержится информация о стакане на спотовом рынке."""
        raise NotImplementedError()
