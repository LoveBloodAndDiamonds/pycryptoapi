__all__ = ["BinanceClient"]

from csv import DictReader
from typing import Any, Optional, Dict, List

from ..abstract import AbstractClient


class BinanceClient(AbstractClient):
    _BASE_SPOT_URL: str = "https://api.binance.com"
    _BASE_FUTURES_URL: str = "https://fapi.binance.com"

    async def ticker(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/ticker/24hr"
        params = self.filter_params({'symbol': symbol})
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/ticker/24hr"
        params = self.filter_params({'symbol': symbol})
        return await self._make_request(method="GET", url=url, params=params)

    async def funding_rate(self, symbol: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Получает ставку финансирования для фьючерсного рынка.
        Используется эндпоинт: /fapi/v1/premiumIndex

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными ставок финансирования.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/premiumIndex"
        params = self.filter_params({"symbol": symbol})
        return await self._make_request(method="GET", url=url, params=params)

    async def open_interest(self, symbol: str) -> Dict[str, str]:
        """
        Получает значение открытого интереса (Open Interest) для указанного торгового инструмента
        на фьючерсном рынке Binance.

        Используется эндпоинт: /fapi/v1/openInterest

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :return: JSON-ответ с данными об открытом интересе.
            {'openInterest': '84548.990', 'symbol': 'BTCUSDT', 'time': 1738480839502}
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/openInterest"
        params = {"symbol": symbol}
        return await self._make_request(method="GET", url=url, params=params)
