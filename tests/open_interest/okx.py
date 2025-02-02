import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.okx import OkxClient, OkxAdapter


async def test_okx_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = OkxClient(session)

        # Пример вызова функции funding_rate
        result = []
        for t in ["BTC", "ETH", "XRP"]:
            result.append(await client.open_interest(symbol=t + "-USDT-SWAP"))

        # Печать результата с использованием prettyprint
        pprint(result)

        a = OkxAdapter.open_interest(raw_data=result)

        pprint(a)


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_okx_funding_rate())
