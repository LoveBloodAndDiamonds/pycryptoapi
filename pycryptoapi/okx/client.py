__all__ = ["OkxClient"]

from typing import Any

from ..abstract import AbstractClient


class OkxClient(AbstractClient):
    _BASE_URL: str = "https://www.okx.com"

    async def ticker(self) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :return: JSON-ответ с данными тикеров.
        """
        url = f"{self._BASE_URL}/api/v5/market/tickers"
        params = {"instType": "SPOT"}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker(self) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :return: JSON-ответ с данными тикеров.
        """
        url = f"{self._BASE_URL}/api/v5/market/tickers"
        params = {"instType": "SWAP"}
        return await self._make_request(method="GET", url=url, params=params)
