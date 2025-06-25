__all__ = [
    "init_mexc_perpetual_fix",
    "mexc_perpetual_ticker_daily_fix",
    "mexc_perpetual_open_interest_fix",
    "mexc_perpetual_aggtrade_fix",
]

import asyncio

import aiohttp
from loguru import logger


class _MexcExchangeInfo:
    logger = logger

    def __init__(self):
        self._contract_sizes: dict[str, float] = {}
        self._task = None
        self._is_running = True

    async def _fetch_contract_sizes(self) -> dict:
        """Fetch contract sizes from MEXC."""
        url = "https://contract.mexc.com/api/v1/contract/detail"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def _update_contract_sizes_task(self):
        """Background task to periodically update contract sizes."""
        while self._is_running:
            try:
                data = await self._fetch_contract_sizes()
                for contract in data["data"]:
                    self._contract_sizes[contract["symbol"]] = float(contract["contractSize"])
            except Exception as e:
                logger.error(f"Failed to update contract sizes: {e}")
            await asyncio.sleep(60 * 60)  # обновляем раз в час

    def get_contract_size(self, symbol: str) -> float:
        """Returns the contract size for a given symbol."""
        return self._contract_sizes[symbol]

    def start(self):
        """Starts the background task."""
        if not self._task:
            self._task = asyncio.create_task(self._update_contract_sizes_task())

    async def wait_ready(self, timeout: float = 30.0) -> None:
        """Waits for contract sizes to be loaded."""
        start_time = asyncio.get_event_loop().time()
        while not self._contract_sizes:
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError("MEXC contract sizes didn't load in time")
            await asyncio.sleep(0.1)


_mexc_exchange_info = _MexcExchangeInfo()


async def init_mexc_perpetual_fix() -> None:
    """Initializes and starts the MEXC contract size updater."""
    _mexc_exchange_info.start()
    await _mexc_exchange_info.wait_ready()


def mexc_perpetual_ticker_daily_fix(raw_data: dict) -> dict:
    """
    Функция принимает сырое сообщения с http запроса и возвращает пофикшенный вариант.
    !Note: Обязательно нужно запустить _mexc_exchange_info перед вызовом этой функции.
    """
    # {'contractId': 10,
    #  'symbol': 'BTC_USDT',
    #  'lastPrice': 109630.3,
    #  'bid1': 109630.2,
    #  'ask1': 109630.3,
    #  'volume24': 378537842,
    #  'amount24': 4171772565.52051,
    #  'holdVol': 253676226,
    #  'lower24Price': 107261.5,
    #  'high24Price': 111957.2,
    #  'riseFallRate': -0.0144,
    #  'riseFallValue': -1612.9,
    #  'indexPrice': 109691.3,
    #  'fairPrice': 109644.5,
    #  'fundingRate': 9.7e-05,
    #  'maxBidPrice': 120660.4,
    #  'minAskPrice': 98722.1,
    #  'timestamp': 1748014472368,
    #  'riseFallRates': {'zone': 'UTC+8',
    #                    'r': -0.0144,
    #                    'v': -1612.9,
    #                    'r7': 0.0621,
    #                    'r30': 0.2063,
    #                    'r90': 0.118,
    #                    'r180': 0.1138,
    #                    'r365': 0.5553},
    #  'riseFallRatesOfTimezone': [-0.011, -0.0182, -0.0144]}
    for ticker in raw_data["data"]:
        try:
            ticker["volume24"] = ticker["volume24"] * _mexc_exchange_info.get_contract_size(ticker["symbol"])
        except Exception as e:
            logger.error(f"Can not fix ticker daily: {ticker=}: {e}")
    return raw_data


def mexc_perpetual_open_interest_fix(raw_data: dict) -> dict:
    """
    Функция принимает сырой ответ с http запроса открытого интереса с фьючерсов MEXC.
    Возвращает пофикшенный вариант с правильным значением открытого интереса.
    """
    # {'amount24': 101140.06,
    #  'ask1': 2.948,
    #  'bid1': 2.947,
    #  'contractId': 1149,
    #  'fairPrice': 2.948,
    #  'fundingRate': 0.0001,
    #  'high24Price': 3.161,
    #  'holdVol': 47206,
    #  'indexPrice': 2.948,
    #  'lastPrice': 2.948,
    #  'lower24Price': 2.845,
    #  'maxBidPrice': 3.537,
    #  'minAskPrice': 2.358,
    #  'riseFallRate': 0.0109,
    #  'riseFallRates': {'r': 0.0109,
    #                    'r30': 0.1844,
    #                    'r7': 0.02,
    #                    'v': 0.032,
    #                    'zone': 'UTC+8'},
    #  'riseFallRatesOfTimezone': [-0.034, -0.0419, 0.0109],
    #  'riseFallValue': 0.032,
    #  'symbol': 'NEAR_USDC',
    #  'timestamp': 1748020547110,
    #  'volume24': 33342},
    for item in raw_data["data"]:
        try:
            item["holdVol"] = item["holdVol"] * _mexc_exchange_info.get_contract_size(item["symbol"])
        except Exception as e:
            logger.debug(f"Can not fix open interest: {item=}: {e}")
    return raw_data


def mexc_perpetual_aggtrade_fix(raw_msg: dict) -> dict:
    """
    Функция принимает сырое сообщение с вебсокета и возвращает его пофикшенный вариант.
    !Note: Обязательно нужно запустить _mexc_exchange_info перед вызовом этой функции.
    """
    # {'symbol': 'ETH_USDT', 'data': {'p': 2575.2, 'v': 1, 'T': 2, 'O': 1, 'M': 2, 't': 1748023214750}, 'channel': 'push.deal', 'ts': 1748023214750}
    # Преобразуем данные
    try:
        raw_msg["data"]["v"] = raw_msg["data"]["v"] * _mexc_exchange_info.get_contract_size(raw_msg["symbol"])
    except Exception as e:
        logger.error(f"Can not fix aggtrade: {raw_msg=}: {e}")
    return raw_msg
