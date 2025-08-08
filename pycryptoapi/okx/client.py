__all__ = ["OkxClient"]

from typing import Any, Dict

from ..abstract import AbstractClient


class OkxClient(AbstractClient):
    _BASE_URL: str = "https://www.okx.com"

    async def klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    # Rate Limit: 20 requests per 2 seconds
    async def ticker(self) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :return: JSON-ответ с данными тикеров.
        """
        url = f"{self._BASE_URL}/api/v5/market/tickers"
        params = {"instType": "SPOT"}
        return await self._make_request(method="GET", url=url, params=params)

    # Rate Limit: 20 requests per 2 seconds
    async def futures_ticker(self) -> Any:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :return: JSON-ответ с данными тикеров.
        """
        url = f"{self._BASE_URL}/api/v5/market/tickers"
        params = {"instType": "SWAP"}
        return await self._make_request(method="GET", url=url, params=params)

    # Rate Limit: 20 requests per 2 seconds
    async def funding_rate(self, symbol: str) -> Any:
        """
        Получает текущую ставку финансирования для указанного символа.

        :param symbol: Торговая пара, например 'BTC-USDT-SWAP'.
        :return: JSON-ответ с текущей ставкой финансирования.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v5/public/funding-rate"
        params = {"instId": symbol}
        return await self._make_request(method="GET", url=url, params=params)

    # Rate Limit: 20 requests per 2 seconds
    async def open_interest(self) -> Dict[str, Any]:
        """
        Получает данные, которые содержат информацию о открытом интересе.

        :return: JSON-ответ с данными открытого интереса.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v5/public/open-interest?"
        params = {"instType": "SWAP"}
        return await self._make_request(method="GET", url=url, params=params)

    # Rate Limit: 40 requests per 2 seconds
    async def depth(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Получает книгу ордеров (глубину рынка) для заданной торговой пары.

        :param symbol: 	Instrument ID, e.g. BTC-USDT.
        :param limit: Order book depth per side. Maximum 400, e.g. 400 bids + 400 asks. Default returns to 1 depth data.
        :return: JSON-ответ с данными глубины рынка.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v5/market/books"
        params = {"instId": symbol, "sz": limit}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_last_price(self, *args, **kwargs) -> Any:
        return await self.futures_ticker()
