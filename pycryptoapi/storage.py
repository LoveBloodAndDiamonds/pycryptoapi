__all__ = ["RedisStorage", ]

import enum
import time
from datetime import datetime
from typing import Dict, Any, Optional, List

import loguru
import orjson
from loguru._logger import Logger  # noqa

try:
    import redis
except ImportError:
    raise ImportError(
        "RedisStorage requires the `redis` package. Install it with:\n"
        "```pip install redis``` or ```poetry add redis```"
    )

from pycryptoapi.enums import Exchange, MarketType
from pycryptoapi.types import TickerDailyItem, OpenInterestItem


class RedisStorage:
    """Вспомогательный клиент для работы с редисом."""

    MARK_TIME: bool = True
    '''Записывать время обновления?'''

    class _StorageKeys(enum.StrEnum):
        TIME_MARK: str = "TIME_MARK"
        CMC_RATING: str = "CMC_RATING"
        TICKERS_24H: str = "TICKERS_24H"
        FUNDING_RATE: str = "FUNDING_RATE"
        OPEN_INTEREST: str = "OPEN_INTEREST"

    def __init__(self, conn: redis.Redis, logger: Optional[Logger] = loguru.logger) -> None:
        self._redis: redis.Redis = conn
        self._logger: Logger = logger

    async def _get(self, key: str, default=None) -> Optional[Any]:
        """Вспомогательный метод для получения значения из Redis."""
        start_time = time.perf_counter()  # Начало замера времени
        value = await self._redis.get(key)

        # Логируем время выполнения запроса
        elapsed_time = time.perf_counter() - start_time
        self._logger.debug(f"Time taken to get key '{key}' from Redis: {elapsed_time:.4f} seconds.")

        if value is None:
            self._logger.error(f"Key '{key}' not found in Redis.")
            return default
        try:
            return orjson.loads(value)
        except orjson.JSONDecodeError as e:
            self._logger.error(f"Failed to decode value for key '{key}' in Redis: {e}")
            return default

    async def _set(self, key: str, value: Any) -> None:
        """Вспомогательный метод для установки значения в Redis с добавлением временной метки."""
        start_time = time.perf_counter()  # Начало замера времени
        try:
            # Устанавливаем основной ключ
            await self._redis.set(key, orjson.dumps(value))
            elapsed_time = time.perf_counter() - start_time
            self._logger.debug(f"Time taken to set key '{key}' in Redis: {elapsed_time:.4f} seconds.")

            self._logger.info(f"Key '{key}' updated in Redis.")

            if self.MARK_TIME:
                # Добавляем ключ для временной метки
                update_time = datetime.now().isoformat()

                # Записываем временную метку
                await self._redis.set(f"{self._StorageKeys.TIME_MARK}:{key}", update_time)
                self._logger.debug(f"Time for '{self._StorageKeys.TIME_MARK}:{key}' set to {update_time} in Redis.")
        except Exception as e:
            self._logger.error(f"Failed to set value for key '{key}' in Redis: {e}")
            raise

    def _keygen(self, *args: str) -> str:
        return ":".join(args)

    async def set_cmc_rating(self, data: Dict[str, int]) -> None:
        """Установить CMC рейтинг в Redis."""
        await self._set(self._StorageKeys.CMC_RATING, data)

    async def get_cmc_rating(self) -> Optional[Dict[str, int]]:
        """Получить CMC рейтинг из Redis."""
        return await self._get(self._StorageKeys.CMC_RATING)

    async def set_tickers_24h(self, data: Dict[str, TickerDailyItem], ex: Exchange, m_type: MarketType) -> None:
        """Установить Ticker24h в Redis."""
        await self._set(self._keygen(self._StorageKeys.TICKERS_24H, ex, m_type), data)

    async def get_tickers_24h(self, ex: Exchange, m_type: MarketType) -> Optional[Dict[str, TickerDailyItem]]:
        """Получить Ticker24h из Redis."""
        return await self._get(self._keygen(self._StorageKeys.TICKERS_24H, ex, m_type))

    async def set_funding_rate(self, data: Dict[str, float], ex: Exchange) -> None:
        """Установить FundingRate в Redis."""
        await self._set(self._keygen(self._StorageKeys.FUNDING_RATE, ex), data)

    async def get_funding_rate(self, ex: Exchange) -> Optional[Dict[str, float]]:
        """Получить FundingRate из Redis."""
        return await self._get(self._keygen(self._StorageKeys.FUNDING_RATE, ex))

    async def set_open_interest(self, data: Dict[str, List[OpenInterestItem]], ex: Exchange) -> None:
        """Установить OpenInterest в Redis."""
        await self._set(self._keygen(self._StorageKeys.OPEN_INTEREST, ex), data)

    async def get_open_interest(self, ex: Exchange) -> Optional[Dict[str, List[OpenInterestItem]]]:
        """Получить открытый интерес из Redis."""
        return await self._get(self._keygen(self._StorageKeys.OPEN_INTEREST, ex))
