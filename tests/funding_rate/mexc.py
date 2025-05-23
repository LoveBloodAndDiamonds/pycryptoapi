import aiohttp
from pycryptoapi.mexc import MexcClient, MexcAdapter
from pprint import pprint
import asyncio


async def test_mexc_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = MexcClient(session)

        # Пример вызова функции funding_rate
        result = await client.funding_rate()

        # Печать результата с использованием prettyprint
        # pprint(result)

        a = MexcAdapter.funding_rate(raw_data=result)

        pprint(a)

# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_mexc_funding_rate())
