"""
По аналогии с OKX и MEXC и XT, разработчики KCEX возвращают контракты вместо монет.
Этот класс служит для того, чтобы получать множитель контрактов.

Реализован через асинхронный loop, чтобы не блокировать проект.
Работает как фоновая задача, автоматически умирает при закрытии event loop.
"""

__all__ = [
    "init_kcex_perpetual_fix",
    "kcex_perpetual_aggtrade_fix",
    "kcex_perpetual_open_interest_fix",
]

import asyncio

import aiohttp
from loguru import logger


class _KcexExchangeInfo:
    logger = logger
    precisions: dict[str, float] = {}

    def __init__(self):
        self._task = None  # Ссылка на фоновую задачу

    async def run(self):
        """Асинхронно обновляет множители контрактов XT раз в час."""
        while True:
            try:
                url = "https://www.kcex.com/fapi/v1/contract/detailV2?client=web"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = (await response.json())["data"]
                        for el in data:
                            # symbol -> контрактный тикер
                            # contractSize -> стоимость одного контракта
                            symbol = el["symbol"]
                            contract_size = float(el["cs"])

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


_kcex_exchange_info = _KcexExchangeInfo()


async def init_kcex_perpetual_fix() -> None:
    """
    Запускает объект, который обновляет данные о рынке Kcex.
    """
    _kcex_exchange_info.start()
    await _kcex_exchange_info.wait_ready()


def kcex_perpetual_aggtrade_fix(raw_msg: dict) -> dict:
    """
    Функция принимает сырое сообщение с вебсокета и возвращает его пофикшенный вариант.
    !Note: Обязательно нужно запустить _kcex_exchange_info перед вызовом этой функции.
    {'symbol': 'TRX_USDT', 'data': [{'p': 0.33793, 'v': 2, 'T': 1, 'O': 3, 'M': 1, 't': 1756575883544}], 'channel': 'push.deal', 'ts': 1756575883544}
    """
    if raw_msg.get("channel") == "pong":
        return raw_msg
    try:
        symbol = raw_msg["symbol"]
        ct_val = _kcex_exchange_info.get_ct_val(symbol)
        for item in raw_msg["data"]:
            item["v"] *= ct_val
    except Exception as e:
        logger.debug(f"Can not fix aggtrade: {raw_msg=}: {e}")
    return raw_msg


def kcex_perpetual_open_interest_fix(raw_data: dict) -> dict:
    """
    Функция принимает сырой ответ с http запроса и возвращает пофикшенный вид, где
    в качестве ОИ не контракты, а монеты.

    {'code': 0,
     'data': [{'amount24': 4450393505.06824,
               'ask1': 108690.8,
               'bid1': 108690.7,
               'contractId': 1,
               'fairPrice': 108691.3,
               'fundingRate': 4.1e-05,
               'high24Price': 108879.6,
               'holdVol': 19809470,
               'indexPrice': 108749.7,
               'lastPrice': 108690.7,
               'lower24Price': 107291.7,
               'maxBidPrice': 125062.1,
               'minAskPrice': 92437.2,
               'riseFallRate': -0.0012,
               'riseFallRates': {'r': -0.0012,
                                 'r180': 0.2043,
                                 'r30': -0.0765,
                                 'r365': 0.8547,
                                 'r7': -0.0552,
                                 'r90': 0.035,
                                 'v': -136.3,
                                 'zone': 'UTC+8'},
               'riseFallRatesOfTimezone': [0.0025, 0.0034, -0.0012],
               'riseFallValue': -136.3,
               'symbol': 'BTC_USDT',
               'timestamp': 1756577586007,
               'volume24': 410864085},
               { ... }, ...
    }
    """
    for item in raw_data["data"]:
        ct_val = _kcex_exchange_info.get_ct_val(item["symbol"])
        item["holdVol"] *= ct_val
    return raw_data
