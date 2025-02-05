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
        s = None
        for t in ["BTCUSDT", "ETHUSDT", "SKLUSDT"]:
            resp = await client.open_interest(symbol=t)
            r.append(resp)
            s = resp


        # Печать результата с использованием prettyprint
        pprint(r)

        a = BitgetAdapter.open_interest(raw_data=r)

        pprint(a)

        b = BitgetAdapter.open_interest(s)

        print(b)

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_bitget_funding_rate())
