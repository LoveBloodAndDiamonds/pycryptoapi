"""
По аналогии с OKX и MEXC, разработчики XT возвращают контракты вместо монет.
Этот класс служит для того, чтобы получать множитель контрактов.

Реализован через асинхронный loop, чтобы не блокировать проект.
Работает как фоновая задача, автоматически умирает при закрытии event loop.
"""

__all__ = [
    "init_xt_perpetual_fix",
    "xt_perpetual_aggtrade_fix",
]

import asyncio
import aiohttp
from loguru import logger


class _XtExchangeInfo:
    logger = logger
    precisions: dict[str, float] = {}

    def __init__(self):
        self._task = None  # Ссылка на фоновую задачу

    async def run(self):
        """Асинхронно обновляет множители контрактов XT раз в час."""
        while True:
            try:
                url = "https://fapi.xt.com/future/market/v3/public/symbol/list"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = (await response.json())["result"]["symbols"]
                        for el in data:
                            # symbol -> контрактный тикер
                            # contractSize -> стоимость одного контракта
                            symbol = el["symbol"]
                            contract_size = float(el["contractSize"])

                            self.precisions[symbol] = contract_size

            except Exception as error:
                logger.error(f"{type(error)} in async run method for XT: {error}")
            await asyncio.sleep(60 * 60)  # Спим 1 час между обновлениями

    def get_ct_val(self, ticker: str) -> float:
        """Возвращает множитель контрактов (contractSize) для указанного тикера."""
        return self.precisions[ticker]

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
                raise TimeoutError("XT exchange info didn't load in time")
            await asyncio.sleep(0.1)


_xt_exchange_info = _XtExchangeInfo()


async def init_xt_perpetual_fix() -> None:
    """
    Запускает объект, который обновляет данные о рынке XT.
    """
    _xt_exchange_info.start()
    await _xt_exchange_info.wait_ready()


def xt_perpetual_aggtrade_fix(raw_msg: dict) -> dict:
    """
    Функция принимает сырое сообщение с вебсокета и возвращает его пофикшенный вариант.
    !Note: Обязательно нужно запустить _xt_exchange_info перед вызовом этой функции.
    {'topic': 'trade', 'event': 'trade@btc_usdt', 'data': {'s': 'btc_usdt', 'p': '118300', 'a': '4', 'm': 'ASK',
    't': 1753710542640}}
    """
    # Преобразуем данные
    try:
        raw_msg["data"]["a"] = float(raw_msg["data"]["a"]) * _xt_exchange_info.get_ct_val(raw_msg["data"]["s"])
    except Exception as e:
        logger.error(f"Can not fix aggtrade: {raw_msg=}: {e}")
    return raw_msg
