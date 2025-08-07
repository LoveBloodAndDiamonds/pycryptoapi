import asyncio
from pprint import pprint

import aiohttp

from pycryptoapi.gate import GateClient, GateAdapter


async def test_okx_funding_rate():
    # Инициализация клиента
    async with aiohttp.ClientSession() as session:
        client = GateClient(session)

        a = GateAdapter()

        # Пример вызова функции funding_rate
        result = await client.open_interest("ETH_USDT")

        # Печать результата с использованием prettyprint
        pprint(result)

        r = a.open_interest(result)

        pprint(r)

        # for item in result:
            # if item["name"] == "BTC_USDT":
            #     pprint(item)
            #     pprint(item)
                # print(item["name"], float(item["position_size"]) / float(item["last_price"]))
                # print(item["name"], float(item["position_size"]))
                # print(item["quanto_multiplier"])

        # a = OkxAdapter.open_interest(raw_data=result)

        # pprint(a)

        # print(len(a))


# Запуск теста
if __name__ == "__main__":
    asyncio.run(test_okx_funding_rate())
