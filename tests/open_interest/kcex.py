from pprint import pprint

import aiohttp

from pycryptoapi.enums import Exchange, MarketType
from pycryptoapi.kcex import KcexClient, KcexAdapter
import asyncio

from pycryptoapi.fixes import init_kcex_perpetual_fix, kcex_perpetual_open_interest_fix


async def test_mexc_funding_rate():
    await init_kcex_perpetual_fix()

    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = KcexClient(session)

        # Пример вызова функции funding_rate
        result = await client.open_interest()

        # Печать результата с использованием prettyprint
        result = kcex_perpetual_open_interest_fix(result)

        # for i in result["data"]:
        #     print(i["symbol"], i["holdVol"])

        a = KcexAdapter.open_interest(raw_data=result)

        pprint(a)

        print(len(a))

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_mexc_funding_rate())
