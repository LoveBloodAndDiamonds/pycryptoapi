import itertools
import logging
import time
from typing import Dict, Any, Literal, Optional, Self, Union
from typing import List

import aiohttp
import loguru
from loguru._logger import Logger  # noqa

from ..abstract import BaseClient


class CoinalyzeClient(BaseClient):
    """Клиент для работы с coinalyze.com"""

    _BASE_URL: str = "https://api.coinalyze.net/v1"

    def __init__(
            self,
            session: aiohttp.ClientSession,
            api_keys: Union[List[str], str],
            max_retries: Optional[int] = 3,
            retry_delay: Optional[int | float] = 0.1,
            logger: logging.Logger | Logger = loguru.logger,
    ) -> None:
        super().__init__(session=session, logger=logger, max_retries=max_retries, retry_delay=retry_delay)

        # next(self._keys_generator) to use it
        self._keys_generator = itertools.cycle(api_keys if isinstance(api_keys, list) else [api_keys])

    @classmethod
    async def create(
            cls,
            session: Optional[aiohttp.ClientSession] = None,
            logger: logging.Logger | Logger = loguru.logger,
            max_retries: Optional[int] = 3,
            retry_delay: Optional[int | float] = 0.1,
            **kwargs
    ) -> Self:
        """
        Создает инстанцию клиента.
        Создать клиент можно и через __init__, но в таком случае session: aiohttp.ClientSession - обязательный параметр.
        :return:
        """
        api_keys: Union[List[str], str, None] = kwargs.get("api_keys")
        if not api_keys:
            raise ValueError("api_key required paramets and it must be a string")

        return cls(
            api_keys=api_keys,
            session=session or aiohttp.ClientSession(),
            logger=logger,
            max_retries=max_retries,
            retry_delay=retry_delay
        )

    async def open_interest(
            self,
            tickers: Union[List[str], str],
            timeframe: Literal[
                "1min", "5min", "15min", "30min",
                "1hour", "2hour", "4hour", "6hour",
                "12hour", "daily", "weekly"],
            limit: int
    ) -> List[Dict[str, Any]]:
        """ Returns open interest history.
        Tickers example: ["BTCUSDT_PERP.{E}", "ETHUSDT_PERP.{E}"] or "BTCUSDT_PERP.{E},ETHUSDT_PERP.{3}"
         """
        start, end = self._get_request_time(timeframe=timeframe, limit=limit)
        return await self._make_request(
            "GET",
            self._BASE_URL + "/open-interest-history",
            {
                "symbols": tickers if isinstance(tickers, str) else ",".join(tickers),
                "interval": timeframe,
                "from": start,
                "to": end,
                "convert_to_usd": "false"
            },
            headers={"api_key": next(self._keys_generator)},
        )

    async def liquidations(
            self,
            tickers: Union[List[str], str],
            timeframe: Literal[
                "1min", "5min", "15min", "30min",
                "1hour", "2hour", "4hour", "6hour",
                "12hour", "daily", "weekly"],
            limit: int,
            convert_to_usd: bool = False
    ) -> List[Dict[str, Any]]:
        """ Returns liquidations history.
         Tickers example: ["BTCUSDT_PERP.{E}", "ETHUSDT_PERP.{E}"] or "BTCUSDT_PERP.{E},ETHUSDT_PERP.{3}"
         """
        start, end = self._get_request_time(timeframe=timeframe, limit=limit)
        return await self._make_request(
            "GET",
            self._BASE_URL + "/liquidation-history",
            {
                "symbols": tickers if isinstance(tickers, str) else ",".join(tickers),
                "interval": timeframe,
                "from": start,
                "to": end,
                "convert_to_usd": "true" if convert_to_usd else "false"
            },
            headers={"api_key": next(self._keys_generator)},
        )

    async def exchanges(self) -> List[Dict[str, str]]:
        """Returns list of supported exhanges."""
        return await self._make_request(
            "GET",
            self._BASE_URL + "/exchanges",
            headers={"api_key": next(self._keys_generator)},
        )

    def _get_request_time(self, timeframe: str, limit: int) -> tuple[int, int]:
        """ Function defines start and end time. """
        timeframe_to_seconds: int = {
            "1min": 60,
            "5min": 60 * 5,
            "15min": 60 * 15,
            "30min": 60 * 30,
            "1hour": 60 * 60,
            "2hour": 60 * 60 * 2,
            "4hour": 60 * 60 * 4,
            "6hour": 60 * 60 * 6,
            "12hour": 60 * 60 * 12,
            "daily": 60 * 60 * 24,
            "weekly": 60 * 60 * 24 * 7,
        }[timeframe]
        return int(time.time() - timeframe_to_seconds * limit - 3), int(time.time() + 10)
