__all__ = ["BinanceClient"]

from typing import Any, Optional

from ..abstract import AbstractClient


class BinanceClient(AbstractClient):
    _BASE_SPOT_URL: str = "https://api.binance.com"
    _BASE_FUTURES_URL: str = "https://fapi.binance.com"

    async def tickers(self) -> Any:
        """
        Получает текущие цены для всех спотовых торговых пар на Binance.

        :return: JSON-ответ со списком текущих цен для всех доступных торговых пар.
            Пример ответа:
            [
                {
                    "symbol": "BTCUSDT",
                    "price": "45000.00"
                },
                {
                    "symbol": "ETHUSDT",
                    "price": "3000.00"
                }
            ]
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/ticker/price"
        return await self._make_request(method="GET", url=url)

    async def futures_tickers(self) -> Any:
        """
        Получает текущие цены для всех фьючерсных торговых пар на Binance.

        :return: JSON-ответ со списком текущих цен для всех доступных фьючерсных торговых пар.
            Пример ответа:
            [
                {
                    "symbol": "BTCUSDT",
                    "price": "45000.00"
                },
                {
                    "symbol": "ETHUSDT",
                    "price": "3000.00"
                }
            ]
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/ticker/price"
        return await self._make_request(method="GET", url=url)

    async def ticker24h(self, symbol: Optional[str] = None) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/ticker/24hr"
        params = {'symbol': symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker24h(self, symbol: Optional[str] = None) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/ticker/24hr"
        params = {'symbol': symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)
