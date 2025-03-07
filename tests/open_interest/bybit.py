import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.bybit import BybitClient, BybitAdapter


async def test_bybit_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        # async with session.get("https://api-testnet.bybit.com/v5/market/funding/history?category=linear&symbol=BTCUSDT") as res:
        client = BybitClient(session)

        # Пример вызова функции funding_rate
        result = await client.open_interest()

        # Печать результата с использованием prettyprint
        # pprint(result)

        a = BybitAdapter.open_interest(raw_data=result)

        pprint(a)


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_bybit_funding_rate())
