__all__ = ["RedisStorage", ]

from datetime import datetime
from typing import Dict, Any, Optional

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

from pycryptoapi.enums import StorageKeys, Exchange, MarketType
from pycryptoapi.types import TickerDailyItem


class RedisStorage:
    """Вспомогательный клиент для работы с редисом."""

    MARK_TIME: bool = True
    '''Записывать время обновления?'''

    def __init__(self, conn: redis.Redis, logger: Logger = loguru.logger) -> None:
        self._redis: redis.Redis = conn
        self._logger: Logger = logger

    async def _get(self, key: str, default=None) -> Optional[Any]:
        """Вспомогательный метод для получения значения из Redis."""
        value = await self._redis.get(key)
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
        try:
            # Устанавливаем основной ключ
            await self._redis.set(key, orjson.dumps(value))
            self._logger.info(f"Key '{key}' updated in Redis.")

            if self.MARK_TIME:
                # Добавляем ключ для временной метки
                update_time = datetime.now().isoformat()
                await self._redis.set(f"{StorageKeys.TIME_MARK}:{key}", update_time)
                self._logger.info(f"Time for '{StorageKeys.TIME_MARK}:{key}' set to {update_time} in Redis.")
        except Exception as e:
            self._logger.error(f"Failed to set value for key '{key}' in Redis: {e}")
            raise

    def _keygen(self, *args: str) -> str:
        return ":".join(args)

    async def set_cmc_rating(self, data: Dict[str, int]) -> None:
        """Установить CMC рейтинг в Redis."""
        await self._set(StorageKeys.CMC_RATING, data)

    async def get_cmc_rating(self) -> Optional[Dict[str, int]]:
        """Получить CMC рейтинг из Redis."""
        return await self._get(StorageKeys.CMC_RATING)

    async def set_tickers_24h(self, data: Dict[str, TickerDailyItem], exchange: Exchange,
                              market_type: MarketType) -> None:
        """Установить Ticker24h в Redis."""
        await self._set(self._keygen(StorageKeys.TICKERS_DAILY, exchange, market_type), data)

    async def get_tickers_24h(self, exchange: Exchange, market_type: MarketType) -> Optional[
        Dict[str, TickerDailyItem]]:
        """Получить Ticker24h из Redis."""
        return await self._get(self._keygen(StorageKeys.TICKERS_DAILY, exchange, market_type))

    async def set_funding_rate(self, data: Dict[str, float], exchange: Exchange) -> None:
        """Установить FundingRate в Redis."""
        await self._set(self._keygen(StorageKeys.FUNDING_RATE, ex), data)

    async def get_funding_rate(self, exchange: Exchange) -> Dict[str, float]:
        """Получить FundingRate из Redis."""
        return await self._get(self._keygen(StorageKeys.FUNDING_RATE, ex))
