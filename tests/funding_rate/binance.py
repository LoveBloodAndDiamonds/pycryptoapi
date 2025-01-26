import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.binance import BinanceClient, BinanceAdapter


async def test_binance_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = BinanceClient(session)

        # Пример вызова функции funding_rate
        result = await client.funding_rate()

        # Печать результата с использованием prettyprint
        pprint(result)
        print(len(result), "LEN")

        a = BinanceAdapter.funding_rate(raw_data=result)

        sorted_dict = sorted(a.items(), key=lambda item: item[1])

        pprint(sorted_dict)
        print(len(a), "LEN")


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_binance_funding_rate())
