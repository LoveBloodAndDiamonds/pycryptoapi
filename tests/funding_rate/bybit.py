import aiohttp
from pycryptoapi.bybit import BybitClient, BybitAdapter
from pprint import pprint
import asyncio


async def test_bybit_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        # async with session.get("https://api-testnet.bybit.com/v5/market/funding/history?category=linear&symbol=BTCUSDT") as res:
        client = BybitClient(session)

        # Пример вызова функции funding_rate
        result = await client.funding_rate()

        # Печать результата с использованием prettyprint
        pprint(result)

        a = BybitAdapter.funding_rate(raw_data=result)

        pprint(a)


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_bybit_funding_rate())
