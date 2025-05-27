import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.bitget import BitgetClient, BitgetAdapter


async def test_bitget_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = BitgetClient(session)

        # Пример вызова функции funding_rate
        r = await client.funding_rate()

        # Печать результата с использованием prettyprint
        pprint(r)

        a = BitgetAdapter.funding_rate(raw_data=r)

        pprint(a)


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_bitget_funding_rate())
