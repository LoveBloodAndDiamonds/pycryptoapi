__all__ = ["BitgetClient"]

from typing import Any, Optional

from ..abstract import AbstractClient


class BitgetClient(AbstractClient):
    _BASE_URL: str = "https://api.bitget.com"

    async def ticker(self, symbol: Optional[str] = None) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v2/spot/market/tickers"
        params = {'symbol': symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker(self, symbol: Optional[str] = None) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v2/mix/market/tickers"
        params = {'productType': 'USDT-FUTURES'}
        if symbol:
            params["symbol"] = symbol
        return await self._make_request(method="GET", url=url, params=params)
