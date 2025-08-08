__all__ = ["BitgetClient"]

from typing import Any, Optional, Dict

from ..abstract import AbstractClient


class BitgetClient(AbstractClient):

    _BASE_URL: str = "https://api.bitget.com"

    async def klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    # Frequency limit: 20 times/1s (IP)
    async def ticker(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v2/spot/market/tickers"
        params = {'symbol': symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    # Frequency limit: 20 times/1s (IP)
    async def futures_ticker(self, product_type: str = "USDT-FUTURES") -> Dict[str, Any]:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param product_type: Тип продукта (по умолчанию: 'USDT-FUTURES' для USDT-Margined Futures).
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v2/mix/market/tickers"
        params = {'productType': product_type}
        return await self._make_request(method="GET", url=url, params=params)

    # Frequency limit: 20 times/1s (IP)
    async def funding_rate(self, symbol: Optional[str] = None, product_type: str = "USDT-FUTURES") -> Dict[str, Any]:
        """
        Получает текущую ставку финансирования для указанного символа.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param product_type: Тип продукта (по умолчанию: 'USDT-FUTURES' для USDT-Margined Futures).
        :return: JSON-ответ с текущей ставкой финансирования.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/api/v2/mix/market/current-fund-rate"
        params = {
            "productType": product_type,
        }
        if symbol:
            params["symbol"] = symbol
        return await self._make_request(method="GET", url=url, params=params)

    # Frequency limit: 20 times/1s (IP)
    async def open_interest(self, product_type: str = "USDT-FUTURES") -> Dict[str, Any]:
        """
        Получает текущий открытый интерес для указанного символа.

        :param product_type: Тип продукта (по умолчанию: 'USDT-FUTURES' для USDT-Margined Futures).
        :return: JSON-ответ с текущим открытым интересом.
        :raises Exception: Если запрос не выполнен успешно.
        """
        return await self.futures_ticker(product_type=product_type)

    # Frequency limit: 20 times/1s (IP)
    async def depth(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Получает стакан ордеров (Order Book) для спотового рынка Bitget.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param limit: Количество уровней стакана (1-200, по умолчанию 100).
        :return: JSON-ответ, содержащий массивы bids и asks.
        """
        url = f"{self._BASE_URL}/api/v2/spot/market/orderbook"
        params = {"symbol": symbol, "limit": limit}
        return await self._make_request(method="GET", url=url, params=params)

    # Frequency limit: 20 times/1s (IP)
    async def futures_depth(self, symbol: str, product_type: str = "USDT-FUTURES", limit: int = 100) -> Dict[str, Any]:
        """
        Получает стакан ордеров (Order Book) для фьючерсного рынка Bitget.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param product_type: Тип продукта (по умолчанию 'USDT-FUTURES').
        :param limit: Количество уровней стакана (1-200, по умолчанию 100).
        :return: JSON-ответ, содержащий массивы bids и asks.
        """
        url = f"{self._BASE_URL}/api/v2/mix/market/orderbook"
        params = {"symbol": symbol, "productType": product_type, "limit": limit}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_last_price(self, product_type: str = "USDT-FUTURES") -> Any:
        return await self.futures_ticker(product_type)
