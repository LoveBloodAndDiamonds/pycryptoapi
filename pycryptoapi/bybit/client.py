__all__ = ["BybitClient"]

from typing import Any, Optional, Dict, Literal

from ..abstract import AbstractClient
from ..enums import Timeframe, Exchange


class BybitClient(AbstractClient):
    _BASE_URL: str = "https://api.bybit.kz"  # Kazakhstan as default

    @classmethod
    def set_tld(cls, tld: Literal["nl", "tr", "hk", "testnet", "kz"]) -> None:
        """
        Устанавливает .tld для HTTP запросов.
        :param tld:
        :return:
        """
        if tld == "nl":
            cls._BASE_URL: str = "https://api.bybit.nl"
        elif tld == "tr":
            cls._BASE_URL: str = "https://api.bybit-tr.com"
        elif tld == "hk":
            cls._BASE_URL: str = "https://api.byhkbit.com"
        elif tld == "kz":
            cls._BASE_URL: str = "https://api.bybit.kz"
        elif tld == "testnet":
            cls._BASE_URL: str = "https://api-testnet.bybit.com"
        else:
            raise ValueError(f"Wrong tld! {tld} is not available for this exchange. "
                             f"Available tld's: ['nl', 'tr' 'hk', 'testnet' 'kz']")

    async def ticker(
            self,
            symbol: Optional[str] = None,
            _category: Literal["spot", "linear"] = "spot"
    ) -> Dict[str, Dict[str, Any]]:
        """
        Получает 24-часовую статистику изменения цены и объема для спотового рынка.

        :param symbol: (опционально) Торговая пара, например 'BTCUSDT'. Если не указано, возвращает данные по всем парам.
        :param _category: Не указывается в аргументах, используется внутри клиента.
        :return: JSON-ответ с данными статистики.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/v5/market/tickers"
        params = {"category": _category}
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
        return await self.ticker(symbol=symbol, _category="linear")

    async def funding_rate(self, symbol: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Получает данные, которые содержат информацию о текущей ставке финансирования.

        :param symbol: Торговая пара, например 'BTCUSDT'. Опциольнально.
        :return: JSON-ответ с данными ставок финансирования.
        :raises Exception: Если запрос не выполнен успешно.
        """
        return await self.ticker(symbol=symbol, _category="linear")

    async def open_interest(self, symbol: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        Получает данные, которые содержат информацию о открытом интересе.

        :param symbol: Торговая пара, например 'BTCUSDT'. Опциольнально.
        :return: JSON-ответ с данными открытого интереса.
        :raises Exception: Если запрос не выполнен успешно.
        """
        return await self.ticker(symbol=symbol, _category="linear")

    async def klines(
            self,
            symbol: str,
            interval: Timeframe,
            start: Optional[int] = None,
            end: Optional[int] = None,
            limit: Optional[int] = 200,
            _category: Literal["spot", "linear"] = "spot",
    ) -> Dict[str, Any]:
        """
        Получает данные, которые содержат список свечей..

        :param symbol: Торговая пара.
        :param interval: Интервал.
        :param start: Опционально. Время начала получения данных.
        :param end: Опционально. Время окончания получения данных.
        :param limit: Опционально. Количество свечей.
        :param _category: Категория рынка.
        :return: JSON-ответ с данными свеч.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/v5/market/kline"
        params = {
            "category": _category,
            "symbol": symbol,
            "interval": interval.to_exchange_format(Exchange.BYBIT),
            "limit": limit
        }
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        return await self._make_request(method="GET", url=url, params=params)

    async def futures_klines(
            self,
            symbol: str,
            interval: Timeframe,
            start: Optional[int] = None,
            end: Optional[int] = None,
            limit: Optional[int] = 200,
    ) -> Dict[str, Any]:
        """
        Получает данные, которые содержат список свечей.

        :param symbol: Торговая пара.
        :param interval: Интервал.
        :param start: Опционально. Время начала получения данных.
        :param end: Опционально. Время окончания получения данных.
        :param limit: Опционально. Количество свечей.
        :return: JSON-ответ с данными свеч.
        :raises Exception: Если запрос не выполнен успешно.
        """
        return await self.klines(
            symbol=symbol, interval=interval, start=start, end=end, limit=limit, _category="linear")

    async def depth(
        self,
        symbol: str,
        limit: int = 50,
        _category: Literal["spot", "linear"] = "spot"
    ) -> Dict[str, Any]:
        """
        Получает данные ордербука (глубину рынка) для указанного символа.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param limit: Количество записей (по умолчанию 50).
        :param _category: Категория рынка (по умолчанию "spot").
        :return: JSON-ответ с данными ордербука.
        :raises Exception: Если запрос не выполнен успешно.
        """
        url = f"{self._BASE_URL}/v5/market/orderbook"
        params = {
            "category": _category,
            "symbol": symbol,
            "limit": limit
        }
        return await self._make_request(method="GET", url=url, params=params)

    async def futures_depth(
        self,
        symbol: str,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Получает данные ордербука для фьючерсов.
        """
        return await self.depth(symbol=symbol, limit=limit, _category="linear")

    async def futures_last_price(self) -> Any:
        return await self.futures_ticker()
