import aiohttp
from pycryptoapi.mexc import MexcClient, MexcAdapter
from pprint import pprint
import asyncio


async def test_mexc_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)

        # Пример вызова функции funding_rate
        result = await client.open_interest()

        # Печать результата с использованием prettyprint
        pprint(result)

        for i in result["data"]:
            print(i["symbol"], i["holdVol"])

        # a = MexcAdapter.open_interest(raw_data=result)

        # pprint(a)

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_mexc_funding_rate())
