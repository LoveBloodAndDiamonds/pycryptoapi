__all__ = [
    "init_mexc_perpetual_fix",
    "mexc_perpetual_ticker_daily_fix"
]

import asyncio

import aiohttp
from loguru import logger


class _MexcExchangeInfo:
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
