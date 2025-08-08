__all__ = ["BinanceClient"]

from typing import Any, Optional, Dict, List

import aiohttp

from ..abstract import AbstractClient
from ..enums import Timeframe, Exchange
from ..exceptions import APIException
from ..types import JsonLike


class BinanceClient(AbstractClient):
    _BASE_SPOT_URL: str = "https://api.binance.com"
    _BASE_FUTURES_URL: str = "https://fapi.binance.com"

    async def _handle_response(self, response: aiohttp.ClientResponse) -> JsonLike:
        """
        Функция обрабатывает ответ от HTTP запроса.
        :return:
        """
        # Handle 429 status code
        if response.status == 429:
            raise APIException(429, "Rate limit is violated...")

        # Handle other bad codes
        response.raise_for_status()

        # Handle used weight
        try:
            used_weight: int = int(response.headers.get("x-mbx-used-weight-1m"))
        except Exception as e:
            used_weight: int = 0
            self._logger.error(f"Can not handle used weight: {e}")

        result = await response.json()

        # try to log result if it's not too large
        try:
            result_str: str = str(result)
            self._logger.debug(
                f"Response: {result_str[:100]} {'...' if len(result_str) > 100 else ''}. Used weight={used_weight}")
        except Exception as e:
            self._logger.error(f"Error while log response: {e}")

        return result

    # 1 for a single symbol; 40 when the symbol parameter is omitted
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

    # 1 for a single symbol; 40 when the symbol parameter is omitted
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

    # 1 for a single symbol; 10 when the symbol parameter is omitted
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

    # 1 weight
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

    async def klines(
            self,
            symbol: str,
            interval: Timeframe,
            limit: int = 500,
            start_time: Optional[str] = None,
            end_time: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Получает свечи с указанного торгового инструмента на спотовом рынке Binance

        Используется эндпоинт: GET /api/v3/klines

        Пример ответа:
        [
          [
            1499040000000,      // Kline open time
            "0.01634790",       // Open price
            "0.80000000",       // High price
            "0.01575800",       // Low price
            "0.01577100",       // Close price
            "148976.11427815",  // Volume
            1499644799999,      // Kline Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "0"                 // Unused field, ignore.
          ]
        ]
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/klines"
        params = self.filter_params(
            {
                "symbol": symbol,
                "interval": interval.to_exchange_format(Exchange.BINANCE),
                "limit": limit,
                "startTime": start_time,
                "endTime": end_time
            }
        )
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_klines(
            self,
            symbol: str,
            interval: Timeframe,
            limit: int = 500,
            start_time: Optional[str] = None,
            end_time: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Получает свечи с указанного торгового инструмента на фьючерсном рынке Binance

        Используется эндпоинт: GET /api/v3/klines

        Пример ответа:
        [
          [
            1499040000000,      // Kline open time
            "0.01634790",       // Open price
            "0.80000000",       // High price
            "0.01575800",       // Low price
            "0.01577100",       // Close price
            "148976.11427815",  // Volume
            1499644799999,      // Kline Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "0"                 // Unused field, ignore.
          ]
        ]
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/klines"
        params = self.filter_params(
            {
                "symbol": symbol,
                "interval": interval.to_exchange_format(Exchange.BINANCE),
                "limit": limit,
                "startTime": start_time,
                "endTime": end_time
            }
        )
        return await self._make_request(method="GET", url=url, params=params)

    async def depth(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Получает стакан ордеров (Order Book) для спотового рынка Binance.

        Используется эндпоинт: GET /api/v3/depth

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param limit: Количество уровней стакана (допустимые значения: 5, 10, 20, 50, 100, 500, 1000, 5000).
        :return: JSON-ответ, содержащий массивы bids и asks.
        """
        url = f"{self._BASE_SPOT_URL}/api/v3/depth"
        params = {"symbol": symbol, "limit": limit}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_depth(self, symbol: str, limit: int = 100) -> Dict[str, Any]:
        """
        Получает стакан ордеров (Order Book) для фьючерсного рынка Binance.

        Используется эндпоинт: GET /fapi/v1/depth

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param limit: Количество уровней стакана (допустимые значения: 5, 10, 20, 50, 100, 500, 1000, 5000).
        :return: JSON-ответ, содержащий массивы bids и asks.
        """
        url = f"{self._BASE_FUTURES_URL}/fapi/v1/depth"
        params = {"symbol": symbol, "limit": limit}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_last_price(self, symbol: Optional[str] = None) -> Any:
        """

        """
        return await self.futures_ticker(symbol)
    