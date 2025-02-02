__all__ = ["BybitClient"]

from typing import Any, Optional, Dict

from ..abstract import AbstractClient


class BybitClient(AbstractClient):
    _BASE_URL: str = "https://api.bybit.kz"  # Kazakhstan

    # _BASE_URL: str = "https://api.bybit.nl"  # Netherland
    # _BASE_URL: str = "https://api.bybit-tr.com"  # Turkey
    # _BASE_URL: str = "https://api.byhkbit.com"  # Hong Kong
    # _BASE_URL: str = "https://api-testnet.bybit.com"  # Testnet

    async def ticker(self, symbol: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/v5/market/tickers"
        params = {"category": "spot"}
        if symbol:
            params["symbol"] = symbol
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker(self, symbol: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/v5/market/tickers"
        params = {"category": "linear"}
        if symbol:
            params["symbol"] = symbol
        return await self._make_request(method="GET", url=url, params=params)

    async def funding_rate(self, symbol: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Получает данные, которые содержат информацию о текущей ставке финансирования.

        :param symbol: Торговая пара, например 'BTCUSDT'. Опциольнально.
        :return: JSON-ответ с данными ставок финансирования.
        :raises Exception: Если запрос не выполнен успешно.
        """
        return await self.futures_ticker(symbol=symbol)
