__all__ = ["GateClient"]

import time
from typing import Any, Optional, Dict

from typing_extensions import Literal

from ..abstract import AbstractClient
from ..types import JsonLike


class GateClient(AbstractClient):
    _BASE_URL: str = "https://api.gateio.ws/api/v4"

    async def klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def futures_klines(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    async def ticker(self, symbol: Optional[str] = None) -> JsonLike:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/spot/tickers"
        params = {"currency_pair": symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_ticker(self, symbol: Optional[str] = None, settle: Literal["btc", "usdt"] = "usdt") -> JsonLike:
        """
        Получает 24-часовую статистику изменения цены и объема для фьючерсного рынка.

        :param symbol: (опционально) Торговая пара, например 'BTC_USDT'. Если не указано, возвращает данные по всем парам.
        :param settle: (опционально) Постфикс торговых пар для поиска. По умолчанию: usdt
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/futures/{settle}/tickers"
        params = {"contract": symbol} if symbol else {}
        return await self._make_request(method="GET", url=url, params=params)

    async def depth(self, symbol: str, limit: int = 100) -> JsonLike:
        """
        Получает данные ордербука (глубины рынка) для спотового рынка.

        :param symbol: Торговая пара в формате 'BTC_USDT'
        :param limit: Количество уровней ордербука (доступные значения: 5, 10, 20, 50, 100, 200, 500, 1000)
        :return: JSON-ответ с ордерами на покупку и продажу.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/spot/order_book"
        params = {"currency_pair": symbol, "limit": limit}
        return await self._make_request(method="GET", url=url, params=params)

    async def funding_rate(self) -> Dict[str, Any]:
        raise NotImplementedError()

    # 200r/10s per endpoint
    async def open_interest(self, symbol: str, settle: Literal["btc", "usdt"] = "usdt") -> JsonLike:
        """
        Получает данные об открытом интересе для фьючерсных контрактов.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param settle: Тип расчета контракта (по умолчанию 'usdt', возможны значения: 'btc', 'usdt').
        :return: JSON-ответ с информацией об открытом интересе.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/futures/{settle}/contract_stats"
        params = {"contract": symbol}
        result = await self._make_request(method="GET", url=url, params=params)
        result = result[-1]
        result["symbol"] = symbol  # Patch
        result["time"] = time.time() * 1000
        return result

    async def futures_last_price(self) -> Any:
        return await self.futures_ticker()
