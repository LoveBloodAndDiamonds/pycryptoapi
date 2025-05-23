"""
По какой-то неведомой причине долб*ебы на разработчиках в OKX решили возвращать на фьючерсах контракты, а не монеты.
Этот класс служит для того, чтобы получать множитель контрактов.

Теперь реализован через асинхронный loop, чтобы не тащить блокирующий requests
в полностью асинхронный проект. Работает как фоновая задача, автоматически
умирает при закрытии event loop.
"""

__all__ = [
    "init_okx_perpetual_fix",
    "okx_perpetual_aggtrade_fix",
    "okx_perpetual_ticker_daily_fix",
]

import asyncio
import re

import aiohttp
from loguru import logger


class _OkxExchangeInfo:
    logger = logger
    precisions: dict[str, list[int]] = {}

    def __init__(self):
        self._task = None  # Ссылка на фоновую задачу

    async def run(self):
        """Асинхронно обновляет множители контрактов OKX раз в час."""
        while True:
            try:
                url = "https://www.okx.com/api/v5/public/instruments?instType=SWAP"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = (await response.json())["data"]
                        for el in data:
                            # tick_size = минимальный шаг цены
                            tick_size = el["tickSz"]
                            # step_size (теперь ctVal) = стоимость одного контракта
                            step_size = el["ctVal"]

                            # Определяем точность tick_size
                            tick_size = list(re.sub("0+$", "", tick_size))
                            if len(tick_size) == 1:
                                tick_size = 1
                            else:
                                tick_size = len(tick_size) - 2

                            self.precisions[el["instId"]] = [tick_size, float(step_size)]

            except Exception as error:
                logger.error(f"{type(error)} in async run method for OKX: {error}")
            await asyncio.sleep(60 * 60)  # Спим 1 час между обновлениями

    def get_ct_val(self, ticker: str) -> float:
        """Возвращает множитель контрактов (ctVal) для указанного тикера."""
        return self.precisions[ticker][1]

    def start(self):
        """Запускает фоновую задачу, которая обновляет данные раз в час."""
        if not self._task:
            self._task = asyncio.create_task(self.run())

    async def wait_ready(self, timeout: float = 30.0) -> None:
        """Ожидает загрузки данных об инструментах.

        Args:
            timeout: Максимальное время ожидания в секундах.

        Raises:
            TimeoutError: Если данные не загрузились за указанное время.
        """
        start_time = asyncio.get_event_loop().time()
        while not self.precisions:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError("OKX exchange info didn't load in time")
            await asyncio.sleep(0.1)


_okx_exchange_info = _OkxExchangeInfo()


async def init_okx_perpetual_fix() -> None:
    """
    Запускает объект, который обновляет данные о рынке OKX.
    """
    _okx_exchange_info.start()
    await _okx_exchange_info.wait_ready()


def okx_perpetual_aggtrade_fix(raw_msg: dict) -> dict:
    """
    Функция принимает сырое сообщение с вебсокета и возвращает его пофикшенный вариант.
    !Note: Обязательно нужно запустить _okx_exchange_info перед вызовом этой функции.
    """
    # Преобразуем данные
    for trade in raw_msg["data"]:
        try:
            trade["sz"] = str(float(trade["sz"]) * _okx_exchange_info.get_ct_val(ticker=trade["instId"]))
        except Exception as e:
            logger.error(f"Can not fix aggtrade: {trade=}: {e}")
    return raw_msg


def okx_perpetual_ticker_daily_fix(raw_data: dict) -> dict:
    """
    Функция принимает сырое сообщения с http запроса и возвращает пофикшенный вариант.
    !Note: Обязательно нужно запустить _okx_exchange_info перед вызовом этой функции.
    """
    # {'instType': 'SWAP', 'instId': 'BTC-USDT-SWAP', 'last': '104690', 'lastSz': '0.25', 'askPx': '104690',
    #  'askSz': '225.18', 'bidPx': '104689.9', 'bidSz': '734.07', 'open24h': '104492.9', 'high24h': '106853',
    #  'low24h': '104137.9', 'volCcy24h': '99054.5377', 'vol24h': '9905453.77', 'ts': '1747753958313',
    #  'sodUtc0': '105534.5', 'sodUtc8': '104750.5'},
    for ticker in raw_data["data"]:
        try:
            ticker["vol24h"] = float(ticker["volCcy24h"]) * float(ticker["last"])
        except Exception as e:
            logger.error(f"Can not fix ticker daily: {ticker=}: {e}")
    return raw_data
