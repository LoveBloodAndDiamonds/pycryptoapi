import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.bitget import BitgetClient, BitgetAdapter


async def test_bitget_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = BitgetClient(session)

        # Пример вызова функции funding_rate
        r = []
        for t in ["BTCUSDT", "ETHUSDT", "SKLUSDT"]:
            r.append(await client.open_interest(symbol=t))

        # Печать результата с использованием prettyprint
        pprint(r)

        a = BitgetAdapter.open_interest(raw_data=r)

        pprint(a)


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_bitget_funding_rate())
