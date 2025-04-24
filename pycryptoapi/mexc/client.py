__all__ = ["MexcClient"]

from typing import Any, Optional, Dict

from ..abstract import AbstractClient


class MexcClient(AbstractClient):
    _BASE_SPOT_URL: str = "https://api.mexc.com"
    _BASE_FUTURES_URL: str = "https://contract.mexc.com"

    # Rate limit: 1w w/ symbol or 40w w/o symbol
    async def ticker(self, symbol: Optional[str] = None) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/ticker/24hr"
        params = {"symbol": symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    # Rate limit:20 times/2 seconds
    async def futures_ticker(self, symbol: Optional[str] = None) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param symbol: (опционально) Торговая пара, например 'BTC_USDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/api/v1/contract/ticker"
        params = {"symbol": symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    # Weight(IP): 1
    async def depth(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Получает книгу ордеров (глубину рынка) для заданной торговой пары.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param limit: Количество уровней книги заявок (допустимые значения: 5, 10, 20, 50, 100, 500, 1000, 5000).
        :return: JSON-ответ с данными глубины рынка.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/depth"
        params = {"symbol": symbol, "limit": limit}
        return await self._make_request(method="GET", url=url, params=params)

    async def funding_rate(self) -> Dict[str, Any]:
        """
        Получает текущую ставку финансирования для всех символов.

        :return: JSON-ответ с текущей ставкой финансирования.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_FUTURES_URL}/api/v1/contract/funding_rate"
        return await self._make_request(method="GET", url=url)

    async def open_interest(self, symbol: str) -> Dict[str, str]:
        raise NotImplementedError("Mexc exchange are not allow to get open interest via API now (5feb2025).")
